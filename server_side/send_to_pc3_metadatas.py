import socket
import json
import os
import time
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

# PC2 (Server) details
sender_ip = '192.168.137.185'
sender_port = 8088 

receiver_ip = '192.168.137.56'  
receiver_port = 8080

# Load PC3's public key
with open('received_public.pem', 'rb') as f:
    pc3_public_key = RSA.import_key(f.read())

# Function to encrypt metadata with symmetric key and RSA
def encrypt_metadata(metadata):
    # Generate a random symmetric key
    symmetric_key = os.urandom(16)  # 16 bytes for AES-128
    
    # Initialize AES cipher with the symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)
    
    # Pad the metadata to align with block size boundary
    padded_metadata = pad(metadata.encode(), AES.block_size)
    
    # Encrypt padded metadata with AES
    encrypted_metadata = cipher_aes.encrypt(padded_metadata)
    
    # Encrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(pc3_public_key)
    encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)
    
    return encrypted_symmetric_key, encrypted_metadata

# Function to send encrypted metadata to PC3
def send_encrypted_metadata(client_socket):
    metadata_directory = 'duplicate_metadata_store'

    # Check if metadata directory exists
    if not os.path.exists(metadata_directory):
        print("Metadata directory not found.")
        return
    
    print("Sending metadata from pc2(server) to pc3")
    # Iterate through metadata files
    for filename in os.listdir(metadata_directory):
        metadata_path = os.path.join(metadata_directory, filename)
        
        # Read metadata from file
        with open(metadata_path, 'r') as file:
            metadata = file.read()

        # Encrypt metadata
        encrypted_symmetric_key, encrypted_metadata = encrypt_metadata(metadata)

        # Send encrypted metadata to PC3
        client_socket.sendall(encrypted_symmetric_key)
        client_socket.sendall(encrypted_metadata)
        print(f"Sent encrypted metadata for {filename} to PC3.")
        
        # Introduce a small delay before sending the next metadata
        time.sleep(0.1)

# Function to handle client connections
def handle_client(client_socket):
    try:
        # Send encrypted metadata to PC3
        send_encrypted_metadata(client_socket)
    except Exception as e:
        print(f"An error occurred while handling client: {str(e)}")
    finally:
        # Close the client socket
        client_socket.close()

# Set up server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    try:
        server_socket.bind((sender_ip, sender_port))
        server_socket.listen()
        print("PC2 (server) is listening for connections.")

        while True:
            # Accept connection from PC3
            client_socket, client_address = server_socket.accept()
            print(f"Connected to PC3 at {client_address}.")

            # Handle client connection in a new thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    