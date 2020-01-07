from PIL import Image
import sys
import os
import pandas as pd

playerX = []
playerY = []

path = f'F:\\ralph\\2019_11_01_00_28_56\\evaluation'
folders = os.listdir(path)
pathPicture = f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\out2\\'

a = 0
for folder in folders:
    if a == 5:
        break   
    stateDump = pd.read_csv(f'{path}\\{folder}\\stateDump')
    episodeX = []
    episodeY = []
    for i in range (0, len(stateDump)): 
        x = int(stateDump['Agent coordinate X'][i])
        y = int(stateDump['Agent coordinate Y'][i])
        if stateDump['Is agent turn'][i] == True:
            episodeX.append(x)
            episodeY.append(y)
        else:
            continue
    playerX.append(episodeX)
    playerY.append(episodeY)
    a = a + 1

count = 0

past = [(3,1),(4,1),(5,1),(6,1),(7,1),(3,5),(4,5),(5,5),(6,5),(7,5)]
poklad = ((8,2),(8,3),(8,4))

for i in range (0, len(playerX)):
	pokladVBludisti = [1,1,1]
	for j in range (0, len(playerX[i])):
		robot = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\robot.png', 'r')
		x = playerX[i][j]
		y = playerY[i][j]
		print((x,y))
		if (x,y) in poklad:
			nalezeno = poklad.index((x,y))
			pokladVBludisti[nalezeno] = 0
			print(pokladVBludisti)
		x = playerY[i][j]*40
		y = playerX[i][j]*40
		print((x,y))
		if pokladVBludisti == [1,1,1]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_111.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		elif pokladVBludisti == [1,1,0]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_110.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		elif pokladVBludisti == [1,0,1]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_101.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		elif pokladVBludisti == [0,1,1]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_011.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		elif pokladVBludisti == [1,0,0]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_100.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		elif pokladVBludisti == [0,1,0]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_010.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		elif pokladVBludisti == [0,0,1]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_001.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		elif pokladVBludisti == [0,0,0]:
			bludiste = Image.open(f'C:\\Users\\Jana\\Documents\\czechitas\\00_projekt\\animace\\male_bludiste\\bludiste_000.png', 'r')
			bludiste.paste(robot, (x, y))
			bludiste.save(f'{pathPicture}im_{count}.png')
		count = count + 1
		j = j + 1
	i = i + 1