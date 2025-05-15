import pandas as pd

import os
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "..", "dataMouseKeybord", "mouse_keyboard_actions_2025-05-13_num2.json")

df = pd.read_json(file_path)

print(" Affichage des premières lignes de fichier JSON :")
print(df.head())


print(df['time_diff'])

df_without_NaN_button  = df.loc[df['button'].notna()]
df_without_NaN_key = df.loc[df['key'].notna()]

print("Affichage des premières lignes de df_without_NaN_button :")
print(df_without_NaN_button.head())
print("Affichage des premières lignes de df_without_NaN_key :") 
print(df_without_NaN_key.head())


import matplotlib.pyplot as plt
hist = df.hist()
plt.show()