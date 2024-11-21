def medium_cipher(text,shift,mode = 'encrypt'):
    result = ""
    if mode == 'encrypt':
        for char in text:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            elif char.isdigit():
                result += str(9 - int(char))
            else:
                result += char
        result = result[::-1]

    elif mode == 'decrypt':
        text = text[::-1]
        for char in text:
            if char.isalpha():
                shift_base = ord('A') if char.isupper else ord('a')
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            elif char.isdigit():
                result += str(9 - int(char))
            else:
                result += char

    else:
        raise ValueError("Invalid Mode! use 'encrypt' or 'decrypt'.")

    return result

if __name__ == "__main__":
    mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()
    text = input("Enter the text: ")
    shift = int(input("Enter the shift: "))

    try:
        result = medium_cipher(text, shift, mode)
        print("Result: ", result)
    except ValueError as e:
        print("Error", e)
