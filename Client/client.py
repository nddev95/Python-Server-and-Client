import socket
import time
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    handlers=[
                        logging.FileHandler("client_log.txt"),
                        logging.StreamHandler()
                    ])

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
                message = f"Keep Alive from {client_name}"
                client_socket.send(message.encode())
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
