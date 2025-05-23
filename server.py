import socket
import subprocess
import asyncio
from g3pylib import connect_to_glasses

HOST = '0.0.0.0'  # Écoute toutes les interfaces
PORT = 5000       # Port d'écoute
G3_HOSTNAME = "192.168.75.51"

async def connect():
    async with connect_to_glasses.with_hostname( G3_HOSTNAME, using_zeroconf=False, using_ip=True) as g3:
        serial = await g3.system.get_recording_unit_serial()
        print(f"Connecté à : {serial} ")

        await g3.recorder.start()
        print("Enregistrement a comméncé !")

        await asyncio.sleep(10)

        await g3.recorder.stop()
        print("Enregistrement terminéé ")


async def main():
    await connect()


     

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[En attente de connexion sur le port {PORT}]")
    conn, addr = s.accept()
    with conn:
        print(f"[Connecté par] {addr}")
        data = conn.recv(1024).decode()
        if data == "LANCER":
            print("[Signal reçu] Lancement du programme...")
            # Remplace 'notepad.exe' par le programme que tu veux lancer
            asyncio.run(main())   
        else:
            print("[Signal invalide]")