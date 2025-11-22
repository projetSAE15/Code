import os  #importe le module pour interagir avec le système d'exploitation
import sys  #importe le module qui donne accès à des informations sur l'environnement python
!{sys.executable} -m pip install --user folium  #installe la bibliothèque folium pour les cartes interactives
!{sys.executable} -m pip install --user pandasgui  #installe pandasgui pour explorer les données facilement
import pandas as pd  #importe la bibliothèque pandas pour manipuler les données
import folium  #importe folium pour créer des cartes
import webbrowser  #importe webbrowser pour ouvrir des fichiers html dans le navigateur

#1.lecture du fichier csv
chemin_fichier = "C:/experimentations_5G.csv"  #définit le chemin du fichier csv
donnees = pd.read_csv(chemin_fichier, sep=';', encoding='cp1252')  #lit le fichier csv avec le bon séparateur et encodage

#2.nettoyage des données
donnees["Latitude"] = donnees["Latitude"].str.replace(",", ".").astype(float)  #remplace les virgules par des points et convertit en nombre pour latitude
donnees["Longitude"] = donnees["Longitude"].str.replace(",", ".").astype(float)  #remplace les virgules par des points et convertit en nombre pour longitude

#3.création d'une synthèse par région
synthese_region = (  #créer un tableau récapitulatif regroupé par région
    donnees.groupby("Région")
    .agg({
        "Expérimentateur": lambda x: ", ".join(sorted(set(x))),  #regroupe les expérimentateurs uniques
        "Bande de fréquences": lambda x: ", ".join(sorted(set(x))),  #regroupe les bandes de fréquences uniques
        "Latitude": "count"  #compte le nombre d'expérimentations
    })
    .rename(columns={  #renomme les colonnes pour plus de clarté
        "Latitude": "Nombre d'expérimentations",
        "Expérimentateur": "Acteurs",
        "Bande de fréquences": "Bandes"
    })
    .reset_index()  #remet la colonne région comme colonne normale
)

#4.génération d’un tableau html lisible
tableau_html = synthese_region.to_html(index=False, justify='left', border=1)  #convertit la synthèse en table html

#5.ajout d’un titre et du style à la page
page_html = f"""  
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
    {tableau_html}
    <br><br>
    <a href="carte_5G.html">Voir la carte interactive</a>
</body>
</html>
"""  
#crée une page html avec titre, tableau et lien vers la carte

#6.sauvegarde du tableau html
with open("synthese_5G.html", "w", encoding="utf-8") as fichier_html:  #ouvre un fichier html en écriture
    fichier_html.write(page_html)  #écrit le contenu html dans le fichier

#7.création de la carte interactive
carte = folium.Map(location=[46.6, 2.5], zoom_start=5)  #crée une carte centrée sur la france
for _, ligne in donnees.iterrows():  #parcourt chaque ligne du tableau
    info_popup = (  #crée le contenu de la bulle d'information
        f"<b>{ligne['Région']}</b><br>"
        f"Acteur : {ligne['Expérimentateur']}<br>"
        f"Bande : {ligne['Bande de fréquences']}"
    )
    folium.Marker(  #ajoute un marqueur sur la carte
        location=[ligne["Latitude"], ligne["Longitude"]],
        popup=info_popup,
        tooltip=ligne["Région"]
    ).add_to(carte)  #ajoute le marqueur à la carte

carte.save("carte_5G.html")  #sauvegarde la carte en fichier html

#8.ouverture automatique du tableau dans le navigateur
webbrowser.open("synthese_5G.html")  #ouvre le fichier html de la synthèse dans le navigateur

print("tableau ouvert dans le navigateur (synthese_5G.html)")  #affiche un message de confirmation

