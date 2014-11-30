#!usr/bin/python

#coding:utf-8

import pickle
import networkx as nx
import matplotlib.pyplot as plt

FOLDER_SAVINGS = "maps_read"
REMOVE_NONAME_VERTICES = True

HIGHWAYS_ACCEPTED = ['motorway','trunk','primary','secondary','tertiary','unclassified','residential','service','motorway_link','trunk_link','primary_link','secondary_link','tertiary_link']

def visit_neighbors_of_node(dict_streets_nodes,g,node):
    e = g.edge[node]
    for node_id in e.keys():
        if not e[node_id]['data'].tags.has_key('highway'):
            g.remove_edge(node,node_id)
            continue

        if not e[node_id]['data'].tags['highway'] in HIGHWAYS_ACCEPTED: 
            g.remove_edge(node,node_id)
            continue

        if not e[node_id]['data'].tags.has_key('name'):
            if REMOVE_NONAME_VERTICES:
                g.remove_edge(node,node_id) #REMOVE EDGES WITH NONAME
            continue
        else:
            street_name = e[node_id]['data'].tags['name']

        if not dict_streets_nodes.has_key(street_name):
            dict_streets_nodes[street_name] = {}

        dict_streets_nodes[street_name].update( {node_id:g.node[node_id]} )

    return dict_streets_nodes

def discover_street_endpoints(dict_streets_nodes,g):
    dict_streets_endpoints = {}     
    for s in dict_streets_nodes.keys(): #For each street
        # print "START"
        s_nodes = dict_streets_nodes[s]        
        dict_streets_endpoints.update({s:s_nodes.values()[0]})  #Silva Freire eh Circular (Meier.nx)
        for node in s_nodes.values(): #For each node belonging to that street
            e = g.edge[node['data'].id]    #Check the neighbors of this node            

            l = filter( lambda x: x in s_nodes, e.keys() )
            if len(l) == 1: #If this node has only one neighbor in street s
                # print "FOUND IT"
                dict_streets_endpoints.update({s:node})
                break

    return dict_streets_endpoints

def visit_in_order(streets_end_point,g):
    dict_streets_nodes_ordered = {}   #Dictionary whose key is the street name and the value a list of nodes                             
                                      #ordered by the sequence of the nodes along the street    

    for s in streets_end_point.keys():
        already_visited = []
        dict_streets_nodes_ordered[s] = []
        cur_node_id = streets_end_point[s]['data'].id
        already_visited.append(cur_node_id)
        while cur_node_id != None:
            dict_streets_nodes_ordered[s].append(cur_node_id)
            e = g.edge[cur_node_id] #Fetch the info about the edges of cur_node_id

            cur_node_id = None            
            for neigh_id in e.keys():   #For each neighbor of cur_node_id
                if not e[neigh_id]['data'].tags.has_key('name'):
                    continue
                if e[neigh_id]['data'].tags['name']==s:  #If the neighbor has an edge with cur_node_id in street s
                    if neigh_id not in already_visited: #Make sure it is an unvisited one
                        cur_node_id = neigh_id
                        already_visited.append(neigh_id)
                        break   #That`s only one per street--xx--Its not true. Some streets are circular

    return dict_streets_nodes_ordered

def draw(g,street_nodes_order):
    pos = {node_id:(g.node[node_id]['data'].lat,g.node[node_id]['data'].lon) for node_id in g.nodes()}
    edge_labels = {e:"" for e in g.edges()}
    for s in street_nodes_order:
        nodes = street_nodes_order[s]
        m = ( len(nodes)/2 ) -1

        edge_labels.update( { (nodes[m],nodes[m+1]):s} )
        edge_labels.update( { (nodes[m+1],nodes[m]):s} )

    nx.draw_networkx(g,pos=pos,with_labels=False,node_size=1)
    nx.draw_networkx_edge_labels(g,pos=pos,edge_labels=edge_labels)
    plt.show()    

def get_labeling_info(g):
    dict_streets_nodes = {} #Dictionary whose key is the street name and the value is a dict of nodes with node key as id
    for node in g.edge.keys():
        dict_streets_nodes = visit_neighbors_of_node( dict_streets_nodes,g,node )

    #REMOVE NODES WITH NO EDGES
    if REMOVE_NONAME_VERTICES:
        count_remove = 0
        for node in g.edge.keys():
            if len(g.edge[node])==0:
                g.remove_node(node)
                count_remove+=1
        print "VERTICES REMOVED FROM NONAME EDGES: ",count_remove

    street_end_points = discover_street_endpoints(dict_streets_nodes,g)
    street_nodes_order = visit_in_order(street_end_points,g)

    # draw(g,street_nodes_order)

    return dict_streets_nodes,street_end_points,street_nodes_order

def main():
    map_filename = raw_input("Enter with the map filename: ")
    g = pickle.load(open("%s/%s" % (FOLDER_SAVINGS,map_filename),"rb"))

    return get_labeling_info(g)

if __name__=='__main__':
    get_labeling_info()