import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from recordMouseKeyboardMovement import record, replay


recording_flag = {"stop": False}
record_thread = None

def should_stop():
    return recording_flag["stop"]

recorded_filename = {"name": None}

def start_record():
    global record_thread
    recording_flag["stop"] = False

    def run_record():
        filename = record(should_stop_callback=should_stop)
        recorded_filename["name"] = filename

    record_thread = Thread(target=run_record)
    record_thread.daemon = True
    record_thread.start()

def stop_record():
    recording_flag["stop"] = True
    if record_thread and record_thread.is_alive():
        record_thread.join()
    if recorded_filename["name"]:
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
