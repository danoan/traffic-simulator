#!usr/bin/python

#coding:utf-8

import math
import pickle
import matplotlib.pyplot as plt

import open_to_netx as onx
import networkx as nx
import map_labeling as ml
import map_weight as mp
import map_direct as md
import map_remove_middle as mr

FOLDER_SAVINGS = "maps_read"

def draw(g,ebc,max_ebc,save_name="saida.png"):
    node_colors = []
    nodes_to_label = {n:"" for n in g.nodes()}
    for n in g.nodes():
        node_colors.append( -ebc[n]/(1.0*max_ebc) )
        
        if ebc[n]>=(max_ebc*0.4):
            print n
            nodes_to_label.update({n:n})

    nx.draw_networkx(g,pos=nx.fruchterman_reingold_layout(g),font_size=12,with_labels=True,labels=nodes_to_label,linewidths=None,node_size=30,arrows=False,node_color=node_colors,cmap=plt.cm.RdYlGn, vmin=-1.0, vmax=0.0)
    # plt.savefig("%s/%s" % (FOLDER_IMG,save_name),dpi=1200)
    plt.show()

def compute_betweenness(g):
    ebc = nx.betweenness_centrality(g,weight='weight')

    m = 0
    for v in ebc.values():
        if v>m:
            m = v

    return ebc,m        

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

        first_vertice = dict_streets_nodes_ordered[s][1]
        ng.node[s]['data'] = g.node[first_vertice]['data']
        ng.node[s]['weight'] = 1

    for s in dict_streets_intersections.keys():
        inters_list = dict_streets_intersections[s]
        for i in inters_list:
            ng.add_edge(s,i)
            inters_name = "%s - %s" % (s,i)
            ng[s][i]['data'] = onx.Way(inters_name,None)
            ng[s][i]['data'].tags = {'name':inters_name }
            ng[s][i]['weight'] = 1

    return ng


def main():
    filename = raw_input("Enter the map filename: ")
    g = pickle.load(open("%s/%s" % (FOLDER_SAVINGS,filename),"rb")) 
    dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)

    g = map_streets_are_vertices(g,street_nodes_order)
    ebc,m = compute_betweenness(g)

    draw(g,ebc,m)    

    return g

if __name__=='__main__':
    main()
