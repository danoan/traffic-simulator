#!usr/bin/python

#coding:utf-8

import math
import pickle

import networkx as nx

import map_global as mg

import map_labeling as ml
import map_metrics as mm
import map_weight as mp
import map_direct as md
import map_draw as mdr

def map_remove_middle(g,dict_streets_nodes_ordered):
    count_remove = 0
    for s in dict_streets_nodes_ordered.keys():
        nodes = dict_streets_nodes_ordered[s]

        if len(nodes)==1:
            continue

        to_keep = []
        to_keep.append( 0 )
        for i in xrange(1,len(nodes)-1):
            n = nodes[i]

            keep = False
            for neigh in g[n]:
                if g[n][neigh]['data'].tags.has_key('name'):
                    if g[n][neigh]['data'].tags['name']!=s:
                        keep = True

            if keep:
                to_keep.append(i)

        to_keep.append( len(nodes)-1 )              
        dict_streets_nodes_ordered[s] = [ nodes[ to_keep[i] ] for i in xrange(0,len(to_keep)) ]  

        data = g[ nodes[0] ][ nodes[1] ]['data']
        for i in xrange(0,len(to_keep)-1):
            b = to_keep[i]
            e = to_keep[i+1]

            g.add_edge( nodes[b], nodes[e] )
            g[ nodes[b] ][ nodes[e] ]['data'] = data
            for r in xrange(b+1,e):
                g.remove_node( nodes[r] )
                count_remove+=1

    print "MIDDLE VERTICES REMOVED ", count_remove

    return g

def run(filename):
    g = pickle.load(open("%s/%s" % (mg.FOLDER_SAVINGS,filename),"rb")) 
    dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)

    g = map_remove_middle(g,street_nodes_order)

    print "WEIGHT"
    mp.weight_graph(g)
    print "DIRECT"
    dg = md.map_direct(g,street_nodes_order)

    ebc,m = mm.compute_edge_betweenness(dg)

    mdr.draw_edge_betweenness(dg,street_nodes_order,ebc,m)    

    return dg

def main():
    filename = raw_input("Enter the map filename: ")
    return run(filename)

if __name__=='__main__':
    main()
