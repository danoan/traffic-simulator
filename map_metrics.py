#!/usr/bin/python

#coding:utf-8

import pickle
import networkx as nx
import map_labeling as ml
import map_weight as mp
import matplotlib.pyplot as plt

FOLDER_SAVINGS = "maps_read"
FOLDER_IMG = "images"

def draw(g,street_nodes_order,ebc,max_ebc,save_name="saida.png"):
    pos = {node_id:(g.node[node_id]['data'].lat,g.node[node_id]['data'].lon) for node_id in g.nodes()}

    edge_colors = []
    street_to_label = {}
    for e in g.edges():
        edge_colors.append( -ebc[e]/(1.0*max_ebc) )
        
        if ebc[e]>=(max_ebc*0.4):
            if g.edge[e[0]][e[1]]['data'].tags.has_key('name'):
                street_to_label.update({g.edge[e[0]][e[1]]['data'].tags['name']:True})
            else:
                print "NONAME"        

    edge_labels = {e:"" for e in g.edges()}
    for s in street_to_label.keys():#street_nodes_order.keys():
        nodes = street_nodes_order[s]
        m = ( len(nodes)/2 ) -1

        if g[nodes[m]].has_key(nodes[m+1]):
            edge_labels.update( { (nodes[m],nodes[m+1]):s} )         
        else:
            edge_labels.update( { (nodes[m+1],nodes[m]):s} )

    nx.draw_networkx(g,pos=pos,font_size=8,with_labels=False,node_size=0,arrows=False,edge_color=edge_colors,edge_cmap=plt.cm.RdYlGn, edge_vmin=-1.0, edge_vmax=0.0)
    nx.draw_networkx_edge_labels(g,font_size=8,alpha=0.5,label_pos=0.5,pos=pos,edge_labels=edge_labels)
    # plt.savefig("%s/%s" % (FOLDER_IMG,save_name),dpi=1200)
    plt.show()

def compute_betweenness(g):
    mp.weight_graph(g)
    ebc = nx.edge_betweenness_centrality(g,'weight')

    m = 0
    for v in ebc.values():
        if v>m:
            m = v

    return ebc,m    

def main():
    map_filename = raw_input("Enter with the map filename: ")
    g = pickle.load(open("%s/%s" % (FOLDER_SAVINGS,map_filename),"rb"))

    dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)
    ebc,m = compute_betweenness(g)
    

    draw(g,street_nodes_order,ebc,m)

if __name__=='__main__':
    main()