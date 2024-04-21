import socket
import json

# PC1 (Receiver) details
sender_ip = '192.168.137.56'  # Replace with the actual IP of PC1
sender_port = 8080  # Replace with the port PC1 is listening on

# Set up server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((sender_ip, sender_port))
    server_socket.listen()
    print("PC1 server is listening for connections.")

    # Accept connection from PC2
    client_socket, client_address = server_socket.accept()
    print(f"Connected to PC2 at {client_address}.")

    try:
        # Receive metadata from PC2
        metadata_json = client_socket.recv(1024).decode()
        metadata = json.loads(metadata_json)
        print("Received metadata from PC2 to update ownership:", metadata)

        # Process the received metadata as needed
        # For example, save it to a database or perform some operations
       
    except Exception as e:
        print(f"An error occurred while receiving metadata: {str(e)}")
    finally:
        # Close the client socket
        client_socket.close()