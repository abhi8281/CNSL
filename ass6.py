from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.serialization import (
    Encoding, PrivateFormat, NoEncryption, PublicFormat
)

# Step 1: Generate RSA key pairs for both X (sender) and Y (receiver)
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

# Generate keys for X and Y
private_key_x, public_key_x = generate_keys()
private_key_y, public_key_y = generate_keys()

# Step 2: X creates a confidential message and signs it
def create_signed_message(private_key, message):
    # Hash the message
    message_hash = hashes.Hash(hashes.SHA256())
    message_hash.update(message.encode())
    hashed_message = message_hash.finalize()

    # Create a digital signature
    signature = private_key.sign(
        hashed_message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        utils.Prehashed(hashes.SHA256())
    )
    return hashed_message, signature

message = "Confidential Message from X to Y"
hashed_message, signature = create_signed_message(private_key_x, message)

# Step 3: Encrypt the message using Y's public key
def encrypt_message(public_key, message):
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

encrypted_message = encrypt_message(public_key_y, message)

# Step 4: Y receives the encrypted message and decrypts it using their private key
def decrypt_message(private_key, encrypted_message):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()

decrypted_message = decrypt_message(private_key_y, encrypted_message)

# Step 5: Y verifies the integrity and authenticity of the message
def verify_message(public_key, hashed_message, signature):
    try:
        public_key.verify(
            signature,
            hashed_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256())
        )
        return True
    except Exception as e:
        print("Verification failed:", e)
        return False

verification_status = verify_message(public_key_x, hashed_message, signature)

# Output results
print("Original Message:", message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", decrypted_message)
print("Verification Status:", "Successful" if verification_status else "Failed")
