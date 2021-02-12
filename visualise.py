
from __future__ import print_function

import math 
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import os
from functions import ackley_function, griewank, schaeffer
from mpl_toolkits.mplot3d import Axes3D
import functools
import time
from scipy import optimize
import matplotlib.animation as animation

from scipy.optimize import minimize
from PSO import pso, optimize


def convergence(n_iterations,func_name=''):
	
	
	# Limits of the function being plotted   
	plt.plot((0,n_iterations),(0,0), '--g', label="min$f(x)$")


	ax1 = plt.axes()
	ax1.plot(np.arange(n_iterations),fi,label='Nelder-Mead')
	ax1.plot(np.arange(len(fi2)),fi2,label='BFGS')
	# Convergence of the best particle 
	ax1.plot(history['global_best'])
	plt.legend(['$f$ min','Nelder-Mead','BFGS','PSO','PSO'])

	ax1.set_xlim((0,n_iterations))
	ax1.set_ylabel('$f(x)$')
	ax1.set_xlabel('$i$ (iteration)')
	ax1.set_title('Convergence Plot'.format(func_name))
	
	plt.show()

def visualise(f=None, history=None, bounds=None, minima=None, func_name=''):

    """Visualize the process of optimizing
    # Arguments
    
        func: object function
        history: dict, object returned from pso above
        bounds: list, bounds of each dimention
        minima: list, the exact minima to show in the plot
        func_name: str, the name of the object function

    """


    # define meshgrid according to given boundaries
    x = np.linspace(bounds[0][0], bounds[0][1], 50)
    y = np.linspace(bounds[1][0], bounds[1][1], 50)
    X, Y = np.meshgrid(x, y)
    Z = np.array([f([x, y]) for x, y in zip(X, Y)])
    


    fig = plt.figure(figsize=(12, 6))
    ax1 = plt.axes()

    def animate(frame, history):

        ax1.cla()
        ax1.set_xlabel('X1')
        ax1.set_ylabel('X2')
        ax1.set_xlim(bounds[0][0], bounds[0][1])
        ax1.set_ylim(bounds[1][0], bounds[1][1])


        # Particles paths and global best for plotting
        data = history['particles'][frame]
        global_best = np.array(history['global_best'])

        # Contour plot and global minimum
        contour = ax1.contour(X,Y,Z, levels=20, cmap=cm.jet)
        ax1.plot(minima[0], minima[1] ,marker='o', color='black')

        # Plot particles
        ax1.scatter(data[:,0], data[:,1], marker='*', color='red')
        
        if frame > 1:
            for i in range(len(data)):
                ax1.plot([history['particles'][frame-n][i][0] for n in range(2,-1,-1)],
                         [history['particles'][frame-n][i][1] for n in range(2,-1,-1)])
        elif frame == 1:
            for i in range(len(data)):
                ax1.plot([history['particles'][frame-n][i][0] for n in range(1,-1,-1)],
                         [history['particles'][frame-n][i][1] for n in range(1,-1,-1)])

        
    fig.suptitle('PSO Optimisation of {} function'.format(func_name))#, fontsize=14)

    # Run matplotlib animation
    ani = animation.FuncAnimation(fig, animate, fargs=(history,),
                    frames=len(history['particles']), interval=20, repeat=False, blit=False)
                    
    # Save animation as gif
    #ani.save('PSO_schaeffer.gif', fps=10)
                    
    plt.show()



# Visualise results 

for f in [schaeffer, griewank, ackley_function]:


        history = pso(f, bounds = [[-5,5],[-5,5]], particle_size = 20, inertia = 0.5,w_min = 0.6, w_max = 0.7, n_iterations = 20, func_name = 'Ackley')

        print('global best:',history['global_best'][-1], ', global best position:', history['global_best'][-1])

        visualise(f=f, history=history, bounds=[[-5,5],[-5,5]], minima=[0,0], func_name= 'Ackley') 


        # initial guess 
        x0=[(-2,2)] 

        for model in ['nelder-mead','bfgs']:

            for a in [False, True]:
            
                if model == 'nelder-mead' and a == False:
                
                    xi,yi,fi = optimize(x0,f,model)
                    
                if model == 'bfgs' and a == True:
                    xi2,yi2,fi2 = optimize(x0,f,model)
                    
                    
        #Plot convergence
        convergence(n_iterations = 19,func_name = '')



