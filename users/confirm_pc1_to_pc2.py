import socket

# PC2 (Server) details
server_ip = '192.168.137.185'  # Replace with PC2's IP address
server_port = 8088  # Replace  with PC2's port number

# Unique ID of the image to be sold
unique_id = "ldLjO1apo5"  # Replace with the unique ID of the image

# Confirmation to sell the image
confirmation = "yes"

# Connect to PC2
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    print("Waiting PC2 to connect...")
    client_socket.connect((server_ip, server_port))
    print("Connected to PC2.")

    # Send confirmation and unique ID to PC2
    data = confirmation + ":" + unique_id
    client_socket.sendall(data.encode())
    print(f"Confirmation ({confirmation}) and unique ID ({unique_id}) sent to PC2.")

print("Process completed.")