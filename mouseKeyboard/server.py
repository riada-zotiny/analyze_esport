# serveur_enregistrement.py
import socket
import threading
from recordMouseKeyboardMovement import record
import sys

HOST = "0.0.0.0"
PORT = 5001

recording_flag = {"stop": False}
record_thread = None

def should_stop():
    return recording_flag["stop"]

def start_recording(filename=None):
    global record_thread
    recording_flag["stop"] = False
    def run_record():
        print(f"Démarrage de l'enregistrement clavier/souris : {filename}")
        record(should_stop_callback=should_stop, filename=filename)
        print("🛑 Enregistrement terminé")
    record_thread = threading.Thread(target=run_record, daemon=True)
    record_thread.start()

def stop_recording():
    print("Arrêt demandé")
    recording_flag["stop"] = True
    if record_thread:
        record_thread.join(timeout=5)
    print("Enregistrement arrêté")
    sys.exit(0)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[Serveur prêt sur le port {PORT}]")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[Signal reçu de {addr}]")
                data = conn.recv(1024).decode().strip()
                if data == "LANCER":
                    conn.sendall(b"NAME?")
                    filename = conn.recv(1024).decode().strip()
                    if not filename.endswith(".json"):
                        filename += ".json"
                    conn.sendall(b"OK")
                    start_recording(filename)
                elif data == "STOP":
                    conn.sendall(b"OK")
                    stop_recording()
                else:
                    conn.sendall(b"Signal inconnu")

if __name__ == "__main__":
    main()
