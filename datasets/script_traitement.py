"""
Nous utilisons ici le jeu de de donnees issu du Github de ARUNARN dans le repertoire “datasets/cmu”, dont le lien est 
https://github.com/arunarn2/GeoLocationTagging

Comme il contient trois fichiers, .train, .dev et .test, nous les fusionnons d'abord en un afin de mieux exploiter 
de geolocalisation, le fichier resultant est data_colmplete.csv

Pour petit rappel, l'idee ici est de lier ces coordonnees geographiques par des expressions de geolocalisation relatives
C'est a dire pouvoir ressortir les dependances du genre, loc1 est au nord-est de loc2, loc1 est au sud-ouest de loc5, etc...
ainsi de suite ceci pour toutes les paires possibles entre ces localissations

Ensuite il sera question de faire pareil en tenant compte de trois localites,
C'est a dire pouvoir ressortir les dependances du genre, loc1 est au devant a droite du chemin entre loc2 et loc5,
loc4 est au devant a gauche du chemin entre loc1 et loc5, loc3 est au derriere a droite du chemin entre loc2 et loc15 etc...

Apres execution de ce code, deux fichiers csv sont generes deux_deux.csv et trois_trois.csv contenant respectivement les expressions de
localisations relatives, en tenant compte de deux deux localites et les expressions de localite relatives en tenant compte de trois trois 
localites
"""

# IMPORTATIONS DES DIFFERENTES LIBRAIRIES.

import csv
from geopy.point import Point
import time

debut = time.time()

# CAS DE 2-2 LOCALITES.

# Creation du fichier csv resultant
i=0
with open('deux_deux.csv', 'w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv)

    # Ouverture du csv de toutes donnees pour extraction des coordonnees gps
    colonnes_a_extraire = [1,2] # ce sont les colonnes cntenant les coordonnees gps
    gps_infos = [] #liste contenant toutes ces coordonnees gps

    with open('data_complete.csv', 'r') as file:
        lecteur_csv = file.readlines() 

        # Lire chaque ligne du fichier CSV e
        for ligne in lecteur_csv:
            ligne = ligne.strip().split(',')
            colonnes_extraction = [ligne[indice] for indice in colonnes_a_extraire]
            gps_infos.append(colonnes_extraction)

    
    for loc1 in range(len(gps_infos)):
        
        localisation1 = Point(gps_infos[loc1][0], gps_infos[loc1][1])

        for loc2 in range(len(gps_infos)):
            localisation2 = Point(gps_infos[loc2][0], gps_infos[loc2][1])

            # Comparaison des latitudes et longitudes pour déterminer si localisation 1 est au nord ou au sud etc ... de localisation 2
            if localisation1.latitude > localisation2.latitude:
                if localisation1.longitude > localisation2.longitude:
                    exp = "Nord-Est"
                elif localisation1.longitude == localisation2.longitude:
                    exp = "Nord"
                else:
                    exp = "Nord-Ouest"
            elif localisation1.latitude == localisation2.latitude:
                if localisation1.longitude > localisation2.longitude:
                    exp = "Est"
                elif localisation1.longitude == localisation2.longitude:
                    exp = "Confondu"
                else:
                    exp = "Ouest"
            else:
                if localisation1.longitude > localisation2.longitude:
                    exp = "Sud-Est"
                elif localisation1.longitude == localisation2.longitude:
                    exp = "Sud"
                else:
                    exp = "Sud-Ouest"
            
            writer.writerow([loc1+1, loc2+1, exp])

        i = i + 1
        print("deja a la localite", i)
        if i == 10: break
        
        
# CAS DE 3-3 LOCALITES.

# Generons d'abord toutes les combinaisons possibles de localites deux a deux.
combinaisons = []
for i in range(len(gps_infos)):
    for j in range(i + 1, len(gps_infos)):
        combinaisons.append([i,j])

# Creation du fichier csv resultant
k = 0
with open('trois_trois.csv', 'w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv)

    # pour chacune de ces combinaisons la, considerer chaque localite et associer l'expression de localisation relative
    for occ in combinaisons:
        localisation1 = Point(gps_infos[occ[0]][0], gps_infos[occ[0]][1])
        localisation2 = Point(gps_infos[occ[1]][0], gps_infos[occ[1]][1])
        
        for i in range(len(gps_infos)):

            localisation3 = Point(gps_infos[i][0], gps_infos[i][1])
            if localisation3 != localisation1 and localisation3 != localisation2 :
                
                # calcul de l'expression de localisation relative
                if localisation3.latitude > localisation1.latitude:
                    if localisation3.latitude > localisation2.latitude:
                        if localisation3.longitude > localisation2.longitude:
                            exp = "Devant à droite"
                        elif localisation3.longitude == localisation2.longitude:
                            exp = "Devant"
                        else:
                            exp = "Devant à gauche"
                    elif localisation3.latitude <= localisation2.latitude and localisation3.latitude >= localisation1.latitude:
                        if localisation3.longitude > localisation2.longitude:
                            exp = "Droite"
                        else:
                            exp = "Gauche"
                else:
                    if localisation3.longitude > localisation2.longitude:
                        exp = "Derriere à droite"
                    elif localisation3.longitude == localisation2.longitude:
                        exp = "Derriere"
                    else:
                        exp = "Derriere à gauche"
                
                writer.writerow([occ[0]+1,occ[1]+1,i+1,exp])
        k = k + 1
        print("deja a", k, "/", len(combinaisons))   
        if k == 5: break 


fin = time.time()        

# Calcul de la durée d'exécution
duree = fin - debut

# Affichage du temps d'exécution
print("Temps d'exécution:", duree, "secondes")




