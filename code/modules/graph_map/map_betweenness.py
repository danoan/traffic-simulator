#!usr/bin/python

#coding:utf-8

import math
import pickle

import networkx as nx

import map_global as mg

import map_labeling as ml
import map_weight as mp
import map_direct as md
import map_metrics as mm
import map_draw as mdr

def run(filename):
	print "DOING FOR %s: " % (filename,)
	g = pickle.load(open("%s/%s" % (mg.FOLDER_SAVINGS,filename),"rb"))	

	print "LABELING"
	dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)
	print "WEIGHT"
	mp.weight_graph(g)
	print "DIRECT"
	dg = md.map_direct(g,street_nodes_order)

	print "BETWEENNESS"
	ebc,m = mm.compute_edge_betweenness(dg)

	mdr.draw_edge_betweenness(dg,street_nodes_order,ebc,m,save_name="%s.png" % (filename.split(".")[0],))

def main():
	'''
		Compute the edge betweenness metric of centrality for a Networkx graph of an OpenStreetMap map.
		The graph is generated at the end and the edges with higher betweenness are colored differently 
		and has its street name labeled.

		Maps can be retrieved from two different folders: few_vertices and full_vertices
	'''
	filename = raw_input("Enter the map filename: ")
	run(filename)

if __name__=='__main__':
	main()
