import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


print('Chemin du fichier')
chemin = "D:/ESIREM/4A/Python-microonde/Ccode/Projet4AFDTD/Data2D/Ez2D1point"

data = np.zeros((60,60))
num=0
with open(chemin, newline='') as csvdata:
    datareader = csv.reader(csvdata, delimiter=' ')
    for row in datareader:
        for i in range(60):
            data[num][i]=float(row[i])
        num+=1
#print(data)

#donnees
x = np.arange(len(data))
y = np.arange(len(data))
x,y = X, Y = np.meshgrid(x, y)
z = data
#figure
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(x, y, z, cmap=cm.coolwarm,linewidth=0, antialiased=False)
#axe
ax.set_zlim(-0.5, 0.5)
#afficahge
plt.show()