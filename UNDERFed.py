# UNDERFed v1.0
# By Saumil Shah

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare

def initMeal():
    
    print ('')
    print (' {}'.format('='*55))
    print ('')
    print (' {:^55s}'.format('UNDERFed v1.0'))
    print ('')
    print ('     UNDERFed aims to automatize the process of data    ')
    print ('     fitting in bulk and provides several assesmants    ')
    print ('             to evaluate the goodness-of-fit.           ')
    print ('')
    print (' {}'.format('='*55))
    print ('')
    print ('    This program was made as a part of summer project   ')
    print ('                     by Saumil Shah.                    ')
    print ('       email: saumil.shah@students.iiserpune.ac.in      ')
    print ('')
    print (' {}'.format('='*55))
    
    print ('\n example: /home/username/Documents/Example.xyz')
    print ('')
    print (' [y]\t[x1]\t[x2] ...')
    print ('  11\t 12\t 13  ...')
    print ('  21\t 22\t 23  ...')
    print ('  31\t 32\t 33  ...')
    print ('  .\n  .\n  .')
    print ('')
    print (' path = /home/username/Documents')
    print (' extension = xyz ')
    print (" examples: 'csv', 'dat', 'xvg' etc.")
    print (' delimiter = tab ')
    print (" examples: 'tab', 'comma', 'space'")
    
def eatData():
    
    global path, dlim, no_f, name
    
    path = input(' Please enter path: ')
    fext = input(' Please enter extension: ')
    dlim = delimiters[input(' Please enter delimiter: ')]
    
    for file in os.listdir(path):
        if file.endswith('.' + fext):
            name.append(file)
    
    name.sort()
    no_f = len(name)
    
    return path, dlim, no_f, name
    
def chewData():
    
    global path, name, fext, dlim, nrow, nvar
    
    os.chdir(path)
    
    print ('')
    print (' {}'.format('='*55))
    print (' {:^55s}'.format('File-list'))
    print (' {}'.format('='*55))
    print ('')
    
    i = 0
    while i < no_f:
        with open(name[i], 'r') as temp:
            nrow[i] = sum(1 for line in temp)
        with open(name[i], 'r') as temp:
            nvar[i] = len(temp.readline().split(dlim))
        print (' {:^20s}   entries:{}   variables:{}'.format(name[i], nrow[i], nvar[i]))
        i += 1
    
    print ('')
    print (' {}'.format('='*55))
    print (' \t\tTotal {} .'.format(no_f) + fext + ' files were found.')
    print (' {}'.format('='*55))
    
    return nrow, nvar
        
def swallowData():
    
    global path, name, i, y, x
    
    os.chdir(path)
    
    x, y = np.genfromtxt(name[i], dtype=float, delimiter=dlim, unpack=True)
    
    return y, x
    
def digestData():
    
    global path, name, i, y, x, otxt, fext
    
    popt, pcov = curve_fit(cuisine, x, y)
    
    print ('\n')
    print (name[i])    
    print (popt)
    print (pcov)
    
    plt.figure()
    plt.plot(x, y, 'ko', label="Experimental Data")
    plt.plot(x, cuisine(x, *popt), 'r-', label="Fitted Curve")
    plt.legend()
    plt.annotate(' y = {0:.3f}*( exp({1:.3f}*x) ) + {2:.3f}'.format(*popt), xy=(5,2000))
    plt.savefig(path + '/plots/' + name[i][:-3] + 'pdf')
    plt.close()
    
#    print (chisquare(y, cuisine(x, *popt)))
    print (' r-squared = {:.3f}'.format(np.corrcoef(y, cuisine(x, *popt))[0,1]))

    with open('Output.txt', 'a') as otxt:
        otxt.write(name[i][:-4])
        otxt.write('\t\t y = {0:.3f}*( exp({1:.3f}*x) ) + {2:.3f}'.format(*popt))
#        otxt.write('\n chi-squared = {:.3f} p = {:.5f}'.format(*chisquare(y, cuisine(x, *popt))))
        otxt.write('\t\t r-squared = {:.3f} \n'.format(np.corrcoef(y, cuisine(x, *popt))[0,1]))
    
    return popt, pcov
    
def cuisine(x, a, b, c):
    return a * ( np.exp(b*x) ) + c

initMeal()
    
path = ''
fext = ''
delimiters = {'tab': '\t', 'comma': ',', 'space': None}
no_f = 0
name = []

eatData()

nrow = [0]*no_f
nvar = [0]*no_f

chewData()

os.makedirs(path+'/plots', exist_ok=True)

i = 0
while i < no_f:
    
    y = np.zeros((1, nrow[i]), dtype=float)
    x = np.zeros((1, nrow[i]), dtype=float)
    
    swallowData()
    
    digestData()
    
    i += 1
