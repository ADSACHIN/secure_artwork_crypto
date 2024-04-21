import socket
import json

# Sender's details
sender_ip = '192.168.137.185'  
sender_port = 8088

receiver_ip = '192.168.137.56'  
receiver_port = 8080

# Establish connection with receiver
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
    sender_socket.bind((sender_ip, sender_port))
    sender_socket.listen()
    print("pc2(server) waiting for receiver to connect...")
    print("--------------------------------")
    sender_conn, sender_addr = sender_socket.accept()
    print(f"Sender connected with {sender_addr}")

    # Sending encrypted data
    with open('encrypted_image.enc', 'rb') as file:
        data = file.read(1024)
        while data:
            sender_conn.send(data)
            data = file.read(1024)
    print("Encrypted data sent to PC3 successfully.")
