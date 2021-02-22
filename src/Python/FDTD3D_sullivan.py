import numpy as np




#PB VALEUR QUI APRTENT A L'INFINI

def main():

    IE =62
    JE = 120
    KE = 14
    ia = 14
    ja =15
    ka =7
    NFREQS =3
    ktop=2

    dx=dy=dz = np.zeros(((IE,JE,KE)))
    ex=ey=ez = np.zeros(((IE,JE,KE)))
    hx=hy=hz = np.zeros(((IE,JE,KE)))
    gax=gay=gaz = np.ones(((IE,JE,KE)))
    l= m= n= i= j= k= ic= jc= kc= nsteps= n_pml = 0
    ddz= ra_x= ra_y= dt= T= epsz= muz= pi= eaf= npml = 0.0
    ib=jb=kb = 0
    xn=xxn=xnim=xd = 0.0
    t0=spread=pulse=0.0
    #Pas d'ouverture de fichier
    ez_inc=hx_inc= np.zeros(JE)

    idxl=idxh=ihxl=ihxh = np.zeros(((ia,JE,KE)))
    idyl=idyh=ihyl=ihyh = np.zeros(((IE,ja,KE)))
    idzl=idzh=ihzl=ihzh = np.zeros(((IE,JE,ka)))
    ixh=jyh=kzh=0

    gi1=gi2=gi3=np.zeros(IE)
    gj1=gj2=gj3=np.zeros(JE)
    gk1=gk2=gk3=np.zeros(KE)
    fi1=fi2=fi3=np.zeros(IE)
    fj1=fj2=fj3=np.zeros(JE)
    fk1=fk2=fk3=np.zeros(KE)

    curl_h=curl_e=0.0

    istart=iend=k_ref=jebd=i_ref=0
    j_patch_st=j_patch_end=j_ref=0
    i_patch_st=i_patch_end=0
    eps_sub=half_wv=0.0
    shape = np.zeros((IE,KE))

    ic=IE/2
    jc=JE/2
    kc=KE/2
    ib = IE - ia - 1
    jb = JE - ja - 1
    kb = KE - ka -1

    i_patch_st=ia+5
    i_patch_end=i_patch_st+31
    j_patch_end=jb-5
    j_patch_st=j_patch_end-39
    j_ref=j_patch_st-30
    k_ref=ktop-1

    pi = 3.14159
    epsz = 8.8e-12
    muz = 4 * pi * 1.0e-7
    ddz = .265e-3
    ra_y = .6625
    ra_x = .6812
    dt = ddz/6e8

    print("ddz : %12.5e  dt : %12.5e"% (ddz, dt))

    #CALCUL DES PARAMETRE DE LA PML
    #
    for i in  range(IE):
        gi1[i]=0.0
        fi1[i]=0.0
        gi2[i]=1.0
        fi2[i]=1.0
        gi3[i]=1.0
        fi3[i]=1.0

    for j in  range(JE):
        gj1[j]=0.0
        fj1[j]=0.0
        gj2[j]=1.0
        fj2[j]=1.0
        gj3[j]=1.0
        fj3[j]=1.0
    
    for k in  range(KE):
        gk1[k]=0.0
        fk1[k]=0.0
        gk2[k]=1.0
        fk2[k]=1.0
        gk3[k]=1.0
        fk3[k]=1.0
    
    print("Number of PML cells -->")
    npml= int(input())
    print("%f"%npml)
    n_pml=npml

    for i in  range(n_pml):
        xxn=(npml-i)/npml
        xn = 0.33*pow(xxn,3.0)
        print("%d xn = %8.4f  xn = %8.4f"%(i,xxn,xn))
        fi1[i]= xn
        fi1[IE-i-1]=xn
        gi2[i]= 1.0/(1.0+xn)
        gi2[IE-i-1] = 1.0/(1.0+xn)
        gi3[i]=(1.0-xn)/(1.0+xn)
        gi3[IE-i-1] = (1.0-xn)/(1.0+xn)
        xxn=(npml-i-0.5)/npml
        xn = 0.33*pow(xxn,3.0)
        gi1[i]=xn
        gi1[IE-i-2]=xn
        fi2[i]=1.0/(1.0+xn)
        fi2[IE-i-2]=1.0/(1.0+xn)
        fi3[i]=(1.0-xn)/(1.0+xn)
        fi3[IE-i-2]=(1.0-xn)/(1.0+xn)

    for j in  range(n_pml):
        xxn=(npml-j)/npml
        xn = 0.33*pow(xxn,3.0)
        fj1[j]= xn
        fj1[JE-j-1]=xn
        gj2[j]= 1.0/(1.0+xn)
        gj2[JE-j-1] = 1.0/(1.0+xn)
        gj3[j]=(1.0-xn)/(1.0+xn)
        gj3[JE-j-1] = (1.0-xn)/(1.0+xn)
        xxn=(npml-j-0.5)/npml
        xn = 0.33*pow(xxn,3.0)
        gj1[j]=xn
        gj1[JE-j-2]=xn
        fj2[j]=1.0/(1.0+xn)
        fj2[JE-j-2]=1.0/(1.0+xn)
        fj3[j]=(1.0-xn)/(1.0+xn)
        fj3[JE-j-2]=(1.0-xn)/(1.0+xn)

        
    for k in  range(n_pml): #PML VERS k=0 p112 livre 124 lecteur
        xxn=(npml-k)/npml
        xn = 0.33*pow(xxn,3.0)
        fk1[k]= xn
        fk1[KE-k-1]=xn
        gk2[k]= 1.0/(1.0+xn)
        gk2[KE-k-1] = 1.0/(1.0+xn)
        gk3[k]=(1.0-xn)/(1.0+xn)
        gk3[KE-k-1] = (1.0-xn)/(1.0+xn)
        xxn=(npml-k-0.5)/npml
        xn = 0.33*pow(xxn,3.0)
        gk1[k]=xn
        gk1[KE-k-2]=xn
        fk2[k]=1.0/(1.0+xn)
        fk2[KE-k-2]=1.0/(1.0+xn)
        fk3[k]=(1.0-xn)/(1.0+xn)
        fk3[KE-k-2]=(1.0-xn)/(1.0+xn)
        



    #Constante dielectrique du matériau

    eps_sub=2.2
    print("eps_sub : %f"% eps_sub)

    for j in  range(JE):
        for i in  range(IE):
            for k in  range((ktop+1)):
                gax[i][j][k] = (1.0 / eps_sub)
                gay[i][j][k] = (1.0 / eps_sub)
                gaz[i][j][k] = (1.0 / eps_sub)
    
    for i in  range(1,(IE-1)):
        for j in   range(1,(JE-1)):
            k=0
            gax[i][j][k] = 0
            gay[i][j][k] = 0
    
    istart = ia + 6
    iend = istart + 6
    i_ref = istart + int((iend - istart)/2)
    print("istart : %d  iend : %d  i_ref : %d"% (istart, iend, i_ref))

    half_wv = (iend - istart)/2.
    print("half_wv = %5.2f"% half_wv)

    for i in  range(istart,iend+1):
        for k in  range(ktop+1):
            shape[i][k]=1.0
    

    #ajout du conducteur jusqu'au patch à ktop+1

    for j in  range(1,(j_patch_st+1)): 
        for i in  range(istart,iend):
            gax[i][j][ktop + 1] = 0.0
        for i in  range(istart,iend):
            gay[i][j][ktop + 1] = 0.0

    for j in  range(j_patch_st,(j_patch_end+1)):
        for i in  range((ia+1),ib):
            gax[i][j][ktop + 1] = 0.0
        for i in  range((ia+1),ib):
            gay[i][j][ktop + 1] = 0.0
    
    t0=150.0
    spread=25.0
    print("Pulse width is " +str( spread * dt))
    T = 0
    nsteps = 1

    fpt = open("Data3D/Timeplane", "w")

    while nsteps > 0:
        print("nsteps --> ")
        nsteps = int(input())
        print("nsteps : %d"% nsteps)

        for n in  range(1,nsteps):
            T=T+1

            #Debut de la boucle principale

            for j in  range(1,JE):
                ez_inc[j] = gj3[j] * ez_inc[j] + gj2[j] * (0.5 * ra_y / eps_sub) * (hx_inc[j - 1] - hx_inc[j])
            
            #Source

            pulse = np.exp(-0.5*(pow((t0-T)/spread,2.0)))
            ez_inc[ja-2]=pulse
            print("T : %4.0f  Pulse : %6.2e"% (T, pulse))

            #Calcul du champ Dx

            for i in  range(1,ia):
                for j in  range(1,JE):
                    for k in  range(1,KE):
                        curl_h = (ra_y * (hz[i][j][k] - hz[i][j - 1][k]) - hy[i][j][k] + hy[i][j][k - 1])
                        idxl[i][j][k] = idxl[i][j][k] + curl_h
                        dx[i][j][k] = gj3[j] * gk3[k] * dx[i][j][k] + gj2[j] * gk2[k] * 0.5 * (curl_h + gi1[i] * idxl[i][j][k])

            for i in  range(ia,(ib+1)):
                for j in  range(1,JE):
                    for k in  range(1,KE):
                         curl_h = (ra_y * (hz[i][j][k] - hz[i][j - 1][k]) - hy[i][j][k] + hy[i][j][k - 1])
                         dx[i][j][k] = gj3[j] * gk3[k] * dx[i][j][k] + gj2[j] * gk2[k] * 0.5 * curl_h
            
            for i in  range((ib+1),IE):
                ixh = i - ib - 1
                for j in  range(1,JE):
                    for k in  range(1,KE):
                        curl_h = (ra_y * (hz[i][j][k] - hz[i][j - 1][k]) - hy[i][j][k] + hy[i][j][k - 1])
                        idxh[ixh][j][k] = idxh[ixh][j][k] + curl_h
                        dx[i][j][k] = gj3[j] * gk3[k] * dx[i][j][k] + gj2[j] * gk2[k] * 0.5 * (curl_h + gi1[i] * idxh[ixh][j][k])

            #Calcul du champ Dy
            for i in  range(1,IE):
                for j in  range(1,ja):
                    for k in  range(1,KE):
                        curl_h = (hx[i][j][k] - hx[i][j][k - 1] - ra_x * (hz[i][j][k] - hz[i - 1][j][k]))
                        idyl[i][j][k] = idyl[i][j][k] + curl_h
                        dy[i][j][k] = gi3[i] * gk3[k] * dy[i][j][k] + gi2[i] * gk2[k] * 0.5 * (curl_h + gj1[j] * idyl[i][j][k])

            for i in  range(1,IE):
                for j in  range(ja,(jb+1)):
                    for k in  range(1,KE):
                        curl_h = (hx[i][j][k] - hx[i][j][k - 1] - ra_x * (hz[i][j][k] - hz[i - 1][j][k]))
                        dy[i][j][k] = gi3[i] * gk3[k] * dy[i][j][k] + gi2[i] * gk2[k] * 0.5 * curl_h
            
            for i in  range(1,IE):
                for j in  range((jb+1),JE):
                    jyh=j - jb - 1
                    for k in  range(1,KE):
                        curl_h = (hx[i][j][k] - hx[i][j][k - 1] - ra_x * (hz[i][j][k] - hz[i - 1][j][k]))
                        idyh[i][jyh][k] = idyh[i][jyh][k] + curl_h
                        dy[i][j][k] = gi3[i] * gk3[k] * dy[i][j][k] + gi2[i] * gk2[k] * 0.5 * (curl_h + gj1[j] * idyh[i][jyh][k])

            #Calcul du champ Dz

            for i in  range(1,IE):
                for j in  range(1,JE):
                    for k in  range(0,ka):
                        curl_h = (ra_x * (hy[i][j][k] - hy[i - 1][j][k]) - ra_y * (hx[i][j][k] - hx[i][j - 1][k]))
                        idzl[i][j][k] = idzl[i][j][k] + curl_h
                        dz[i][j][k] = gi3[i] * gj3[j] * dz[i][j][k] + gi2[i] * gj2[j] * 0.5 * (curl_h + gk1[k] * idzl[i][j][k])

            for i in  range(1,IE):
                for j in  range(1,JE):
                    for k in  range(ka,(kb+1)):
                        curl_h = (ra_x * (hy[i][j][k] - hy[i - 1][j][k]) - ra_y * (hx[i][j][k] - hx[i][j - 1][k]))
                        dz[i][j][k] = gi3[i] * gj3[j] * dz[i][j][k] + gi2[i] * gj2[j] * 0.5 * curl_h

            for i in  range(1,IE):
                for j in  range(1,JE):
                    for k in  range((kb+1),KE):
                        kzh = k - kb - 1
                        curl_h = (ra_x * (hy[i][j][k] - hy[i - 1][j][k]) - ra_y * (hx[i][j][k] - hx[i][j - 1][k]))
                        idzh[i][j][kzh] = idzh[i][j][kzh] + curl_h
                        dz[i][j][k] = gi3[i] * gj3[j] * dz[i][j][k] + gi2[i] * gj2[j] * 0.5 * (curl_h + gk1[k] * idzl[i][j][kzh])

            #Incident Dz

            for i in  range(istart,(iend+1)):
                for k in  range((ktop+1)):
                    dz[i][ja][k] = dz[i][ja][k] + (0.5 / eps_sub) * shape[i][k] * hx_inc[ja - 1]
            
            # Calcul de E depuis le champ D
            # Ex et Ey sont à 0 pour k=0

            for i in  range(1,(IE-1)):
                for j in  range(1,(JE-1)):
                    for k in  range(1,(KE-1)):
                        ex[i][j][k] = gax[i][j][k] * dx[i][j][k]
                        ey[i][j][k] = gay[i][j][k] * dy[i][j][k]
                        ez[i][j][k] = gaz[i][j][k] * dz[i][j][k]

            #Ecriture des données temporelles dans le port d'entré

            fpt.write( "%.4f \n"% ez[i_ref][j_ref][k_ref]) #Pb de calcul dans ez

            for j in  range((JE-1)):
                hx_inc[j] = fj3[j] * hx_inc[j] + 0.5 * fj2[j] * (ez_inc[j] - ez_inc[j + 1])

            #Calcul de Hx

            for i in  range(ia):
                for j in  range((JE-1)):
                    for k in  range((KE-1)):
                        curl_e = (ey[i][j][k + 1] - ey[i][j][k] - ra_y * (ez[i][j + 1][k] - ez[i][j][k]))
                        ihxl[i][j][k] = ihxl[i][j][k] + curl_e
                        hx[i][j][k] = fj3[j] * fk3[k] * hx[i][j][k] + fj2[j] * fk2[k] * 0.5 * (curl_e + fi1[i] * ihxl[i][j][k])


            for i in  range(ia,(ib+1)):
                for j in  range((JE-1)):
                    for k in  range((KE-1)):
                        curl_e = (ey[i][j][k + 1] - ey[i][j][k] - ra_y * (ez[i][j + 1][k] - ez[i][j][k]))
                        hx[i][j][k] = fj3[j] * fk3[k] * hx[i][j][k] + fj2[j] * fk2[k] * 0.5 * curl_e

            for i in  range((ib+1),IE):
                ixh=i-ib-1
                for j in  range((JE-1)):
                    for k in  range((KE-1)):
                        curl_e = (ey[i][j][k + 1] - ey[i][j][k] - ra_y * (ez[i][j + 1][k] - ez[i][j][k]))
                        ihxh[ixh][j][k] = ihxh[ixh][j][k] + curl_e
                        hx[i][j][k] = fj3[j] * fk3[k] * hx[i][j][k] + fj2[j] * fk2[k] * 0.5 * (curl_e + fi1[i] * ihxh[ixh][j][k])

            #incident Hx
            
            for i in  range(istart,(iend+1)):
                for k in  range(ktop+1):
                    hx[i][ja - 1][k] = hx[i][ja - 1][k] + (0.5 / eps_sub) * shape[i][k] * ez_inc[ja]

            #Hy

            for i in  range((IE-1)):
                for j in  range(ja):
                    for k in  range((KE-1)):
                        curl_e = (ra_x * (ez[i + 1][j][k] - ez[i][j][k]) - ex[i][j][k + 1] + ex[i][j][k])
                        ihyl[i][j][k] = ihyl[i][j][k] + curl_e
                        hy[i][j][k] = fi3[i] * fk3[k] * hy[i][j][k] + fi2[i] * fk2[k] * 0.5 * (curl_e + fj1[j] * ihyl[i][j][k])

            for i in  range((IE-1)):
                for j in  range(ja,jb+1):
                    for k in  range(KE-1):
                        curl_e = (ra_x * (ez[i + 1][j][k] - ez[i][j][k]) - ex[i][j][k + 1] + ex[i][j][k])
                        hy[i][j][k] = fi3[i] * fk3[k] * hy[i][j][k] + fi2[i] * fk3[k] * 0.5 * curl_e

            for i in  range((IE-1)):
                for j in  range((jb+1),JE):
                    jyh = j - jb - 1
                    for k in  range((KE-1)):
                        curl_e = (ra_x * (ez[i + 1][j][k] - ez[i][j][k]) - ex[i][j][k + 1] + ex[i][j][k])
                        ihyh[i][jyh][k] = ihyh[i][jyh][k] + curl_e
                        hy[i][j][k] = fi3[i] * fk3[k] * hy[i][j][k] + fi2[i] * fk2[k] * 0.5 * (curl_e + fj1[j] * ihyh[i][jyh][k])
            
            #Hz

            for i in  range((IE-1)):
                for j in  range((JE-1)):
                    for k in  range(ka):
                        curl_e = (ra_y * (ex[i][j + 1][k] - ex[i][j][k]) - ra_x * (ey[i + 1][j][k] - ey[i][j][k]))
                        ihzl[i][j][k] = ihzl[i][j][k] + curl_e
                        hz[i][j][k] = fi3[i] * fj3[j] * hz[i][j][k] + fi2[i] * fj2[j] * 0.5 * (curl_e + fk1[k] * ihzl[i][j][k])

            

            for i in  range((IE-1)):
                for j in  range((JE-1)):
                    for k in  range(ka,(kb+1)):
                        curl_e = (ra_y * (ex[i][j + 1][k] - ex[i][j][k]) - ra_x * (ey[i + 1][j][k] - ey[i][j][k]))
                        hz[i][j][k] = fi3[i] * fj3[j] * hz[i][j][k] + fi2[i] * fj2[j] * 0.5 * curl_e


            for i in  range((IE-1)):
                for j in  range((JE-1)):
                    for k in  range((kb+1),KE):
                        kzh = k - kb - 1
                        curl_e = (ra_y * (ex[i][j + 1][k] - ex[i][j][k]) - ra_x * (ey[i + 1][j][k] - ey[i][j][k]))
                        ihzh[i][j][kzh] = ihzh[i][j][kzh] + curl_e
                        hz[i][j][k] = fi3[i] * fj3[j] * hz[i][j][k] + fi2[i] * fj2[j] * 0.5 * (curl_e + fk1[k] * ihzh[i][j][kzh])

            
        #Fin boucle principale

        fp = open("Data3D/Ezplane", "w")

        for j in  range(JE):
            for i in  range(IE):
                fp.write("%.3f "% ez[i][j][ktop])
            fp.write("\n")
        
        fp.close()

        print("T=%4.0f"% T)

    fpt.close()

            

            
main()