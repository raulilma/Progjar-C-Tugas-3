import sys
import socket
import logging
from concurrent.futures import ThreadPoolExecutor # untuk mengimplementasikan threadpool pada klien
import time # untuk melakukan analisis testing thread

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

def threadpool_kirim():
    with ThreadPoolExecutor() as executor:
        threadpool = 0
        catat_awal = time.time()
        futures = set()
        while time.time() - catat_awal < 60:
            future = executor.submit(kirim_data)
            futures.add(future)
            
            # Hapus future yang sudah selesai dari arr dan tambahkan ke futures_selesai
            futures_selesai = {future for future in futures if future.done()}
            threadpool += len(futures_selesai)
            futures -= futures_selesai

        # Tunggu semua task selesai sebelum keluar dari program
        for future in futures:
            future.result()

        # Cetak jumlah request yang telah dikirim setelah loop selesai
        logging.warning(f"Total threadpool yang dikirim: {threadpool}")

if __name__=='__main__':
    threadpool_kirim()
