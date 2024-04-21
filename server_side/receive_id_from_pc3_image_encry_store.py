import socket
import json
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad

# PC3 (Client) details
pc3_ip = '192.168.137.56'  # Replace with PC3's IP address
pc3_port = 8089  # Replace with PC3's port number

# PC2 (Server) details
server_ip = '192.168.137.185'  # Replace with PC2's IP address
server_port = 8088  # Replace with PC2's port number


# Function to receive unique ID from PC3
def receive_unique_id_from_pc3():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen()
        print("PC2 (server) is listening for connections from PC3.")

        # Accept connection from PC3
        client_socket, client_address = server_socket.accept()
        print(f"Connected to PC3 at {client_address}.")

        # Receive unique ID from PC3
        unique_id = client_socket.recv(1024).decode()
        print(f"Received unique ID ({unique_id}) from PC3.")
        return unique_id

# Function to encrypt the image with the received unique ID
def encrypt_image_with_unique_id(unique_id):
    # Paths to image, public key, and output
    image_path = os.path.join('image_store', f"{unique_id}.jpg")  # Assuming the image file extension is jpg
    public_key_path = 'received_public.pem'  # Path to PC2's public key file
    output_path = os.path.join('encrypted_image.enc')  # Output path for encrypted image
    
    # Load public key
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    
    # Generate a random symmetric key
    symmetric_key = os.urandom(16)  # 16 bytes for AES-128
    
    # Initialize AES cipher with the symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)
    
    # Read image data
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Pad the image data to align with block size boundary
    padded_image_data = pad(image_data, AES.block_size)
    
    # Encrypt padded image data with AES
    encrypted_image_data = cipher_aes.encrypt(padded_image_data)
    
    # Encrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)
    
    # Write encrypted image data and encrypted symmetric key to file
    with open(output_path, 'wb') as f:
        f.write(encrypted_symmetric_key)
        f.write(encrypted_image_data)
    
    print("Image encrypted and stored successfully.")

# Main function to handle the process
def main():
    # Receive unique ID from PC3
    unique_id = receive_unique_id_from_pc3()

    # Encrypt the image with the received unique ID
    encrypt_image_with_unique_id(unique_id)

    print("Process completed.")

if __name__ == "__main__":
    main()
