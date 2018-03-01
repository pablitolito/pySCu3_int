#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np
import csv
import pylab
import os.path as path
import pmagplotlib as pmagpl
import pyscu_libs as scu
import sys
import os
rad=np.pi/180.
deg=180./np.pi
import easygui as eg


def main():
    
        
    """
    NAME
        pyscu_draw.py

    DESCRIPTION
        plot the data calculated in pyscu_calc.py
    
    INPUT
        ouput files from pyscu_calc.py
        You must open the *_main.txt
        
        interactive data entry using Easygui
        (http://easygui.sourceforge.net/)
       """

    
    print ('\nThis program uses the PmagPy and pySCu softwares utilities\n\tTauxe et al. 2016, G3, http://dx.doi.org/10.1002/2016GC006307\n\tCalvín et al. 2017, C&G, http://dx.doi.org/10.1016/j.cageo.2017.07.002')

    
   
    if '-h' in sys.argv:
        print(main.__doc__)
        sys.exit()
        
    infile = eg.fileopenbox(msg="Open File",
                         title="Control: fileopenbox",
                         default='')   
    outfile=infile[:-9]
    
    infile_m=infile[:-8]+'mat.txt'
    infile_ref=infile[:-8]+'Ref.txt'
    infile_inter=infile[:-8]+'inter.txt'
    infile_sci=infile[:-8]+'SCIs.txt'    

    if path.exists(infile_ref):    Ref='true'
    else: Ref='false'
    
    if path.exists(infile_m):    matrix='true'
    else: matrix='false'
    
    if path.exists(infile_inter):    inter='true'
    else: inter='false'
    
    if path.exists(infile_sci):    SCIs='true'
    else: SCIs='false'
    
    if Ref=='false':
        campos = ['Dec','Inc','Eta','Dec_Eta','Inc_Eta','Zeta','Dec_Zeta','Inc_Zeta']
        ref = []
        ref = eg.multenterbox(msg="I can't found the file with the reference direction \n Please, input the Kent parameters of it",
                        title='Interactive entry of the remagnetization direction',
                        fields=campos, values=(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))
        
    if Ref=='false' and ref!=None:
        print(ref)
        ref[0]=float(ref[0])
        ref[1]=float(ref[1])        
        ref[2]=float(ref[2])
        ref[3]=float(ref[3])
        ref[4]=float(ref[4])  
        ref[5]=float(ref[5])
        ref[6]=float(ref[6])  
        ref[7]=float(ref[7])
        iRef='true'
        
        print (ref)
    ans_mat = eg.boolbox(msg='Do you want to plot te A matrix?',
                       title='Control: boolbox',
                       choices=('Yes', 'No'))
        
    preS = eg.buttonbox(msg='Doy you want plot the SCI solutions (s), the intersections (i) or none (n)',
                         title='Control: buttonbox',
                         choices=('s', 'i', 'n'))
    

    if matrix=='false' and ans_mat==True:
        	print("\nTake care, I don't found the file", infile_m, ' whit the A/N matriz data')
    if inter=='false' and preS=='i':
        	print("\nTake care, I don't found the file", infile_inter, ' whit the intersections directions')
    if SCIs=='false' and preS=='s':
        	print("\nTake care, I don't found the file", infile_sci, ' whit the SCIs directions')
    

    
    out_name_bbc=outfile+'_bbc.svg'
    out_name_bfd=outfile+'_bfd.svg'
    out_name_atbc=outfile+'_atbc.svg'
    out_name_mat=outfile+'_mat.svg'
    
    
    print('\nPlease, wait a moment')
    print('\nPlots will be saved as', out_name_bbc, ', ', out_name_bfd, '...\n')
    
    
    #Saving the data in different list
    site,sc,geo,tilt,bfd=scu.getInFile_main(infile) #main file
    n=len(site)
    
    if Ref=='true': #reference direction
        	reader=csv.reader(open(infile_ref), delimiter=' ')
        	dat_Ref=list(reader)
        	ref=[float(dat_Ref[1][1]),float(dat_Ref[1][2]),float(dat_Ref[1][3]),float(dat_Ref[1][5]),
              float(dat_Ref[1][6]),float(dat_Ref[1][4]),float(dat_Ref[1][7]),float(dat_Ref[1][8]),float(dat_Ref[1][11])]
    
    if inter=='true' and preS=='i': #intersections directions
    	reader=csv.reader(open(infile_inter), delimiter=' ')
    	dat_inter_h=list(reader)
    	dat_inter=dat_inter_h[1:]
    
    if SCIs=='true' and preS=='s': #intersections directions
        reader=csv.reader(open(infile_sci), delimiter=' ')
        dat_SCIs_h=list(reader)
        dat_SCIs=dat_SCIs_h[1:]
    
    if matrix=='true' and ans_mat==True: #A/n values
        	X,Y,Z,minA,maxA=scu.getInFile_mat(infile_m)  
    
    
    #Drawing...
    plt.figure(num=1,figsize=(6,6),facecolor='white')
    
    #Plotting the BBC directions, the SCs and the reference
    pmagpl.plotNET(1)
    pylab.figtext(.02, .045, 'pySCu v3.1')
    plt.text(0.85, 0.7, 'BBC', fontsize = 13)
    plt.scatter(0.8, 0.74, color='r',marker='s',s=30)
    plt.text(0.70, 0.85, 'n='+str(n), fontsize = 13)
    
    for dato in sc: #The SCs
        	scu.smallcirc(dato,1)
    
    for dato in geo: #The BBC directions
        	scu.plot_di_mean(dato[0],dato[1],dato[2],color='r',marker='s',markersize=8,label='Geo',legend='no',zorder=3)
    	#You can change the marker (+, ., o, *, p, s, x, D, h, ^), the color (b, g, r, c, m, y, k, w) or the size as you prefere
    
    if Ref=='true' or iRef=='true': #The reference
        scu.plotCONF(ref)
        plt.text(0.51, -1.05, 'Reference', fontsize = 13)
        plt.scatter(0.45, -1, color='m',marker='*',s=100)
        plt.title('Before Bedding Correction',fontsize=20)
        plt.savefig(out_name_bbc)
    
    #Plotting the ATBC directions, the SCs and the reference
    plt.figure(num=2,figsize=(6,6),facecolor='white')
    pmagpl.plotNET(2)
    pylab.figtext(.02, .045, 'pySCu v3.1')
    plt.text(0.85, 0.7, 'ATBC', fontsize = 13)
    plt.scatter(0.8, 0.745, color='g',marker='^',s=40)
    plt.text(0.70, 0.85, 'n='+str(n), fontsize = 13)
    
    for dato in sc:
        	scu.smallcirc(dato,1)
    if Ref=='true' or iRef=='true':
        	scu.plotCONF(ref)
        	plt.text(0.51, -1.05, 'Reference', fontsize = 13)
        	plt.scatter(0.45, -1, color='m',marker='*',s=100)
    
    for dato in tilt:
        	scu.plot_di_mean(dato[0],dato[1],dato[2],color='g',marker='^',markersize=9,label='Tilt',legend='no',zorder=3)
    
    plt.savefig(out_name_atbc)
    
    #Plotting the BFD directions, the SCs and the reference
    plt.figure(num=3,figsize=(6,6),facecolor='white')
    pmagpl.plotNET(3)
    pylab.figtext(.02, .045, 'pySCu v3.1')
    plt.text(0.85, 0.7, 'BFD', fontsize = 13)
    plt.scatter(0.8, 0.74, color='b',marker='o',s=30)
    plt.text(0.70, 0.85, 'n='+str(n), fontsize = 13)
    
    for dato in sc:
        	scu.smallcirc(dato,1)
    
    for dato in bfd:
        	scu.plot_di_mean(dato[0],dato[1],dato[2],color='b',marker='o',markersize=5,label='BFD',legend='no',zorder=3)
    
    if Ref=='true' or iRef=='true': #Ploting the reference and the leyend
        scu.plotCONF(ref)
        plt.text(0.51, -1.05, 'Reference', fontsize = 13)
        plt.scatter(0.45, -1, color='m',marker='*',s=100)
        plt.savefig(out_name_bfd)
    
    #Plotting the A/n contour plot and/or the intersections
    if (ans_mat==True and matrix=='true') or (preS=='i' and inter=='true') or (preS=='s' and SCIs=='true'):
        plt.figure(num=4,figsize=(6,6),facecolor='white')
        pmagpl.plotNET(4)
        pylab.figtext(.02, .045, 'pySCu v3.1')
        fig4='true'
    else: fig4='false'
    		
    if ans_mat==True and matrix=='true': #plotting the A/n contour plot
        max_z=max(Z)
        max_z_s=max_z+(5-max_z%5)+0.1
        min_z=min(Z)
        min_z_s=min_z-(min_z%5)
    
        levels5 = np.arange(min_z_s,max_z_s, 5)
        levels1 = np.arange(min_z_s,max_z_s, 1)
    
        CS=plt.tricontourf(X, Y, Z, vmin=min_z,vmax=max_z, cmap = 'Blues', levels=levels1) #Other colormaps (as 'rainbow') are possibles. Change 'Blues' for the choosed colormap
        cbar=plt.colorbar(CS, orientation='horizontal',pad=0.05)
        CS2=plt.tricontour(X,Y,Z, colors='k',linewidths = .5, levels=levels5)
    
        #plt.clabel(CS2,levels=levels5, inline=1, fmt='%1.0f', fontsize=10)
        cbar.ax.set_xlabel('A/n value'+' ('+str(round(minA,1))+'-'+str(round(maxA,1))+')')
        #cbar.add_lines(CS2)
        plt.axis((-1.35,1.35,-1.35,1.35))
    else:
        for dato in sc:
            scu.smallcirc(dato,1)
    
    
    if preS=='i' and inter=='true': #plotting the intersections
        text_i='SCs intersec. (n='+str(len(dat_inter))+')'
        plt.text(-0.3, -1.2, text_i, fontsize = 12)
        plt.scatter(-0.38, -1.12, color='k',marker='.',s=50)
        for dato in dat_inter:
            scu.plot_di_mean(float(dato[0]),float(dato[1]),0.,color='k',marker='.',markersize=1,label='Intersections',legend='no')
    
    if preS=='s' and SCIs=='true': #plotting the SCIs
        text_s='SCIs solutions (n='+str(len(dat_SCIs))+')'
        plt.text(-0.3, -1.2, text_s, fontsize = 12)
        plt.scatter(-0.38, -1.12, color='k',marker='.',s=50)
        for dato in dat_SCIs:
            scu.plot_di_mean(float(dato[0]),float(dato[1]),0.,color='k',marker='.',markersize=1,label='SCIs',legend='no')
    		
    if fig4=='true' and (Ref=='true' or iRef=='true'): #Plotting the reference and the leyend
        scu.plotCONF(ref)
        plt.text(0.6, 0.83, 'Reference', fontsize = 13)
        plt.scatter(0.93, 0.73, color='m',marker='*',s=100)
        text_rat='mr/mp='+str(ref[8])+';'
        plt.text(-1.37, -1.2, text_rat, fontsize = 12)
    
    if fig4=='true':
        plt.savefig(out_name_mat)
    
    
    
    plt.show()
    
main()
