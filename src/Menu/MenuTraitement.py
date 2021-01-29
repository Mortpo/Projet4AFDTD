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
        for u in range(indice*tailleY):
            datareader.__next__()

        for u in range(tailleX):
            ligne = datareader.__next__()
            for i in np.arange(tailleY):
                img[u][i]=float(ligne[i])
    return img




def generate3DAnimation(start,end,Valmin,Valmax,tailleX,tailleY, chemin):
    
    X, Y = np.meshgrid(tailleX,tailleY)
    scale = 25
    fig = mlab.figure(size=(480,360),bgcolor = (0,0,0))
    img = np.zeros((tailleX,tailleY),dtype="float")
    s = mlab.surf(img, warp_scale=scale,vmin = Valmin, vmax = Valmax,colormap='viridis', figure = fig)
    f = mlab.gcf()
    f.scene._lift()
    mlab.view(azimuth= 180+45)
    mlab.axes(figure = fig,nb_labels = 3,ranges = [0,tailleX, 0,tailleY,Valmin*scale ,Valmax*scale],xlabel="Delta X",ylabel="Delta Y",zlabel="Ez",x_axis_visibility=True,y_axis_visibility=False,z_axis_visibility=True)
    mlab.colorbar(object=s, title="Champ Ez", orientation='vertical', nb_labels=None, nb_colors=255)
    mlab.move(forward= -30)
    files = []
    @mlab.animate(delay=20)
    def anim():
        for i in range(start,end):
            s.scene.disable_render = True
            img = getImageForAnimation(i,tailleX,tailleY, chemin)
            s.mlab_source.scalars=img
            stringPath = "D:/ESIREM/4A/Python-microonde/Projet4AFDTD/render/img"+str(i)+".png"
            files.append( stringPath)
            mlab.savefig(stringPath)
            s.scene.disable_render = False
            yield

    anim()
    mlab.show()

    clip = mpy.ImageSequenceClip(sequence=files, fps=24)
    clip.write_gif('2DSinusSansAxesTest.gif')
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

chemin = "D:/ESIREM/4A/Python-microonde/Projet4AFDTD/Data2D/Ez2DpySin.data"
tailleX , tailleY = 60,60
#image = getImageForAnimation(0,tailleX , tailleY,chemin)
#generateFixed3DSurface(image)
generate3DAnimation(0,400,-0.2,0.2,60,60,chemin)
