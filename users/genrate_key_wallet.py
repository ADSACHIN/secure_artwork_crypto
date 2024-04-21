import os
import json
from Crypto.PublicKey import RSA

# Function to generate RSA keys and PC1 details
def generate_pc1_details():
    # Generate RSA keys
    key = RSA.generate(2048)

    # Extract private key
    private_key = key.export_key()

    # Generate random wallet address (for demonstration purposes)
    # In a real scenario, the wallet address may be derived from the private key
    wallet_address = os.urandom(32).hex()

    # Export public key
    public_key = key.publickey().export_key()

    # Save public key to file
    with open('public.pem', 'wb') as f:
        f.write(public_key)

    # Save private key to file
    with open('private.pem', 'wb') as f:
        f.write(private_key)

    # Store PC1 details securely
    pc1_details = {
        "wallet_address": wallet_address,
        "private_key": private_key.decode()  # Convert bytes to string for JSON serialization
    }

    # Save PC1 details to a JSON file
    with open('pc1_details.json', 'w') as f:
        json.dump(pc1_details, f)

    print("PC1 details generated and saved successfully.")

def main():
    print("Generating PC1 details...")
    generate_pc1_details()
    print("PC1 details generation complete.")

if __name__ == "__main__":
    main()
