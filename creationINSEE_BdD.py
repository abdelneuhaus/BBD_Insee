import psycopg2
import pandas as pd
import numpy as np
import csv

try:
    # Ouverture de la connexion avec une base de données créée manuellement
    connection = psycopg2.connect(user = "username", password = "password", host = "127.0.0.1", port = 5432, database = "databaseName")
    cursor = connection.cursor()

    # permet d'executer une operation ou requete sur la database
    # On crée la table région (fichier csv)
    cursor.execute("""CREATE TABLE Regions(reg varchar(2) PRIMARY KEY, 
    cheflieu varchar(10) not null, 
    tncc varchar(10) not null, 
    ncc varchar(40) not null, 
    nccenr varchar(40) not null, 
    libelle varchar(40) not null)""")
    with open('region2020.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute("INSERT INTO Regions VALUES (%s, %s, %s, %s, %s, %s)",row)


    # On crée la table départements (fichier csv)
    cursor.execute("""CREATE TABLE Departements(
    dep varchar(4) PRIMARY KEY, reg varchar(2) not null, cheflieu varchar(10) not null, tncc varchar(10) not null, ncc varchar(40) not null, nccenr varchar(40) not null, libelle varchar(40) not null)""")
    with open('departement2020.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)   
        for row in reader:
            cursor.execute("INSERT INTO Departements VALUES (%s, %s, %s, %s, %s, %s, %s)",row)


    # On crée la table des infos sur les régions (fichier excel)
    cursor.execute("""CREATE TABLE RegionsInfos(
    cheflieu varchar(10) PRIMARY KEY, nccenr varchar(40), pauvrete float, jeunesNonInseres2014 float, jeunesNonInseres2009 float, poidsEcoSoc float)""")
    fileOpen = pd.ExcelFile('DD-indic-reg-dep_janv2018.xls')
    dataFrame1 = pd.read_excel(fileOpen, sheet_name= "Social", usecols= "A:F", skiprows= 3, nrows= 21, header= None)
    dataFrame1.replace(["nd", "nd ", "nc", "nc "], np.NaN, inplace = True)
    for i in range (len(dataFrame1)):
        values = dataFrame1.iloc[i]
        cursor.execute("INSERT INTO RegionsInfos values (%s, %s, %s, %s, %s, %s)", values) 


    # On crée la table des infos sur les départements (fichier excel)
    cursor.execute("""CREATE TABLE DepartementsInfos(
    cheflieu varchar(10) PRIMARY KEY, 
    dep varchar(30), 
    espH2015 float, 
    espH2010 float, 
    espF2015 float, 
    espF2010 float, 
    disSanteSup7 float, 
    inondable2013 float, 
    inondable2008 float)""")
    fileOpen = pd.ExcelFile('DD-indic-reg-dep_janv2018.xls')
    dataFrame2 = pd.read_excel(fileOpen, sheet_name= "Social", usecols= "A:I", skiprows= 28, nrows= 104 , header= None)
    dataFrame2.replace(["nd", "nd ", "nc", "nc "], np.NaN, inplace = True)
    for i in range (len(dataFrame2)):
        values = dataFrame2.iloc[i]
        cursor.execute("INSERT INTO DepartementsInfos values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", values)


    # On crée la table des infos environnementales (fichier excel)
    cursor.execute("""CREATE TABLE Environnement(cheflieu varchar(40) PRIMARY KEY, dep varchar(30), valOrga2013 float, valOrga2009 float, 
    surfArti2012 float, surfArti2006 float, agriBio2016 float, agriBio2010 float, granulats2014 float, granulats2009 float, eolienne2015 float, 
    eolienne2010 float, photovoltaique2015 float, photovoltaique2010 float,autreEnergie2015 float, autreEnergie2010 float)""")
    fileOpen = pd.ExcelFile('DD-indic-reg-dep_janv2018.xls')
    dataFrame3 = pd.read_excel(fileOpen, sheet_name= "Environnement", usecols= "A:P", skiprows= 3, nrows= 104 , header= None)
    dataFrame3.replace(["nd", "nd ", "nc", "nc "], np.NaN, inplace = True)
    for i in range (len(dataFrame3)):
        values = dataFrame3.iloc[i]
        cursor.execute("INSERT INTO Environnement values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)

    connection.commit()

# Affichage des erreurs lors de l'utiisation de la base de données
except(Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL :", error)

finally:
    if(connection):
        # fermeture pour eviter d'eventuels problemes
        cursor.close()
        connection.close()
        print("Terminé sans problèmes rencontrés.\nLa connexion PostgreSQL est fermée")