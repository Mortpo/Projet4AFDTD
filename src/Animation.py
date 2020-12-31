


import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
from matplotlib import cm
import matplotlib.animation as animation
import ffmpeg


print('Chemin du fichier')
chemin = "D:/ESIREM/4A/Python-microonde/Ccode/Projet4AFDTD/Data2D/Ez2D1pointpy"
print(chemin)

data = np.zeros((60,60))
tailleX, tailleY = data.shape
x = np.arange(tailleX)
y = np.arange(tailleY)
X,Y= np.meshgrid(x,y)
def animate(i): 


    with open(chemin, newline='') as csvdata:
        datareader = csv.reader(csvdata, delimiter=' ')
        for u in np.arange(i*60):
            datareader.__next__()

        for u in np.arange(60):
            ligne = datareader.__next__()
            for i in np.arange(60):
                
                data[u][i]=float(ligne[i])

    
    
    return data

set2D = False
print("1 pour le 2D et 0 pour le 3D")
if int(input()):
    set2D=True

print("T---->")
T=int(input())
print("Vmin---->")
Valmin=float(input())
print("Vmax---->")
Valmax=float(input())

if set2D:

    fig = plt.figure()
    norm = cm.colors.Normalize(vmin=Valmin,vmax=Valmax)
    ims=[]
    for i in range(T):
        im = plt.imshow(animate(i), animated=True, cmap=cm.magma,norm=norm ,aspect='auto')
        ims.append([im])

    plt.grid(True)
    plt.title("Animation du champ Ez au cours du temps")
    plt.xlabel("Position X")
    plt.ylabel("Position Y")

    ani = animation.ArtistAnimation(fig, ims, interval=30, blit=True,
                                    repeat_delay=1000)

    plt.show()
    print("sauvegarde")
    f = "Resultat/AnimationGauss_2D_800T.mp4" 
    FFwriter = animation.FFMpegWriter(fps=8)
    anim.save(f, writer=FFwriter)
else:
    print('3D')
    fig = plt.figure()
    ax = Axes3D(fig)
    norm = cm.colors.Normalize(vmin=Valmin,vmax=Valmax)
    ims=[]
    #lecture
    with open(chemin, newline='') as csvdata:
        datareader = csv.reader(csvdata, delimiter=' ')
        for v in range(T):

            for u in np.arange(60):
                ligne = datareader.__next__()
                for i in np.arange(60):
                    
                    data[u][i]=float(ligne[i])

            im = ax.plot_surface(X, Y, data,animated=True, linewidth=0,rstride=1,cstride=1 ,cmap=cm.magma,norm=norm, antialiased=True)
            ims.append([im])

    plt.title("Animation du champ Ez au cours du temps")
    plt.xlabel("Position X")
    plt.ylabel("Position Y")
    ax.set_zlim(Valmin,Valmax)
    print('creation animation')

    anim = animation.ArtistAnimation(fig, ims, interval=123, blit=True,
                                    repeat_delay=10000)

    
    #plt.show()
    print("sauvegarde")
    f = "Resultat/FDTD2D_Onde.mp4" 
    FFwriter = animation.FFMpegWriter(fps=8)
    anim.save(f, writer=FFwriter)

