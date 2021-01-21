import csv
import numpy as np
from moviepy.editor import VideoClip
import numpy as np
import mayavi.mlab as mlab
import  moviepy.editor as mpy
import glob
import os



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



def generateFixed3DSurface(img):
    mlab.figure(bgcolor=(1,1,1))
    mlab.surf(img,warp_scale='auto',colormap='viridis')
    mlab.show()


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
    return img


def generate3DAnimation(start,end,Valmin,Valmax,tailleX,tailleY, chemin):
    
    X, Y = np.meshgrid(tailleX,tailleY) 
    fig = mlab.figure(size=(1920,1080))
    img = np.zeros((60,60),dtype="float")
    s = mlab.surf(img, warp_scale=25,vmin = Valmin, vmax = Valmax,colormap='viridis', figure = fig)
    f = mlab.gcf()
    f.scene._lift()
    @mlab.animate(delay=20)
    def anim():
        for i in range(start,end):
            s.scene.disable_render = True
            img = getImageForAnimation(i,tailleX,tailleY, chemin)
            s.mlab_source.scalars=img
            mlab.savefig("D:/ESIREM/4A/Python-microonde/Projet4AFDTD/render/img"+str(i)+".png")
            s.scene.disable_render = False
            yield

    anim()
    mlab.show()
    imdir = 'D:/ESIREM/4A/Python-microonde/Projet4AFDTD/render/'
    ext = ['png']  

    files = []
    [files.extend(glob.glob(imdir + '*.' + e)) for e in ext]
    clip = mpy.ImageSequenceClip(sequence=files, fps=24)
    clip.write_gif('2DSinusSansAxes.gif')
    for filePath in files:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")






'''def savePlot(anim):
        print("Nom du fichier avec l'extension ? \nPour rappel le fichier source est " + str(chemin))
        nomfichier = input()
        print("Quel est le nombre de FPS désiré")
        nbfps = input()
        print("sauvegarde")
        f = nomfichier
        FFwriter = animation.FFMpegWriter(fps=nbfps)
        anim.save(f, writer=FFwriter)'''

'''def showAnimOrPicture():
    plt.show()
'''

chemin = "D:/ESIREM/4A/Python-microonde/Projet4AFDTD/Data2D/Ez2D1pointpySin"
tailleX , tailleY = 60,60
#image = getImageForAnimation(0,tailleX , tailleY,chemin)
#generateFixed3DSurface(image)
generate3DAnimation(0,400,-0.2,0.2,60,60,chemin)
