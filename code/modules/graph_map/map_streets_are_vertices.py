#!usr/bin/python

#coding:utf-8

import math
import pickle
import matplotlib.pyplot as plt

from graph_map import *
import networkx as nx

import map_global as mg

import map_labeling as ml
import map_weight as mp
import map_direct as md
import map_remove_middle as mr    
import map_metrics as mm
import map_draw as mdr

def discover_streets_intersections(g,dict_streets_nodes_ordered):
    dict_street_intersections = {}

    # print dict_streets_nodes_ordered["Rua Silva Freire"]
    for s in dict_streets_nodes_ordered.keys():
        nodes = dict_streets_nodes_ordered[s]
        dict_street_intersections.update({s:[]})

        for n in nodes:
            for neigh in g[n]:
                if g[n][neigh]['data'].tags.has_key('name'):
                    inters = g[n][neigh]['data'].tags['name']
                    if inters != s:
                        dict_street_intersections[s].append(inters)

    return dict_street_intersections

def map_streets_are_vertices(g,dict_streets_nodes_ordered):
    dict_streets_intersections = discover_streets_intersections(g,dict_streets_nodes_ordered)
    ng = nx.Graph()

    for s in dict_streets_intersections.keys():        
        ng.add_node(s)

        if len(dict_streets_nodes_ordered[s])>1:
            first_vertice = dict_streets_nodes_ordered[s][1]
        else:
            first_vertice = dict_streets_nodes_ordered[s][0]

        ng.node[s]['data'] = g.node[first_vertice]['data']
        ng.node[s]['weight'] = 1

    for s in dict_streets_intersections.keys():
        inters_list = dict_streets_intersections[s]
        for i in inters_list:
            ng.add_edge(s,i)
            inters_name = "%s - %s" % (s,i)
            ng[s][i]['data'] = Way(inters_name,None)
            ng[s][i]['data'].tags = {'name':inters_name }
            ng[s][i]['weight'] = 1

    return ng

def compute(mapname,filename):
    g = pickle.load(open(filename,"rb")) 
    dict_streets_nodes,street_end_points,dict_endpoints_streets,street_nodes_order = ml.get_labeling_info(g)

    g = map_streets_are_vertices(g,street_nodes_order)
    ebc,m = mm.compute_vertex_betweenness(g)

    return ebc,m    

def run(mapname,filename):
    mdr.draw_streets_as_vertices(g,ebc,m)    

def main():
    mapname = raw_input("Enter the map mapname: ")
    filename = "%s/%s" % (mg.FOLDER_SAVINGS,mapname)
    return run(mapname,filename)

if __name__=='__main__':
    main()
