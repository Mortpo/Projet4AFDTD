import Antenne
import numpy as np
import Materiau as Mat
import Cellule
#numpy fft

#defini les parametre de la simulation et les parametres 
class DeviceInfo:


    def __init__(self,rawPatch:Antenne):
        self.cellSizeX = rawPatch.cellSizeX
        self.cellSizeY = rawPatch.cellSizeY
        self.cellSizeZ = rawPatch.cellSizeZ
        self.typeUnite = rawPatch.typeUnite
        self.ra_x = .6625
        self.ra_y = .6812
        self.celerite = 3e8
        self.pi = np.pi
        self.nbPMLlayer = 8
        self.nbFreeSpaceLayer = 4
        self.timeStep = self.cellSizeZ/6e8
        self.curl_h=0.0
        self.curl_e=0.0
        self.gi1,self.gi2,self.gi3 = [],[],[]
        self.gj1,self.gj2,self.gj3 = [],[],[]
        self.gk1,self.gk2,self.gk3 = [],[],[]
        self.fi1,self.fi2,self.fi3 = [],[],[]
        self.fj1,self.fj2,self.fj3 = [],[],[]
        self.fk1,self.fk2,self.fk3 = [],[],[]
        self.patch = self.convertRawPatchToCell(rawPatch)
        self.setPML()
        self.ia=self.nbPMLlayer+self.nbFreeSpaceLayer
        self.ib=self.nbPMLlayer+self.nbFreeSpaceLayer+rawPatch.patch.shape[0]
        self.ja=self.nbPMLlayer+self.nbFreeSpaceLayer
        self.jb=self.nbPMLlayer+self.nbFreeSpaceLayer+rawPatch.patch.shape[1]
        self.ka=self.nbPMLlayer+self.nbFreeSpaceLayer
        self.kb=self.nbPMLlayer+self.nbFreeSpaceLayer+rawPatch.patch.shape[2]
        self.hx_inc = np.zeros(self.patch.shape[1])
        self.ez_inc = np.zeros(self.patch.shape[1])




#permet de reecrire les parametres si il y a eu un changement
    def initialise(self):
        setPML()
        print("Parametre deltaX,Y,Z et T ok = True Sinon False" + testCellSize(self.timeStep,self.rawPatch.cellSizeX,self.rawPatch.cellSizeY,self.rawPatch.cellSizeZ))
        self.patch.convertRawPatchToCell(self.rawPatch)


#test la taille des cellules comparai au temps
    def testCellSize(self):
        valide = False
        if self.timeStep <= (1/self.celerite) * np.sqrt((1/(self.cellSizeX*self.cellSizeX)) + (1/(self.cellSizeY*self.cellSizeY)) + (1/(self.cellSizeZ*self.cellSizeZ))):
            valide = True
            ratio=self.timeStep/((1/self.celerite) * np.sqrt((1/(self.cellSizeX*self.cellSizeX)) + (1/(self.cellSizeY*self.cellSizeY)) + (1/(self.cellSizeZ*self.cellSizeZ))))
            if ratio<90 or ratio >=1:
                print("Warning ratio can be source of problem " + str(ratio))
        return valide



#convertie le patch de la classe antenne en patch avec les cellules de la classe Cellule avec les bons matériaux
    def convertRawPatchToCell(self,rawPatch:Antenne):
        tailleX,tailleY,tailleZ = rawPatch.patch.shape
        patch = np.empty(((rawPatch.patch.shape)),dtype=object )
        for k in range(tailleZ):
            for i in range(tailleX):
                for j in range(tailleY):
                    patch[i][j][k]=Cellule.Cellule(Mat.freeSpace)
                    for l in range(len(Mat.MateriauType)):
                        if rawPatch.patch[i][j][k] == Mat.MateriauType[l].patchValue:
                            patch[i][j][k].gax = Mat.MateriauType[l].conductiviteX
                            patch[i][j][k].gay = Mat.MateriauType[l].conductiviteY
                            patch[i][j][k].gaz = Mat.MateriauType[l].conductiviteZ
                            patch[i][j][k].materiau = Mat.MateriauType[l]
        padding = self.nbFreeSpaceLayer
        patch = np.pad(patch, ((padding,padding),(padding,padding),(padding,padding)), 'constant', constant_values=Cellule.Cellule(Mat.freeSpace))
        padding = self.nbPMLlayer
        patch = np.pad(patch, ((padding,padding),(padding,padding),(padding,padding)), 'constant', constant_values=Cellule.Cellule(Mat.PML))
        return patch

#Calcul les paramètre de PML
    def setPML(self):

        #LES COUCHE DE PML MANGE LE PATCH
        tailleX,tailleY,tailleZ = self.patch.shape

        self.gi1 = np.zeros(tailleX,dtype=float)
        self.fi1 = np.zeros(tailleX,dtype=float)
        self.gi2 = np.ones(tailleX,dtype=float)
        self.fi2 = np.ones(tailleX,dtype=float)
        self.gi3 = np.ones(tailleX,dtype=float)
        self.fi3 = np.ones(tailleX,dtype=float)

        self.gj1 = np.zeros(tailleY,dtype=float)
        self.fj1 = np.zeros(tailleY,dtype=float)
        self.gj2 = np.ones(tailleY,dtype=float)
        self.fj2 = np.ones(tailleY,dtype=float)
        self.gj3 = np.ones(tailleY,dtype=float)
        self.fj3 = np.ones(tailleY,dtype=float)

        self.gk1 = np.zeros(tailleZ,dtype=float)
        self.fk1 = np.zeros(tailleZ,dtype=float)
        self.gk2 = np.ones(tailleZ,dtype=float)
        self.fk2 = np.ones(tailleZ,dtype=float)
        self.gk3 = np.ones(tailleZ,dtype=float)
        self.fk3 = np.ones(tailleZ,dtype=float)

        for i in range(self.nbPMLlayer):
            xxn = (self.nbPMLlayer-i)/(self.nbPMLlayer)
            xn = 0.33*pow(xxn,3.0)
            self.fi1[i]=xn
            self.fi1[tailleX-i-1]=xn
            self.gi2[i] = 1.0/(1.0+xn)
            self.gi2[tailleX-i-1] = 1.0/(1.0+xn)
            self.gi3[i]=(1.0-xn)/(1.0+xn)
            self.gi3[tailleX-i-1]=(1.0-xn)/(1.0+xn) 
            xxn=(self.nbPMLlayer-i-0.5)/self.nbPMLlayer
            xn=0.33*pow(xxn,3.0)
            self.gi1[i]=xn
            self.gi1[tailleX-i-2]=xn
            self.fi2[i]=1.0/(1.0+xn)
            self.fi2[tailleX-i-2] = 1.0/(1.0+xn)
            self.fi3[i] = (1.0-xn)/(1.0+xn) 
            self.fi3[tailleX-i-2] = (1.0-xn)/(1.0+xn)
        
        
        for j in range(self.nbPMLlayer):
            xxn = (self.nbPMLlayer-j)/(self.nbPMLlayer)
            xn = 0.33*pow(xxn,3.0)
            self.fj1[j]=xn
            self.fj1[tailleY-j-1]=xn
            self.gj2[j] = 1.0/(1.0+xn)
            self.gj2[tailleY-j-1] = 1.0/(1.0+xn)
            self.gj3[j]=(1.0-xn)/(1.0+xn)
            self.gj3[tailleY-j-1]=(1.0-xn)/(1.0+xn) 
            xxn=(self.nbPMLlayer-j-0.5)/self.nbPMLlayer
            xn=0.33*pow(xxn,3.0)
            self.gj1[j]=xn
            self.gj1[tailleY-j-2]=xn
            self.fj2[j]=1.0/(1.0+xn)
            self.fj2[tailleY-j-2] = 1.0/(1.0+xn)
            self.fj3[j] = (1.0-xn)/(1.0+xn) 
            self.fj3[tailleY-j-2] = (1.0-xn)/(1.0+xn)

        for k in range(self.nbPMLlayer):
            xxn = (self.nbPMLlayer-k)/(self.nbPMLlayer)
            xn = 0.33*pow(xxn,3.0)
            self.fk1[k]=xn
            self.fk1[tailleZ-k-1]=xn
            self.gk2[k] = 1.0/(1.0+xn)
            self.gk2[tailleZ-k-1] = 1.0/(1.0+xn)
            self.gk3[k]=(1.0-xn)/(1.0+xn)
            self.gk3[tailleZ-k-1]=(1.0-xn)/(1.0+xn) 
            xxn=(self.nbPMLlayer-k-0.5)/self.nbPMLlayer
            xn=0.33*pow(xxn,3.0)
            self.gk1[k]=xn
            self.gk1[tailleZ-k-2]=xn
            self.fk2[k]=1.0/(1.0+xn)
            self.fk2[tailleZ-k-2] = 1.0/(1.0+xn)
            self.fk3[k] = (1.0-xn)/(1.0+xn) 
            self.fk3[tailleZ-k-2] = (1.0-xn)/(1.0+xn)

#Ecrit le patch dans un fichier avec les couche d'air et de pml
    def printfile(self,nameOfTheFile):
        dessusX,dessusY,profondeur = self.patch.shape
        f = open(str(nameOfTheFile)+".txt","w")
        print("File writen to "+ str(nameOfTheFile)+".txt")
        f.write("Bottom\n")
        for z in range(profondeur):
            for x in range(dessusX):
                for y in range(dessusY):
                    f.write(str(self.patch[x][y][z].materiau.patchValue)+";")
                f.write("\n")
            #f.write("\n")

        f.close()

