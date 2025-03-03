import socket
from machine import Pin

class HTTPServer:
    def __init__(self, port=80):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.sock.listen(1)
    
    def get_ip(self):
        return self.wifi.ifconfig()[0]
    
    def start(self):
        while True:
            conn, addr = self.sock.accept()
            request = conn.recv(1024).decode()
            
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
            conn.send(response.encode())
            conn.close()