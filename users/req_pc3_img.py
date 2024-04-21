import socket

# PC2 (Server) details
server_ip = '192.168.137.185'  # PC2's IP address
server_port = 8088 # Port to connect to
 
# Unique ID of the
#  image requested by PC3
unique_id = "ldLjO1apo5"

# Establish connection with PC2
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    print("Waiting for PC2 to accept")
    client_socket.connect((server_ip, server_port))
    print("Connected to PC2.")

    # Send unique ID to PC2
    client_socket.send(unique_id.encode())
    #print("Sent request to see the image with unique ID:", unique_id)
    print(f"Sent request to update the ownership on image with unique id {unique_id}")

#print("Request sent to PC2 to see the image.")