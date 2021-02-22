import csv
import numpy as np
from moviepy.editor import VideoClip
import numpy as np
import mayavi.mlab as mlab
import  moviepy.editor as mpy
import glob
import os
import pyvista as pv



#Code pour faire le menu de traitement choisir l'image si c'est une animation ou non
#combine le code de traitement et animation

#Pour la premiere image du fichier

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
            img = getImageForAnimation(i,tailleX,tailleY, chemin) #Pas opti
            s.mlab_source.scalars=img
            stringPath = "render/img"+str(i)+".png"
            files.append( stringPath)
            mlab.savefig(stringPath)
            s.scene.disable_render = False
            yield

    anim()
    mlab.show()

    print("1 pour gif, autre chose pour mp4")
    gif = int(input())
    print("Nom du fichier sans extension")
    nomgif = input()

    clip = mpy.ImageSequenceClip(files , fps=24)

    if gif==1:
        clip.write_gif(str(nomgif)+".gif",program='imageio', opt='nq')
    else:
        clip.write_videofile(str(nomgif)+".mp4",audio=False)



    for filePath in files:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")






def showPatch(chemin,tailleX,tailleY,tailleZ):
    patch = np.zeros((tailleX,tailleY,tailleZ),dtype = int)
    with open(chemin, newline='') as csvdata:
        datareader = csv.reader(csvdata, delimiter=';')
        k=0
        j=0
        
        for ligne in datareader:
            for i in range(tailleX):
                patch[i][j][k]=int(ligne[i])
            j=(j+1)%tailleY
            if j == 0:
                k= (k+1)
           
    #point_cloud = mlab.points3d(patch,opacity = 0.5,transparent=True,line_width=1.0,scale_factor=0.3,mask_points=20,mode='cube',scale_mode='scalar',vmin = 0,vmax = 4)
    #mlab.show()
    
    p = pv.Plotter(window_size=(1080,720))
    mesh = pv.UniformGrid()
    mesh.dimensions=patch.shape
    mesh.point_arrays["values"] = patch.flatten(order="F")
    opacity = [1, 0.5, 0.1, 0.1]
    p.add_volume(mesh, cmap="viridis",opacity=opacity,shade=False)
    p.enable_terrain_style()
    p.show()
 



#chemin = "Data/Data2D/Ez2DGaussPy.data"
#tailleX , tailleY = 60,60
showPatch("Data\Data3D\ShowPatch.txt",40+8*4,40+8*4,4+8*4)
#generateFixed3DSurface(image)
#generate3DAnimation(0,250,-0.2,0.2,60,60,chemin)
