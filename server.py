import socket
from dotenv import load_dotenv
import os

load_dotenv()
auth_token = os.getenv('AUTH_KEY')

if auth_token is None:
    print("Auth key not found. Make sure to set in .env file.")
    exit(1)

UDP_IP = "localhost"
UDP_PORT = 10120

sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

sock.bind((UDP_IP, UDP_PORT))

print(f"Server running on {UDP_IP}:{UDP_PORT}")

try:
    while True:
        data, addr = sock.recvfrom(1024)

        token, message = data.decode('utf-8').split(':', 1)

        if token == auth_token:
            print(f"received message from {addr}: {data.decode('utf-8')}")
            sock.sendto(f"Message received from {addr}: {message}".encode('utf-8'), addr)

        else:
            sock.sendto("Unauthorized access!".encode('utf-8'), addr)

except KeyboardInterrupt:
    print("Server stopped")
finally:
    sock.close()

