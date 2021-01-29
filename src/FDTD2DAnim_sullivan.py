import numpy as np

IE=60
JE=60

def main():

    #definition des tableaux #attention ceux sont des floats
    ga=np.ones((IE,JE))
    dz=np.zeros((IE,JE))
    ez=np.zeros((IE,JE))
    hx=np.zeros((IE,JE))
    hy=np.zeros((IE,JE))

    l, n, i, j, ic, jc, nsteps, npml = 0,0,0,0,0,0,0,0 #int

    #float
    ddx, dt, T, epsz, pi, epsilon, sigma, eaf = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
    xn, xxn, xnum, xd, curl_e = 0.0,0.0,0.0,0.0,0.0
    t0, spread, pulse = 0.0,0.0,0.0

    gi2, gi3 , gj2,gj3 = np.ones(IE),np.ones(IE),np.ones(JE),np.ones(IE)
    fi1,fi2,fi3,fj1,fj2,fj3 = np.zeros(IE),np.ones(IE),np.ones(JE),np.zeros(JE),np.ones(JE),np.ones(JE)
    ihx,ihy=np.zeros((IE,JE)),np.zeros((IE,JE))

    #pas de FILE *fp, *fopen(); car ouverture à la volée

    ic = int(IE/2)-5
    jc = int(JE/2)-5
    ddx = 0.01 #taille des cellules
    dt = ddx / 6e8 #pas de temps
    epsz = 8.8e-12
    pi = 3.14159


    #INITIALISATION DES TABLEAUX

    print(ga)

    #CALCUL DES PARAMETRES DU PML

    print("Number of PML cells -->")
    npml= int(input())

    for i in np.arange(npml+1):
        xnum = npml - i # pas une somme inversé mais plutot un suite arithmétique
        xd = npml
        xxn = xnum / xd
        xn = 0.33 * pow(xxn, 3.0)
        print('i= '+ str(i)+'  xxn= '+ str(xxn)+'  xn= '+ str(xn))
        gi2[i] = 1.0 / (1.0 + xn) #parametre PML (voir formules)
        gi2[IE - 1 - i] = 1.0 / (1.0 + xn)
        gi3[i] = (1.0 - xn) / (1.0 + xn)
        gi3[IE - i - 1] = (1.0 - xn) / (1.0 + xn)
        xxn = (xnum - 0.5) / xd
        xn = 0.25 * pow(xxn, 3.0)
        fi1[i] = xn; #parametre PML (voir formules)
        fi1[IE - 2 - i] = xn
        fi2[i] = 1.0 / (1.0 + xn)
        fi2[IE - 2 - i] = 1.0 / (1.0 + xn)
        fi3[i] = (1.0 - xn) / (1.0 + xn)
        fi3[IE - 2 - i] = (1.0 - xn) / (1.0 + xn)

    for j in np.arange(npml+1):
        xnum = npml - j
        xd = npml
        xxn = xnum / xd
        xn = 0.33 * pow(xxn, 3.0)
        print('j= '+ str(j)+'  xxn= '+ str(xxn)+'  xn= '+ str(xn))
        gj2[j] = 1.0 / (1.0 + xn)
        gj2[JE - 1 - j] = 1.0 / (1.0 + xn)
        gj3[j] = (1.0 - xn) / (1.0 + xn)
        gj3[JE - j - 1] = (1.0 - xn) / (1.0 + xn)
        xxn = (xnum - 0.5) / xd
        xn = 0.25 * pow(xxn, 3.0)
        fj1[j] = xn
        fj1[JE - 2 - j] = xn
        fj2[j] = 1.0 / (1.0 + xn)
        fj2[JE - 2 - j] = 1.0 / (1.0 + xn)
        fj3[j] = (1.0 - xn) / (1.0 + xn)
        fj3[JE - 2 - j] = (1.0 - xn) / (1.0 + xn)
    

    print("gi+fi")
    for i in np.arange(IE):
        print('i= '+ str(i)+'  gi2= '+ str(gi2[i])+'  gi3= '+ str(gi3[i]))
        print('i= '+ str(i)+'  fi1= '+ str(fi1[i])+'  fi2= '+ str(fi2[i])+'  fi3= '+ str(fi3[i]))

    print("gj+fj")
    for j in np.arange(JE):
        print('i= '+ str(j)+'  gj2= '+ str(gj2[j])+'  gj3= '+ str(gj3[j]))
        print('i= '+ str(j)+'  fj1= '+ str(fj1[j])+'  fj2= '+ str(fj2[j])+'  fj3= '+ str(fj3[j]))

    """t0 = 40.0 #sinus
    spread = 15.0"""
    t0 = 20.0 #exp
    spread = 6.0
    T = 0
    nsteps = 1
    fp = open("Data2D\Ez2DpyGauss.data","w")
    while nsteps>0:
        
        print(" nsteps --> ")
        nsteps= int(input())
        print("nsteps = "+str(nsteps))

        for n in np.arange(1,(nsteps+1)): #+1 car <= (for (n = 1; n <= nsteps; n++))
            T = T + 1
            
            
            #---------- DEBUT DE LA BOUCLE PRINCIPALE ----------


            #Calcul de Dz

            for j in np.arange(1,IE): #IE ? 1?
                for i in np.arange(1,IE):
                    dz[i][j] = gi3[i] * gj3[j] * dz[i][j] + gi2[i] * gj2[j] * 0.5 * (hy[i][j] - hy[i - 1][j] - hx[i][j] + hx[i][j - 1])

            #source Sinusoidal
            #pulse = np.sin(2 * pi * 1500 * 1e6 * dt * T)

            #source Gaussienne
            pulse = np.exp(-0.5 * (pow((t0 - T) / spread, 2.0)))

            dz[ic][jc]=pulse

            #Calcul Ez

            for j in np.arange(0,JE): #0 ?
                for i in np.arange(0,IE):
                    ez[i][j] = ga[i][j] * dz[i][j]
            print('T= '+ str(T)+'  ez= '+ str(ez[ic][jc])) #champ ez à la source

            #Mise à 0 de EZ sur les des bords, cela fait partie de la PML
            #Bizarre ??? j>JE-1 ça fait que j ne vas que jusqu'a 58 soit JE-2
            
            for j in np.arange(0,(JE-1)):
                ez[0][j] = 0.0
                ez[IE - 1][j] = 0.0
            
            for i in np.arange(0,IE-1): 
                ez[i][0] = 0.0
                ez[i][JE - 1] = 0.0

            #calcul de Hx

            for j in np.arange(0,JE-1):
                for i in np.arange(0,IE):
                    curl_e = ez[i][j] - ez[i][j + 1]        #dy
                    ihx[i][j] = ihx[i][j] + fi1[i] * curl_e #intégrale donné dans le livre vers la fin de la PML
                    hx[i][j] = fj3[j] * hx[i][j] + fj2[j] * 0.5 * (curl_e + ihx[i][j])
            
            #calcul de Hy

            for j in np.arange(0,JE-1):
                for i in np.arange(0,IE-1):
                    curl_e = ez[i + 1][j] - ez[i][j] #dx
                    ihy[i][j] = ihy[i][j] + fj1[j] * curl_e
                    hy[i][j] = fi3[i] * hy[i][j] + fi2[i] * 0.5*(curl_e + ihy[i][j])
        
            for j in np.arange(JE):
                for i in np.arange(IE):
                    fp.write("%.3f " % ez[i][j])
                fp.write(" \n")
        #Fin boucle principale


        print("T=  "+str(T))
    fp.close()
        
    """        #ecriture de EZ
    fp = open("../Data2D/Ez2D1pointpy","w")
    for j in np.arange(JE):
        for i in np.arange(IE):
            fp.write("%.3f " % ez[i][j])
        fp.write(" \n")

    fp.close()
    print("T=  "+str(T))"""



main()