# client.py (PC émetteur)
import socket
import time

HOST = '192.168.1.2'  
PORT = 5000


# signal = "LANCER"  # Signal to send to the server
# signal = "STOP"  # Signal to send to the server
def send_signal(signal):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"signal")
        data = s.recv(1024)
        print("[Signal envoyé]")
        time.sleep(1)
        print("Réponse du serveur :", data.decode())

send_signal("LANCER")

