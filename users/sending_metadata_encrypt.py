import socket
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# Sender's details
sender_ip = '192.168.137.56'
sender_port = 8080

receiver_ip = '192.168.137.185'
receiver_port = 8088

# Load PC2's public key
with open('received_public.pem', 'rb') as f:
    pc2_public_key = RSA.import_key(f.read())

# Function to encrypt metadata with symmetric key and then encrypt the symmetric key with RSA
def encrypt_metadata(metadata, public_key):
    # Generate a random symmetric key
    symmetric_key = os.urandom(16)  # 16 bytes for AES-128
   
    # Initialize AES cipher with the symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)
   
    # Pad the metadata to align with block size boundary
    padded_metadata = pad(metadata.encode(), AES.block_size)
   
    # Encrypt padded metadata with AES
    encrypted_metadata = cipher_aes.encrypt(padded_metadata)
   
    # Encrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)
   
    return encrypted_symmetric_key, encrypted_metadata

# Establish connection with receiver
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
    sender_socket.bind((sender_ip, sender_port))
    sender_socket.listen()
    print("PC1 waiting for PC2 to connect...")
    print("--------------------------------")
    sender_conn, sender_addr = sender_socket.accept()
    print(f"PC1 connected with {sender_addr}")

    # Read metadata from file
    with open('nft_metadata_pc1.json', 'r') as file:
        metadata = file.read()

    # Encrypt metadata
    encrypted_symmetric_key, encrypted_metadata = encrypt_metadata(metadata, pc2_public_key)

    # Sending encrypted metadata
    sender_conn.sendall(encrypted_symmetric_key)
    sender_conn.sendall(encrypted_metadata)
    print("Encrypted metadata sent to PC2 successfully.")
