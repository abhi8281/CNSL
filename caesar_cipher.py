def caesar_cipher(text,shift,mode = 'encrypt'):
    result = ""

    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift ) % 26 + shift_base)
        else:
            result += char

    return result

mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ")

if mode not in['encrypt', 'decrypt']:
    print("Invalid mode! Please enter 'encrypt' or 'decrypt'.")
else:
    text = input("Enter the text: ")
    shift = int(input("Enter the shift value : "))

output = caesar_cipher(text, shift, mode)
print("Result", output)

