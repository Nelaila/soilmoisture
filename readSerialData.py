import serial
import time
import os


def readserial(comport, baudrate, output_file):
    # check if output_file already exists, and if yes delete it
    try:
        os.remove(output_file)
    except OSError:
        pass

    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read


    with open(output_file, 'a') as file:
        while True:

            data = ser.readline().decode().strip()

            if data:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                line = f'{timestamp}\t{data}'
                file.write(line + '\n')
                file.flush()


if __name__ == '__main__':

    readserial('COM3', 9600, 'realtimeData.txt')