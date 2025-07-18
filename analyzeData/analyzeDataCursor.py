import os
import json
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data_dir = os.path.join(os.getcwd(), "dataMouseKeybord")
files = [f for f in os.listdir(data_dir) if f.endswith(".json")]

if not files:
    print("Aucun fichier JSON trouvé dans dataMouseKeybord.")
    exit()

print("Fichiers disponibles :")
for idx, fname in enumerate(files, 1):
    print(f"{idx}. {fname}")

choice = input("Entrez le numéro du fichier à importer : ")
try:
    idx = int(choice) - 1
    if idx < 0 or idx >= len(files):
        raise ValueError
except ValueError:
    print("Choix invalide.")
    exit()

selected_file = os.path.join(data_dir, files[idx])
print(f"Fichier sélectionné : {selected_file}")

with open(selected_file, "r", encoding="utf-8") as f:
    data = json.load(f)


if isinstance(data, list) and data:
    print("Premier élément du tableau :")
    print(data[0])
    start_time = data[0].get("timestamp", "Inconnu")
    print(f"Heure de début : {start_time}") 
    print("\nDernier élément du tableau :")
    print(data[-1])
    end_time = data[-1].get("timestamp", "Inconnu")
    print(f"Heure de fin : {end_time}")

    if start_time != "Inconnu" and end_time != "Inconnu":
        try:
            t1 = datetime.fromisoformat(start_time)
            t2 = datetime.fromisoformat(end_time)
            duree = t2 - t1
            print(f"\nDurée totale : {duree}")
        except Exception as e:
            print("Erreur lors du calcul de la durée :", e)
    else:
        print("Impossible de calculer la durée (timestamp manquant).")
else:
    print("Le fichier ne contient pas un tableau JSON non vide.")

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

df['position'] = df['position'].apply(
    lambda x: x if isinstance(x, list) and len(x) == 2 else [None, None]
)
df[['x', 'y']] = pd.DataFrame(df['position'].tolist(), index=df.index)

print("\nAperçu des données :")
print(df.head())

mode = input("\nChoisissez le type de visualisation ('heatmap' ou 'scanpath') : ").strip().lower()

if mode == "heatmap":
    # Filtrer uniquement les positions lors d'un clic souris (action "press")
    mouse_clicks = df[df['action'] == 'press'] 
    mouse_clicks = mouse_clicks.dropna(subset=['x', 'y'])
    plt.figure(figsize=(10, 6))
    if not mouse_clicks.empty:
        sns.kdeplot(x=mouse_clicks['x'], y=mouse_clicks['y'], fill=True, cmap="viridis", thresh=0.05)
        plt.title("Heatmap des positions du curseur lors des clics souris")
        plt.xlabel("Position X")
        plt.ylabel("Position Y")
        plt.xlim(0, 1920)
        plt.ylim(0, 1080)
        plt.show()
    else:
        print("Aucun clic souris à afficher pour la heatmap.")

elif mode == "scanpath":
    clicks = df[(df['action'] == 'press') & (df['button'] == 'Button.left')]
    scan_points = []
    for _, row in clicks.iterrows():
        if isinstance(row['position'], list) and len(row['position']) == 2:
            scan_points.append({'x': row['x'], 'y': row['y'], 'timestamp': row['timestamp']})

    # On enlève les deux premiers et les deux derniers clics
    if len(scan_points) > 4:
        scan_points = scan_points[2:-2]
    else:
        scan_points = []

    scan_df = pd.DataFrame(scan_points)

    if not scan_df.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(scan_df['x'], scan_df['y'], marker='o', linestyle='-', markersize=6)
        plt.gca().invert_yaxis()  
        plt.title("Scan Path des clics gauche (origine en haut à gauche)")
        plt.xlabel("Position X")
        plt.ylabel("Position Y")
        plt.xlim(0, 1920)
        plt.ylim(0, 1080)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("Pas assez de clics gauche pour générer un scan path (au moins 5 nécessaires).")
