import socket
import json

# PC2 (Server) details
pc2_ip = '192.168.137.185'  # Replace with PC2's IP address
pc2_port = 8087 # Replace with PC2's port number

# PC3 (Client) details
client_ip = '192.168.137.56'  # Replace with PC3's IP address
client_port = 8089  # Replace with PC3's receive port number
# Function to receive confirmation from PC2
def receive_confirmation():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((client_ip, client_port))
        server_socket.listen()
        print("PC3 is listening for connections from PC2.")

        # Accept connection from PC2
        client_socket, client_address = server_socket.accept()
        print(f"Connected to PC2 at {client_address}.")

        # Receive confirmation from PC2
        confirmation = client_socket.recv(1024).decode()
        print(f"Received confirmation ({confirmation}) from PC2.")
        return confirmation

# Function to send nft_metadata_pc3.json to PC2
def send_metadata():
    # Read metadata from file
    with open('nft_metadata_pc3.json', 'r') as file:
        metadata = json.load(file)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((pc2_ip, pc2_port))
        print("Connected to PC2.")

        # Send metadata to PC2
        metadata_json = json.dumps(metadata)
        client_socket.sendall(metadata_json.encode())
        print("Metadata sent to PC2.")

# Main function to handle the process
def main():
    # Receive confirmation from PC2
    confirmation = receive_confirmation()

    # If confirmation is received, send metadata to PC2
    if confirmation == "yes":
        send_metadata()
    else:
        print("No confirmation received from PC2.")

if __name__ == "__main__":
    main()
