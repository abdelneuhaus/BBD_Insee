# le module pour les fichiers csv
import csv

# ouvrir le fichier en lecture
file=open("departement2020.csv","r")

# initialisation d’un lecteur de fichier
reader = csv.reader(file, delimiter = ",") 

# parcours des lignes du fichier avec une boucle
for row in reader:
        print(row)
        
# fermeture du fichier
file.close()
