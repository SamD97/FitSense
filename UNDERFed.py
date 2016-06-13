# UNDERFed v1.0
# By Saumil Shah
# main

import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit
from scipy.stats import chisquare

def initMeal():
    
    print ()
    print (' {}'.format('='*70))
    print ()
    print (' {:^70s}'.format('UNDERFed v1.0'))
    print ()
    print (' {:^70s}'.format('UNDERFed aims to automatize the process of data'))
    print (' {:^70s}'.format('fitting in bulk and provides several assesmants'))
    print (' {:^70s}'.format('to evaluate the goodness-of-fit.'))
    print ()
    print (' {}'.format('='*70))
    print ()
    print (' {:^70s}'.format('This program was made as a part of summer project'))
    print (' {:^70s}'.format('by Saumil Shah.'))
    print (' {:^70s}'.format('email: saumil.shah@students.iiserpune.ac.in'))
    print ()
    print (' {}'.format('='*70))
    print (' {:^70s}'.format('Example'))
    print (' {}'.format('='*70))
    print ()
    print (' dummy file: ')
    print (' /home/username/Documents/Example.xyz')
    print ()
    print (' [TYPE 1]')
    print (' [independent]\t[dependent]')
    print ('  11\t\t 12')
    print ('  21\t\t 22')
    print ('  31\t\t 32')
    print ('  .\n  .\n  .')
    print ()
    print (' [TYPE 2]')
    print (' [dependent]\t[independent]')
    print ('  11\t\t 12')
    print ('  21\t\t 22')
    print ('  31\t\t 32')
    print ('  .\n  .\n  .')
    print ()
    print (' path = /home/username/Documents')
    print ()
    print (' extension = xyz ')
    print (" examples: 'csv', 'dat', 'xvg' etc.")
    print ()
    print (' delimiter = tab ')
    print (" examples: 'tab', 'comma', 'space'")
    print ()
    print (' type = 1')
    print (" examples: '1', '2'")
    print ()
    print (' {}'.format('='*70))
    
def eatData():
    
    global path, fext, dlim, no_f, name, dtype, title, xaxis, yaxis
    
    path = input(' Please enter path to folder: ')
    fext = input(' Please enter extension of files: ')
    print (delimiters)
    dlim = delimiters[input(' Please enter delimiter: ')]
    dtype = int(input(' Please enter type of file: '))
    title = input(' Please enter title of the plots: ')
    xaxis = input(' Please enter x-axis label of the plots: ')
    yaxis = input(' Please enter y-axis label of the plots: ')
    
    for file in os.listdir(path):
        if file.endswith(fext):
            name.append(file)
    
    name.sort()
    no_f = len(name)
    
    return path, fext, dlim, no_f, name, dtype, title, xaxis, yaxis
    
def chewData():
    
    global path, name, fext, dlim, nrow
    
    os.chdir(path)
    
    print ()
    print (' {}'.format('='*70))
    print (' {:^70s}'.format('File-list'))
    print (' {}'.format('='*70))
    print ()
    
    i = 0
    while i < no_f:
        with open(name[i], 'r') as temp:
            nrow[i] = sum(1 for line in temp)
        
        print (' {:^50s}   entries:{}'.format(name[i], nrow[i]))
        i += 1
    
    print ()
    print (' {}'.format('='*70))
    print (' \t\tTotal {} .{} files were found.'.format(no_f, fext))
    print (' {}'.format('='*70))
    print ()
    print ()
    
    return nrow
        
def swallowData():
    
    global path, name, i, y, x, dtype
    
    os.chdir(path)
    
    if dtype == 1:
        x, y = np.genfromtxt(name[i], dtype=float, delimiter=dlim, unpack=True)
    elif dtype == 2:
        y, x = np.genfromtxt(name[i], dtype=float, delimiter=dlim, unpack=True)
    
    return y, x
    
def digestData():
    
    global path, name, i, y, x, otxt, fext, no_f, title, xaxis, yaxis
    
    # p0 contains initial guess for coefficients, remove incase of no guesses
    popt, pcov = curve_fit(cuisine, x, y, p0=(100, 2, 0.9))
    
    plt.figure()
    plt.plot(x, y, 'ko', label='Experimental Data', markersize=2)
    plt.plot(x, cuisine(x, *popt), 'r-', label='Fitted Curve')
    plt.grid()
    plt.legend()
    plt.title(title + ' - ' + name[i][:-4])
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    pdf.savefig()
    plt.close()
    
    sys.stdout.write('\r[{}{}] {}% {}\t'.format('#'*int(((i+1)*70)/no_f),'-'*int(((no_f-i-1)*70)/no_f), int(((i+1)*100)/no_f), name[i]))
    sys.stdout.flush()

    with open('output.txt', 'a') as otxt:
        otxt.write(name[i][:-4])
        # change the next otxt.write with your description of coefficients
        otxt.write('\twdepth: {:.2f}\tblength: {:.2f}\tfreq: {:.2f}'.format(*popt))
        otxt.write('\n chi-squared = {:.3f} \tp = {:.5f}'.format(*chisquare(y, cuisine(x, *popt))))
        otxt.write('\t\t r-squared = {:.3f} \n\n'.format(np.corrcoef(y, cuisine(x, *popt))[0,1]))
    
    return popt, pcov

# change this dummy function with your function
def cuisine(x, a1,b1,c1):
    return ( a1*( np.power((1-np.exp(-c1*(x-b1))),2) - 1 ) )

initMeal()
    
path = ''
fext = ''
delimiters = {'tab'     : '\t'  ,
              'comma'   : ','   ,
              'space'   : None  ,
              'colon'   : ':'   ,
              'scolon'  : ';'
              }
dtype = 1
title = ''
xaxis = ''
yaxis = ''
no_f = 0
name = []

eatData()

nrow = [0]*no_f

chewData()

i = 0
with PdfPages('Plots.pdf') as pdf:
    while i < no_f:
    
        y = np.zeros((1, nrow[i]), dtype=float)
        x = np.zeros((1, nrow[i]), dtype=float)
    
        swallowData()
    
        digestData()
    
        i += 1
    
with open('output.txt', 'a') as otxt:
    otxt.write(' These results were generated using UNDERFed.\n\n' )