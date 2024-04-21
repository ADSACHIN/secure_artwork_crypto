import socket
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# PC2 (Sender) details
sender_ip = '192.168.137.185'
sender_port = 8088  

# Load PC3's private key
with open('private.pem', 'rb') as f:
    pc3_private_key = RSA.import_key(f.read())

# Function to decrypt metadata using symmetric key and RSA
def decrypt_metadata(encrypted_symmetric_key, encrypted_metadata):
    # Decrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(pc3_private_key)
    symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)

    # Initialize AES cipher with the decrypted symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)

    # Decrypt metadata using AES
    metadata = cipher_aes.decrypt(encrypted_metadata)

    # Unpad the decrypted metadata
    metadata = unpad(metadata, AES.block_size)

    return metadata

# Function to receive metadata from PC2
def receive_metadata(server_socket):
    received_metadata = []

    # Receive metadata from PC2
    while True:
        # Receive encrypted symmetric key
        encrypted_symmetric_key = server_socket.recv(256)
        if not encrypted_symmetric_key:
            break

        # Receive encrypted metadata
        encrypted_metadata = server_socket.recv(4096)
        if not encrypted_metadata:
            break

        # Decrypt metadata
        metadata = decrypt_metadata(encrypted_symmetric_key, encrypted_metadata)
        #print(metadata)
        received_metadata.append(metadata.decode())

    return received_metadata

# Set up client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((sender_ip, sender_port))
        print("PC3 Connected to PC2.")

        # Receive metadata from PC2
        received_metadata = receive_metadata(client_socket)
        print("PC3 Received metadata from PC2:")
        for metadata in received_metadata:
            print(metadata)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
