import socket
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# PC2 (Server) details
pc2_ip = '192.168.137.185'  # Replace with PC2's IP address
pc2_port = 8087 # Replace with PC2's port number

# PC3 (Client) details
client_ip = '192.168.137.56'  # Replace with PC3's IP address
client_port = 8089  # Replace with PC3's receive port number

# Load PC2's public key
with open('received_public.pem', 'rb') as f:
    pc2_public_key = RSA.import_key(f.read())

# Function to encrypt metadata using symmetric key and RSA
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
    cipher_rsa = PKCS1_OAEP.new(pc2_public_key)
    encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)
   
    return encrypted_symmetric_key, encrypted_metadata

# Function to receive confirmation from PC2
def receive_confirmation():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((client_ip, client_port))
        server_socket.listen()
        print("PC3 is listening for connections from PC2.")

        # Accept connection from PC2
        client_socket, client_address = server_socket.accept()
        print(f"Connected to PC2 at {client_address}.")

        # Receive confirmation from PC2
        confirmation = client_socket.recv(1024).decode()
        print(f"Received confirmation ({confirmation}) from PC2.")
        return confirmation

# Function to send encrypted metadata to PC2
def send_encrypted_metadata():
    # Read metadata from file
    with open('nft_metadata_pc3.json', 'r') as file:
        metadata = file.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((pc2_ip, pc2_port))
        print("Connected to PC2.")

        # Encrypt metadata
        encrypted_symmetric_key, encrypted_metadata = encrypt_metadata(metadata)

        # Send encrypted metadata to PC2
        client_socket.sendall(encrypted_symmetric_key)
        client_socket.sendall(encrypted_metadata)
        print("Encrypted metadata sent to PC2.")

# Main function to handle the process
def main():
    # Receive confirmation from PC2
    confirmation = receive_confirmation()

    # If confirmation is received, send encrypted metadata to PC2
    if confirmation == "yes":
        send_encrypted_metadata()
    else:
        print("No confirmation received from PC2.")

if __name__ == "__main__":
    main()