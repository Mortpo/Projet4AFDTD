import MicroOnde1.Antenne
import numpy as np
import MicroOnde1.Materiaux as Mat
import MicroOnde1.Cellule as Cellule

class DeviceInfo:


    def __init__(self,rawPatch:Antenne):
        self.ra_x
        self.ra_y
        self.ra_z
        self.celerite = 3e8
        self.pi = np.pi
        #self.timeStep # = ddz/6e8?
        self.nbPMLlayer
        self.nbFreeSpaceLayer
        self.timeStep
        self.curl_h,self.curl_e
        self.gi1,self.gi2,self.gi3
        self.gj1,self.gj2,self.gj3
        self.gk1,self.gk2,self.gk3
        self.fi1,self.fi2,self.fi3
        self.fj1,self.fj2,self.fj3
        self.fk1,self.fk2,self.fk3
        setPML(self.nbPMLlayer)
        self.rawPatch = rawPatch
        self.patchnopml = convertRawPatchToCell(rawPatch) # RAJOUTER TOUT PML ET FREE SPACE




    def testCellSize(self,timeStep,cellSizeX,cellSizeY,cellSizeZ):
        valide = False
        if timeStep <= (1/celerite) * np.sqrt((1/(cellSizeX*cellSizeX)) + (1/(cellSizeY*cellSizeY)) + (1/(cellSizeZ*cellSizeZ))):
            valide = True
            ratio=timeStep/((1/celerite) * np.sqrt((1/(cellSizeX*cellSizeX)) + (1/(cellSizeY*cellSizeY)) + (1/(cellSizeZ*cellSizeZ))))
            if ratio<90 or ratio >=1:
                print("Warning ration can be source of problem " + str(ratio))
        return valide

    def sourcePulse(self,t0,spread,T):
        pulse = np.exp(-0.5 * (pow((t0 - T) / spread, 2.0)))
        return pulse

    
    #pas d'air ni pml actuellement
    def convertRawPatchToCell(self):
        tailleX,tailleY,tailleZ = self.rawPatch.shape
        patch = np.zeros(((self.rawPatch.shape)),dtype = Cellule)
        nbMat = len(Mat.materiauxType)
        for k in range(tailleZ):
            for i in range(tailleX):
                for j in range(tailleY):

                    for l in nbMat:
                        if self.rawPatch[i][j][k] == Mat.materiauxType[l].patchValue:
                            patch[i][j][k].gax = Mat.materiauxType[l].conductiviteX
                            patch[i][j][k].gay = Mat.materiauxType[l].conductiviteY
                            patch[i][j][k].gaz = Mat.materiauxType[l].conductiviteZ
        return patch

    def setPML(self):
        #Surement faux pas le bon patch il faut rajouter les couches pml
        #LES COUCHE DE PML MANGE LE PATCH
        tailleX,tailleY,tailleZ = self.patchnopml.shape

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
            fi1[i]=xn
            fi1[tailleX-i-1]=xn
            gi2[i] = 1.0/(1.0+xn)
            gi2[tailleX-i-1] = 1.0/(1.0+xn)
            gi3[i]=(1.0-xn)/(1.0+xn)
            gi3[tailleX-i-1]=(1.0-xn)/(1.0+xn) 
            xxn=(self.nbPMLlayer-i-0.5)/self.nbPMLlayer
            xn=0.33*pow(xxn,3.0)
            gi1[i]=xn
            gi1[tailleX-i-2]=xn
            fi2[i]=1.0/(1.0+xn)
            fi2[tailleX-i-2] = 1.0/(1.0+xn)
            fi3[i] = (1.0-xn)/(1.0+xn) 
            fi3[tailleX-i-2] = (1.0-xn)/(1.0+xn)
        
        
        for j in range(self.nbPMLlayer):
            xxn = (self.nbPMLlayer-j)/(self.nbPMLlayer)
            xn = 0.33*pow(xxn,3.0)
            fj1[j]=xn
            fj1[tailleY-j-1]=xn
            gj2[j] = 1.0/(1.0+xn)
            gj2[tailleY-j-1] = 1.0/(1.0+xn)
            gj3[j]=(1.0-xn)/(1.0+xn)
            gj3[tailleY-j-1]=(1.0-xn)/(1.0+xn) 
            xxn=(self.nbPMLlayer-j-0.5)/self.nbPMLlayer
            xn=0.33*pow(xxn,3.0)
            gj1[j]=xn
            gj1[tailleY-j-2]=xn
            fj2[j]=1.0/(1.0+xn)
            fj2[tailleY-j-2] = 1.0/(1.0+xn)
            fj3[j] = (1.0-xn)/(1.0+xn) 
            fj3[tailleY-j-2] = (1.0-xn)/(1.0+xn)

        for k in range(self.nbPMLlayer):
            xxn = (self.nbPMLlayer-k)/(self.nbPMLlayer)
            xn = 0.33*pow(xxn,3.0)
            fk1[k]=xn
            fk1[tailleZ-k-1]=xn
            gk2[k] = 1.0/(1.0+xn)
            gk2[tailleZ-k-1] = 1.0/(1.0+xn)
            gk3[k]=(1.0-xn)/(1.0+xn)
            gk3[tailleZ-k-1]=(1.0-xn)/(1.0+xn) 
            xxn=(self.nbPMLlayer-k-0.5)/self.nbPMLlayer
            xn=0.33*pow(xxn,3.0)
            gk1[k]=xn
            gk1[tailleZ-k-2]=xn
            fk2[k]=1.0/(1.0+xn)
            fk2[tailleZ-k-2] = 1.0/(1.0+xn)
            fk3[k] = (1.0-xn)/(1.0+xn) 
            fk3[tailleZ-k-2] = (1.0-xn)/(1.0+xn)

