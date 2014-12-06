#!usr/bin/python

#coding:utf-8

import pickle
import networkx as nx
import matplotlib.pyplot as plt

import map_global as mg

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
        dict_streets_endpoints[s] = [ s_nodes.values()[0] ]  #Silva Freire eh Circular (Meier.nx)
        for node in s_nodes.values(): #For each node belonging to that street
            e = g.edge[node['data'].id]    #Check the neighbors of this node            

            l = filter( lambda x: x in s_nodes, e.keys() )
            if len(l) == 1: #If this node has only one neighbor in street s
                if node==dict_streets_endpoints[s][0]:
                    continue
                # print "FOUND IT"
                dict_streets_endpoints[s].append(node)
                break

    return dict_streets_endpoints

def street_version(name,version):
    if version==0: 
        return name
    else: 
        return "%s $(%s)$" % (name,version,)

def walk_path(g,street,begin_point,already_visited):    
    path = []

    if begin_point in already_visited:
        return path

    cur_node_id = begin_point
    already_visited.append(cur_node_id)

    while cur_node_id != None:
        path.append(cur_node_id)
        e = g.edge[cur_node_id] #Fetch the info about the edges of cur_node_id

        cur_node_id = None              
        for neigh_id in e.keys():   #For each neighbor of cur_node_id
            if not e[neigh_id]['data'].tags.has_key('name'):
                continue
            if e[neigh_id]['data'].tags['name']==street:  #If the neighbor has an edge with cur_node_id in street s
                if neigh_id not in already_visited: #Make sure it is an unvisited one
                    cur_node_id = neigh_id
                    already_visited.append(neigh_id)
                    break   #That`s only one per street--xx--Its not true. Some streets are circular    
    return path

def visit_in_order(streets_end_point,dict_streets_nodes,g):
    dict_streets_nodes_ordered = {}   #Dictionary whose key is the street name and the value a list of nodes                             
                                      #ordered by the sequence of the nodes along the street    

    dict_endpoints_streets = {}
    for s in streets_end_point.keys():

        version = 0
        already_visited = []
        for end in streets_end_point[s]:
            path = walk_path(g,s,end['data'].id,already_visited)
            if len(path)==0:
                continue

            st_name = street_version(s,version)
            dict_streets_nodes_ordered[st_name] = path

            version +=1

        for node in dict_streets_nodes[s]:
            if node in already_visited:
                continue

            path = walk_path(g,s,node,already_visited)
            if len(path)==0:
                continue

            st_name = street_version(s,version)
            dict_streets_nodes_ordered[st_name] = path

            version +=1


        #TODO: Nao Esta funcionando
        for i in xrange(1,len(dict_streets_nodes_ordered[s])):
            n0 = dict_streets_nodes_ordered[s][i-1]
            n1 = dict_streets_nodes_ordered[s][i]

            dict_endpoints_streets.update( { (n0,n1):s } )
            dict_endpoints_streets.update( { (n1,n0):s } )

    s=0
    for i in xrange(0,10):
        key = street_version("Rua Dias da Cruz",i)        
        if not dict_streets_nodes_ordered.has_key(key):
            break
        else:
            s+= len( dict_streets_nodes_ordered[key] )
        print key
    print "DIAS DA CRUZ ", s

    return dict_streets_nodes_ordered,dict_endpoints_streets

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
    street_nodes_order,dict_endpoints_streets = visit_in_order(street_end_points,dict_streets_nodes,g)

    for s in dict_streets_nodes.keys():
        if len(dict_streets_nodes[s])!=len(street_nodes_order[s]):
            print s.encode("ascii","ignore"),len(dict_streets_nodes[s].keys()),len(street_nodes_order[s])

    # draw(g,street_nodes_order)

    return dict_streets_nodes,street_end_points,dict_endpoints_streets,street_nodes_order

def run(filename):
    g = pickle.load(open("%s/%s" % (mg.FOLDER_SAVINGS,filename),"rb"))
    return get_labeling_info(g)

def main():
    filename = raw_input("Enter with the map filename: ")
    filename = "few_vertices/meier.nx"
    return run(filename)

if __name__=='__main__':
    main()