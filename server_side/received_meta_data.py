import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

# Receiver's details
receiver_ip = '192.168.137.56'
receiver_port = 8080

# Load receiver's private key
with open('private.pem', 'rb') as f:
    receiver_private_key = RSA.import_key(f.read())

# Function to decrypt metadata with symmetric key and RSA
def decrypt_metadata(encrypted_symmetric_key, encrypted_metadata, private_key):
    # Decrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)
    
    # Initialize AES cipher with the symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)
    
    # Decrypt the metadata with AES
    decrypted_metadata = cipher_aes.decrypt(encrypted_metadata)
    
    # Remove padding
    decrypted_metadata = unpad(decrypted_metadata, AES.block_size)
    
    return decrypted_metadata.decode()

# Establish connection with sender
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver_socket:
    receiver_socket.connect((receiver_ip, receiver_port))
    print("pc2(server) connected to pc1...")
    print("--------------------------------")
    
    # Receive encrypted symmetric key
    encrypted_symmetric_key = receiver_socket.recv(1024)
    
    # Receive encrypted metadata
    encrypted_metadata = receiver_socket.recv(1024)
    
    # Decrypt metadata
    decrypted_metadata = decrypt_metadata(encrypted_symmetric_key, encrypted_metadata, receiver_private_key)
    
    # Write decrypted metadata to a JSON file
    with open('received_nft_metadata.json', 'w') as file:
        file.write(decrypted_metadata)
    
    print("Decrypted metadata written to 'received_nft_metadata.json' file.")
