import socket
import json

# PC2 (Sender) details
sender_ip = '192.168.137.185'
sender_port = 8088  

# Function to receive metadata from PC2
def receive_metadata(server_socket):
    received_metadata = []

    # Receive metadata from PC2
    while True:
        metadata_json = server_socket.recv(4096).decode()
        if not metadata_json:
            break
        metadata = json.loads(metadata_json)
        received_metadata.append(metadata)

    return received_metadata

# Set up client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((sender_ip, sender_port))
        print("Connected to PC2.")

        # Receive metadata from PC2
        received_metadata = receive_metadata(client_socket)
        print("Received metadata from PC2:")
        for metadata in received_metadata:
            print(metadata)

    except Exception as e:
        print(f"An error occurred: {str(e)}")