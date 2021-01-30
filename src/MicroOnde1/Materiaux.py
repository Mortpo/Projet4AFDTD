class Materiaux:

    def __init__(self,conductivite,rgbValue,patchValue):
        self.conductiviteX=conductivite[0]
        self.conductiviteY=conductivite[1]
        self.conductiviteZ=conductivite[2]
        self.rgbValue=rgbValue
        self.patchValue=patchValue

#def materiaux
isolant = Materiaux([1/2.2,1/2.2,1/2.2],[255,255,255],0)
patch = Materiaux([0,0,1],[0,0,0],1)
freeSpace= Materiaux([1,1,1],[0,0,255],3) #Air/vide
PML = Materiaux([1,1,1],[255,0,0],4) #couche de PML ; QUID de la conductivité ? Surement conductivité de l'air on prend sur des cellules d'air ?

materiauxType = [patch,isolant]