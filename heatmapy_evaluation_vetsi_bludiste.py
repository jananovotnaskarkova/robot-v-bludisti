import pandas as pd 
import os

path = 'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\data_k_nahrani'
folders = os.listdir(path) # ulozi do seznamu nazvy slozek = datasetu

n = 7 # pocet radku bludiste
m = 15 # pocet sloupcu bludiste

for	folder in folders:
	matrix = [0] * n # postupne vytvorim prazdnou matici odpovidajici bludisti
	for i in range (0, n):
		matrix[i] = [0] * m
	for y in range (0, 1000): # scitam vyskyt robota na jednotlivych souradnicich ve vsech epizodach dane stage
		sd = pd.read_csv(f'{path}\\{folder}\\evaluation\\episodeId_{y}\\stateDump') # otviram soubor
		for j in range (0, len(sd)): # postupne prohledavam vsechny radky souboru 'stateDump'
			a = int(sd['Agent coordinate X'][j]) # souradnici 'x' ukladam do 'a'
			b = int(sd['Agent coordinate Y'][j]) # souradnici 'y' ukladam do 'b'
			if sd['Is agent turn'][j] == True: # kontroluju, zda je v danem kroku na tahu robot	
				matrix[a][b] = matrix[a][b] + 1 # pokud ano, navysuju hodnotu na danem miste matice o 1
			else:
				continue # pokud ne, jdu na dalsi radek
		matrix[5][1] = matrix[5][1] - 1	# na startu odecitam "nulty" krok

	print(folder)
	for i in range (0, n): # tisk matice na vystup
		for j in range (0, m):
			print(f"{matrix[i][j]:>4}", end=" ")
		print()

	f = open(f'{folder}_map_evaluation.txt', 'w') # vytvarim soubor pro vypis
	f.write(f'{folder}\n')
	for i in range (0, n): # vypis do souboru
		for j in range (0, m):
			if j < (m - 1):
				f.write(str(matrix[i][j]))
				f.write(',')
			else:
				f.write(str(matrix[i][j]))	
		f.write('\n')