def vigenere_cipher(text, key, mode='encrypt'):
    """
    Encrypts or decrypts text using the Vigenère cipher.

    Parameters:
    - text (str): The input text to encrypt or decrypt.
    - key (str): The keyword used for shifting.
    - mode (str): 'encrypt' to encrypt the text, 'decrypt' to decrypt it.

    Returns:
    - str: The resulting encrypted or decrypted text.
    """
    result = []
    key = key.lower()  # Convert key to lowercase for consistency
    key_length = len(key)
    key_index = 0  # To track the position in the key

    for char in text:
        if char.isalpha():
            # Calculate shift based on the current key character
            shift = ord(key[key_index]) - ord('a')
            if mode == 'decrypt':
                shift = -shift  # Reverse shift for decryption

            # Determine ASCII base (uppercase or lowercase)
            shift_base = ord('A') if char.isupper() else ord('a')

            # Perform the shift with wrapping using modulo 26
            new_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            result.append(new_char)

            # Move to the next character in the key
            key_index = (key_index + 1) % key_length
        else:
            # Non-alphabet characters are added unchanged
            result.append(char)

    return ''.join(result)

# Taking input from the user
def main():
    mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()

    # Validate mode input
    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode! Please enter 'encrypt' or 'decrypt'.")
        return

    text = input("Enter the text: ")
    key = input("Enter the key: ")

    # Validate key input
    if not key.isalpha():
        print("Invalid key! The key must consist of alphabetic characters only.")
        return

    # Perform encryption or decryption
    output = vigenere_cipher(text, key, mode)
    print(f"Result: {output}")

if __name__ == "__main__":
    main()
