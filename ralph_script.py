import os 
import pyodbc 
import sys 
import pandas 

# pripojeni k databazi
server = 'server' 
database = 'database' 
username = 'username' 
password = 'password' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

path = sys.argv[1] #  cesta do slozky s daty   

folders = os.listdir(path) # ulozi do seznamu nazvy slozek = datasetu
 
for folder in folders: # postupne prochazi vsechny datasety

    # plneni tabulky Dataset
    query = f"INSERT INTO Dataset (NazevSlozky) OUTPUT INSERTED.DatasetID VALUES ('{folder}')"
    print(query)
    cursor.execute(query) # do sloupce NazevSlozky v tabulce Dataset vlozi nazev slozky = datasetu
    DatasetID = cursor.fetchone() # predchozi prikaz dava na vystup DatasetID a my ho prirazujeme do promenne
    print(DatasetID)

    # plneni tabulky AlgorithmConfig
    file = f"{path}\\{folder}\\algorithmConfig" # cesta k souboru algorithmConfig 
    f = open(file, "r") # otevreme soubor pro cteni a ulozime do promenne f
    line = f.readline() # nacteme prvni radek ze souboru

    cnt = 1 # nastavime pocitadlo
    dictionary = {} # vytvorime prazdny slovnik

    while line: # postupne prochazime radky souboru
        line = line.rstrip() # nejprve odstranime prazdne znaky na konci nacteneho radku
        if cnt > 1 and cnt not in (28, 29, 30): # tady mame podminku, protoze chceme nektere radky preskocit
            items = line.split(",") # rozdelime radek, znak pro rozdeleni je carka
            dictionary[items[0]] = items[1] # vytvarime zaznam ve slovniku, klic je retezec pred carkou, hodnota je retezec za carkou
        line = f.readline() # nacteme dalsi radek
        cnt = cnt + 1 # navysime pocitadlo
    
    # nektere hodnoty je nutne upravit
    position1 = dictionary["treeUpdateConditionFactory"].find("=") + 1 # vyhledame pozici rovnitka a pricteme 1
    position2 = dictionary["treeUpdateConditionFactory"].find("}") # vyhledame pozici slozene zavorky
    dictionary["treeUpdateConditionFactory"] = dictionary["treeUpdateConditionFactory"][position1:position2] # hodnotu ve slovniku nahradime novou hodnotou - retezcem mezi rovnitkem a zavorkou
    pozice1 = dictionary["explorationConstantSupplier"].find(">") + 2 # vyhledame pozici > a pricteme 2
    dictionary["explorationConstantSupplier"] = dictionary["explorationConstantSupplier"][pozice1:] # hodnotu ve slovniku nahradime novou hodnotou - retezcem za >
    pozice1 = dictionary["temperatureSupplier"].find(">") + 2 # vyhledame pozici > a pricteme 2
    dictionary["temperatureSupplier"] = dictionary["temperatureSupplier"][pozice1:] # hodnotu ve slovniku nahradime novou hodnotou - retezcem za >

    begin = "INSERT INTO AlgorithmConfig(DatasetID," # predchysteme si zacatek prikazu
    values = f"VALUES({str(DatasetID[0])}," # predchystame si konec prikazu
    
    for entry in dictionary: # postupne prochazim vytvoreny slovnik
        begin = f"{begin}{entry}," # doplnuju prvni cast prikazu
        values = f"{values}'{dictionary[entry]}'," # doplnuju druhou cast prikazu
    
    query = f"{begin[:-1]}) {values[:-1]})" # obe casti prikazu propojim (ale bez carek na konci)

    cursor.execute(query) # provedu prikaz
    f.close() #  soubor zavru

    # plneni tabulky s epizodami
    # evaluation
    evaluationPath = f"{path}\\{folder}\\evaluation"
    listEpisodes = os.listdir(evaluationPath)
    data = []
    i = 0

    for eachEpisode in listEpisodes:
        metadataPath = f"{evaluationPath}\\{eachEpisode}\\metadata"
        f = open(metadataPath, "r")
        line = f.readline()
        line = f.readline()
        while line:
            items = line.split(",")
            keyText = items[0]
            if keyText == "Duration [ms]":
                keyText = "Duration"
            elif keyText == "Player step count":
                keyText = "PlayerStepCount"
            elif keyText == "Total Payoff":
                keyText = "TotalPayoff"
            elif keyText == "Risk Hit":
                keyText = "RiskHit"
            dictionary[keyText] = items[1][1:-1]
            line = f.readline()
        f.close()

        episodeId = eachEpisode[eachEpisode.find("_")+1:]
        dictionary["CisloEpizody"] = episodeId 
        dictionary["Evaluation"] = True
        dictionary["Training"] = False

        # nacitani nalezenych zlat
        fileStateDump = pandas.read_csv(f"{evaluationPath}\\{eachEpisode}\\stateDump") # otevreme soubor stateDump
        rewardCount = 0 # vytvorime promennou pro pocitani zlat
        lastLine = fileStateDump.shape[0] - 1 # zjistim, kolik radku ma stateDump a odectu 1
        if fileStateDump['Reward_0'][lastLine] == False: # zjistuju, jestli prvni zlato zustalo nenalezene v bludisti
            rewardCount = rewardCount + 1 # nacitam nalezena zlata
        if fileStateDump['Reward_1'][lastLine] == False: # zjistuju, jestli druhe zlato zustalo nenalezene v bludisti
            rewardCount = rewardCount + 1 # nacitam nalezena zlata
        if fileStateDump['Reward_2'][lastLine] == False: # zjistuju, jestli treti zlato zustalo nenalezene v bludisti
            rewardCount = rewardCount + 1 # nacitam nalezena zlata
        dictionary["PocetZlat"] = rewardCount # ulozim to do slovniku

        data.insert(i, (str(DatasetID[0]), dictionary["CisloEpizody"], dictionary["Training"], dictionary["Evaluation"], dictionary["TotalPayoff"], dictionary["RiskHit"], dictionary["PocetZlat"], dictionary["PlayerStepCount"], dictionary["Duration"]))
        print(data[i])
        i = i + 1 
        statement = "INSERT INTO Epizoda (DatasetID, CisloEpizody, Training, Evaluation, TotalPayoff, RiskHit, PocetZlat, PlayerStepCount, Duration) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor.executemany(statement, data)

    # plneni tabulky s epizodami
    # training
    trainingPath =  f"{path}\\{folder}\\training"
    listStages = os.listdir(trainingPath)
    data = []
    i = 0

    for eachStage in listStages:
        stageEpisodePath = f"{trainingPath}\\{eachStage}"
        listStageEpisodes = os.listdir(stageEpisodePath)
        stageId = eachStage[eachStage.find("_")+1:]
        for eachStageEpisode in listStageEpisodes:
            metadataTrainPath = f"{trainingPath}\\{eachStage}\\{eachStageEpisode}\\metadata"
            f = open(metadataTrainPath, "r")
            line = f.readline()
            line = f.readline()
            while line:
                items = line.split(",")
                keyText = items[0]
                if keyText == "Duration [ms]":
                    keyText = "Duration"
                elif keyText == "Player step count":
                    keyText = "PlayerStepCount"
                elif keyText == "Total Payoff":
                    keyText = "TotalPayoff"
                elif keyText == "Risk Hit":
                    keyText = "RiskHit"
                dictionary[keyText] = items[1][1:-1]
                line = f.readline()
            f.close()

            episodeId = eachStageEpisode[eachStageEpisode.find("_")+1:]
            dictionary["CisloEpizody"] = episodeId 
            dictionary["CisloStage"] = stageId
            dictionary["Evaluation"] = False
            dictionary["Training"] = True
            
            # nacitani nalezenych zlat
            fileStateDump = pandas.read_csv(f"{trainingPath}\\{eachStage}\\{eachStageEpisode}\\stateDump") # otevreme soubor stateDump
            rewardCount = 0 # vytvorime promennou pro pocitani zlat
            lastLine = fileStateDump.shape[0] - 1 # zjistim kolik radku ma stateDump a odectu 1
            if fileStateDump['Reward_0'][lastLine] == False: # zjistuju, jestli prvni zlato zustalo nenalezene v bludisti
                rewardCount = rewardCount + 1 # nacitam nalezena zlata
            if fileStateDump['Reward_1'][lastLine] == False: # zjistuju, jestli druhe zlato zustalo nenalezene v bludisti
                rewardCount = rewardCount + 1 # nacitam nalezena zlata
            if fileStateDump['Reward_2'][lastLine] == False: # zjistuju, jestli treti zlato zustalo nenalezene v bludisti
                rewardCount = rewardCount + 1 # nacitam nalezena zlata
            dictionary["PocetZlat"] = rewardCount # ulozim to do slovniku
    
            data.insert(i, (str(DatasetID[0]), dictionary["CisloEpizody"], dictionary["CisloStage"], dictionary["Training"], dictionary["Evaluation"], dictionary["TotalPayoff"], dictionary["RiskHit"], dictionary["PocetZlat"], dictionary["PlayerStepCount"], dictionary["Duration"]))
            print(data[i])
            i = i + 1 
            statement = "INSERT INTO Epizoda (DatasetID, CisloEpizody, CisloStage, Training, Evaluation, TotalPayoff, RiskHit, PocetZlat, PlayerStepCount, Duration) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    
    cursor.executemany(statement, data)

    # plneni tabulky s bludistem
    hallwayPath =  f"{path}\\{folder}\\hallwayInstance"
    f = open(hallwayPath, "r")
    line = f.readline() # nacteme dalsi radek
    PocetRad = -1
    PocetZlat = 0
    PocetPasti = 0
    PocetSloupcu = line.count('W')

    while line: # postupne prochazime radky souboru
        line = f.readline() # nacteme dalsi radek
        PocetZlat = PocetZlat + line.count('G')
        PocetPasti = PocetPasti + line.count('X')
        PocetRad = PocetRad + 1 # navysime pocitadlo
    f.close() # zavru soubor

    query = f"INSERT INTO Bludiste (DatasetID, HallwayInstance, PocetRad, PocetSloupcu, PocetZlat, PocetPasti) VALUES ('{str(DatasetID[0])}', '{dictionary['hallwayInstance']}', '{PocetRad}', '{PocetSloupcu}', '{PocetZlat}', '{PocetPasti}')"
    cursor.execute(query) # provedu prikaz

    cnxn.commit() # potvrdim transakci