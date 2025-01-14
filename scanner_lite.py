
import os
import serial
import time
from picamera2 import Picamera2
import subprocess

# Initialize serial communication (update with your port and baud rate)
SERIAL_PORT = '/dev/ttyACM0'  # Change to '/dev/ttyAMA0' or your specific port
BAUD_RATE = 9600

# Initialize PiCamera2
camera = Picamera2()
camera.configure(camera.create_still_configuration())

# Ask for project name and create folder
project_name = input("Enter project name: ").strip()
project_folder = os.path.join(os.getcwd(), project_name)
os.makedirs(project_folder, exist_ok=True)
print(f"Project folder created: {project_folder}")

try:
    # Set up serial communication
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud.")
    camera.start()  # Start the camera

    image_count = 0  # Counter for images

    while True:
        # Read incoming serial data
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').strip()
            print(f"Received command: {command}")

            if command == "CAPTURE":
                # Generate a unique filename for the image
                filename = os.path.join(project_folder, f"image_{image_count:03}.jpg")
                print(f"Capturing image: {filename}")
                camera.capture_file(filename)
                image_count += 1

                # Send acknowledgment back to Arduino
                ser.write(b"Image Captured\n")
                print("Acknowledgment sent.")

            elif command == "DONE":
                print("Arduino has finished its task.")
                # Clean up resources
                camera.stop()
                if 'ser' in locals():
                    ser.close()
                print("Camera and serial communication closed.")

                break  # O continuare se il flusso deve proseguire
            else:
                print("Unknown command received.")

    
