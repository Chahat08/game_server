import socket
from dotenv import load_dotenv
import os

load_dotenv()
auth_token = os.getenv('AUTH_KEY')

if auth_token is None:
    print("Auth key not found. Make sure to set it in .env file.")
    exit(1)

UDP_IP = "0.0.0.0"
UDP_PORT = 10120

ALLOWED_CLIENTS = {"130.245.192.1", "223.178.210.32", "localhost"}

sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

sock.bind((UDP_IP, UDP_PORT))

print(f"Server running on {UDP_IP}:{UDP_PORT}")

CONNECTED_CLIENTS = {}

while True:
    try:
        data, addr = sock.recvfrom(1024)

        token, msg_type, msg = data.decode('utf-8').split(':')
        # message = {auth_key}:{msg_type}:{msg}

        if addr[0] in ALLOWED_CLIENTS:
            if token == auth_token:

                if addr not in CONNECTED_CLIENTS.keys():
                    print(f"Received connection request from {addr}")
                    if msg_type == "ClientHello":
                        CONNECTED_CLIENTS[addr] = msg
                        print(f"Added client {addr} ({msg})")

                        sock.sendto(f"Hello, {msg}!".encode('utf-8'), addr)

                        for client in CONNECTED_CLIENTS.keys():
                            sock.sendto(f"New user {msg} joined!".encode('utf-8'), client)

                    else:
                        print(f"Incorrect ClientHello")
                        sock.sendto("Incorrect auth token.".encode('utf-8'), addr)

                else:
                    if msg_type == "ListUsers":
                        print(f"{addr} ({CONNECTED_CLIENTS[addr]}) requested user list")
                        users_list = "\n".join(CONNECTED_CLIENTS.values())
                        sock.sendto(users_list.encode('utf-8'), addr)

                    elif msg_type == "ClientBye":
                        print(f"{addr} ({CONNECTED_CLIENTS[addr]}) disconnecting")

                        del CONNECTED_CLIENTS[addr]
                        sock.sendto(f"Bye, {msg}!".encode('utf-8'), addr)

                        for client in CONNECTED_CLIENTS.keys():
                            sock.sendto(f"User {msg} left!".encode('utf-8'), client)
            else: 
                sock.sendto("Incorrect auth token.".encode('utf-8'), addr)

        else:
            sock.sendto("Unauthorized access!".encode('utf-8'), addr)

    except KeyboardInterrupt:
        print("Server stopped")
        break

sock.close()
