import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import serialization

# Helper functions for file operations
def read_binary_file(filepath):
    with open(filepath, "rb") as f:
        return f.read()

def write_binary_file(filepath, data):
    with open(filepath, "wb") as f:
        f.write(data)

# RSA Key Generation
def generate_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

# Image Encryption using AES
def encrypt_image_aes(image_data, aes_key):
    iv = os.urandom(16)  # Initialization Vector
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_image = iv + encryptor.update(image_data) + encryptor.finalize()
    return encrypted_image

# AES Key Encryption using RSA
def encrypt_aes_key(public_key, aes_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

# Digital Signature Creation
def create_signature(private_key, data):
    hashed_data = hashes.Hash(hashes.SHA256())
    hashed_data.update(data)
    digest = hashed_data.finalize()

    signature = private_key.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        utils.Prehashed(hashes.SHA256())
    )
    return signature

# Image Decryption using AES
def decrypt_image_aes(encrypted_image, aes_key):
    iv = encrypted_image[:16]
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_image = decryptor.update(encrypted_image[16:]) + decryptor.finalize()
    return decrypted_image

# AES Key Decryption using RSA
def decrypt_aes_key(private_key, encrypted_aes_key):
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key

# Digital Signature Verification
def verify_signature(public_key, data, signature):
    hashed_data = hashes.Hash(hashes.SHA256())
    hashed_data.update(data)
    digest = hashed_data.finalize()

    try:
        public_key.verify(
            signature,
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256())
        )
        return True
    except Exception as e:
        print("Signature verification failed:", e)
        return False

# Main Workflow
# Generate RSA keys for User A (Sender) and User B (Receiver)
private_key_a, public_key_a = generate_rsa_keys()
private_key_b, public_key_b = generate_rsa_keys()

# Sender (User A): Encrypt the image and create a signature
image_path = "path/to/image.jpg"  # Replace with your image path
image_data = read_binary_file(image_path)

aes_key = os.urandom(32)  # Generate a random AES key
encrypted_image = encrypt_image_aes(image_data, aes_key)
encrypted_aes_key = encrypt_aes_key(public_key_b, aes_key)
signature = create_signature(private_key_a, image_data)

# Transmit encrypted_image, encrypted_aes_key, and signature

# Receiver (User B): Decrypt and verify the image
received_encrypted_image = encrypted_image  # Replace with received data
received_encrypted_aes_key = encrypted_aes_key  # Replace with received data
received_signature = signature  # Replace with received data

# Decrypt the AES key and image
decrypted_aes_key = decrypt_aes_key(private_key_b, received_encrypted_aes_key)
decrypted_image = decrypt_image_aes(received_encrypted_image, decrypted_aes_key)

# Verify the signature
is_valid = verify_signature(public_key_a, decrypted_image, received_signature)

# Save the decrypted image
if is_valid:
    output_path = "path/to/decrypted_image.jpg"  # Replace with your output path
    write_binary_file(output_path, decrypted_image)
    print("Image successfully decrypted and verified!")
else:
    print("Image verification failed. Transmission may have been tampered with.")
