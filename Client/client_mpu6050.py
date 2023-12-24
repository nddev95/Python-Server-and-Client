import socket
import time
import logging
import sys
from mpu6050 import mpu6050  # Import der MPU6050-Bibliothek

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    handlers=[
                        logging.FileHandler("client_log.txt"),
                        logging.StreamHandler()
                    ])

def read_sensor_values():
    sensor = mpu6050(0x68)  # Adresse des MPU6050-Sensors

    while True:
        try:
            gyro_data = sensor.get_gyro_data()  # Gyroskop-Daten abrufen
            # Hier könntest du weitere Sensordaten wie Beschleunigung, Temperatur usw. abrufen

            # Formatieren der Sensorwerte als Nachricht an den Server
            message = f"Gyro Data - X: {gyro_data['x']}, Y: {gyro_data['y']}, Z: {gyro_data['z']}"

            return message
        except Exception as e:
            logging.error(f"Fehler beim Lesen des Sensors: {str(e)}")
            time.sleep(1)
            continue

def client_program(client_name):
    host = '0.0.0.0'
    port = 5000

    while True:
        client_socket = socket.socket()

        try:
            client_socket.settimeout(5)
            client_socket.connect((host, port))
            client_socket.send(client_name.encode())
            logging.info("Connected to server.")
        except ConnectionRefusedError:
            logging.info("Connection to server failed. Server may be unavailable.")
            time.sleep(5)
            continue
        except socket.timeout:
            logging.info("Connection attempt timed out. Server may be unreachable.")
            time.sleep(5)
            continue

        while True:
            try:
                sensor_message = read_sensor_values()  # Sensorwerte lesen
                client_socket.send(sensor_message.encode())  # Sensorwerte an den Server senden
                data = client_socket.recv(1024).decode()

                if data == "Duplicate client name. Please choose a different name.":
                    logging.info("Duplicate client name. Exiting.")
                    sys.exit()

                logging.info(f"Received from server: {str(data)}")
                time.sleep(5)
            except ConnectionError:
                logging.info("Connection to server lost.")
                break

        client_socket.close()

if __name__ == '__main__':
    client_program("Client1")
