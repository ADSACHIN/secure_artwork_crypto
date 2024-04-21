import socket

# Receiver's details
sender_ip = '192.168.137.185'  # Replace with receiver's IP address
sender_port = 8008  # Choose the same port number as sender

received_public_key_path = 'received_public.pem'

# Establishing connection with sender
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver_socket:
    receiver_socket.connect((sender_ip, sender_port))
    print("Receiver connected with sender.")

    with open(received_public_key_path, 'wb') as file:
        while True:
            data = receiver_socket.recv(1024)
            if not data:
                break
            file.write(data)
    print("Receiver received RSA public key from sender successfully.")
