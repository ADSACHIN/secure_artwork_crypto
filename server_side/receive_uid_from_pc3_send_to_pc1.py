import socket
import json
import os

# PC2 (Server) details
pc2_ip = '192.168.137.185'  # Replace with the actual IP of PC2
pc2_port = 8088  # Replace with the port PC2 is listening on

# Function to send metadata to PC1
def send_metadata_to_pc1(metadata, sender_ip, sender_port):
    try:
        # Create a socket to connect to PC1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pc1_socket:
            pc1_socket.connect((sender_ip, sender_port))
            
            # Send metadata to PC1
            metadata_json = json.dumps(metadata)
            pc1_socket.send(metadata_json.encode())
            print("Metadata sent to PC1.")

    except Exception as e:
        print(f"An error occurred while sending metadata to PC1: {str(e)}")

# Function to handle client connections
def handle_client(client_socket):
    try:
        # Receive unique ID from PC3
        unique_id = client_socket.recv(1024).decode()
        print("Received unique ID from PC3:", unique_id)

        # Search for metadata corresponding to the unique ID
        metadata_directory = 'duplicate_metadata_store'
        metadata_file = os.path.join(metadata_directory, f"{unique_id}.json")

        if os.path.exists(metadata_file):
            # Read metadata from file
            with open(metadata_file, 'r') as file:
                metadata = json.load(file)
                
                # Extract sender IP and sender port from metadata
                sender_ip = metadata.get('sender_ip')
                sender_port = metadata.get('sender_port')

                # Send metadata to PC1
                send_metadata_to_pc1(metadata, sender_ip, sender_port)
        else:
            print("Metadata not found for unique ID:", unique_id)
            # Send error response to PC3 if metadata not found
            client_socket.send("Metadata not found".encode())

    except Exception as e:
        print(f"An error occurred while handling client: {str(e)}")
    finally:
        # Close the client socket
        client_socket.close()

# Set up server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((pc2_ip, pc2_port))
    server_socket.listen()
    print("PC2 (server) is listening for connections.")

    while True:
        # Accept connection from PC3
        client_socket, client_address = server_socket.accept()
        print(f"Connected to PC3 at {client_address}.")

        # Handle client connection in a new thread
        handle_client(client_socket)
