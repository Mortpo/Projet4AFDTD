// 3D simulation of a patch antenna.

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define IE 62
#define JE 120
#define KE 14
#define ia 14
#define ja 15
#define ka 7
#define NFREQS 3
#define ktop 2

void main()
{
    //initialisation , double>float ?
    float dx[IE][JE][KE], dy[IE][JE][KE], dz[IE][JE][KE];
    float ex[IE][JE][KE], ey[IE][JE][KE], ez[IE][JE][KE];
    float hx[IE][JE][KE], hy[IE][JE][KE], hz[IE][JE][KE];
    float gax[IE][JE][KE], gay[IE][JE][KE], gaz[IE][JE][KE];
    int l, m, n, i, j, k, ic, jc, kc, nsteps, n_pml; //itérateurs ?
    float ddz, ra_x, ra_y, dt, T, epsz, muz, pi, eaf, npml;
    int ib, jb, kb; // coord cellule
    float xn, xxn, xnim, xd;
    float t0, spread, pulse;
    FILE *fp, *fopen(), *fpt; //ouverture de fichier
    float ez_inc[JE], hx_inc[JE];
    float ez_low_m1, ez_low_m2, ez_high_m1, ez_high_m2;

    //valeur en 3D de ?
    float idxl[ia][JE][KE], idxh[ia][JE][KE];
    float ihxl[ia][JE][KE], ihxh[ia][JE][KE];
    float idyl[IE][ja][KE], idyh[IE][ja][KE];
    float ihyl[IE][ja][KE], ihyh[IE][ja][KE];
    float idzl[IE][JE][ka], idzh[IE][JE][ka];
    float ihzl[IE][JE][ka], ihzh[IE][JE][ka];
    int ixh, jyh, kzh;

    //g et f lier a chaque cellule
    float gi1[IE], gi2[IE], gi3[IE];
    float gj1[JE], gj2[JE], gj3[JE];
    float gk1[KE], gk2[KE], gk3[KE];
    float fi1[IE], fi2[IE], fi3[IE];
    float fj1[JE], fj2[JE], fj3[JE];
    float fk1[KE], fk2[KE], fk3[KE];

    float curl_h, curl_e;

    int ii, jj, kk, numsph;
    float dist, xdist, ydist, zdist;
    int istart, iend, k_ref, jebd, i_ref;
    int j_patch_st, j_patch_end, j_ref;
    int i_patch_st, i_patch_end;
    float eps_sub;
    float shape[IE][KE], half_wv;

    //p 123

    ic = IE/2; //31
    jc = JE/2; //60
    kc = KE/2; //7
    ib = IE - ia - 1; //47
    jb = JE - ja - 1; //104
    kb = KE - ka - 1; //6

    //definition de distances
    i_patch_st = ia + 5; //19
    i_patch_end = i_patch_st + 31; //50
    j_patch_end = jb - 5; //99
    j_patch_st = j_patch_end - 39; //60
    j_ref = j_patch_st - 30; //30
    k_ref = ktop - 1; //1

    pi = 3.14159;
    epsz = 8.8e-12;
    muz = 4 * pi * 1.0e-7;
    ddz = .265e-3; //taille des cellules
    ra_y = .6625;
    ra_x = .6812;
    dt = ddz / 6e8; //pas temporel

    printf("ddz : %12.5e  dt : %12.5e    \n", ddz, dt);

    // INITIALIZATION DES PARAMETRES, CALCUL DES PARAMETRES PML

        for (i = 0 ; i<IE;i++){
        gi1[i]=0.0;
        fi1[i]=0.0;
        gi2[i]=1.0;
        fi2[i]=1.0;
        gi3[i]=1.0;
        fi3[i]=1.0;}

    for (j = 0 ; j<JE;j++){
        gj1[j]=0.0;
        fj1[j]=0.0;
        gj2[j]=1.0;
        fj2[j]=1.0;
        gj3[j]=1.0;
        fj3[j]=1.0;}
    
    for (k = 0 ; k<KE;k++){
        gk1[k]=0.0;
        fk1[k]=0.0;
        gk2[k]=1.0;
        fk2[k]=1.0;
        gk3[k]=1.0;
        fk3[k]=1.0;}
    
    printf("Number of PML cells -->");
    scanf("%f",&npml);
    printf("%f \n",npml);
    n_pml=npml;

    for (i = 0 ; i<n_pml;i++){
        xxn=(npml-i)/npml;
        xn = 0.33*pow(xxn,3);
        printf("%d xn = %8.4f  xn = %8.4f",i,xxn,xn);
        fi1[i]= xn;
        fi1[IE-i-1]=xn;
        gi2[i]= 1.0/(1.0+xn);
        gi2[IE-i-1] = 1.0/(1.0+xn);
        gi3[i]=(1.0-xn)/(1.0+xn);
        gi3[IE-i-1] = (1.0-xn)/(1.0+xn);
        xxn=(npml-i-0.5)/npml;
        xn = 0.33*pow(xxn,3.0);
        gi1[i]=xn;
        gi1[IE-i-2]=xn;
        fi2[i]=1.0/(1.0+xn);
        fi2[IE-i-2]=1.0/(1.0+xn);
        fi3[i]=(1.0-xn)/(1.0+xn);
        fi3[IE-i-2]=(1.0-xn)/(1.0+xn);}

    for (j = 0 ; j<n_pml;j++){
        xxn=(npml-j)/npml;
        xn = 0.33*pow(xxn,3);
        fj1[j]= xn;
        fj1[JE-j-1]=xn;
        gj2[j]= 1.0/(1.0+xn);
        gj2[JE-j-1] = 1.0/(1.0+xn);
        gj3[j]=(1.0-xn)/(1.0+xn);
        gj3[JE-j-1] = (1.0-xn)/(1.0+xn);
        xxn=(npml-j-0.5)/npml;
        xn = 0.33*pow(xxn,3.0);
        gj1[j]=xn;
        gj1[JE-j-2]=xn;
        fj2[j]=1.0/(1.0+xn);
        fj2[JE-j-2]=1.0/(1.0+xn);
        fj3[j]=(1.0-xn)/(1.0+xn);
        fj3[JE-j-2]=(1.0-xn)/(1.0+xn);}

        
    for  (k = 0 ; k<n_pml;k++){
        xxn=(npml-k)/npml;
        xn = 0.33*pow(xxn,3);
        fk1[k]= xn;
        fk1[KE-k-1]=xn;
        gk2[k]= 1.0/(1.0+xn);
        gk2[KE-k-1] = 1.0/(1.0+xn);
        gk3[k]=(1.0-xn)/(1.0+xn);
        gk3[KE-k-1] = (1.0-xn)/(1.0+xn);
        xxn=(npml-k-0.5)/npml;
        xn = 0.33*pow(xxn,3.0);
        gk1[k]=xn;
        gk1[KE-k-2]=xn;
        fk2[k]=1.0/(1.0+xn);
        fk2[KE-k-2]=1.0/(1.0+xn);
        fk3[k]=(1.0-xn)/(1.0+xn);
        fk3[KE-k-2]=(1.0-xn)/(1.0+xn);}
        

    //  Constante Dielectric du substrat

    eps_sub = 2.2;
    printf("eps_sub : %f  \n", eps_sub);

    for (j = 0; j < JE; j++)
    {
        for (i = 0; i < IE; i++)
        {
            for (k = 0; k <= ktop; k++)
            {
                gax[i][j][k] = (1.0 / eps_sub);
                gay[i][j][k] = (1.0 / eps_sub);
                gaz[i][j][k] = (1.0 / eps_sub);
            }
        }
    }

    //ajout de la plaque de métal à k=0

    for (i = 1; i < IE - 1; i++)
    {
        for (j = 1; j < JE - 1; j++)
        {
            k = 0;
            gax[i][j][k] = 0;
            gay[i][j][k] = 0;
        }
    }

    istart = ia + 6; //20
    iend = istart + 6; //26
    i_ref = istart + (iend - istart)/2; // 20 + (26 -20)/2 =23
    printf("istart : %d  iend : %d  i_ref : %d\n", istart, iend, i_ref);

    half_wv = (iend - istart)/2.;
    printf("half_wv = %5.2f\n", half_wv);

    for (i = istart; i <= iend; i++)
    {
        for (k = 0; k <= ktop; k++)
        {
            shape[i][k] = 1.;
        }
    }

    // ajout du conducteur jusqu'au patch à k = ktop+1

    for (j = 1; j <= j_patch_st; j++)
    {
        for (i = istart; i <= iend - 1; i++)
        {
            gax[i][j][ktop + 1] = 0.;
        }
        for (i = istart; i <= iend - 1; i++)
        {
            gay[i][j][ktop + 1] = 0.;
        }
    }

    // ajout du patch rectangulaire à k = ktop

    for (j = j_patch_st; j <= j_patch_end; j++) 
    {
        for (i = ia + 1; i <= ib - 1; i++)
        {
            gax[i][j][ktop + 1] = 0.;
        }
        for (i = ia + 1; i <= ib - 1; i++)
        {
            gay[i][j][ktop + 1] = 0.;
        }
    }

    t0 = 150.0;
    spread = 25.0;
    printf("Pulse width is %12.5e  \n", spread * dt);
    T = 0;
    nsteps = 1;

    fpt = fopen("../Data3D/CTimeplane", "w");

    while (nsteps > 0)
    {
        printf("nsteps --> ");
        scanf("%d", &nsteps);
        printf("nsteps : %d  \n", nsteps);

        for (n = 1; n < nsteps; n++)
        {
            T = T + 1;

            ///////////////////////}? //surement pas car sinon on incrémente une variable
            // Début de la boucle principale

            //calcul du buffer incident
            for (j = 1; j < JE; j++)
            {
                ez_inc[j] = gj3[j] * ez_inc[j] + gj2[j] * (0.5 * ra_y / eps_sub) * (hx_inc[j - 1] - hx_inc[j]);
            }

            //Source
            pulse = exp(-0.5 * (pow((t0 - T) / spread, 2.0)));
            ez_inc[ja - 2] = pulse;
            printf("T : %4.0f  Pulse : %6.2e \n", T, pulse);

            //calcul du champ Dx

            for (i = 1; i < ia; i++)
            {
                for (j = 1; j < JE; j++)
                {
                    for (k = 1; k < KE; k++)
                    {
                        curl_h = (ra_y * (hz[i][j][k] - hz[i][j - 1][k]) - hy[i][j][k] + hy[i][j][k - 1]);
                        idxl[i][j][k] = idxl[i][j][k] + curl_h;
                        dx[i][j][k] = gj3[j] * gk3[k] * dx[i][j][k] + gj2[j] * gk2[k] * 0.5 * (curl_h + gi1[i] * idxl[i][j][k]);
                    }
                }
            }

            for (i = ia; i <= ib; i++)
            {
                for (j = 1; j < JE; j++)
                {
                    for (k = 1; k < KE; k++)
                    {
                        curl_h = (ra_y * (hz[i][j][k] - hz[i][j - 1][k]) - hy[i][j][k] + hy[i][j][k - 1]);
                        dx[i][j][k] = gj3[j] * gk3[k] * dx[i][j][k] + gj2[j] * gk2[k] * 0.5 * curl_h;
                    }
                }
            }

            for (i = ib + 1; i < IE; i++)
            {
                ixh = i - ib - 1;
                for (j = 1; j < JE; j++)
                {
                    for (k = 1; k < KE; k++)
                    {
                        curl_h = (ra_y * (hz[i][j][k] - hz[i][j - 1][k]) - hy[i][j][k] + hy[i][j][k - 1]);
                        idxh[ixh][j][k] = idxh[ixh][j][k] + curl_h;
                        dx[i][j][k] = gj3[j] * gk3[k] * dx[i][j][k] + gj2[j] * gk2[k] * 0.5 * (curl_h + gi1[i] * idxh[ixh][j][k]);
                    }
                }
            }

            //Calcul du champ Dy

            for (i = 1; i < IE; i++)
            {
                for (j = 1; j < ja; j++)
                {
                    for (k = 1; k < KE; k++)
                    {
                        curl_h = (hx[i][j][k] - hx[i][j][k - 1] - ra_x * (hz[i][j][k] - hz[i - 1][j][k]));
                        idyl[i][j][k] = idyl[i][j][k] + curl_h;
                        dy[i][j][k] = gi3[i] * gk3[k] * dy[i][j][k] + gi2[i] * gk2[k] * 0.5 * (curl_h + gj1[j] * idyl[i][j][k]);
                    }
                }
            }

            for (i = 1; i < IE; i++)
            {
                for (j = ja; j <= jb; j++)
                {
                    for (k = 1; k < KE; k++)
                    {
                        curl_h = (hx[i][j][k] - hx[i][j][k - 1] - ra_x * (hz[i][j][k] - hz[i - 1][j][k]));
                        dy[i][j][k] = gi3[i] * gk3[k] * dy[i][j][k] + gi2[i] * gk2[k] * 0.5 * curl_h;
                    }
                }
            }

            for (i = 1; i < IE; i++)
            {
                for (j = jb + 1; j < JE; j++)
                {
                    jyh = j - jb - 1;
                    for (k = 1; k < KE; k++)
                    {
                        curl_h = (hx[i][j][k] - hx[i][j][k - 1] - ra_x * (hz[i][j][k] - hz[i - 1][j][k]));
                        idyh[i][jyh][k] = idyh[i][jyh][k] + curl_h;
                        dy[i][j][k] = gi3[i] * gk3[k] * dy[i][j][k] + gi2[i] * gk2[k] * 0.5 * (curl_h + gj1[j] * idyh[i][jyh][k]);
                    }
                }
            }

            //calcul du champ Dz

            for (i = 1; i < IE; i++)
            {
                for (j = 1; j < JE; j++)
                {
                    for (k = 0; k < ka; k++)
                    {
                        curl_h = (ra_x * (hy[i][j][k] - hy[i - 1][j][k]) - ra_y * (hx[i][j][k] - hx[i][j - 1][k]));
                        idzl[i][j][k] = idzl[i][j][k] + curl_h;
                        dz[i][j][k] = gi3[i] * gj3[j] * dz[i][j][k] + gi2[i] * gj2[j] * 0.5 * (curl_h + gk1[k] * idzl[i][j][k]);
                    }
                }
            }

            for (i = 1; i < IE; i++)
            {
                for (j = 1; j < JE; j++)
                {
                    for (k = ka; k <= kb; k++)
                    {
                        curl_h = (ra_x * (hy[i][j][k] - hy[i - 1][j][k]) - ra_y * (hx[i][j][k] - hx[i][j - 1][k]));
                        dz[i][j][k] = gi3[i] * gj3[j] * dz[i][j][k] + gi2[i] * gj2[j] * 0.5 * curl_h;
                    }
                }
            }

            for (i = 1; i < IE; i++)
            {
                for (j = 1; j < JE; j++)
                {
                    for (k = kb + 1; k < KE; k++)
                    {
                        kzh = k - kb - 1;
                        curl_h = (ra_x * (hy[i][j][k] - hy[i - 1][j][k]) - ra_y * (hx[i][j][k] - hx[i][j - 1][k]));
                        idzh[i][j][kzh] = idzh[i][j][kzh] + curl_h;
                        dz[i][j][k] = gi3[i] * gj3[j] * dz[i][j][k] + gi2[i] * gj2[j] * 0.5 * (curl_h + gk1[k] * idzl[i][j][kzh]);
                    }
                }
            }

            //Incident Dz

            for (i = istart; i <= iend; i++)
            {
                for (k = 0; k <= ktop; k++)
                {
                    dz[i][ja][k] = dz[i][ja][k] + (0.5 / eps_sub) * shape[i][k] * hx_inc[ja - 1];
                }
            }

            // Calcul de E depuis le champ D
            // Ex et Ey sont à 0 pour k=0

            for (i = 1; i < IE - 1; i++)
            {
                for (j = 1; j < JE - 1; j++)
                {
                    for (k = 1; k < KE - 1; k++)
                    {
                        ex[i][j][k] = gax[i][j][k] * dx[i][j][k];
                        ey[i][j][k] = gay[i][j][k] * dy[i][j][k];
                        ez[i][j][k] = gaz[i][j][k] * dz[i][j][k];
                    }
                }
            }

            //Ecriture des données temporelles dans le port d'entré

            fprintf(fpt, "%8.4f \n", ez[i_ref][j_ref][k_ref]); // 23 30 1

            //Calcul du champ incident

            for (j = 0; j < JE - 1; j++)
            {
                hx_inc[j] = fj3[j] * hx_inc[j] + 0.5 * fj2[j] * (ez_inc[j] - ez_inc[j + 1]);
            }

            //Calcul de champ Hx (fin page 139)

            //FIN Romain Début anass

            for (i = 0; i < ia; i++)
            {
                for (j = 0; j < JE - 1; j++)
                {
                    for (k = 0; k < KE - 1; k++)
                    {
                        curl_e = (ey[i][j][k + 1] - ey[i][j][k] - ra_y * (ez[i][j + 1][k] - ez[i][j][k]));
                        ihxl[i][j][k] = ihxl[i][j][k] + curl_e;
                        hx[i][j][k] = fj3[j] * fk3[k] * hx[i][j][k] + fj2[j] * fk2[k] * 0.5 * (curl_e + fi1[i] * ihxl[i][j][k]);
                    }
                }
            }
            for (i = ia; i <= ib; i++)
            {
                for (j = 0; j < JE - 1; j++)
                {
                    for (k = 0; k < KE - 1; k++)
                    {
                        curl_e = (ey[i][j][k + 1] - ey[i][j][k] - ra_y * (ez[i][j + 1][k] - ez[i][j][k]));
                        hx[i][j][k] = fj3[j] * fk3[k] * hx[i][j][k] + fj2[j] * fk2[k] * 0.5 * curl_e;
                    }
                }
            }
            for (i = ib + 1; i < IE; i++) //PB sur k
            {
                ixh = i - ib - 1;
                for (j = 0; j < JE - 1; j++)
                {
                    for (k = 0; k < KE - 1; k++)
                    {
                        curl_e = (ey[i][j][k + 1] - ey[i][j][k] - ra_y * (ez[i][j + 1][k] - ez[i][j][k]));
                        ihxh[ixh][j][k] = ihxh[ixh][j][k] + curl_e;
                        hx[i][j][k] = fj3[j] * fk3[k] * hx[i][j][k] + fj2[j] * fk2[k] * 0.5 * (curl_e + fi1[i] * ihxh[ixh][j][k]);
                    }
                }
            }

            /* incident Hx */
            for (i = istart; i <= iend; i++)
            {
                for (k = 0; k <= ktop; k++)
                {
                    hx[i][ja - 1][k] = hx[i][ja - 1][k] + (0.5 / eps_sub) * shape[i][k] * ez_inc[ja];
                }
            }
            /* calculate  Hy filed */
            for (i = 0; i < IE - 1; i++)
            {
                for (j = 0; j < ja; j++)
                {
                    for (k = 0; k < KE - 1; k++)
                    {
                        curl_e = (ra_x * (ez[i + 1][j][k] - ez[i][j][k]) - ex[i][j][k + 1] + ex[i][j][k]);
                        ihyl[i][j][k] = ihyl[i][j][k] + curl_e;
                        hy[i][j][k] = fi3[i] * fk3[k] * hy[i][j][k] + fi2[i] * fk2[k] * 0.5 * (curl_e + fj1[j] * ihyl[i][j][k]);
                    }
                }
            }

            for (i = 0; i < IE - 1; i++)
            {
                for (j = ja; j <= jb; j++)
                {
                    for (k = 0; k < KE - 1; k++)
                    {
                        curl_e = (ra_x * (ez[i + 1][j][k] - ez[i][j][k]) - ex[i][j][k + 1] + ex[i][j][k]);
                        hy[i][j][k] = fi3[i] * fk3[k] * hy[i][j][k] + fi2[i] * fk3[k] * 0.5 * curl_e;
                    }
                }
            }
            for (i = 0; i < IE - 1; i++)
            {
                for (j = jb + 1; j < JE; j++)
                {
                    jyh = j - jb - 1;
                    for (k = 0; k < KE - 1; k++)
                    {
                        curl_e = (ra_x * (ez[i + 1][j][k] - ez[i][j][k]) - ex[i][j][k + 1] + ex[i][j][k]);
                        ihyh[i][jyh][k] = ihyh[i][jyh][k] + curl_e;
                        hy[i][j][k] = fi3[i] * fk3[k] * hy[i][j][k] + fi2[i] * fk2[k] * 0.5 * (curl_e + fj1[j] * ihyh[i][jyh][k]);
                    }
                }
            }
            /* calculate the Hz fieled */
            for (i = 0; i < IE - 1; i++)
            {
                for (j = 0; j < JE - 1; j++)
                {
                    for (k = 0; k < ka; k++)
                    {
                        curl_e = (ra_y * (ex[i][j + 1][k] - ex[i][j][k]) - ra_x * (ey[i + 1][j][k] - ey[i][j][k]));
                        ihzl[i][j][k] = ihzl[i][j][k] + curl_e;
                        hz[i][j][k] = fi3[i] * fj3[j] * hz[i][j][k] + fi2[i] * fj2[j] * 0.5 * (curl_e + fk1[k] * ihzl[i][j][k]);
                    }
                }
            }
            for (i = 0; i < IE - 1; i++)
            {
                for (j = 0; j < JE - 1; j++)
                {
                    for (k = ka; k <= kb; k++)
                    {
                        curl_e = (ra_y * (ex[i][j + 1][k] - ex[i][j][k]) - ra_x * (ey[i + 1][j][k] - ey[i][j][k]));
                        hz[i][j][k] = fi3[i] * fj3[j] * hz[i][j][k] + fi2[i] * fj2[j] * 0.5 * curl_e;
                    }
                }
            }

            for (i = 0; i < IE - 1; i++)
            {
                for (j = 0; j < JE - 1; j++)
                {
                    for (k = kb + 1; k < KE; k++)
                    {
                        kzh = k - kb - 1;
                        curl_e = (ra_y * (ex[i][j + 1][k] - ex[i][j][k]) - ra_x * (ey[i + 1][j][k] - ey[i][j][k]));
                        ihzh[i][j][kzh] = ihzh[i][j][kzh] + curl_e;
                        hz[i][j][k] = fi3[i] * fj3[j] * hz[i][j][k] + fi2[i] * fj2[j] * 0.5 * (curl_e + fk1[k] * ihzh[i][j][kzh]);
                    }
                }
            }
        }
        /* end of the main FDTD LOOP */
        /* write the E field out to file "Ez" */
        fp = fopen("../Data3D/CEzplane", "w");
        for (j = 0; j < JE; j++)
        {
            for (i = 0; i < IE; i++)
            {
                fprintf(fp, "%.3f ", ez[i][j][ktop]); // i j 2
            }
            fprintf(fp, "\n");
        }
        fclose(fp);
        printf("T=%4.0f\n", T);
    }
    fclose(fpt);
}
//////////////////STOP CORRECTION ///////////////////////////////////////////////////////////////////////////////////////////////////////