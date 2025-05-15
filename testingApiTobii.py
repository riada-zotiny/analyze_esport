import asyncio
import threading
import tkinter as tk
from tkinter import messagebox
from g3pylib import TobiiG3

# Remplace par l’adresse de TES lunettes (ex: 192.168.75.51 ou TG03B-xxxx.local)
G3_ADDRESS = "192.168.75.51"

class TobiiApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tobii Glasses 3 Controller")

        self.status_label = tk.Label(master, text="Status: Déconnecté", fg="red")
        self.status_label.pack(pady=10)

        tk.Button(master, text="Connecter aux lunettes", command=self.run_async(self.connect)).pack(pady=5)
        tk.Button(master, text="Calibration", command=self.run_async(self.calibrate)).pack(pady=5)
        tk.Button(master, text="Démarrer l'enregistrement", command=self.run_async(self.start_recording)).pack(pady=5)
        tk.Button(master, text="Arrêter l'enregistrement", command=self.run_async(self.stop_recording)).pack(pady=5)
        tk.Button(master, text="Quitter", command=self.quit).pack(pady=10)

        self.loop = asyncio.new_event_loop()
        self.glasses = TobiiG3(G3_ADDRESS)

        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def run_async(self, coro_func):
        def wrapper():
            asyncio.run_coroutine_threadsafe(coro_func(), self.loop)
        return wrapper

    async def connect(self):
        try:
            await self.glasses.connect()
            self.status_label.config(text="Status: Connecté", fg="green")
        except Exception as e:
            messagebox.showerror("Erreur de connexion", str(e))

    async def calibrate(self):
        try:
            await self.glasses.perform_action("calibrate!emit-markers")
            await asyncio.sleep(3)
            await self.glasses.perform_action("calibrate!run")
            messagebox.showinfo("Calibration", "Calibration terminée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur de calibration", str(e))

    async def start_recording(self):
        try:
            await self.glasses.perform_action("recorder!start")
            await self.glasses.set_property("recorder.visible-name", "TestRecording")
            messagebox.showinfo("Enregistrement", "Enregistrement démarré.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    async def stop_recording(self):
        try:
            await self.glasses.perform_action("recorder!stop")
            messagebox.showinfo("Enregistrement", "Enregistrement arrêté.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def quit(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.master.destroy()

# Lancer l'app
root = tk.Tk()
app = TobiiApp(root)
root.mainloop()
