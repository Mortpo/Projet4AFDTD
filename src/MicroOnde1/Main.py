import Antenne as Ant
import SimDevTestInfo as DI
import Materiau as Mat
import Simulation as Sim
from numba import jit

rawPatch = Ant.Antenne("src\MicroOnde1\Dessus.png",0.002,0.002,0.002,1)
for i in range(2):
    rawPatch.AddLayer(rawPatch.loadLayerFromPicture("src\MicroOnde1\dielectrique.png"))
rawPatch.AddLayer(rawPatch.loadLayerFromPicture("src\MicroOnde1\Dessus.png"))

'''device = DI.DeviceInfo(rawPatch)
print(device.testCellSize())

simulation = Sim.Simulation(device)

nsteps = 1
T=0
while nsteps>0:
    print("nsteps --> ")
    nsteps = int(input())

    for n in range(1,nsteps):
        T+=1
        print(T)
        simulation.input(T,(36,36,20))
        print(device.patch[36][36][20].ez)
        simulation.updateSim()
    simulation.printToFile(20,"testSim")'''