import socket

TARGET_UDP_IP = "localhost"
TARGET_UDP_PORT = 10120

print(f'UDP target IP: {TARGET_UDP_IP}')
print(f'UDP target PORT: {TARGET_UDP_PORT}')

SERVER_ADDRESS = (TARGET_UDP_IP, TARGET_UDP_PORT)
sock = socket.socket(
        socket.AF_INET, 
        socket.SOCK_DGRAM
    )

auth_token = "33aee0ec5ce9816b7c8be17dcd899871235d6583312829316b6f72ce65a5b791"

try:
    while True:
        message = input("Enter message to send: ")
        sock.sendto(f"{auth_token}:{message}".encode('utf-8'), (SERVER_ADDRESS))

        acknowledgement, server_add = sock.recvfrom(1024)
        print(f"Acknowledgement from server: {acknowledgement.decode('utf-8')}")

except KeyboardInterrupt:
    print('Client stopping')

finally:
    sock.close()
