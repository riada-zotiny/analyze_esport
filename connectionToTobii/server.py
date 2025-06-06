import socket
import asyncio
from g3pylib import connect_to_glasses
import sys
import aiohttp
import shutil

HOST = '0.0.0.0'
PORT = 5000
G3_HOSTNAME = "192.168.75.51"

async def start_recording():
    async with connect_to_glasses.with_hostname(G3_HOSTNAME) as g3:
        serial = await g3.system.get_recording_unit_serial()
        print(f"Connecté à : {serial}")
        await g3.recorder.start()
        print("Enregistrement a commencé !")

async def stop_recording():
    async with connect_to_glasses.with_hostname(G3_HOSTNAME) as g3:
        serial = await g3.system.get_recording_unit_serial()
        await g3.recorder.stop()
        print("Enregistrement arrêté !")
        
        recordings = await g3.recordings.list()
        if not recordings:
            print("Aucun enregistrement trouvé.")
            sys.exit()


        last_recording = recordings[-1]
        rec_id = last_recording["id"]
        print(f"Téléchargement de l'enregistrement {rec_id}...")
        url = f"http://{G3_HOSTNAME}/rest/recordings/{rec_id}/export"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(f"recording_{rec_id}.zip", "wb") as f:
                        shutil.copyfileobj(await resp.content, f)
                    print(f"Enregistrement sauvegardé sous recording_{rec_id}.zip")
                else:
                    print("Erreur lors du téléchargement :", resp.status)
        sys.exit()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[En attente de connexion sur le port {PORT}]")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[Connecté par] {addr}")
                data = conn.recv(1024).decode().strip()
                if data == "LANCER":
                    print("[Signal reçu] Lancement du programme...")
                    conn.sendall(b"OK")
                    asyncio.run(start_recording())
                elif data == "STOP":
                    print("[Signal reçu] Arrêt de l'enregistrement...")
                    conn.sendall(b"OK")
                    asyncio.run(stop_recording())
                else:
                    print("[Signal invalide]")
                    conn.sendall(b"Signal invalide")

if __name__ == "__main__":
    main()