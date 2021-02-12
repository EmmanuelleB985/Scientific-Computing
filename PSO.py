

from __future__ import print_function
import os
import math 
from numpy.random import rand
from matplotlib import cm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import animation
from functions import ackley_function, griewank, schaeffer
from mpl_toolkits.mplot3d import Axes3D
import functools
import time
from scipy import optimize
from scipy.optimize import minimize
import matplotlib.animation as animation





def optimize(x0, f, m):

	"""
	Run optimisation using scipy optimisation methods
	"""

	all_x_i = []
	all_y_i = []
	all_f_i = []

	def store(X):
		x, y = X
		all_x_i.append(x)
		all_y_i.append(y)
		all_f_i.append(f(X))	
		
	res = minimize(f, x0, method=m, options={'maxiter': 20}, callback = store)
    

	return all_x_i, all_y_i, all_f_i


n_iterations = 19
    

#%matplotlib inline
plt.style.use('bmh')
#@timing
def pso(func, bounds, particle_size=10, inertia=0.5, w_min = 0.6, w_max = 0.7, phi_p=0.8, phi_g=0.9, 
        max_vnorm=10, n_iterations=500, func_name=None):

	"""Particle Swarm Optimization (PSO)

		func: function to be optimized
		bounds: bounds of each dimention
		particle_size: swarm population size
		inertia: weight factor
		w_min: minimum weight used for dynamic weight update
		w_max: maximum weight used for dynamic weight update
		phi_p: particle personal acceleration
		phi_g: particle global acceleration
		max_vnorm: max velocity norm
		nu_iterations: number of iterations
		func_name: the name of function to optimize

	"""
	# Set the bounds
	bounds = np.array(bounds)
	assert np.all(bounds[:,0] < bounds[:,1]), "Unbound x and y limits, the first value of the list needs to be higher"
	dim = len(bounds)

	# Set the search space 
	X = np.random.rand(particle_size, dim)
	print('## Optimize:',func_name)

	def clip_by_norm(x, max_norm):
		norm = np.linalg.norm(x)
		return x if norm <=max_norm else x * max_norm / norm
		
		
	# Implement the adaptive weight factor
	def adaptive_weight(scores):

		mean_score = np.mean(scores)
		min_score = np.min(scores)

		return [new_w(mean_score, score, min_score) for score in scores]

	def new_w(mean_score, score, min_score):

		if score <= mean_score and min_score < mean_score:
			return w_min + (((w_max - w_min) * (score - min_score)) /
					(mean_score - min_score))
		else:
			return w_max

	#Initialize the particles positions randomly in space
	particles = X * (bounds[:,1]-bounds[:,0]) + bounds[:,0]
	velocities = X * (bounds[:,1]-bounds[:,0]) + bounds[:,0]

	personal_bests = np.copy(particles)
	personal_best_fitness = [np.inf for p in particles]
	global_best_idx = np.argmin(personal_best_fitness)
	global_best = personal_bests[global_best_idx]
	global_best_fitness = func(global_best)
	history = {'particles':[],  
				'global_best':[[np.inf, np.inf] for i in range(n_iterations)],
				'obj_func': func_name,}

	#PSO starts
	for i in range(n_iterations):
		
		history['particles'].append(particles)
		history['global_best'][i][0] = global_best[0]
		history['global_best'][i][1] = global_best[1]

		# personal best
		for p_i in range(particle_size):
			fitness = func(particles[p_i])
			if fitness < personal_best_fitness[p_i]:
				personal_bests[p_i] = particles[p_i] 
				personal_best_fitness[p_i] = fitness 

		# global best
		if np.min(personal_best_fitness) < global_best_fitness:
			global_best_idx = np.argmin(personal_best_fitness)
			global_best = personal_bests[global_best_idx]
			global_best_fitness = func(global_best)

		# Set the weight factor based on the scores
		inertia = adaptive_weight(global_best)

		# Compute acceleration and momentum
		m = inertia * velocities
		acc_local = phi_p * np.random.rand() * (personal_bests - particles)
		acc_global = phi_g * np.random.rand() * (global_best - particles)

		# Compute the velocities with updated weight
		velocities = m + acc_local + acc_global
		velocities = clip_by_norm(velocities, max_vnorm)

		#Update the position of particles
		particles = particles + velocities


		print('Global Best:{}, Velocity:{}'.format(global_best, np.linalg.norm(velocities)))
			
	return history


