from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import random
import math


def griewank(x):
	
	n = len(x)
	
	sum = 0
	
	product = 1

	for i in range (1,n):

		sum += x[i]**2/4000

	for i in range(n):
	
		product *= np.cos(x[i]/np.sqrt(i+1))
	
	y = sum - product + 1
	
	return y
	
def ackley_function(x):

	x1 = x[0]
	
	x2 = x[1]

	p1 = -0.2*np.sqrt(0.5*(x1*x1 + x2*x2))
	
	p2 = 0.5*(np.cos(2*math.pi*x1) + np.cos(2*np.pi*x2))
	
	y = np.exp(1) + 20 -20*np.exp(p1) - np.exp(p2)
	
	return y


def schaeffer(x):
	
	x1 = x[0]
	
	x2 = x[1]

	f1 = (np.sin(x1**2-x2**2))**2 - 0.5
	
	f2 = (1 + 0.001*(x1**2+x2**2))**2

	y = 0.5 + f1/f2

	return y 
	

	
X = np.linspace(-5, 5, 50)    
Y = np.linspace(-5, 5, 50) 

# Define the meshgrid 
xg, yg = np.meshgrid(X, Y)

# Plot the function 
fig = plt.figure()


#plt.plot(X,schaeffer([X,X]))

#3d plotting
ax = fig.gca(projection='3d')
cset = ax.contourf(xg, yg, schaeffer(([xg, yg])), zdir='z', offset=np.min(griewank(([xg, yg]))), cmap=cm.jet)
ax.plot_surface(xg, yg, schaeffer([xg, yg]), rstride=1, cstride=1, cmap=cm.jet)
ax.set_title('Schaeffer function')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
