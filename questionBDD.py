import psycopg2
import sys

try:
    connection = psycopg2.connect(user = "jojo", password = "abdelnbajao647", host = "127.0.0.1", port = 5432, database = "insee_db")
    cursor = connection.cursor()

    ### Menu ###
    def menu():
        print("")
        print("Menu")
        print("")
        print("0: Quitter")
        print("1: Afficher les régions")
        print("2: Afficher les départements")
        print("3: Afficher les informations concernants une région")
        print("4: Afficher les informations sociales ou environnementales d'un département")
        print("5: Afficher les départements où un type d'énergie est plus utilisé qu'avant")
        print("6: Affichage des départements dont la région a eu une production de granulats supérieure à 25 millions de tonnes en 2014")
        print("7: Affichage des 5 départements utilisant l'éolienne comme source majeur d'électricité")
        print("8: Affichage de la région dont le département a plus faible taux de valorisation matière/organique en 2013")
        print("9: ")
        print("10: Affichage du taux de pauvreté en 2014 dans les régions où la part de jeunes non insérés est supérieure à 30%")
        print("11")
        print("")


    ### QUESTION 1 ###
    def afficheRegions():
        cursor.execute("SELECT nccenr FROM Regions;")
        print("Liste de toutes les régions :")
        for x in cursor.fetchall():
            print(x[0])


    ### QUESTION 2 ###
    def afficheDepartements():
        cursor.execute("SELECT nccenr FROM Departements;")
        print("Liste de tous les départements :")
        for x in cursor.fetchall():
            print(x[0])        


    ### QUESTION 3 ###
    def infosRegions():
        nom = cursor.execute("SELECT nccenr FROM Regions;")
        choixRegion = input("Choisissez une région : ")
        for x in cursor.fetchall():
            if(choixRegion == x[0]):
                print("")
                print("Nom :", x[0])
                cheflieu = cursor.execute("""SELECT cheflieu FROM Regions WHERE nccenr = '%s'; """ % choixRegion)
                for x in cursor.fetchall():
                    print("Chef-lieu :", x[0])
                reg = cursor.execute("""SELECT tncc FROM Regions WHERE nccenr = '%s'; """ % choixRegion)
                for x in cursor.fetchall():
                    print("Type de nom en clair (TNCC) :", x[0])
                    print("")


    ### QUESTION 4 ###
    def infosDepartements():
        nom = cursor.execute("SELECT nccenr FROM Departements;")
        choixDepartement = input("Choisissez un département : ")
        print("")
        print("Choisissiez un thème :")
        print("1: Social")
        print("2: Environnement")
        saisie = int(input(">> "))
        while (saisie != 1 and saisie != 2):
            saisie = int(input("Mauvaise saisie. Recommencer.\n>> "))
        print("")
        if(saisie == 1):
            for x in cursor.fetchall():
                if(choixDepartement == x[0]):
                    print("")
                    print("Nom :", choixDepartement)
                    cursor.execute("""SELECT cheflieu, espH2015, espH2010, espF2015, espF2010, distravailsup7, inondable2013, inondable2008 
                    FROM DepartementsInfos WHERE dep = '%s'; """ % choixDepartement)
                    for x in cursor.fetchall():
                        print("Chef-lieu :", x[0])
                        print("Espérence de vie des hommes en 2015 :", x[1], "ans")
                        print("Espérance de vie des hommes en 2010 :", x[2], "ans")
                        print("Espérance de vie des femmes en 2015 :", x[3], "ans")
                        print("Espérance de vie des femmes en 2010 :", x[4], "ans")
                        print("Pourcentage de personnes dont la durée pour aller au travail est supérieure à 7 minutes :", x[5], "%")
                        print("Population en zones inondables en 2013 :", x[6], "%")
                        print("Population en zones inondables en 2008 :", x[7], "%")
                        print("")
        elif(saisie == 2):
            for x in cursor.fetchall():
                if(choixDepartement == x[0]):
                    print("")
                    print("Nom :", choixDepartement)
                    cursor.execute("""SELECT cheflieu, valorga2013, valorga2009, surfarti2012, surfarti2006, agribio2016, agribio2010, granulats2014,
                    granulats2009, eolienne2015, eolienne2010, photovoltaique2015, photovoltaique2010, autreenergie2015, autreenergie2010 
                    FROM Environnement WHERE dep = '%s'; """ % choixDepartement)
                    for x in cursor.fetchall():
                        print("Chef-lieu :", x[0])
                        print("Taux de valorisation matière et organique en 2013:", x[1], "%")
                        print("Taux de valorisation matière et organique en 2009:", x[2], "%")
                        print("Surface artificelle en 2012 :", x[3], "%")
                        print("Surface artificielle en 2006 :", x[4], "ans")
                        print("Part de l'agriculture bio en 2016 :", x[5], "%")
                        print("Part de l'agriculture bio en 2010 :", x[6], "%")
                        print("Production de granulats (tonnes) en 2014 :", x[7])
                        print("Production de granulats en 2009 :", x[8])
                        print("Eolien en 2015 :", x[9], "%")
                        print("Eolien en 2010:", x[10], "%")
                        print("Photovoltaique en 2015:", x[11], "%")
                        print("Photovoltaique en 2010:", x[12], "%")
                        print("Autres énergies utilisées en 2015 :", x[13], "%")
                        print("Autres énergies utilisées en 2010 :", x[14], "%")
                        print("")


    ### QUESTION 5 ###
    def infosEnergie():
        print("Choix du type d'énergie :")
        print("1: Voltaïque\n2: Eolien\n3: Autres")
        choix = int(input(">> "))
        print("")
        while (choix != 1 and choix != 2 and choix != 3):
            choix = int(input("Erreur de saisie. Recommencer.\n>> "))
        if(choix == 1):
            cursor.execute("SELECT dep FROM environnement ORDER BY photovoltaique2015/photovoltaique2010 DESC;")
            print("Régions dont la part d'utilisation du photovoltaïque a augmenté (ordre décroissant) :")            
            print("")
            for x in cursor.fetchall():
                print(x[0])
        elif(choix == 2):
            cursor.execute("SELECT dep FROM environnement ORDER BY eolienne2015 / NULLIF(eolienne2010, 0) DESC;")
            print("Régions dont la part d'utilisation de l'éolien a augmenté (ordre décroissant) :")
            print("")
            for x in cursor.fetchall():
                print(x[0])
        elif(choix == 3):
            cursor.execute("SELECT dep FROM environnement ORDER BY autreenergie2015/NULLIF(autreenergie2010, 0) DESC;")
            print("Régions dont la part d'utilisation d'autres énergies a augmenté (ordre décroissant) :")
            print("")
            for x in cursor.fetchall():
                print(x[0])


    ### QUESTION 6 ###
    def granulatSupe25M():
        # Fusion du tableau
        # select departements.nccenr from departements inner join environnement on environnement.dep = departements.nccenr;
        # select cheflieu, SUM(granulats2014)>25000000 from environnement group by environnement.cheflieu;
        return


    ### QUESTION 7 ###
    def top5eolien():
        cursor.execute("SELECT dep FROM environnement ORDER BY eolienne2015 DESC LIMIT 5;")
        print("Liste des 5 départements avec le plus grand taux d’énergie éolienne comme source de la puissance électrique en 2015 :")
        for x in cursor.fetchall():
            print(x[0])


    ### QUESTION 8 ###
    def faibleVMO13():
        cursor.execute("SELECT dep FROM environnement WHERE valorga2013 != -1 ORDER BY valorga2013 ASC LIMIT 1;")
        for x in cursor.fetchall():
            print("Département ayant le plus faible taux de valorisation matière et organique en 2013 :", x[0])


    ### QUESTION 9 ###



    ### QUESTION 10 ###
    def pauvreteJeunesNI13():    
        cursor.execute("SELECT reg, pauvrete FROM regionsinfos WHERE jeunesnoninseres2014 > 30 AND pauvrete != - 1;")
        print("Taux de pauvreté en 2014 des régions dont la part des jeunes non insérés est supérieure à 30% en 2014 :")
        for x in cursor.fetchall():
            print(x[0], " - Taux de pauvreté : %.2f" % x[1],"%")


    ### QUESTION 11 ###
    



    while(True):
        menu()
        choix = int(input("Saisir un choix : "))
        print("")
        while(choix < 0 or choix > 12):
            choix = int(input("Ce choix n'existe pas. Recommencer.\nChoix : "))
        if(choix == 0):
            sys.exit(0)
        elif(choix == 1):
            afficheRegions()
        elif(choix == 2):
            afficheDepartements()
        elif(choix == 3):
            infosRegions()
        elif(choix == 4):
            infosDepartements()
        elif(choix == 5):
            infosEnergie()
        elif(choix == 6):
            granulatSupe25M()
        elif(choix == 7):
            top5eolien()
        elif(choix == 8):
            faibleVMO13()
        elif(choix == 9):
            pass
        elif(choix == 10):
            pauvreteJeunesNI13()
        elif(choix == 11):
            pass


    connection.commit()

except(Exception, psycopg2.Error) as error:     # gestion des erreurs
    print("Erreur lors de la connexion à PostgreSQL :", error)

finally:
    if(connection):
        # fermeture pour eviter d'eventuels problemes
        cursor.close()
        connection.close()