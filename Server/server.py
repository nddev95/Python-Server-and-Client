import socket
import time
import logging
import threading
from datetime import datetime

connected_clients = {}

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    handlers=[
                        logging.FileHandler("server_log.txt"),
                        logging.StreamHandler()
                    ])

def handle_client(client_socket, client_name):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                logging.info(f"{client_name} disconnected.")
                connected_clients.pop(client_name)
                break

            logging.info(f"Received from {client_name}: {data}")

            # Sende Keep Alive zurück zum Client
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Keep Alive from server at {timestamp}"
            client_socket.send(message.encode())

            time.sleep(5)
        except ConnectionResetError:
            logging.info(f"{client_name} closed the connection.")
            connected_clients.pop(client_name) 
            break

    client_socket.close()

def server_program():
    host = '0.0.0.0'
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        conn, address = server_socket.accept()
        client_name = conn.recv(1024).decode()
        logging.info(f"Connection from {client_name}: {str(address)}")

        if client_name in connected_clients:
            logging.info(f"{client_name} is already connected.")
            conn.send("Duplicate client name. Please choose a different name.".encode())
            conn.close()
            continue

        connected_clients[client_name] = conn

        client_thread = threading.Thread(target=handle_client, args=(conn, client_name))
        client_thread.start()

if __name__ == '__main__':
    server_program()
