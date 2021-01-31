import Antenne
import numpy as np
import Materiau as Mat
import Cellule
import SimDevTestInfo as Dev
from numba import jit
class Simulation: #potentiel pb si cell non pml genre elle devient pml a cause des calcul de idhxyz

    def __init__(self,device:Dev.DeviceInfo):
        self.simdevice = device
        self.tailleX,self.tailleY,self.tailleZ = self.simdevice.patch.shape
        print(self.simdevice.patch.shape)

    def sourcePulse(self,t0,spread,T):
        pulse = np.exp(-0.5 * (pow((t0 - T) / spread, 2.0)))
        return pulse
    
    def calculateDx(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.curl_h = (self.simdevice.ra_y * (self.simdevice.patch[i][j][k].hz - self.simdevice.patch[i][j - 1][k].hz) - self.simdevice.patch[i][j][k].hy + self.simdevice.patch[i][j][k - 1].hy)
                        self.simdevice.patch[i][j][k].idx = self.simdevice.patch[i][j][k].idx + self.simdevice.curl_h
                        self.simdevice.patch[i][j][k].dx = self.simdevice.gj3[j] * self.simdevice.gk3[k] * self.simdevice.patch[i][j][k].dx + self.simdevice.gj2[j] * self.simdevice.gk2[k] * 0.5 * (self.simdevice.curl_h + self.simdevice.gi1[i] * self.simdevice.patch[i][j][k].idx)

    def calculateDy(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.curl_h = (self.simdevice.patch[i][j][k].hx - self.simdevice.patch[i][j][k - 1].hx - self.simdevice.ra_x * (self.simdevice.patch[i][j][k].hz - self.simdevice.patch[i - 1][j][k].hz))
                        self.simdevice.patch[i][j][k].idy = self.simdevice.patch[i][j][k].idy + self.simdevice.curl_h
                        self.simdevice.patch[i][j][k].dy = self.simdevice.gi3[i] * self.simdevice.gk3[k] * self.simdevice.patch[i][j][k].dy + self.simdevice.gi2[i] * self.simdevice.gk2[k] * 0.5 * (self.simdevice.curl_h + self.simdevice.gj1[j] * self.simdevice.patch[i][j][k].idy)
    
    def calculateDz(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.curl_h = (self.simdevice.ra_x * (self.simdevice.patch[i][j][k].hy - self.simdevice.patch[i - 1][j][k].hy) - self.simdevice.ra_y * (self.simdevice.patch[i][j][k].hx - self.simdevice.patch[i][j - 1][k].hx))
                        self.simdevice.patch[i][j][k].idz = self.simdevice.patch[i][j][k].idz + self.simdevice.curl_h
                        self.simdevice.patch[i][j][k].dz = self.simdevice.gi3[i] * self.simdevice.gj3[j] * self.simdevice.patch[i][j][k].dz + self.simdevice.gi2[i] * self.simdevice.gj2[j] * 0.5 * (self.simdevice.curl_h + self.simdevice.gk1[k] * self.simdevice.patch[i][j][k].idz)
    
    def calculateE(self):
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                for k in range(self.tailleZ):
                        self.simdevice.patch[i][j][k].ex = self.simdevice.patch[i][j][k].gax * self.simdevice.patch[i][j][k].dx
                        self.simdevice.patch[i][j][k].ey = self.simdevice.patch[i][j][k].gay * self.simdevice.patch[i][j][k].dy
                        self.simdevice.patch[i][j][k].ez = self.simdevice.patch[i][j][k].gaz * self.simdevice.patch[i][j][k].dz

    def calculateHx(self):
        for i in range(self.tailleX-1):
            for j in range(self.tailleY-1):
                for k in range(self.tailleZ-1):
                        self.simdevice.curl_e = (self.simdevice.patch[i][j][k + 1].ey - self.simdevice.patch[i][j][k].ey - self.simdevice.ra_y * (self.simdevice.patch[i][j + 1][k].ez - self.simdevice.patch[i][j][k].ez))
                        self.simdevice.patch[i][j][k].ihx = self.simdevice.patch[i][j][k].ihx + self.simdevice.curl_e
                        self.simdevice.patch[i][j][k].hx = self.simdevice.fj3[j] * self.simdevice.fk3[k] * self.simdevice.patch[i][j][k].hx+ self.simdevice.fj2[j] * self.simdevice.fk2[k] * 0.5 * (self.simdevice.curl_e + self.simdevice.fi1[i] * self.simdevice.patch[i][j][k].ihx)

    def calculateHy(self):
        for i in range(self.tailleX-1):
            for j in range(self.tailleY-1):
                for k in range(self.tailleZ-1):
                        self.simdevice.curl_e = (self.simdevice.ra_x * (self.simdevice.patch[i + 1][j][k].ez - self.simdevice.patch[i][j][k].ez) - self.simdevice.patch[i][j][k + 1].ex + self.simdevice.patch[i][j][k].ex)
                        self.simdevice.patch[i][j][k].ihy = self.simdevice.patch[i][j][k].ihy + self.simdevice.curl_e
                        self.simdevice.patch[i][j][k].hy = self.simdevice.fi3[i] * self.simdevice.fk3[k] * self.simdevice.patch[i][j][k].hy + self.simdevice.fi2[i] * self.simdevice.fk2[k] * 0.5 * (self.simdevice.curl_e + self.simdevice.fj1[j] * self.simdevice.patch[i][j][k].ihy)
    
    def calculateHz(self):
        for i in range(self.tailleX-1):
            for j in range(self.tailleY-1):
                for k in range(self.tailleZ-1):
                        self.simdevice.curl_e = (self.simdevice.ra_y * (self.simdevice.patch[i][j + 1][k].ex - self.simdevice.patch[i][j][k].ex) - self.simdevice.ra_x * (self.simdevice.patch[i + 1][j][k].ey - self.simdevice.patch[i][j][k].ey))
                        self.simdevice.patch[i][j][k].ihz = self.simdevice.patch[i][j][k].ihz + self.simdevice.curl_e
                        self.simdevice.patch[i][j][k].hz = self.simdevice.fi3[i] *self.simdevice.fj3[j] * self.simdevice.patch[i][j][k].hz + self.simdevice.fi2[i] * self.simdevice.fj2[j] * 0.5 * (self.simdevice.curl_e + self.simdevice.fk1[k] * self.simdevice.patch[i][j][k].ihz)
    
    def printToFile(self,couche , nomfichier):
        f=open(nomfichier,"w")
        for i in range(self.tailleX):
            for j in range(self.tailleY):
                f.write("%.3f "% self.simdevice.patch[i][j][couche].ez)
            f.write("\n")
        f.close()

    def input(self,T,position):
        self.simdevice.patch[position[0]][position[1]][position[2]].ez = self.sourcePulse(150.0,25.0,T)
        


    def updateSim(self):
        self.calculateDx()
        self.calculateDy()
        self.calculateDz()
        self.calculateE()
        self.calculateHx()
        self.calculateHy()
        self.calculateHz()


