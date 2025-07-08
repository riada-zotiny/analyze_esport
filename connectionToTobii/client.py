import tkinter as tk
from tkinter import messagebox, simpledialog
import asyncio
import sys
import socket
import threading
from g3pylib import connect_to_glasses

G3_HOSTNAME = "192.168.75.51"  # Adresse IP des lunettes Tobii
SERVER_IP = "192.168.1.1"       # Adresse IP du PC enregistreur souris/clavier
SERVER_PORT = 5001

def send_signal(signal, filename=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(signal.encode())
            if signal == "LANCER":
                response = s.recv(1024).decode()
                if response == "NAME?":
                    s.sendall(filename.encode())
                    print(f"[Client] Nom de fichier envoyé : {filename}")
            elif signal == "STOP":
                response = s.recv(1024).decode()
                print(f"[Client] Réponse STOP : {response}")
        print("[Client] Signal envoyé :", signal)
    except Exception as e:
        print(f"Erreur d'envoi du signal : {e}")

async def start_record():
    async with connect_to_glasses.with_hostname(G3_HOSTNAME) as g3:
        serial = await g3.system.get_recording_unit_serial()
        print(f"[Tobii] Connecté à : {serial}")
        await g3.recorder.start()
        print("[Tobii] Enregistrement démarré")

async def stop_record():
    async with connect_to_glasses.with_hostname(G3_HOSTNAME) as g3:
        async with g3.recordings.keep_updated_in_context():
            serial = await g3.system.get_recording_unit_serial()
            await g3.recorder.stop()
            print("[Tobii] Enregistrement arrêté")

def on_record_callback():
    def ask_filename():
        filename = simpledialog.askstring("Nom du fichier", "Entrez un nom pour l'enregistrement :")
        if not filename:
            messagebox.showwarning("Erreur", "Nom invalide.")
            return
        if not filename.endswith(".json"):
            filename += ".json"

        # Envoyer le signal à l'autre PC (serveur souris/clavier)
        send_signal("LANCER", filename=filename)

        # Démarrer l'enregistrement Tobii
        threading.Thread(target=lambda: asyncio.run(start_record())).start()
        messagebox.showinfo("Info", "Enregistrement Tobii démarré avec succès.")

    root.after(0, ask_filename)

def off_record_callback():
    def task():
        asyncio.run(stop_record())
        send_signal("STOP")
        messagebox.showinfo("Info", "Enregistrement Tobii et souris/clavier arrêté.")
    threading.Thread(target=task).start()

# Interface graphique
root = tk.Tk()
root.title("Contrôle Enregistrement Tobii")
root.geometry("400x200")
root.resizable(False, False)

record_button = tk.Button(root, text="Démarrer l'enregistrement", command=on_record_callback,
                          font=("Arial", 12), bg="green", fg="white", width=30)
record_button.pack(pady=20)

stop_button = tk.Button(root, text="Arrêter l'enregistrement", command=off_record_callback,
                        font=("Arial", 12), bg="red", fg="white", width=30)
stop_button.pack(pady=10)

root.mainloop()