import pandas as pd 
import os

folders = []
episodes = []

# csv soubor vygenerovany z databaze se seznamem epizod s nejkratsimi cestami
nejkratsiCesty = pd.read_csv(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\heatmapy\\nejkratsi_cesty\\nejkratsi_cesta.csv', sep=';')

# staci mi data z evaluace
for j in range (0, len(nejkratsiCesty)):
	if nejkratsiCesty['Evaluation'][j] == 1: 
		folders.append(nejkratsiCesty['NazevSlozky'][j])
		episodes.append(nejkratsiCesty['CisloEpizody'][j])	

path = 'F:\\ralph'

n = 10 # pocet radku bludiste
m = 7 # pocet sloupcu bludiste

for	c, folder in enumerate(folders):
	y = episodes[c]
	matrix = [0] * n # postupne vytvorim prazdnou matici odpovidajici bludisti
	for i in range (0, n):
		matrix[i] = [0] * m
	sd = pd.read_csv(f'{path}\\{folder}\\evaluation\\episodeId_{y}\\stateDump') # otviram soubor
	for j in range (0, len(sd)): # postupne prohledavam vsechny radky souboru 'stateDump'
		a = int(sd['Agent coordinate X'][j]) # souradnici 'x' ukladam do 'a'
		b = int(sd['Agent coordinate Y'][j]) # souradnici 'y' ukladam do 'b'
		if sd['Is agent turn'][j] == True: # kontroluju, zda je v danem kroku na tahu robot	
			matrix[a][b] = matrix[a][b] + 1 # pokud ano, navysuju hodnotu na danem miste matice o 1
		else:
			continue # pokud ne, jdu na dalsi radek
	matrix[1][1] = matrix[1][1] - 1	# na startu odecitam "nulty" krok

	print(folder, y) # info o datasetu a epizode
	for i in range (0, n): # tisk matice na vystup
		for j in range (0, m):
			print(f"{matrix[i][j]:>4}", end=" ")
		print()

	f = open(f'nejkratsi_cesty_map_evaluation.txt', 'a') # vytvarim soubor pro vypis
	f.write(f'{path}\\{folder}\\evaluation\\episodeId_{y}\\stateDump\n')
	for i in range (0, n): # vypis do souboru
		for j in range (0, m):
			if j < (m - 1):
				f.write(str(matrix[i][j]))
				f.write(',')
			else:
				f.write(str(matrix[i][j]))	
		f.write('\n')
