#coding:utf-8

import networkx as nx
import graph_tool as gt
import graph_tool.topology as gt_top

import random
import math

from modules.graph_map import map_direct as md
from modules.graph_map import map_remove_middle as mr
from modules.graph_map import map_labeling as ml
from modules.graph_map import map_weight as mw

from modules.simulator import traf_events as te

import pickle

def mockEventsGT(nx_map,gt_map,nx_index,t,n,w,nmid):
    events = []
    for i in xrange(0,n):
        while True:
            b = gt_map.vertex( random.randint(0,gt_map.num_vertices()-1) )
            e = gt_map.vertex( random.randint(0,gt_map.num_vertices()-1) )

            b1 = nx_index[b]
            e1 = nx_index[e]
            if nx.has_path(nx_map,b1,e1) and b1!=e1:
                break

        start = random.randint(0,t)
        gt_path = map(lambda x: nx_index[x], gt_top.shortest_path(gt_map,b,e,weights=w)[0] )
        events.append( te.TrafficEvent(b,e,gt_path, start) )
        print i

    return events

def mockEventsNX(g,t,n,nmid):
    events = []
    for i in xrange(0,n):
        while True:
            b = random.sample(g.nodes(),1)[0]
            e = random.sample(g.nodes(),1)[0]

            if nx.has_path(g,b,e):
                break

        start = random.randint(0,t)
        events.append( te.TrafficEvent(b,e,nx.shortest_path(g,b,e), start) )
        print i

    return events

def convert(nx_map):
    gt_map = gt.Graph(directed=True)
    
    nx_index = gt_map.new_vertex_property("string")
    gt_index = {}
    for n in nx_map.nodes():
        v = gt_map.add_vertex()
        nx_index[v] = n
        gt_index[n] = v.__int__()

    w_prop = gt_map.new_edge_property("double")
    for e in nx_map.edges():
        new_e = gt_map.add_edge( gt_index[ e[0] ], gt_index[ e[1] ] )
        w_prop[new_e] = nx_map[e[0]][e[1]]['weight']

    return gt_map,nx_index,gt_index,w_prop

def main():
    filename = raw_input("Enter filename: ")
    filename = "output/maps_read/few_vertices/meier.nx"
    nx_map = pickle.load( open(filename,"rb") )

    print "LABELING"
    dict_streets_nodes,street_end_points,dict_endpoints_streets,street_nodes_order = ml.get_labeling_info(nx_map)
    nx_map = mr.map_remove_middle(nx_map,street_nodes_order)      

    print "DIRECT"
    nx_map = md.map_direct(nx_map,street_nodes_order)   
    mw.weight_graph(nx_map) 

    gt_map,nx_index,gt_index,w_prop = convert(nx_map)
    e2 = mockEventsGT(nx_map,gt_map,nx_index,400,100,w_prop,0)
    e1 = mockEventsNX(nx_map,400,100,0)    
    
if __name__=='__main__':    
    main()

