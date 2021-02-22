import Antenne as Ant
import SimDevTestInfo as DI
import Materiau as Mat
import Simulation as Sim
from numba import jit

rawPatch = Ant.Antenne("src\MicroOnde1\Dessus.png",0.01,0.01,0.01,1)
for i in range(2):
    rawPatch.AddLayer(rawPatch.loadLayerFromPicture("src\MicroOnde1\dielectrique.png"))
rawPatch.AddLayer(rawPatch.loadLayerFromPicture("src\MicroOnde1\Dessus.png"))

device = DI.DeviceInfo(rawPatch)
print(device.testCellSize())

simulation = Sim.Simulation(device)

nsteps = 1
T=0
while nsteps>0:
    print("nsteps --> ")
    nsteps = int(input()) #test valeurs PML

    for n in range(1,nsteps):
        T+=1
        print(T)

        print(device.patch[20][20][15].ez)
        print(device.patch[20][20][15].dz)
        print(device.patch[20][20][15].hx)#pb
        print(device.patch[20][20][15].hy)#pb
        print(device.patch[20][20][15].hz)#pb
        print()

        print(device.patch[20][20][15].ez)
        print(device.patch[32][32][15].ez)
        print(device.patch[40][40][15].ez)
        simulation.EzInc()
        simulation.calculateDx()
        simulation.calculateDy()
        simulation.DyBuffer()
        simulation.calculateDz()
        simulation.DzBuffer()

        for i in range(simulation.tailleX):
            for k in range(simulation.tailleZ):
                simulation.input(T,(i,12,k))

        simulation.calculateE()
        simulation.HxInc()
        simulation.calculateHx()
        simulation.hxBuffer()
        simulation.calculateHy()
        simulation.hyBuffer()
        simulation.calculateHz()
       

    simulation.printToFile(15,"testSim15")
