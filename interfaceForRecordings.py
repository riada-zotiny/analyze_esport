import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from mouseKeyboard.recordMouseKeyboardMovement  import record, replay
import socket
import datetime
from tkinter import simpledialog

HOST = '192.168.1.2'
PORT = 5000

def send_signal(signal):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(signal.encode())
        data = s.recv(1024)
        print("[Signal envoyé]")
        print("Réponse du serveur :", data.decode())


recording_flag = {"stop": False}
record_thread = None

def should_stop():
    return recording_flag["stop"]

recorded_filename = {"name": None}

def start_record():
    global record_thread
    recording_flag["stop"] = False


    # Demander le nom du fichier à l'utilisateur
    user_filename = simpledialog.askstring("Nom du fichier", "Entrez le nom du fichier (sans extension) :")
    if not user_filename:
        messagebox.showwarning("Nom manquant", "Aucun nom de fichier fourni, enregistrement annulé.")
        return

    # Ajouter la date/heure au nom
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    final_filename = f"{user_filename}_{date_str}.json"
    recorded_filename["name"] = final_filename
    try:
        send_signal("LANCER")
    except ImportError as ie:
        messagebox.showerror("Erreur d'import", f"Impossible d'importer send_signal : {ie}")
        return
    except Exception as e:
        messagebox.showerror("Erreur réseau", f"Impossible d'envoyer le signal : {e}")
        return

    def run_record():
        filename = record(should_stop_callback=should_stop)
        recorded_filename["name"] = filename

    record_thread = Thread(target=run_record)
    record_thread.daemon = True
    record_thread.start()

def stop_record():
    recording_flag["stop"] = True
    try:
        send_signal("STOP")
    except ImportError as ie:
        messagebox.showerror("Erreur d'import", f"Impossible d'importer send_signal : {ie}")
        return
    except Exception as e:
        messagebox.showerror("Erreur réseau", f"Impossible d'envoyer le signal d'arrêt : {e}")
        return

    if recorded_filename["name"]:
        # Extraire la date du nom de fichier
        try:
            date_part = recorded_filename["name"].rsplit("_", 1)[1].replace(".json", "")
            messagebox.showinfo("Enregistrement terminé", f"Fichier enregistré : {recorded_filename['name']}\nDate : {date_part}")
        except Exception:
            messagebox.showinfo("Enregistrement terminé", f"Fichier enregistré : {recorded_filename['name']}")
    else:
        messagebox.showwarning("Enregistrement", "Aucun fichier n'a été enregistré.")
        
def start_replay():
    file_path = filedialog.askopenfilename(
        title="Choisir un fichier JSON",
        filetypes=[("Fichiers JSON", "*.json")],
        initialdir="dataMouseKeybord"
    )
    if file_path:
        try:
            filename = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            replay(filename, key_delay=0, on_finish=root.quit)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


root = tk.Tk()
root.title("Contrôle Souris & Clavier")
root.geometry("400x250")
root.resizable(False, False)

# Boutons
record_button = tk.Button(root, text="Enregistrer", command=start_record, font=("Arial", 10), bg="green", fg="white", width=20)
record_button.pack(pady=10)

stop_button = tk.Button(root, text="Arrêter", command=stop_record, font=("Arial", 10), bg="red", fg="white", width=20)
stop_button.pack(pady=10)

replay_button = tk.Button(root, text="Rejouer", command=start_replay, font=("Arial", 10), bg="blue", fg="white", width=20)
replay_button.pack(pady=10)

root.mainloop()
