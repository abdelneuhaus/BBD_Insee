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
        print("9: Affichage de la part de l'agriculture bio du département dont le pourcentage de personnes à plus de 7 minutes des services de santé est le plus grand")
        print("10: Affichage du taux de pauvreté en 2014 dans les régions où la part de jeunes non insérés est supérieure à 30%")
        print("11: Affichage du poids de l'économie sociale dans les emplois salariés des régions dont l’énergie photovoltaïque est supérieure à 10% et dont la part de l’agriculture biologique était d’au moins 5%")
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
        nom = cursor.execute("SELECT nccenr, cheflieu, tncc FROM Regions;")
        choixRegion = input("Choisissez une région : ")
        for x in cursor.fetchall():
            if(choixRegion == x[0]):
                print("")
                print("Nom :", x[0])
                print("Chef-lieu :", x[1])
                print("Type de nom en clair (TNCC) :", x[2])
                print("")


    ### QUESTION 4 ###
    def infosDepartements():
        nom = cursor.execute("SELECT nccenr FROM Departements;")
        choixDepartement = input("Choisissez un département : ")
        print("")
        print("Choisissiez un thème :")
        print("1: Social")
        print("2: Environnement")
        saisie = gestionErreurSaisie(input(">> "))
        if saisie not in gestion_erreur:
            print("Mauvaise saisie. Recommencer.\n>> ") 
            choix = gestionErreurSaisie(input("Choix : ")) 
        while (saisie != 1 and saisie != 2):
            saisie = int(input("Mauvaise saisie. Recommencer.\n>> "))
        print("")
        if(saisie == 1):
            for x in cursor.fetchall():
                if(choixDepartement == x[0]):
                    print("")
                    print("Nom :", choixDepartement)
                    cursor.execute("""SELECT cheflieu, espH2015, espH2010, espF2015, espF2010, disSanteSup7, inondable2013, inondable2008 
                    FROM DepartementsInfos WHERE dep = '%s'; """ % choixDepartement)
                    for x in cursor.fetchall():
                        print("Chef-lieu :", int(x[0]))
                        print("Espérence de vie des hommes en 2015 :", x[1], "ans")
                        print("Espérance de vie des hommes en 2010 :", x[2], "ans")
                        print("Espérance de vie des femmes en 2015 :", x[3], "ans")
                        print("Espérance de vie des femmes en 2010 :", x[4], "ans")
                        print("Pourcentage de personnes dont la durée pour aller aux services de santé est supérieure à 7 minutes :", x[5], "%")
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
                        print("Chef-lieu :", int(x[0]))
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
        choix = gestionErreurSaisie(input(">> "))
        if choix not in gestion_erreur:
            print("Mauvaise saisie. Recommencer.\n>> ") 
            choix = gestionErreurSaisie(input("Choix : ")) 
        while (choix != 1 and choix != 2 and choix != 3):
            choix = int(input("Mauvaise saisie. Recommencer.\n>>  "))
        print("")
        if(choix == 1):
            cursor.execute("SELECT dep, photovoltaique2010, photovoltaique2015 FROM environnement WHERE photovoltaique2010 < photovoltaique2015 ORDER BY photovoltaique2015 - photovoltaique2010 DESC;")
            print("Régions dont la part d'utilisation du photovoltaïque a augmenté (ordre décroissant) :")            
            print("")
            for x in cursor.fetchall():
                print(x[0], "- Pourcentage d'augmentation :", round(x[2] - x[1], 3), "%")
        elif(choix == 2):
            cursor.execute("SELECT dep, eolienne2010, eolienne2015 FROM environnement WHERE eolienne2015 > eolienne2010 ORDER BY eolienne2015 - eolienne2010 DESC;")
            print("Régions dont la part d'utilisation de l'éolien a augmenté (ordre décroissant) :")
            print("")
            for x in cursor.fetchall():
                print(x[0], "- Part d'augmentation :", round(x[2] - x[1], 3), "%")
        elif(choix == 3):
            cursor.execute("SELECT dep, autreenergie2010, autreenergie2015 FROM environnement WHERE autreenergie2015 > autreenergie2010 ORDER BY autreenergie2015 - autreenergie2010 DESC;")
            print("Régions dont la part d'utilisation d'autres énergies a augmenté (ordre décroissant) :")
            print("")
            for x in cursor.fetchall():
                print(x[0], "- Pourcentage d'augmentation :",round(x[2] - x[1], 3), "%")


    ### QUESTION 6 ###
    def granulatSupe25M():
        cursor.execute("SELECT D1.nccenr FROM departements D1 WHERE D1.reg IN (SELECT R1.reg FROM departements D1 JOIN environnement E1 ON D1.nccenr = E1.dep JOIN regions R1 ON R1.reg = D1.reg GROUP BY R1.reg HAVING SUM(granulats2014) > 25000000);")
        print("Liste des départements dont la région a eu une production de granulats supérieure à 25 000 000 tonnes en 2014 :")
        for x in cursor.fetchall():
            print(x[0])
        

    ### QUESTION 7 ###
    def top5eolien():
        cursor.execute("SELECT dep FROM environnement WHERE eolienne2015 != 'nan' ORDER BY eolienne2015 DESC LIMIT 5;")
        print("Liste des 5 départements avec le plus grand taux d’énergie éolienne comme source de la puissance électrique en 2015 :")
        for x in cursor.fetchall():
            print(x[0])


    ### QUESTION 8 ###
    def faibleVMO13():
        cursor.execute("SELECT dep FROM environnement WHERE valorga2013 != 'nan' ORDER BY valorga2013 ASC LIMIT 1;")
        for x in cursor.fetchall():
            print("Département ayant le plus faible taux de valorisation matière et organique en 2013 :", x[0])


    ### QUESTION 9 ###
    def agriBioSanteSup7():    
        cursor.execute("SELECT E1.dep, agribio2016, disSanteSup7 FROM environnement E1 JOIN departementsinfos D1 ON E1.dep = D1.dep  WHERE agribio2016 != 'nan' and disSanteSup7 != 'nan' ORDER BY disSanteSup7 DESC LIMIT 1;")
        for x in cursor.fetchall():
            print("Département : ", x[0])
            print("Population à plus de 7 minutes des services de sante :", x[2], "%")
            print("Part de l'agriculture bio :", x[1], " %")


    ### QUESTION 10 ###
    def pauvreteJeunesNI13():    
        cursor.execute("SELECT nccenr, pauvrete FROM regionsinfos WHERE pauvrete != 'nan' and jeunesnoninseres2014 > 30;")
        print("Taux de pauvreté en 2014 des régions dont la part des jeunes non insérés est supérieure à 30% en 2014 :")
        for x in cursor.fetchall():
            print(x[0], " - Taux de pauvreté : %.2f" % x[1],"%")


    ### QUESTION 11 ###
    def lastQuestion():    
        cursor.execute("SELECT R1.nccenr, R2.poidsecosoc FROM environnement E1 JOIN departements D1 ON D1.nccenr = E1.dep JOIN regions R1 ON R1.reg = D1.reg JOIN regionsinfos R2 ON R1.nccenr = R2.nccenr GROUP BY R1.nccenr, R2.poidsecosoc  HAVING (SUM(E1.photovoltaique2015)/COUNT(R2.nccenr)) > 10 AND (SUM(E1.agribio2016)/COUNT(R2.nccenr)) > 5 ORDER BY R2.poidsecosoc DESC LIMIT 1;")
        print("Poids de l'économie sociale dans les emplois salariés de la région dont la source de la puissance électrique en énergies renouvelables provenait à au moins 10% de l’énergie photovoltaïque et dont la part de l’agriculture biologique dans la surface agricole totale était d’au moins 5% : \n")
        for x in cursor.fetchall():
            print(x[0], " -  Poids économique et social en 2015 : %.2f" % x[1],"%")
    
    

    gestion_erreur = range(0,12)

    def gestionErreurSaisie(saisie):
        try:
            valeur=int(saisie)
            return valeur
        except ValueError:
            return 0


    while(True):
        menu()
        choix = gestionErreurSaisie(input("Choix : "))
        while(choix not in gestion_erreur):
            print("Il faut saisir un nombre")
            choix = gestionErreurSaisie(input("Choix : ")) 
        print("")
        while(type(choix) != int or choix < 0 or choix > 11):
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
            agriBioSanteSup7()
        elif(choix == 10):
            pauvreteJeunesNI13()
        elif(choix == 11):
            lastQuestion()


    connection.commit()

except(Exception, psycopg2.Error) as error:     # gestion des erreurs
    print("Erreur lors de la connexion à PostgreSQL :", error)

finally:
    if(connection):
        # fermeture pour eviter d'eventuels problemes
        cursor.close()
        connection.close()
