from Crypto.PublicKey import RSA

# Function to generate RSA public and private keys
def generate_rsa_keys():
    
    key = RSA.generate(2048)

    #printing the p value
    p = key.p
    print("The value of p = ",p)
    #printing the q value
    q = key.q
    print("The value of q = ",q)
    #printing the n value
    n = key.n
    print("The value of n = ",n)
    
    # Export public key
    public_key = key.publickey().export_key()
    print(key.publickey())
    with open('public.pem', 'wb') as f:
        f.write(public_key)
    print("Public key generated and saved as 'public.pem'")

    # Export private key
    private_key = key.export_key()
    with open('private.pem', 'wb') as f:
        f.write(private_key)
    print("Private key generated and saved as 'private.pem'")


def main():
    print("Generating RSA keys...")
    generate_rsa_keys()
    print("RSA keys generation complete.")


if __name__ == "__main__":
    main()