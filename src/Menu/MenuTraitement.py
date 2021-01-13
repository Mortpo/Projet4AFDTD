import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
from matplotlib import cm
import matplotlib.animation as animation
import ffmpeg

#Code pour faire le menu de traitement choisir l'image si c'est une annimation ou non
#combine le code de traitement et annimation

#Pour la premiere image du fichier
def getImage(tailleX,tailleY,chemin):
    img = np.zeros(((tailleX,tailleY)))
    num=0
    with open(chemin, newline='') as csvdata:
        datareader = csv.reader(csvdata, delimiter=' ')
        for row in datareader:
            for i in range(tailleY):
                img[num][i]=float(row[i])
            num+=1
    return img


def generateFixedPicture(img):
    plt.figure()
    plt.imshow(img)
    plt.show()

def generateFixed3DSurface(img):
    tailleX, tailleY = img.shape
    x = range(tailleX)
    y = range(tailleY)
    X,Y= np.meshgrid(x,y)
    Z = img

    #figure
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plt.ylim(-0.5, tailleY-0.5)
    plt.xlim(-0.5, tailleX-0.5)
    ax.plot_surface(X, Y, np.transpose(Z), rstride=1,cstride=1 ,cmap=cm.viridis, antialiased=True)
    plt.show()


#Pour l'animation ou une image d'indice N
def getImageForAnimation(indice ,tailleX,tailleY, chemin):
    img = np.zeros((tailleX,tailleY))
    with open(chemin, newline='') as csvdata:
        datareader = csv.reader(csvdata, delimiter=' ')
        for u in np.arange(indice*tailleY):
            datareader.__next__()

        for u in np.arange(tailleX):
            ligne = datareader.__next__()
            for i in np.arange(tailleY):
                img[u][i]=float(ligne[i])
    return np.transpose(img) 

def generate2DAnimation(start,end,Valmin,Valmax,tailleX,tailleY, chemin):
    
    fig = plt.figure()
    if Valmax != Valmin:
        norm = cm.colors.Normalize(vmin=Valmin,vmax=Valmax)
    else:
        norm = cm.colors.Normalize()

    ims=[]
    for i in range(start,end):
        im = plt.imshow(getImageForAnimation(i ,tailleX,tailleY, chemin), animated=True, cmap=cm.magma,norm=norm ,aspect='auto')
        ims.append([im])

    plt.grid(True)
    plt.title("Animation du champ Ez au cours du temps")
    plt.xlabel("Position X")
    plt.ylim(-0.5, tailleY-0.5)
    plt.xlim(-0.5, tailleX-0.5)
    plt.ylabel("Position Y")

    anim = animation.ArtistAnimation(fig, ims, interval=5, blit=True,
                                    repeat_delay=1000)
    plt.show()
    return anim

def generate3DAnimation(start,end,Valmin,Valmax,tailleX,tailleY, chemin):
    
    x = np.arange(tailleX)
    y = np.arange(tailleY)
    X,Y= np.meshgrid(x,y)

    fig = plt.figure()
    ax = Axes3D(fig)
    if Valmax != Valmin:
        norm = cm.colors.Normalize(vmin=Valmin,vmax=Valmax)
        ax.set_zlim(Valmin,Valmax)
    else:
        norm = cm.colors.Normalize()

    ims=[]
    for i in range(start,end):
        data = getImageForAnimation(i ,tailleX,tailleY, chemin)
        im = ax.plot_surface(X, Y, data,animated=True, linewidth=0,rstride=1,cstride=1 ,cmap=cm.magma,norm=norm, antialiased=True)
        ims.append([im])

    plt.grid(True)
    plt.title("Animation du champ Ez au cours du temps")
    plt.xlabel("Position X")
    plt.ylim(-0.5, tailleY-0.5)
    plt.xlim(tailleX-0.5,-0.5 )

    plt.ylabel("Position Y")

    anim = animation.ArtistAnimation(fig, ims, interval=5, blit=True,
                                    repeat_delay=1000)
    #plt.show()
    return anim


def savePlot(anim):
        print("Nom du fichier avec l'extension ? \nPour rappel le fichier source est " + str(chemin))
        nomfichier = input()
        print("Quel est le nombre de FPS désiré")
        nbfps = input()
        print("sauvegarde")
        f = nomfichier
        FFwriter = animation.FFMpegWriter(fps=nbfps)
        anim.save(f, writer=FFwriter)

def showAnimOrPicture():
    plt.show()


chemin = "D:/ESIREM/4A/Python-microonde/Ccode/Projet4AFDTD/Data3D/CEzplane"
tailleX , tailleY = 120,62
#image = getImageForAnimation(800,tailleX , tailleY,chemin)
#generateFixedPicture(image)
#generateFixed3DSurface(image)
ani = generate2DAnimation(400,800,-0.5,1,tailleX , tailleY,chemin)
#ani = generate3DAnimation(0,150,-1,1,60,60,chemin)
#savePlot(ani)