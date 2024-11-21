import random

def generate_public_key(private_key,g,p):
    return pow(g,private_key,p)

def compute_shared_secret(other_public_key,private_key,p):
    return pow(other_public_key,private_key,p)

p=23
g=5

# Alice's private key and public key
alice_private = random.randint(1,p-1)
alice_public = generate_public_key(alice_private,g,p)
# Bob's private key and public key
bob_private = random.randint(1,p-1)
bob_public = generate_public_key(bob_private,g,p)

# Eve's private keys and public keys
eve_private_a = random.randint(1,p-1)
eve_private_b = random.randint(1,p-1)
eve_public_a = generate_public_key(eve_private_a,g,p)
eve_public_b = generate_public_key(eve_private_b,g,p)

# Intercepted public key exchanges
alice_shared_secret = compute_shared_secret(eve_public_a,alice_private,p)
bob_shared_secret = compute_shared_secret(eve_public_b,bob_private,p)

# Eve calculates shared secrets with both
eve_shared_secret_with_alice = compute_shared_secret(alice_public,eve_private_a,p)
eve_shared_secret_with_bob = compute_shared_secret(bob_public,eve_private_b,p)

print("Public Parameters (p,g): ",(p,g))
print("Alice's public key: ",alice_public)
print("Bob's public key: ",bob_public)
print("Eve's public key (A->E, B->E): ",eve_public_a,eve_public_b)

print("\nShared Secrets: ")
print("Alice's shared secret (with eve): ",alice_shared_secret)
print("Bob's shared secret (with eve): ",bob_shared_secret)
print("Eve's shared secret (with Alice): ",eve_shared_secret_with_alice)
print("Eve's shared secret (with Bob): ",eve_shared_secret_with_bob)
