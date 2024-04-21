import socket

# Sender's details
sender_ip = '192.168.137.185'  
sender_port = 8008  

receiver_ip = '192.168.137.56'  
receiver_port = 5500 

# Local path of the sender's public key
sender_public_key_path = 'public.pem'

# Establish connection with receiver
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
    sender_socket.bind((sender_ip, sender_port))
    sender_socket.listen()
    print("Sender waiting for receiver to connect...")
    print("--------------------------------")
    sender_conn, sender_addr = sender_socket.accept()
    print(f"Sender connected with {sender_addr}")

    # Read the sender's public key and send it to receiver
    with open(sender_public_key_path, 'rb') as file:
        data = file.read(1024)
        while data:
            sender_conn.send(data)
            data = file.read(1024)
    print("Sender sent RSA public key to receiver successfully.")
