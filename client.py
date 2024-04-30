import socket

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server IP address and port
server_address = ('172.21.5.26', 5000)
print(f'Connecting to {server_address[0]} port {server_address[1]}')
sock.connect(server_address)

try:
    while True:
        try:
            # Receive a message from the server
            received_message = sock.recv(16)
            if received_message:
                print('Notification was received')
            else:
                # No message means the server has closed the connection
                print("No data received. Server may have closed the connection.")
                break
        except ConnectionResetError:
            print("Server closed the connection")
            break
        except KeyboardInterrupt:
            print('Closing socket')
            sock.close()
            break
except Exception as e:
    print(f'An error occurred: {e}')
    sock.close()
