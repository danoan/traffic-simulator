#!usr/bin/python

#coding:utf-8

import math
import pickle
import os

import networkx as nx
import map_labeling as ml
import map_remove_middle as mr

def run(filenames,output_folder="few_vertices"):
	''' graph_create.py creates Networkx graph versions of OpenStreetMap maps. These maps are very well described and 
		because of that, one single street might have a lot of vertices that are needless for our purpose. For example,
		some vertices of Oxford St are there just to mimify the contours of the street, but this particular vertice has
		edge with other two vertices from the same Oxford St (any information is added). Therefore, this piece of code
		removes all those vertices a street might have and don't add any new information to the graph. Streets with no
		names are removed as well. After that, a smaller version of the corresponding graph is saved.
	'''

	for filename in filenames:

		print "DOING FOR %s: " % (filename,)
		with open("%s" % (filename,),"rb") as inputfile:
			g = pickle.load(inputfile)

			print "LABELING"
			dict_streets_nodes,street_end_points,dict_end_points,street_nodes_order = ml.get_labeling_info(g)

	    	g = mr.map_remove_middle(g,street_nodes_order)		

	    	print "SAVING"
	    	map_name = filename.split(os.path.sep)[-1]
	    	with open("%s/%s" % (output_folder,map_name),"wb") as outfile:
	    		pickle.dump(g,outfile)

def main():	
	l = ['meier.nx']
	run(l)


if __name__=='__main__':
	main()
