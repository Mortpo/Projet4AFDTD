import numpy as np
import cv2 as CV


class Antenne:
    

    def __init__(pathTopPatch,pathSidePatch,pathFrontPatch,largeurXPatch,longueurYPatch,hauteurZPatch,typeUnite):
        self.patch = loadPatchFromPicture(pathTopPatch,pathSidePatch,pathFrontPatch)
        printfile(str(nameOfTheFile)+".txt",self.patch)
        self.largeurXPatch = largeurXPatch
        self.longueurYPatch = longueurYPatch
        self.hauteurZPatch = hauteurZPatch
        self.typeUnite = typeUnite


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
        f = open(str(nameOfTheFile)+".txt","w")
        for z in range(profondeur):
            for x in range(dessusX):
                for y in range(dessusY):
                    f.write(str(patch[x][y][z]))
                    img[x][y] = patch[x][y][z]
                f.write("\n")
            f.write("\n")

        f.close()
