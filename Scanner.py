#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:30:10 2024

@author: stefanopetraccini
"""

import os
import serial
import time
from picamera2 import Picamera2
import subprocess

# Initialize serial communication (update with your port and baud rate)
SERIAL_PORT = '/dev/ttyUSB0'  # Change to '/dev/ttyAMA0' or your specific port
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

            elif command == "STOP":
                print("Stopping capture session...")
                break

            else:
                print("Unknown command received.")

    # After capturing images, start 3D reconstruction
    if image_count > 0:
        print(f"Starting 3D reconstruction with {image_count} images...")
        reconstruction_folder = os.path.join(project_folder, "reconstruction")
        os.makedirs(reconstruction_folder, exist_ok=True)

        # Run pycolmap reconstruction command
        try:
            subprocess.run([
                "pycolmap",
                "reconstruct",
                "--image_path", project_folder,
                "--output_path", reconstruction_folder
            ], check=True)
            print(f"3D reconstruction completed. Results saved in {reconstruction_folder}.")
        except FileNotFoundError:
            print("pycolmap not found. Please ensure it is installed and available in your PATH.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during reconstruction: {e}")

    else:
        print("No images were captured. Skipping reconstruction.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up resources
    camera.stop()
    if 'ser' in locals():
        ser.close()
    print("Camera and serial communication closed.")
