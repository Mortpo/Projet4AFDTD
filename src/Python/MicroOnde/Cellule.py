import numpy as np
import Materiau as Mat


#Definie les cellules et leurs valeurs propres
class Cellule:
    
    def __init__(self,materiau:Mat):
        self.ex,self.ey,self.ez = 0.0,0.0,0.0
        self.dx,self.dy,self.dz = 0.0,0.0,0.0
        self.hx,self.hy,self.hz = 0.0,0.0,0.0
        self.idx,self.idy,self.idz = 0.0,0.0,0.0 #pas opti utile en pml sur les bords uniquement
        self.ihx,self.ihy,self.ihz = 0.0,0.0,0.0
        #pas opti car déja compris dans materiau
        self.gax = materiau.conductiviteX
        self.gay = materiau.conductiviteY
        self.gaz = materiau.conductiviteZ
        self.materiau = materiau
