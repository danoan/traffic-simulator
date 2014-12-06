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

def compute(mapname,filename):
	print "DOING FOR %s: " % (mapname,)
	g = pickle.load(open("%s" % (filename,),"rb"))	

	print "LABELING"
	dict_streets_nodes,street_end_points,dict_endpoints_streets,street_nodes_order = ml.get_labeling_info(g)
	print "WEIGHT"
	mp.weight_graph(g)
	print "DIRECT"
	dg = md.map_direct(g,street_nodes_order)

	print "BETWEENNESS"
	ebc,m = mm.compute_edge_betweenness(dg)

	return ebc,m

def run(mapname,filename):
	ebc,m = compute(mapname,filename)
	mdr.draw_edge_betweenness(dg,street_nodes_order,ebc,m,save_name="%s.png" % (mapname,))

def main():
	'''
		Compute the edge betweenness metric of centrality for a Networkx graph of an OpenStreetMap map.
		The graph is generated at the end and the edges with higher betweenness are colored differently 
		and has its street name labeled.

		Maps can be retrieved from two different folders: few_vertices and full_vertices
	'''
	mapname = raw_input("Enter the map mapname: ")
	run( mapname, "%s/%s" % (mg.FOLDER_SAVINGS,mapname) )

if __name__=='__main__':
	main()
