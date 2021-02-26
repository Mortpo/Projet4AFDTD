#définie les materiaux et fait la liaison entre image et patch dans la memoire
class Materiau:

    def __init__(self,conductivite,rgbValue,patchValue):
        self.conductiviteX=conductivite[0]
        self.conductiviteY=conductivite[1]
        self.conductiviteZ=conductivite[2]
        self.rgbValue=rgbValue
        self.patchValue=patchValue

#definition des materiaux
eps_sub=2.2
isolant = Materiau([1/eps_sub,1/eps_sub,1/eps_sub],[255,255,255],0)
patch = Materiau([0,0,1],[0,0,0],1)
freeSpace= Materiau([1,1,1],[0,0,255],3) #Air/vide
PML = Materiau([1,1,1],[255,0,0],4) #couche de PML ; QUID de la conductivité ? Surement conductivité de l'air on prend sur des cellules d'air ?

MateriauType = [patch,isolant]