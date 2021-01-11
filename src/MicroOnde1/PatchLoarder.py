import numpy as np
from PIL import Image
import cv2 as CV
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation


#Methode pour 2 types de materiaux
def loadPatchFromPicture(pathTopPatch,pathSidePatch,pathFrontPatch):
    dessus = CV.imread(pathTopPatch)
    cote=CV.imread(pathSidePatch)
    face = CV.imread(pathFrontPatch)

    dessusX,dessusY , profondeur = dessus.shape
    coteZ , coteX, profondeur =  cote.shape
    faceZ, faceY , profondeur= face.shape

    dessusTraite = np.zeros((dessusX,dessusY),dtype='uint8')
    coteTraite = np.zeros((coteZ , coteX),dtype='uint8')
    faceTraite = np.zeros((faceZ, faceY),dtype='uint8')

    #definition des type de case pour un ID unique
    #Couleur , ID unique
    #tableau externe
    #attention open CV charge en BGR et non RGB
    patch=([255,255,255],1)
    isolant=([0,0,0],0)
    materiauxType = [patch,isolant]

    if(coteZ != faceZ):
        print("Mauvaise dimensention entre 2 images cote et face en Z")
        print(coteZ,faceZ)
    if(dessusY != faceY):
        print("Mauvaise dimensention entre 2 images dessus et face en Y")
        print(dessusY,faceY)
    if(dessusX != coteX):
        print("Mauvaise dimensention entre 2 images dessus et cote en X")
        print(dessusX,coteX)

    for x in range(dessusX):
        for y in range(dessusY):
            for k in range(len(materiauxType)):
                if bool(set(dessus[x][y]).intersection(materiauxType[k][0])):
                    dessusTraite[x][y] = materiauxType[k][1]

        

    for x in range(coteZ):
        for y in range(coteX):
            for k in range(len(materiauxType)):
                if bool(set(cote[x][y]).intersection(materiauxType[k][0])):
                    coteTraite[x][y] = materiauxType[k][1]

    for x in range(faceZ):
        for y in range(faceY):
            for k in range(len(materiauxType)):
                if bool(set(face[x][y]).intersection(materiauxType[k][0])):
                    faceTraite[x][y] = materiauxType[k][1]
    
    patch = np.ones((((dessusX,dessusY,coteZ))),dtype='uint8')

    for x in range(dessusX):
        for y in range(dessusY):
            for z in range(coteZ):
                patch[x][y][z] = 1 if (dessusTraite[x][y] and patch[x][y][z]) else 0


    for x in range(dessusX):
        for y in range(dessusY):
            for z in range(coteZ):
                patch[x][y][z] = 1 if (coteTraite[z][x] and patch[x][y][z]) else 0


    for x in range(dessusX):
        for y in range(dessusY):
            for z in range(coteZ):
                patch[x][y][z] = 1 if (faceTraite[z][y] and patch[x][y][z]) else 0
    
    return patch

def printfile(nameOfTheFile,patch):
    dessusX,dessusY,profondeur = patch.shape
    img=np.zeros( ((dessusX,dessusY)) ,dtype='uint8')
    f = open("patch","w")
    for z in range(profondeur):
        for x in range(dessusX):
            for y in range(dessusY):
                f.write(str(patch[x][y][z]))
                img[x][y] = patch[x][y][z]
            f.write("\n")
        f.write("\n")

    f.close()
    

    

dessus = CV.imread("Dessus.png")
cote=CV.imread("Cote.png")
face = CV.imread("Face.png")

#Methode pour 2 types de mate   riaux

dessusX,dessusY , profondeur = dessus.shape
coteZ , coteX, profondeur =  cote.shape
faceZ, faceY , profondeur= face.shape


dessusTraite = np.uint8(np.zeros((dessusX,dessusY)))
coteTraite = np.uint8(np.zeros((coteZ , coteX)))
faceTraite = np.uint8(np.zeros((faceZ, faceY)))

#definition des type de case pour un ID unique
#Couleur , ID unique
#tableau externe
#attention open CV charge en BGR et non RGB
patch=([255,255,255],1)
isolant=([0,0,0],0)
materiauxType = [([255,255,255],0),([0,0,0],1)]

if(coteZ != faceZ):
    print("Mauvaise dimensention entre 2 images cote et face en Z")
    print(coteZ,faceZ)
if(dessusY != faceY):
    print("Mauvaise dimensention entre 2 images dessus et face en Y")
    print(dessusY,faceY)
if(dessusX != coteX):
    print("Mauvaise dimensention entre 2 images dessus et cote en X")
    print(dessusX,coteX)


for x in range(dessusX):
    for y in range(dessusY):
        for k in range(len(materiauxType)):
            if bool(set(dessus[x][y]).intersection(materiauxType[k][0])):
                dessusTraite[x][y] = materiauxType[k][1]

    

for x in range(coteZ):
    for y in range(coteX):
        for k in range(len(materiauxType)):
            if bool(set(cote[x][y]).intersection(materiauxType[k][0])):
                coteTraite[x][y] = materiauxType[k][1]

for x in range(faceZ):
    for y in range(faceY):
        for k in range(len(materiauxType)):
            if bool(set(face[x][y]).intersection(materiauxType[k][0])):
                faceTraite[x][y] = materiauxType[k][1]
#1 blanc/rien 0 noir/patch


#Creation de la 3D
patch = np.ones((((dessusX,dessusY,coteZ))),dtype='uint8')


for x in range(dessusX):
    for y in range(dessusY):
        for z in range(coteZ):
            patch[x][y][z] = 1 if (dessusTraite[x][y] and patch[x][y][z]) else 0



for x in range(dessusX):
    for y in range(dessusY):
        for z in range(coteZ):
            patch[x][y][z] = 1 if (coteTraite[z][x] and patch[x][y][z]) else 0


for x in range(dessusX):
    for y in range(dessusY):
        for z in range(coteZ):
            patch[x][y][z] = 1 if (faceTraite[z][y] and patch[x][y][z]) else 0

#affichage

fig = plt.figure()
ims=[]
img=np.zeros( ((dessusX,dessusY)) ,dtype='uint8')
f = open("patch","w")
for i in range(4):
    for x in range(dessusX):
        for y in range(dessusY):
            f.write(str(patch[x][y][i]))
            img[x][y] = patch[x][y][i]
        f.write("\n")
    f.write("\n")
    im = plt.imshow(img,cmap='binary',aspect='auto')
    ims.append([im])
    #f.write(str(img))

    

plt.grid(True)
plt.title("Animation du champ Ez au cours du temps")
plt.xlabel("Position X")
plt.ylabel("Position Y")

ani = animation.ArtistAnimation(fig, ims, interval=3000, blit=True,
                                repeat_delay=1000)

plt.show()
f.close()