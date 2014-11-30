#!usr/bin/python

#coding:utf-8

import math
import pickle

import networkx as nx
import map_labeling as ml
import map_weight as mp
import map_direct as md
import map_metrics as mm

FOLDER_SAVINGS = "maps_read"

def main():
	filename = raw_input("Enter the map filename: ")
	
	# l = ['london.nx', 'london menor.nx']
	# for filename in l:

	print "DOING FOR %s: " % (filename,)
	g = pickle.load(open("%s/%s" % (FOLDER_SAVINGS,filename),"rb"))	

	print "LABELING"
	dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)
	print "WEIGHT"
	mp.weight_graph(g)
	print "DIRECT"
	dg = md.map_direct(g,street_nodes_order)

	print "BETWEENNESS"
	ebc,m = mm.compute_betweenness(dg)

	# print street_nodes_order["Rua Dias da Cruz"]
	# print street_nodes_order["Rua Galdino Pimentel"]
	# print filter( lambda x: x in street_nodes_order["Rua Dias da Cruz"], street_nodes_order["Rua Galdino Pimentel"])

	mm.draw(dg,street_nodes_order,ebc,m,save_name="%s.png" % (filename.split(".")[0],))

if __name__=='__main__':
	main()
