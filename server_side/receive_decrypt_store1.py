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

def generate_unique_id(image_name):
    # Generate a random string as unique ID
    unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return unique_id

# Receiver's details
receiver_ip = '192.168.137.56'  
receiver_port = 8080

# Establish connection with sender
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver_socket:
    receiver_socket.connect((receiver_ip, receiver_port))
    print("pc2(server) connected to pc1.")

    # Receiving encrypted data
    with open('received_encrypted_image.enc', 'wb') as file:
        print("Receiving encrypted data...")
        data = receiver_socket.recv(1024)
        while data:
            file.write(data)
            data = receiver_socket.recv(1024)
        print("Encrypted data received successfully.")

# Decrypt the received encrypted image
private_key_path = 'private.pem'  # Path to PC2's private key file
output_path = 'decrypted_image.jpg'
decrypt_image('received_encrypted_image.enc', private_key_path, output_path)
print("Image decrypted and stored successfully.")

# Load metadata from received JSON file
with open('received_nft_metadata.json', 'r') as file:
    metadata = json.load(file)

# Generate a unique ID for the image
image_name = os.path.basename(metadata['file_path'])  # Extract image name from file path
unique_id = generate_unique_id(image_name)

# Store metadata with unique ID
store_directory = 'image_store'
if not os.path.exists(store_directory):
    os.makedirs(store_directory)

# Ensure that the file name is unique
store_path = os.path.join(store_directory, f"{unique_id}.json")
while os.path.exists(store_path):
    unique_id = generate_unique_id(image_name)
    store_path = os.path.join(store_directory, f"{unique_id}.json")

with open(store_path, 'w') as file:
    # Include the unique ID in the metadata
    metadata['unique_id'] = unique_id
    json.dump(metadata, file)

print("Metadata stored successfully with unique ID:", unique_id)

# Move decrypted image to image store with unique ID name
image_output_path = os.path.join(store_directory, f"{unique_id}.jpg")
shutil.move(output_path, image_output_path)
print("Decrypted image moved to 'image_store' directory with unique ID name:", unique_id)

# Make a duplicate copy of the decrypted image in duplicate_store directory
duplicate_store_directory = 'duplicate_store'
if not os.path.exists(duplicate_store_directory):
    os.makedirs(duplicate_store_directory)

duplicate_image_output_path = os.path.join(duplicate_store_directory, f"{unique_id}.jpg")
shutil.copy(image_output_path, duplicate_image_output_path)
print("Duplicate copy of the decrypted image created in 'duplicate_store' directory with unique ID name:", unique_id)

# Store metadata duplicate in duplicate_metadata_store directory
duplicate_metadata_store_directory = 'duplicate_metadata_store'
if not os.path.exists(duplicate_metadata_store_directory):
    os.makedirs(duplicate_metadata_store_directory)

duplicate_metadata_store_path = os.path.join(duplicate_metadata_store_directory, f"{unique_id}.json")
shutil.copy(store_path, duplicate_metadata_store_path)
print("Duplicate copy of metadata created in 'duplicate_metadata_store' directory with unique ID name:", unique_id)
