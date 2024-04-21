import socket
import json

# Sender's details
sender_ip = '192.168.137.56'  
sender_port = 8080 

receiver_ip = '192.168.137.185'  
receiver_port = 8088

# Establish connection with receiver
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
    sender_socket.bind((sender_ip, sender_port))
    sender_socket.listen()
    print("PC1 waiting for PC2 to connect...")
    print("--------------------------------")
    sender_conn, sender_addr = sender_socket.accept()
    print(f"PC1 connected with {sender_addr}")

    # Sending encrypted data
    with open('encrypted_image.enc', 'rb') as file:
        data = file.read(1024)
        while data:
            sender_conn.send(data)
            data = file.read(1024)
    print("Encrypted IMAGE data sent to PC2 successfully.")
