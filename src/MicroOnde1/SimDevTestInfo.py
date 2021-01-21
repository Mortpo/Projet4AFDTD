import Antenne
import numpy as np

class DeviceInfo:


    def __init__(self,rawPatch:Antenne):
        self.ra_x
        self.ra_y
        self.ra_z
        self.celerite = 3e8
        self.pi = np.pi
        #self.timeStep # = ddz/6e8?
        self.cellPatch
        self.nbPMLlayer
        self.cellSizeX
        self.cellSizeY
        self.cellSizeZ
        self.timeStep
        self.curl_h,self.curl_e
        self.gi1,self.gi2,self.gi3
        self.gj1,self.gj2,self.gj3
        self.gk1,self.gk2,self.gk3
        self.fi1,self.fi2,self.fi3
        self.fj1,self.fj2,self.fj3
        self.fk1,self.fk2,self.fk3


    def setCellSizeX(self,cellSize):
        if testCellSize(self.timeStep,cellSize,self.cellSizeY,self.cellSizeZ):
            self.cellSizeX = cellSize
        else:
            raise Exception("bad size X")
    
    def setCellSizeY(self,cellSize):
        if testCellSize(self.timeStep,self.cellSizeX,cellSize,self.cellSizeZ):
            self.cellSizeY = cellSize
        else:
            raise Exception("bad size Y")

    def setCellSizeZ(self,cellSize):
        if testCellSize(self.timeStep,self.cellSizeX,self.cellSizeY,cellSize):
            self.cellSizeZ = cellSize
        else:
            raise Exception("bad size Z")
    
    def settimeStep(self,timeStep):
        if testCellSize(timeStep,self.cellSizeX,self.cellSizeY,self.cellSizeZ):
            self.timeStep = timeStep
        else:
            raise Exception("bad timeStep")

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
    
    def convertRawPatchToCell(self,rawPatch:Antenne):
        return patch