import socket

# Sender's details
sender_ip = '192.168.137.56'  # Replace with sender's IP address
sender_port = 8080  # Choose a port number for sender

# Receiver's details
receiver_ip = '192.168.137.185'  # Replace with receiver's IP address
receiver_port = 8008  # Choose a port number for receiver

# Local path of the sender's public key
encrypted_img_path = 'encrypted_image.bin'

# Establish connection with receiver
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
    sender_socket.bind((sender_ip, sender_port))
    sender_socket.listen()
    print("Sender waiting for receiver to connect...")
    print("--------------------------------")
    sender_conn, sender_addr = sender_socket.accept()
    print(f"Sender connected with {sender_addr}")

    # Read the sender's public key and send it to receiver
    with open(encrypted_img_path, 'rb') as file:
        data = file.read(1024)
        while data:
            sender_conn.send(data)
            data = file.read(1024)
    print("Successfully sent encrytpted image to receiver successfully.")