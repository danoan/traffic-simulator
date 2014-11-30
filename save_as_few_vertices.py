#!usr/bin/python

#coding:utf-8

import math
import pickle

import networkx as nx
import map_labeling as ml
import map_remove_middle as mr

FOLDER_SAVINGS = "maps_read"

def main():
	# filename = raw_input("Enter the map filename: ")
	
	l = ['sao paulo menor.nx', 'sao paulo maior.nx', 'cidade mexico menor.nx', 'cidade mexico maior.nx', 'manhattan menor.nx', 'manhattan maior.nx', 'london menor.nx', 'london maior.nx']
	for filename in l:

		print "DOING FOR %s: " % (filename,)
		with open("%s/full_vertices/%s" % (FOLDER_SAVINGS,filename),"rb") as inputfile:
			g = pickle.load(inputfile)

			print "LABELING"
			dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)

	    	g = mr.map_remove_middle(g,street_nodes_order)		

	    	print "SAVING"
	    	with open("%s/few_vertices/%s" % (FOLDER_SAVINGS,filename),"wb") as outfile:
	    		pickle.dump(g,outfile)

if __name__=='__main__':
	main()
