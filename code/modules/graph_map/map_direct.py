#!usr/bin/python

#coding:utf-8

import math
import pickle

from graph_map import *
import networkx as nx

import map_labeling as ml
import map_global as mg

REMOVE_NONAME=True	#Streets with noname, and vertices belonged to it, will not be representend

def map_direct(g,dict_streets_nodes_ordered):
	'''	Assuming the edges from the undirected graph are written in the right direction, I can't
		transform the undirected in a directed version (g.to_directed), because when I would run 
		the for loop to take over the extra edges on one way streets, I might take out the wrong
		edge. Therefore, the safest way to do it is to construct the digraph by myself
	'''

	dg = nx.DiGraph()
	dg.add_nodes_from(g)
	for n in g.nodes():
		data = g.node[n]['data']		
		dg.node[n]['data'] = Node(data.id, data.lon, data.lat)

	for e in g.edges():
		dg.add_edge(e[0],e[1])
		dg[e[0]][e[1]]['data'] = g[e[0]][e[1]]['data']

	for st in dict_streets_nodes_ordered.keys():		
		nodes = dict_streets_nodes_ordered[st]

		if not g[nodes[0]][nodes[1]]['data'].tags.has_key('oneway'):
			continue

		if g[nodes[0]][nodes[1]]['data'].tags['oneway']=='no':
			for i in xrange(0,len(nodes)-1):
				dg.add_edge(nodes[i+1],nodes[i])
				dg[nodes[i+1]][nodes[i]]['data'] = g[nodes[i]][nodes[i+1]]['data']

	print "TOTAL EDGES (UNDIRECTED VERSION): %d\nTOTAL EDGES (DIRECTED VERSION): %d" % ( len(g.edges()),len(dg.edges()) )

	return dg

def run(filename):
	g = pickle.load(open("%s/%s" % (mg.FOLDER_SAVINGS,filename),"rb"))	
	dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)

	return map_direct(g,street_nodes_order)	

def main():
	filename = raw_input("Enter the map filename: ")
	return run(filename)

if __name__=='__main__':
	main()
