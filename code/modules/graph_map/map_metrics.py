#!/usr/bin/python

#coding:utf-8
import networkx as nx

import map_global as mg
import map_weight as mp

def compute_edge_betweenness(g):
    mp.weight_graph(g)
    ebc = nx.edge_betweenness_centrality(g,'weight')

    m = 0
    for v in ebc.values():
        if v>m:
            m = v

    return ebc,m    

def compute_vertex_betweenness(g):
    ebc = nx.betweenness_centrality(g,weight='weight')

    m = 0
    for v in ebc.values():
        if v>m:
            m = v

    return ebc,m    
