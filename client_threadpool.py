import sys
import socket
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('172.19.0.3', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = "TIME\r\n".encode()
        logging.warning(f"[CLIENT] sending {message}")
        sock.sendall(message)
        # Look for the response
        data = sock.recv(32)
        logging.warning(f"[DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning("closing")
        sock.close()
    return

if __name__ == '__main__':
    threads = 0
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        while True:
            if time.time() - start_time >= 60:
                break
            threads += 1
            executor.submit(kirim_data)
            logging.warning(f"Diff: {time.time() - start_time} - threads: {threads}")
    logging.warning(f"Total thread yang dibuat: {threads}")
