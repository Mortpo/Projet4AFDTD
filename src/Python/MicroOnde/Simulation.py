import Antenne
import numpy as np
import Materiau as Mat
import Cellule
import SimDevTestInfo as Dev


#Classe pour la simulation elle ne modifie ne rien les parametres et ne stocke aucune donnees
class Simulation: #potentiel pb si cell non pml genre elle devient pml a cause des calcul de idhxyz

    def __init__(self,device:Dev.DeviceInfo):
        self.simdevice = device
        self.tailleX,self.tailleY,self.tailleZ = self.simdevice.patch.shape

#fonction du signal à envoyer
    def sourcePulse(self,t0,spread,T):
        pulse = np.exp(-0.5 * (pow((t0 - T) / spread, 2.0))) #gauss
        return pulse


    def EzInc(self):
        for j in range(1,self.simdevice.patch.shape[1]):
            self.simdevice.ez_inc[j] = self.simdevice.ez_inc[j]  + 0.5  * (self.simdevice.hx_inc[j - 1] - self.simdevice.hx_inc[j])

    def HxInc(self):
        for j in range(0,self.simdevice.patch.shape[1]-1):
            self.simdevice.hx_inc[j] = self.simdevice.hx_inc[j] +  0.5 * (self.simdevice.ez_inc[j ] - self.simdevice.ez_inc[j+1])
    
    def DyBuffer(self):
        for i in range(self.simdevice.ia,self.simdevice.ib+1):
            for j in range(self.simdevice.ja,self.simdevice.jb):
                self.simdevice.patch[i][j][self.simdevice.ka].dy = self.simdevice.patch[i][j][self.simdevice.ka].dy - 0.5  * self.simdevice.hx_inc[j]
                self.simdevice.patch[i][j][self.simdevice.kb+1].dy = self.simdevice.patch[i][j][self.simdevice.kb+1].dy + 0.5  * self.simdevice.hx_inc[j]

    def DzBuffer(self):
        for i in range(self.simdevice.ia,self.simdevice.ib+1):
            for k in range(self.simdevice.ka,self.simdevice.kb+1):
                self.simdevice.patch[i][self.simdevice.ja][k].dz = self.simdevice.patch[i][self.simdevice.ja][k].dz + 0.5  * self.simdevice.hx_inc[self.simdevice.ja-1]
                self.simdevice.patch[i][self.simdevice.jb][k].dz = self.simdevice.patch[i][self.simdevice.jb][k].dz - 0.5  * self.simdevice.hx_inc[self.simdevice.jb]

    def hxBuffer(self):
        for i in range(self.simdevice.ia,self.simdevice.ib+1):
            for k in range(self.simdevice.ka,self.simdevice.kb+1):
                self.simdevice.patch[i][self.simdevice.ja-1][k].hx = self.simdevice.patch[i][self.simdevice.ja-1][k].hx - 0.5  * self.simdevice.ez_inc[self.simdevice.ja]
                self.simdevice.patch[i][self.simdevice.jb][k].hx = self.simdevice.patch[i][self.simdevice.jb][k].hx + 0.5  * self.simdevice.ez_inc[self.simdevice.jb]

    def hyBuffer(self):
        for j in range(self.simdevice.ja,self.simdevice.jb+1):
            for k in range(self.simdevice.ka,self.simdevice.kb+1):
                self.simdevice.patch[self.simdevice.ia-1][j][k].hy = self.simdevice.patch[self.simdevice.ia-1][j][k].hy - 0.5  * self.simdevice.ez_inc[j]
                self.simdevice.patch[self.simdevice.ib][j][k].hy = self.simdevice.patch[self.simdevice.ib][j][k].hy + 0.5  * self.simdevice.ez_inc[j]
        
#calcul
    def calculateDx(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.curl_h = (self.simdevice.ra_y * (self.simdevice.patch[i][j][k].hz - self.simdevice.patch[i][j - 1][k].hz) - self.simdevice.patch[i][j][k].hy + self.simdevice.patch[i][j][k - 1].hy)
                        if self.simdevice.patch[i][j][k].materiau.patchValue == Mat.PML.patchValue:
                            self.simdevice.patch[i][j][k].idx = self.simdevice.patch[i][j][k].idx + self.simdevice.curl_h
                        else:
                            self.simdevice.patch[i][j][k].idx = 0
                        self.simdevice.patch[i][j][k].dx = self.simdevice.gj3[j] * self.simdevice.gk3[k] * self.simdevice.patch[i][j][k].dx + self.simdevice.gj2[j] * self.simdevice.gk2[k] * 0.5 * (self.simdevice.curl_h + (self.simdevice.gi1[i] * self.simdevice.patch[i][j][k].idx))
#calcul
    def calculateDy(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.curl_h = (self.simdevice.patch[i][j][k].hx - self.simdevice.patch[i][j][k - 1].hx - self.simdevice.ra_x * (self.simdevice.patch[i][j][k].hz - self.simdevice.patch[i - 1][j][k].hz))
                        if self.simdevice.patch[i][j][k].materiau.patchValue == Mat.PML.patchValue:
                            self.simdevice.patch[i][j][k].idy = self.simdevice.patch[i][j][k].idy + self.simdevice.curl_h
                        else:
                            self.simdevice.patch[i][j][k].idy = 0
                        self.simdevice.patch[i][j][k].dy = self.simdevice.gi3[i] * self.simdevice.gk3[k] * self.simdevice.patch[i][j][k].dy + self.simdevice.gi2[i] * self.simdevice.gk2[k] * 0.5 * (self.simdevice.curl_h + (self.simdevice.gj1[j] * self.simdevice.patch[i][j][k].idy))
#calcul
    def calculateDz(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.curl_h = (self.simdevice.ra_x * (self.simdevice.patch[i][j][k].hy - self.simdevice.patch[i - 1][j][k].hy) - self.simdevice.ra_y * (self.simdevice.patch[i][j][k].hx - self.simdevice.patch[i][j - 1][k].hx))
                        if self.simdevice.patch[i][j][k].materiau.patchValue == Mat.PML.patchValue:
                            self.simdevice.patch[i][j][k].idz = self.simdevice.patch[i][j][k].idz + self.simdevice.curl_h
                        else:
                            self.simdevice.patch[i][j][k].idz = 0
                        self.simdevice.patch[i][j][k].dz = self.simdevice.gi3[i] * self.simdevice.gj3[j] * self.simdevice.patch[i][j][k].dz + self.simdevice.gi2[i] * self.simdevice.gj2[j] * 0.5 * (self.simdevice.curl_h + (self.simdevice.gk1[k] * self.simdevice.patch[i][j][k].idz))
#calcul
    def calculateE(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.patch[i][j][k].ex = self.simdevice.patch[i][j][k].gax * self.simdevice.patch[i][j][k].dx
                        self.simdevice.patch[i][j][k].ey = self.simdevice.patch[i][j][k].gay * self.simdevice.patch[i][j][k].dy
                        self.simdevice.patch[i][j][k].ez = self.simdevice.patch[i][j][k].gaz * self.simdevice.patch[i][j][k].dz

#calcul
    def calculateHx(self):
        for i in range(self.tailleX-1):
            for j in range(self.tailleY-1):
                for k in range(self.tailleZ-1):
                        self.simdevice.curl_e = (self.simdevice.patch[i][j][k + 1].ey - self.simdevice.patch[i][j][k].ey - self.simdevice.ra_y * (self.simdevice.patch[i][j + 1][k].ez - self.simdevice.patch[i][j][k].ez))
                        if self.simdevice.patch[i][j][k].materiau.patchValue == Mat.PML.patchValue:
                            self.simdevice.patch[i][j][k].ihx = self.simdevice.patch[i][j][k].ihx + self.simdevice.curl_e
                        else:
                            self.simdevice.patch[i][j][k].ihx = 0
                        self.simdevice.patch[i][j][k].hx = self.simdevice.fj3[j] * self.simdevice.fk3[k] * self.simdevice.patch[i][j][k].hx+ self.simdevice.fj2[j] * self.simdevice.fk2[k] * 0.5 * (self.simdevice.curl_e + (self.simdevice.fi1[i] * self.simdevice.patch[i][j][k].ihx))
#calcul
    def calculateHy(self):
        for i in range(self.tailleX-1):
            for j in range(self.tailleY-1):
                for k in range(self.tailleZ-1):
                        self.simdevice.curl_e = (self.simdevice.ra_x * (self.simdevice.patch[i + 1][j][k].ez - self.simdevice.patch[i][j][k].ez) - self.simdevice.patch[i][j][k + 1].ex + self.simdevice.patch[i][j][k].ex)
                        if self.simdevice.patch[i][j][k].materiau.patchValue == Mat.PML.patchValue:
                            self.simdevice.patch[i][j][k].ihy = self.simdevice.patch[i][j][k].ihy + self.simdevice.curl_e
                        else:
                            self.simdevice.patch[i][j][k].ihy = 0
                        self.simdevice.patch[i][j][k].hy = self.simdevice.fi3[i] * self.simdevice.fk3[k] * self.simdevice.patch[i][j][k].hy + self.simdevice.fi2[i] * self.simdevice.fk2[k] * 0.5 * (self.simdevice.curl_e + (self.simdevice.fj1[j] * self.simdevice.patch[i][j][k].ihy))
#calcul
    def calculateHz(self):
        for i in range(self.tailleX-1):
            for j in range(self.tailleY-1):
                for k in range(self.tailleZ-1):
                        self.simdevice.curl_e = (self.simdevice.ra_y * (self.simdevice.patch[i][j + 1][k].ex - self.simdevice.patch[i][j][k].ex) - self.simdevice.ra_x * (self.simdevice.patch[i + 1][j][k].ey - self.simdevice.patch[i][j][k].ey))
                        if self.simdevice.patch[i][j][k].materiau.patchValue == Mat.PML.patchValue:
                            self.simdevice.patch[i][j][k].ihz = self.simdevice.patch[i][j][k].ihz + self.simdevice.curl_e
                        else:
                            self.simdevice.patch[i][j][k].ihz = 0
                        self.simdevice.patch[i][j][k].hz = self.simdevice.fi3[i] *self.simdevice.fj3[j] * self.simdevice.patch[i][j][k].hz + self.simdevice.fi2[i] * self.simdevice.fj2[j] * 0.5 * (self.simdevice.curl_e + (self.simdevice.fk1[k] * self.simdevice.patch[i][j][k].ihz))
    #ecrit dans un fichier le champ Ez à une certaine couche
    def printToFile(self,couche , nomfichier):
        f=open(nomfichier+".txt","w")
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                f.write("%.3f "% self.simdevice.patch[i][j][couche].ez)
            f.write("\n")
        f.close()

#ecrit l'impulsion dans le patch
    def input(self,T,position):
        self.simdevice.patch[position[0]][position[1]][position[2]].dz = self.sourcePulse(150.0,25.0,T)
        


    def updateSimD(self):
        self.calculateDx()
        self.calculateDy()
        self.calculateDz()

    def updateSimE(self):
        self.calculateE()
    
    def updateSimH(self):
        self.calculateHx()
        self.calculateHy()
        self.calculateHz()

