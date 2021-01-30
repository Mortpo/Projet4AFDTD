import numpy as np
import cv2 as CV
import MicroOnde1.Materiaux as Mat


class Antenne:
    

    def __init__(self,toplayer,cellSizeX,cellSizeY,cellSizeZ,typeUnite):
        self.patch = loadLayerFromPicture(toplayer)
        self.cellSizeX = cellSizeX
        self.cellSizeY = cellSizeY
        self.cellSizeZ = cellSizeZ
        self.typeUnite = typeUnite
        
    #ajout une couche par le bas
    def AddLayer(self,layer):
        self.patch = np.concatenate((self.patch,layer),axis=2)

    def printfile(self,nameOfTheFile):
        dessusX,dessusY,profondeur = self.patch.shape
        img=np.zeros( ((dessusX,dessusY)) ,dtype='uint8')
        f = open(str(nameOfTheFile)+".txt","w")
        for z in range(profondeur):
            for x in range(dessusX):
                for y in range(dessusY):
                    f.write(str(self.patch[x][y][z]))
                    img[x][y] = self.patch[x][y][z]
                f.write("\n")
            f.write("\n")

        f.close()


    def loadLayerFromPicture(self,pathToLayer): #1 px 1 cellule
        layer = CV.imread(pathToLayer)

        tailleX , tailleY, dim = layer.shape
        couche = np.ones((((tailleX , tailleY, 1))),dtype='uint8')
        for x in range(tailleX):
            for y in range(tailleY):
                for z in range(len(Mat.materiauxType)):
                    if bool(set(layer[x][y]).intersection(set(Mat.materiauxType[z].rgbValue))):
                        couche[x][y][0] = Mat.materiauxType[z].patchValue
        return couche
