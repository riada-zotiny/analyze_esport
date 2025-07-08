import os
import json
import pandas as pd

def load_json_to_df(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df


def type_of_data(df, kind_of_data, keyboard = None):
    if kind_of_data == "movements" and keyboard == "french":
        df = df[(df['event'] == 'q') | (df['event'] == 's') | (df['event'] == 'd') | (df['event'] == 'f')]
        return df
    elif kind_of_data == "movements" and keyboard == "english":
        df = df[ (df['event'] == 'a') | (df['event'] == 's') | (df['event'] == 'd') | (df['event'] == 'f')]
        return df
    elif kind_of_data == "clicks":
        df = df[(df['action'] == 'press') | (df['action'] == 'release')]
        return df
    elif kind_of_data == "cursor":
        df = df[df['action'] == 'move']
        return df
    else:
        raise ValueError("Type de données non reconnu. Choisissez 'movements', 'clicks' ou 'cursor'.")
    
    
# traitement des données manquantes
# à venir 

 



if __name__ == "__main__":
    data_dir = os.path.join(os.getcwd(), "dataMouseKeybord")
    files = [f for f in os.listdir(data_dir) if f.endswith(".json")]

    if not files:
        print("Aucun fichier JSON trouvé dans dataMouseKeybord.")
        exit()

    print("Fichiers disponibles :")
    for idx, fname in enumerate(files, 1):
        print(f"{idx}. {fname}")

    choice = input("Entrez le numéro du fichier à ouvrir : ")
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(files):
            raise ValueError
    except ValueError:
        print("Choix invalide.")
        exit()

    selected_file = os.path.join(data_dir, files[idx])
    df = load_json_to_df(selected_file)
    

    df_cursor = type_of_data(df, kind_of_data="cursor")
    df_clicks = type_of_data(df, kind_of_data="clicks")

    print("Données de curseur :")
    print(df_cursor.head())
    print("\nDonnées de clics :")
    print(df_clicks.head())


    

