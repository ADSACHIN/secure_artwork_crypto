from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import unpad
import socket
import json
import os

# PC2 (Server) details
pc3_ip = '192.168.137.56'  # Replace with PC3's IP address
pc3_port = 8089  # Replace with PC3's port number

# PC2 (Server) details
server_ip = '192.168.137.185'  # Replace with PC2's IP address
server_port = 8088  # Replace with PC2's port number
server_port2 = 8087

# Load PC2's private key
with open('private.pem', 'rb') as f:
    pc2_private_key = RSA.import_key(f.read())

# Function to receive confirmation and unique ID from PC1
def receive_confirmation_and_id(server_socket):
    # Accept connection from PC1
    client_socket, client_address = server_socket.accept()
    print(f"Connected to PC1 at {client_address}.")

    # Receive confirmation and unique ID from PC1
    data = client_socket.recv(1024).decode()
    confirmation, unique_id = data.split(":")
    print(f"Received confirmation ({confirmation}) and unique ID ({unique_id}) from PC1.")

    # Close connection with PC1
    client_socket.close()
    return confirmation, unique_id

# Function to send confirmation to PC3
def send_confirmation_to_pc3():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((pc3_ip, pc3_port))
        print("Connected to PC3.")

        # Send confirmation to PC3
        confirmation = "yes"  # Assuming confirmation is always "yes" for simplicity
        client_socket.sendall(confirmation.encode())
        print(f"Confirmation ({confirmation}) sent to PC3.")

# Function to receive and decrypt metadata from PC3
def receive_and_decrypt_metadata(unique_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port2))
        server_socket.listen()
        print("PC2 (server) is listening for connections from PC3.")

        # Accept connection from PC3
        client_socket, client_address = server_socket.accept()
        print(f"Connected to PC3 at {client_address}.")

        # Receive encrypted symmetric key from PC3
        encrypted_symmetric_key = client_socket.recv(4096)
        
        # Receive encrypted metadata from PC3
        encrypted_metadata = client_socket.recv(4096)

        # Decrypt the metadata
        decrypted_metadata = decrypt_metadata(encrypted_symmetric_key, encrypted_metadata, pc2_private_key)

        # Update metadata file in duplicate store
        metadata_path = os.path.join('duplicate_metadata_store', f"{unique_id}.json")
        with open(metadata_path, 'w') as file:
            # Update metadata with PC3's information
            metadata = json.loads(decrypted_metadata)
            metadata['sender_port'] = client_address[1]  # Update with PC3's port
            metadata['sender_ip'] = client_address[0]  # Update with PC3's IP address
            metadata['unique_id'] = unique_id
            json.dump(metadata, file)
        print("Metadata updated successfully.")

        # Update metadata file in image store
        image_metadata_path = os.path.join('image_store', f"{unique_id}.json")
        with open(image_metadata_path, 'w') as file:
            json.dump(metadata, file)
        print("Image metadata updated successfully.")

# Function to decrypt metadata
def decrypt_metadata(encrypted_symmetric_key, encrypted_metadata, pc2_private_key):
    # Decrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(pc2_private_key)
    symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)
    
    # Initialize AES cipher with the decrypted symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)
    
    # Decrypt the encrypted metadata with AES
    padded_metadata = cipher_aes.decrypt(encrypted_metadata)
    
    # Unpad the decrypted metadata
    metadata = unpad(padded_metadata, AES.block_size).decode()
    
    return metadata

# Main function to handle the process
def main():
    # Set up server socket to receive confirmation and unique ID from PC1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen()
        print("PC2 (server) is listening for connections from PC1.")
        
        # Receive confirmation and unique ID from PC1
        confirmation, unique_id = receive_confirmation_and_id(server_socket)

        # Send confirmation to PC3
        send_confirmation_to_pc3()

        # Receive and decrypt metadata from PC3 and update metadata files
        receive_and_decrypt_metadata(unique_id)

    print("Process completed.")

if __name__ == "__main__":
    main()
