/* Fd2d_3.2.c. 2D TM ¨rogram with the PML*/

#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#define IE 60
#define JE 60

void main()
{
    float ga[IE][JE], dz[IE][JE], ez[IE][JE], hx[IE][JE], hy[IE][JE]; //definition des tableaux pour les champs ga pour Epsilon0 du materiau
    int l, n, i, j, ic, jc, nsteps, npml;
    float ddx, dt, T, epsz, pi, epsilon, sigma, eaf;
    float xn, xxn, xnum, xd, curl_e;
    float t0, spread, pulse;
    float gi2[IE], gi3[IE];
    float gj2[JE], gj3[IE];          //IE ??
    float fi1[IE], fi2[IE], fi3[JE]; //JE ??
    float fj1[JE], fj2[JE], fj3[JE];
    float ihx[IE][JE], ihy[IE][JE];
    FILE *fp, *fopen();

    ic = IE / 2 - 5;
    jc = JE /2  -5;
    ddx = 0.01;     //taille des cellules
    dt = ddx / 6e8; //pas de temps
    epsz = 8.8e-12;
    pi = 3.14159;

    //INITIALISATION DES TABLEAUX

    for (j = 0; j < JE; j++)
    {
        printf("%2d  ", j);
        for (i = 0; i < IE; i++)
        {
            dz[i][j] = 0.0;
            hx[i][j] = 0.0;
            hy[i][j] = 0.0;
            ihx[i][j] = 0.0;
            ihy[i][j] = 0.0;
            ga[i][j] = 1.0;
            printf("%5.2f  ", ga[i][j]);
        }
        printf(" \n");
    }

    //CALCUL DES PARAMETRES DU PML

    for (i = 0; i < IE; i++)
    {
        gi2[i] = 1.0;
        gi3[i] = 1.0;
        fi1[i] = 0.0;
        fi2[i] = 1.0;
        fi3[i] = 1.0;
    }
    for (j = 0; j < IE; j++) //IE ???
    {
        gj2[j] = 1.0;
        gj3[j] = 1.0;
        fj1[j] = 0.0;
        fj2[j] = 1.0;
        fj3[j] = 1.0;
    }

    printf("Number of PML cells -->");
    scanf("%d", &npml);

    for (i = 0; i <= npml; i++)
    {
        xnum = npml - i; // pas une somme inversé mais plutot un suite arithmétique
        xd = npml;
        xxn = xnum / xd;
        xn = 0.33 * pow(xxn, 3.0);
        printf("  %d  %7.4f  %7.4f \n", i, xxn, xn);
        gi2[i] = 1.0 / (1.0 + xn); //parametre PML (voir formules)
        gi2[IE - 1 - i] = 1.0 / (1.0 + xn);
        gi3[i] = (1.0 - xn) / (1.0 + xn);
        gi3[IE - i - 1] = (1.0 - xn) / (1.0 + xn);
        xxn = (xnum - 0.5) / xd;
        xn = 0.25 * pow(xxn, 3.0);
        fi1[i] = xn; //parametre PML (voir formules)
        fi1[IE - 2 - i] = xn;
        fi2[i] = 1.0 / (1.0 + xn);
        fi2[IE - 2 - i] = 1.0 / (1.0 + xn);
        fi3[i] = (1.0 - xn) / (1.0 + xn);
        fi3[IE - 2 - i] = (1.0 - xn) / (1.0 + xn);
    }

    for (j = 0; j < npml; j++)
    {
        xnum = npml - j;
        xd = npml;
        xxn = xnum / xd;
        xn = 0.33 * pow(xxn, 3.0);
        printf(" %d %7.4f %7.4f \n", i, xxn, xn);
        gj2[j] = 1.0 / (1.0 + xn);
        gj2[JE - 1 - j] = 1.0 / (1.0 + xn);
        gj3[j] = (1.0 - xn) / (1.0 + xn);
        gj3[JE - j - 1] = (1.0 - xn) / (1.0 + xn);
        xxn = (xnum - 0.5) / xd;
        xn = 0.25 * pow(xxn, 3.0);
        fj1[j] = xn;
        fj1[JE - 2 - j] = xn;
        fj2[j] = 1.0 / (1.0 + xn);
        fj2[JE - 2 - j] = 1.0 / (1.0 + xn);
        fj3[j] = (1.0 - xn) / (1.0 + xn);
        fj3[JE - 2 - j] = (1.0 - xn) / (1.0 + xn);
    }

    printf("gi+fi \n");
    for (i = 0; i < IE; i++)
    {
        printf("%2d  %5.2f  %5.2f  \n", i, gi2[i], gi3[i]);
        printf("   %5.2f   %5.2f   %5.2f  \n", fi1[i], fi2[i], fi3[i]);
    }

    printf("gj +fj \n");
    for (j = 0; j < JE; j++)
    {
        printf("%2d  %5.2f  %5.2f  \n", i, gj2[i], gj3[i]);
        printf("   %5.2f   %5.2f   %5.2f  \n", fj1[i], fj2[i], fj3[i]);
    }

    t0 = 40.0;
    spread = 15.0;
    T = 0;
    nsteps = 1;

    while (nsteps > 0)
    {
        printf(" nsteps --> ");
        scanf("%d", &nsteps);
        printf("%d  \n", nsteps);

        for (n = 1; n <= nsteps; n++)
        {
            T = T + 1;

            /* ---------- DEBUT DE LA BOUCLE PRINCIPALE ---------- */

            //Calcul du champ Dz

            for (j = 1; j < IE; j++)
            { //2 fois IE ?
                for (i = 1; i < IE; i++)
                {
                    dz[i][j] = gi3[i] * gj3[j] * dz[i][j] + gi2[i] * gj2[j] * 0.5 * (hy[i][j] - hy[i - 1][j] - hx[i][j] + hx[i][j - 1]);
                }
            }

            //source sinusoidal

            pulse = sin(2 * pi * 1500 * 1e6 * dt * T); //;?
            dz[ic][jc] = pulse;                        // point ou l'impulsion est envoyé

            //calcul de EZ

            for (j = 0; j < JE; j++)
            {
                for (i = 0; i < IE; i++)
                {
                    ez[i][j] = ga[i][j] * dz[i][j];
                }
            }
            printf(" T = %3f   Ez[ic][jc] = %6.2f \n", T, ez[ic][jc]); //champs EZ à la source

            //Mise à 0 de EZ sur les des bords, cela fait partie de la PML

            for (j = 0; j < JE - 1; j++)
            {
                ez[0][j] = 0.0;
                ez[IE - 1][j] = 0.0;
            }
            for (i = 0; i < IE - 1; i++)
            {
                ez[i][0] = 0.0;
                ez[i][JE - 1] = 0.0;
            }

            //calcul du champ Hx
            //décalcage de 1/2 car FDTD??
            for (j = 0; j < JE - 1; j++)
            {
                for (i = 0; i < IE; i++)
                {
                    curl_e = ez[i][j] - ez[i][j + 1];        //dy
                    ihx[i][j] = ihx[i][j] + fi1[i] * curl_e; //intégrale donné dans le livre vers la fin de la PML
                    hx[i][j] = fj3[j] * hx[i][j] + fj2[j] * 0.5 * (curl_e + ihx[i][j]);
                }
            }

            //calcul de Hy
            //décalcage de 1/2 dans 2 direction ??
            for (j = 0; j <= JE - 1; j++)
            {
                for (i = 0; i < IE - 1; i++)
                {
                    curl_e = ez[i + 1][j] - ez[i][j]; //dx
                    ihy[i][j] = ihy[i][j] + fj1[j] * curl_e;
                    hy[i][j] = fi3[i] * hy[i][j] + fi2[i] * 0.5*(curl_e + ihy[i][j]);
                }
            }


        }
        //FIN DE LA BOUCLE PRINCIPALE

        for ( j= 1; j < JE; j++)
        {
            printf(" j = %2d",j);
            for ( i = 1; i <= IE; i++)
            {
                printf(" ez = %4.1f",ez[i][j]);
            }
            printf(" \n");
        }
        

        //ecriture de EZ
        fp=fopen("../Data2D/Ez2D1point","w");
        for (j = 0; j < JE; j++)
        {
            for ( i = 0; i < IE; i++)
            {
                fprintf(fp,"%.3f ",ez[i][j]);
            }
            fprintf(fp," \n");
        }
        fclose(fp);
        printf("T= %6.0f \n",T);


    }
}
