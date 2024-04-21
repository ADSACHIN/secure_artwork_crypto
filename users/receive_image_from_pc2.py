import socket
import json
import os
import random
import string
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad
import shutil

def decrypt_image(encrypted_data_path, private_key_path, output_path):
    # Load private key
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    
    # Read encrypted data
    with open(encrypted_data_path, 'rb') as f:
        encrypted_symmetric_key = f.read(256)
        encrypted_image_data = f.read()
    
    # Decrypt symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)
    
    # Initialize AES cipher with the decrypted symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)
    
    # Decrypt image data with AES
    decrypted_image_data = unpad(cipher_aes.decrypt(encrypted_image_data), AES.block_size)
    
    # Write decrypted image data to file
    with open(output_path, 'wb') as f:
        f.write(decrypted_image_data)

# Receiver's details
sender_ip = '192.168.137.185'  
sender_port = 8088

# Establish connection with sender
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver_socket:
    print("Waiting for PC2 to send the image...")
    receiver_socket.connect((sender_ip, sender_port))
    print("PC3 connected to PC2.")

    # Receiving encrypted data
    with open('received_encrypted_image.enc', 'wb') as file:
        print("Receiving encrypted data...")
        data = receiver_socket.recv(1024)
        while data:
            file.write(data)
            data = receiver_socket.recv(1024)
        print("Encrypted data received successfully.")

# Decrypt the received encrypted image using receiver's private key
private_key_path = 'private.pem'  # Path to receiver's private key file
output_path = 'decrypted_image.jpg'
decrypt_image('received_encrypted_image.enc', private_key_path, output_path)
print("Image decrypted and stored successfully.")
