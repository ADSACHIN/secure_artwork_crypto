from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad
import os

def encrypt_image(image_path, public_key_path, output_path):
    # Load public key
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    
    # Generate a random symmetric key
    symmetric_key = os.urandom(16)  # 16 bytes for AES-128
    
    # Initialize AES cipher with the symmetric key
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)
    
    # Read image data
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Pad the image data to align with block size boundary
    padded_image_data = pad(image_data, AES.block_size)
    
    # Encrypt padded image data with AES
    encrypted_image_data = cipher_aes.encrypt(padded_image_data)
    
    # Encrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)
    
    # Write encrypted image data and encrypted symmetric key to file
    with open(output_path, 'wb') as f:
        f.write(encrypted_symmetric_key)
        f.write(encrypted_image_data)

# Paths to image, public key, and output
image_path = 'Mountain.jpg'
public_key_path = 'received_public.pem'  # Path to PC2's public key file
output_path = 'encrypted_image.enc'

# Encrypt image and store encrypted image
encrypt_image(image_path, public_key_path, output_path)
print("Image encrypted and stored successfully.")
