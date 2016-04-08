#!/usr/bin/env python
import matplotlib as mpl
mpl.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from random import random as rand
mpl.rc('figure',facecolor='white')

def main():	
	num_points = 150								#-----random point (x,y) generator (set num)-----#	
	points = np.array([[int(1000*rand())/10.,int(1000*rand())/10.] for p in range(num_points)])
	
	plt.title('Experiments in k-means clustering')	#show initial points
	plt.scatter([p[0] for p in points],[p[1] for p in points])
	plt.tight_layout()
	plt.pause(.1) 
	raw_input("#-----Enter to continue-----#")
	plt.close()
	
	K=5												#-----set number of clusters-----#
	clusters = np.array([[int(1000*rand())/10.,int(1000*rand())/10.] for k in range(K)])		
	
	pc_map = [0 for x in range(len(points))]		#pc_map gets assigned cluster index to each point for color-coding (as clustering proceeds)	
	cluster_history = [clusters[i] for i in range(len(clusters))]			#track cluster_history to draw cluster path
	
	num_iter = 10									#-----set number of iterations-----#
	for iter in range(num_iter):					#perform clustering operation num_iter times
		new_c_coll = [np.array([]) for x in range(K)]
		for p in range(len(points)):				#iterate over points to generate cluster_map
			sq_err =  [np.sum(x) for x in np.power(points[p] - clusters,2)]	#get sum of square error for delta(x) and delta(y) to each cluster (as list)
			cluster_idx = sq_err.index(np.min(sq_err))						#find index of min. square error (closest k)
			if new_c_coll[cluster_idx].size > 0:
				new_c_coll[cluster_idx] = np.vstack([new_c_coll[cluster_idx],points[p]])	#if point matrix exists, stack new point
			else:
				new_c_coll[cluster_idx] = np.array(points[p])								#gen new point matrix for cluster	
			pc_map[p] = cluster_idx
		
		for i in range(K):							#update cluster position if points have been assigned to it
			if len(new_c_coll[i]) > 0: 				#	(otherwise maintain cluster position and avoid division by zero)
				clusters[i] = np.round(1.*sum(new_c_coll[i])/len(new_c_coll[i]))

		for i in range(K):							#stack new cluster coordinates onto each cluster record
			cluster_history[i] = np.vstack([cluster_history[i],clusters[i]])

	color_map = [tuple([rand() for rgb in range(3)]) for x in range(K)]		#random color_map for color coding cluster path and associated points
	
	for p in range(len(pc_map)):					#draw each point color-coded according to cluster to which it belongs
		plt.scatter(points[p][0],points[p][1],color=color_map[pc_map[p]])	
	
	for tracks in range(K):							#draw color-coded cluster bubbles and path lines
		plt.plot([x[0] for x in cluster_history[tracks]],[x[1] for x in cluster_history[tracks]],color=color_map[tracks])
		plt.scatter([x[0] for x in cluster_history[tracks]],[x[1] for x in cluster_history[tracks]],[(10*x+5) for x in range(K)],color=color_map[tracks])
	
	plt.title('Experiments in k-means clustering')	#show kmeans result
	plt.tight_layout()
	plt.show()	
		
if __name__ == '__main__':
	main()