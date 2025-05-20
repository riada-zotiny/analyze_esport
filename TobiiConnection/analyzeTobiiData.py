import pandas as pd

import os
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "..", "dataEyeTracking", "TestTobiiDataexport.tsv")
tobii_data = pd.read_csv(file_path, sep='\t')
print(tobii_data.head())


list_of_columns = list(tobii_data.columns)
for i in range(len(list_of_columns)):
    print(f"Column {i}: {list_of_columns[i]}")


#print("Données sur export date ", tobii_data['Export Date'].unique())


# Affiche les lignes où les deux colonnes sont différentes
diff = tobii_data["Recording timestamp"] != tobii_data["Computer timestamp"]
print("Nombre de différences :", diff.sum())
print(tobii_data[diff][["Recording timestamp", "Computer timestamp"]])


tobii_data['Recording timestamp'] = pd.to_datetime(tobii_data['Recording timestamp'], errors='coerce')
print(tobii_data['Recording timestamp'].head())