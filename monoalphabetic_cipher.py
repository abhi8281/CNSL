import string
import random

def generate_random_key():
    """Generates a random substitution key for the alphabet."""
    alphabet = list(string.ascii_lowercase)
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def monoalphabetic_cipher(text, key, mode='encrypt'):
    result = ""
    reverse_key = {v: k for k, v in key.items()}  # Create reverse key for decryption

    for char in text:
        if char.isalpha():
            lower_char = char.lower()
            if mode == 'encrypt':
                new_char = key[lower_char]
            else:  # decryption
                new_char = reverse_key[lower_char]

            # Preserve case of the original letter
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char  # Non-alphabet characters remain unchanged

    return result

def main():
    # Generate a random substitution key
    key = generate_random_key()

    # Taking input from the user for encryption
    mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()
    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode! Please enter 'encrypt' or 'decrypt'.")
        return

    text = input("Enter the text: ")

    if mode == 'encrypt':
        # Perform encryption
        output = monoalphabetic_cipher(text, key, 'encrypt')
        print(f"Key used: {key}")  # Display the key used for encryption
        print(f"Encrypted Result: {output}")

        # Save the key for future use (optional)
        with open("cipher_key.txt", "w") as key_file:
            for original, encrypted in key.items():
                key_file.write(f"{original}:{encrypted}\n")

    elif mode == 'decrypt':
        # Read the key from the file
        key = {}
        try:
            with open("cipher_key.txt", "r") as key_file:
                for line in key_file:
                    original, encrypted = line.strip().split(':')
                    key[original] = encrypted

        except FileNotFoundError:
            print("Key file not found! Please encrypt a message first to generate a key.")
            return

        # Perform decryption
        output = monoalphabetic_cipher(text, key, 'decrypt')
        print(f"Decrypted Result: {output}")

if __name__ == "__main__":
    main()
