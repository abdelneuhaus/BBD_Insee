import psycopg2
import csv
import xlrd

try:
    connection = psycopg2.connect(user = "jojo", password = "abdelnbajao647", host = "127.0.0.1", port = 5432, database = "insee_db")
    cursor = connection.cursor()

    # permet d'executer une operation ou requete sur la database
    cursor.execute("""CREATE TABLE Regions(reg varchar(4) PRIMARY KEY, cheflieu varchar(40), tncc varchar(10), ncc varchar(40), nccenr varchar(40), libelle varchar(40))""")
    with open('./fichiersFournis/region2020.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute("INSERT INTO Regions VALUES (%s, %s, %s, %s, %s, %s)",row)

    cursor.execute("""CREATE TABLE Departements(dep varchar(5) PRIMARY KEY, reg varchar(4), cheflieu varchar(40), tncc varchar(10), ncc varchar(40), nccenr varchar(40), libelle varchar(40))""")
    with open('./fichiersFournis/departement2020.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)   
        for row in reader:
            cursor.execute("INSERT INTO Departements VALUES (%s, %s, %s, %s, %s, %s, %s)",row)


    cursor.execute("""CREATE TABLE RegionsInfos(cheflieu varchar(40) PRIMARY KEY, reg varchar(30), pauvrete float, jeunesNonInseres2014 float, jeunesNonInseres2009 float, poidsEcoSoc float)""")
    data = xlrd.open_workbook("./fichiersFournis/DD-indic-reg-dep_janv2018.xls")
    reader = data.sheet_by_name("Social")
    query = """INSERT INTO RegionsInfos VALUES (%s, %s, %s, %s, %s, %s)"""
    for r in range(3,reader.nrows - 113):
        cheflieu = reader.cell(r,0).value
        reg = reader.cell(r,1).value
        pauvrete = reader.cell(r,2).value
        jeunesNonInseres2014 = reader.cell(r,3).value
        jeunesNonInseres2009 = reader.cell(r,4).value
        poidsEcoSoc = reader.cell(r,5).value

        values = (cheflieu, reg, pauvrete, jeunesNonInseres2014, jeunesNonInseres2009, poidsEcoSoc)
        cursor.execute(query, values)


    cursor.execute("""CREATE TABLE DepartementsInfos(cheflieu varchar(40) PRIMARY KEY, dep varchar(30), espH2015 float, espH2010 float, espF2015 float, espF2010 float, disSanteSup7 float, inondable2013 varchar(20), inondable2008 float)""")
    data = xlrd.open_workbook("./fichiersFournis/DD-indic-reg-dep_janv2018.xls")
    reader = data.sheet_by_name("Social")
    query = """INSERT INTO DepartementsInfos VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for r in range(28,reader.nrows - 5):
        cheflieu = reader.cell(r,0).value
        dep = reader.cell(r,1).value
        espH2015 = reader.cell(r,2).value
        espH2010 = reader.cell(r,3).value
        espF2015 = reader.cell(r,4).value
        espF2010 = reader.cell(r,5).value
        disSanteSup7 = reader.cell(r,6).value
        inondable2013 = reader.cell(r,7).value
        inondable2008 = reader.cell(r,8).value

        values = (cheflieu, dep, espH2015, espH2010, espF2015, espF2010, disSanteSup7, inondable2013, inondable2008)
        cursor.execute(query, values)


    cursor.execute("""CREATE TABLE Environnement(cheflieu varchar(40) PRIMARY KEY, dep varchar(30), valOrga2013 int, valOrga2009 int, surfArti2012 float, surfArti2006 float, agriBio2016 float, 
                    agriBio2010 float, granulats2014 int, granulats2009 int, eolienne2015 float, eolienne2010 float, photovoltaique2015 float, photovoltaique2010 float,
                    autreEnergie2015 float, autreEnergie2010 float)""")
    data = xlrd.open_workbook("./fichiersFournis/DD-indic-reg-dep_janv2018.xls")
    reader = data.sheet_by_name("Environnement")
    query = """INSERT INTO Environnement VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for r in range(3,reader.nrows - 7):
        cheflieu = reader.cell(r,0).value
        dep = reader.cell(r,1).value
        valOrga2013 = reader.cell(r,2).value
        valOrga2009 = reader.cell(r,3).value
        surfArti2012 = reader.cell(r,4).value
        surfArti2006 = reader.cell(r,5).value
        agriBio2016 = reader.cell(r,6).value
        agriBio2010 = reader.cell(r,7).value
        granulats2014 = reader.cell(r,8).value
        granulats2009 = reader.cell(r,9).value
        eolienne2015 = reader.cell(r,10).value
        eolienne2010 = reader.cell(r,11).value
        photovoltaique2015 = reader.cell(r,12).value
        photovoltaique2010 = reader.cell(r,13).value
        autreEnergie2015 = reader.cell(r,14).value
        autreEnergie2010 = reader.cell(r,15).value

        values = (cheflieu, dep, valOrga2013, valOrga2009, surfArti2012, surfArti2006, agriBio2016, agriBio2010, granulats2014, granulats2009, eolienne2015, eolienne2010, photovoltaique2015, photovoltaique2010, autreEnergie2015, autreEnergie2010)
        cursor.execute(query, values)


    connection.commit()


except(Exception, psycopg2.Error) as error:     # gestion des erreurs
    print("Erreur lors de la connexion à PostgreSQL :", error)

finally:
    if(connection):
        # fermeture pour eviter d'eventuels problemes
        cursor.close()
        connection.close()
        print("Terminé sans problèmes rencontrés.\nLa connexion PostgreSQL est fermée")