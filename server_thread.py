from socket import *
import socket
import threading
import logging
import time
import sys


class ProcessTheClient(threading.Thread):
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)
        
    def run(self):
        rcv = ""
        while True:
            try:
                data = self.connection.recv(32)
                # melakukan perubahan input dari socket yang berbentuk bytes menjadi string
                # untuk melakukan klasifikasi CRLF (karakter 13 dan 10)
                dataText = data.decode()
                rcv = rcv + dataText
                if data:
                    logging.warning(f"Server is receiving {data} from {self.address}")
                    if rcv[:4] == 'TIME' and rcv[-2:] == '\r\n':
                        currTime = time.strftime("%H:%M:%S")
                        responseText = f"JAM {currTime}\r\n".encode()
                        logging.warning(f"Server is sending {responseText} to {self.address}")
                        self.connection.sendall(responseText)
                        rcv = ""
                        self.connection.close()
                    else:
                        responseText = "Req is rejected by the server."
                        self.connection.sendall(responseText.encode())
                else:
                    break
            except OSError as e:
                pass
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0',45000))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")
                     
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()
