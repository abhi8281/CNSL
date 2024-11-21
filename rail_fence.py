def rail_fence_encrypt(text, key):
    # Create an empty list of strings for each rail
    rails = ['' for _ in range(key)]

    # Track direction of writing
    direction_down = False
    row = 0

    # Fill the rails
    for char in text:
        rails[row] += char
        # Change direction if at the top or bottom rail
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1

    # Join all rails to form the cipher text
    return ''.join(rails)

def rail_fence_decrypt(ciphertext, key):
    # Create an empty list for the rail pattern
    rail = [['\n' for _ in range(len(ciphertext))] for _ in range(key)]

    # Mark the positions of the rails
    direction_down = None
    row, col = 0, 0

    # Mark the positions where the ciphertext will go
    for char in ciphertext:
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False

        rail[row][col] = '*'
        col += 1
        row += 1 if direction_down else -1

    # Fill the rail with the ciphertext characters
    index = 0
    for i in range(key):
        for j in range(len(ciphertext)):
            if rail[i][j] == '*' and index < len(ciphertext):
                rail[i][j] = ciphertext[index]
                index += 1

    # Read the plaintext in zigzag manner
    result = []
    row, col = 0, 0
    for char in ciphertext:
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False

        result.append(rail[row][col])
        col += 1
        row += 1 if direction_down else -1

    return ''.join(result)

# Example usage
mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()
text = input("Enter the text: ")
key = int(input("Enter the key (number of rails): "))

if mode == 'encrypt':
    result = rail_fence_encrypt(text, key)  # Pass both text and key
    print("Encrypted text:", result)
elif mode == 'decrypt':
    result = rail_fence_decrypt(text, key)  # Pass both text and key
    print("Decrypted text:", result)
else:
    print("Invalid mode selected.")
