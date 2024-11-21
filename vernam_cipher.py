def vernam_cipher(text,key,mode):
    if mode == 'encrypt':
        if len(key) < len(text):
            raise ValueError("Key must be at least as long as text for encryption.")
        encrypted_text = ''.join(chr(ord(text[i]) ^ ord(key[i])) for i in range(len(text)))
        return encrypted_text.encode('utf-8').hex()

    elif mode == 'decrypt':
        if len(key) < len(text) // 2:
            raise ValueError("Key must be at least as long as text for encryption.")
        text_bytes = bytes.fromhex(text)
        decrypted_text = ''.join(chr(text_bytes[i] ^ ord(key[i])) for i in range(len(text_bytes)))
        return decrypted_text

    else:
        raise ValueError("Invalid Mode! use 'encrypt' or 'decrypt'.")

mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()
text = input("Enter the text: ")
key = input("Enter the Key: ")

try:
    result = vernam_cipher(text, key, mode)
    print("Result: ", result)
except ValueError as e:
    print("Error : ", e)
