import os 

print(os.getcwd())

import sys
!{sys.executable} -m pip install --user folium
!{sys.executable} -m pip install --user pandasgui


import pandas as pd
import folium
import webbrowser

# 1) Lecture du CSV
fichier = "C:\\Users\\vosnitia\\Downloads\\experimentations_5G.csv"
df = pd.read_csv(fichier, sep=';', encoding='cp1252')

# 2) Nettoyage
df["Latitude"] = df["Latitude"].str.replace(",", ".").astype(float)
df["Longitude"] = df["Longitude"].str.replace(",", ".").astype(float)

# 3) Synthèse par région
synthese = (
    df.groupby("Région")
    .agg({
        "Expérimentateur": lambda x: ", ".join(sorted(set(x))),
        "Bande de fréquences": lambda x: ", ".join(sorted(set(x))),
        "Latitude": "count"
    })
    .rename(columns={
        "Latitude": "Nombre d'expérimentations",
        "Expérimentateur": "Acteurs",
        "Bande de fréquences": "Bandes"
    })
    .reset_index()
)

# 4) Génération d’un tableau HTML lisible
html_table = synthese.to_html(index=False, justify='left', border=1)

# 5) On ajoute un titre
html_page = f"""
<html>
<head>
    <meta charset="utf-8">
    <title>Synthèse 5G par région</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ text-align: center; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ padding: 8px 12px; border: 1px solid #aaa; }}
        th {{ background-color: #e5e5e5; }}
    </style>
</head>
<body>
    <h1>Synthèse des expérimentations 5G par région</h1>
    {html_table}
    <br><br>
    <a href="carte_5G.html">Voir la carte interactive</a>
</body>
</html>
"""

# 6) Sauvegarde du tableau HTML
with open("synthese_5G.html", "w", encoding="utf-8") as f:
    f.write(html_page)

# 7) Carte interactive
m = folium.Map(location=[46.6, 2.5], zoom_start=5)

for _, ligne in df.iterrows():
    popup = (
        f"<b>{ligne['Région']}</b><br>"
        f"Acteur : {ligne['Expérimentateur']}<br>"
        f"Bande : {ligne['Bande de fréquences']}"
    )
    folium.Marker(
        location=[ligne["Latitude"], ligne["Longitude"]],
        popup=popup,
        tooltip=ligne["Région"]
    ).add_to(m)

m.save("carte_5G.html")

# 8) Ouverture du tableau dans le navigateur
webbrowser.open("synthese_5G.html")

print("✅ Tableau ouvert dans le navigateur (synthese_5G.html)")