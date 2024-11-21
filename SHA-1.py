import hashlib
import socket

# Function to generate SHA-1 hash of a message
def generate_sha1_hash(message):
    sha1 = hashlib.sha1()  # Initialize SHA-1 hash object
    sha1.update(message.encode('utf-8'))  # Update the hash with the message
    return sha1.hexdigest()  # Return the hexadecimal representation of the hash

# Function to send message over a network
def send_message(host, port, message):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server at the given host and port
    sock.connect((host, port))
    
    try:
        # Send the message (here, we send the SHA-1 hash)
        sha1_hash = generate_sha1_hash(message)
        sock.sendall(sha1_hash.encode('utf-8'))
        print(f"Sent SHA-1 hash: {sha1_hash}")
        
    finally:
        # Close the socket
        sock.close()

# Function to receive message over a network
def receive_message(port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the port
    sock.bind(('localhost', port))
    
    # Listen for incoming connections
    sock.listen(1)
    
    print("Waiting for a connection...")
    
    # Wait for a connection from a client
    connection, client_address = sock.accept()
    
    try:
        print(f"Connection established with {client_address}")
        
        # Receive the data (SHA-1 hash in this case)
        data = connection.recv(1024)
        print(f"Received SHA-1 hash: {data.decode('utf-8')}")
        
    finally:
        # Close the connection
        connection.close()

# Main program execution
if __name__ == "__main__":
    choice = input("Enter 'send' to send message or 'receive' to receive message: ").strip().lower()
    
    if choice == 'send':
        host = input("Enter the destination host (e.g., 'localhost'): ").strip()
        port = int(input("Enter the destination port: ").strip())
        message = input("Enter the message to send: ").strip()
        
        send_message(host, port, message)
    
    elif choice == 'receive':
        port = int(input("Enter the port to listen on: ").strip())
        receive_message(port)
    
    else:
        print("Invalid option! Please enter 'send' or 'receive'.")
