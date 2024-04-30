import socket
import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define button pin
button_pin = 4
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Handle button press
def handle_button_press():
    # Set the pin to output mode
    GPIO.setup(button_pin, GPIO.OUT)
    # Turn the pin on and off to simulate a button press
    GPIO.output(button_pin, GPIO.HIGH)
    GPIO.output(button_pin, GPIO.LOW)
    # Set the pin back to input mode
    GPIO.setup(button_pin, GPIO.IN)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address of 'sunlab D' and port 5000
server_address = ('172.21.5.26', 5000)
print(f'Starting up on {server_address[0]} port {server_address[1]}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print('Waiting for a connection')

# Accept the connection
connection, client_address = sock.accept()

try:
    print(f'Connection from {client_address}')

    while True:
        # Check if the button is pressed
        if GPIO.input(button_pin) == GPIO.LOW:
            handle_button_press()

            # Wait for button release
            while GPIO.input(button_pin) == GPIO.LOW:
                time.sleep(0.1)

            print("The button has been pressed")

            try:
                # Send a message to the client
                connection.send(b'Button pressed')
            except ConnectionResetError:
                print("Client closed the connection")
                break

except KeyboardInterrupt:
    print('Closing socket')
    sock.close()
