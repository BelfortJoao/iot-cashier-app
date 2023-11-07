import serial
import time as t
from matplotlib import pyplot as plt
import numpy as np
import struct

# Define the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Replace 'COMX' with the actual port name

try:
    i = 0  # Initialize the filename index
    while True:
        line = ser.readline()
        line_str = line.decode('utf-8').strip()
        print("foto tirada")  # Print the received line
        t.sleep(1)

        # Split the line into individual values
        values = line_str.split(', ')
        hexadecimal = [int(value, 16) for value in values if value.startswith("0x")]

        if not hexadecimal:
            continue  # Skip lines that don't contain valid hexadecimal values

        # Reformat the bytes into an image
        raw_bytes = np.array(hexadecimal).astype(np.int16)
        image = np.zeros((len(raw_bytes), 3), dtype=np.uint8)  # Ensure data type is uint8

        # Loop through all of the pixels and form the image
        for j in range(len(raw_bytes)):
            # Read 16-bit pixel
            pixel = struct.unpack('>h', raw_bytes[j])[0]

            # Convert RGB565 to RGB 24-bit
            r = ((pixel >> 11) & 0x1f) << 3
            g = ((pixel >> 5) & 0x3f) << 2
            b = ((pixel >> 0) & 0x1f) << 3
            image[j] = [r, g, b]

        image = np.reshape(image, (144, 176, 3))  # QCIF resolution

        plt.imsave(f"images//image_{i}.jpg", image)
        i += 1  # Increment the filename index for each iteration

except KeyboardInterrupt:
    ser.close()
