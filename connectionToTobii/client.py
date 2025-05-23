# client.py (PC émetteur)
import socket

HOST = '192.168.1.2'  # Adresse IP du PC récepteur
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"LANCER")
    print("[Signal envoyé]")
