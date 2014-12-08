#!/usr/bin/python
#coding:utf-8

import math
import pickle

import networkx as nx

from graph_map import *

def mockGraph(w,h):
    g = nx.DiGraph()
    g.add_nodes_from(range(0,w*h))
    nid=0
    for i in xrange(0,h):
        for j in xrange(0,w):
            above = (i-1)*w+j
            right = i*w+(j+1)

            if above>=0:
                g.add_edge(nid,above)
                g.add_edge(above,nid)

            if (j+1)<w:
                g.add_edge(nid,right)
                g.add_edge(right,nid)

            g.node[nid]['data'] = Node(nid,j*2,i*2)
            nid+=1

    # mp.weight_graph(g)
    return g 

class GraphMesh:
    def __draw_mesh__(self,g,vi_map,dict_edges,nmid,min_gap):
        #Draws a graph based on the mesh
        gmesh = nx.Graph()
        for node in g.nodes():
            nmap = vi_map[node]
            gmesh.add_node( nmap )
            gmesh.node[nmap]['data'] = g.node[node]['data'] #This is not a deep copy

        for (u,v) in g.edges():
            umap = vi_map[u]
            vmap = vi_map[v]

            gmesh.add_edge( umap, vmap )

        for u,v in dict_edges.keys():
            umap = vi_map[u]
            vmap = vi_map[v]

            lat0 = gmesh.node[umap]['data'].lat
            lon0 = gmesh.node[umap]['data'].lon
            lat1 = gmesh.node[vmap]['data'].lat 
            lon1 = gmesh.node[vmap]['data'].lon
            
            d = [ lon1 - lon0, lat1 - lat0 ]
            length = math.sqrt( d[0]**2 + d[1]**2 )

            if length!=0:
                d[0] = d[0]/length*min_gap
                d[1] = d[1]/length*min_gap
            else:
                d[0] = 0
                d[1] = 0

            if len(dict_edges[ (u,v) ])>2:
                n = int( math.floor(length/min_gap) )

                v0 = umap
                nmid = dict_edges[ (u,v) ][1]
                for i in xrange(1,n):                   
                    gmesh.add_node( nmid )
                    gmesh.node[nmid]['data'] = Node(nmid,lon0+i*d[0],lat0+i*d[1])
                    gmesh.add_edge(v0,nmid)
                    v0 = nmid

                    nmid+=1
                gmesh.add_edge(nmid-1,vmap)

        print "MESH NODES: ",len(gmesh.nodes())
        return gmesh

    def __build_vertex_index_map__(self,g):
        #Maps the original node id with the node mesh id
        nmid = 0
        index_map = {}
        for n in self.g.nodes():
            index_map[n] = nmid
            nmid+=1

        return index_map,nmid


    def __build_dict_edges__(self,g,vi_map,nmid,min_gap):
        #Build a dictionary where the key is edge mesh and the value is the list of mesh nodes
        #in the mesh edge
        dict_edges = {}
        dict_mesh_edges = {}
        for u,v in g.edges():
            umap = vi_map[u]
            vmap = vi_map[v]

            dict_edges.update({(u,v):[umap]})
            dict_mesh_edges.update( { (umap,vmap): (u,v)} )

            lat0 = g.node[u]['data'].lat
            lon0 = g.node[u]['data'].lon
            lat1 = g.node[v]['data'].lat 
            lon1 = g.node[v]['data'].lon
            
            d = [ lon1 - lon0, lat1 - lat0 ]
            length = math.sqrt( d[0]**2 + d[1]**2 )

            if length>min_gap:
                n = int( math.floor(length/min_gap) )

                for i in xrange(1,n):
                    dict_edges[(u,v)].append(nmid)
                    nmid+=1

            dict_edges[(u,v)].append(vmap)

        return dict_edges,dict_mesh_edges,nmid

    def __build_dict_path__(self,dict_edges):
        dict_path = {}
        for u,v in dict_edges.keys():
            nodes = dict_edges[(u,v)]
            nodes = nodes[1:len(nodes)-1]

            dict_path[u] = {}   #Director Node
            dict_path[v] = {}   #Director Node

            distance = len(nodes)
            for n in nodes:
                if not dict_path.has_key(n):
                    dict_path[n] = {}
                dict_path[n].update({v:distance})

        return dict_path


    def __init__(self,g,min_gap=1.0):
        self.g = g

        self.vi_map, self.nmid_director = self.__build_vertex_index_map__(g)
        self.dict_edges, self.dict_mesh_edges, self.nmid = self.__build_dict_edges__(g,self.vi_map,self.nmid_director,min_gap)
        # print len( self.dict_edges.keys() ), len( self.dict_mesh_edges.keys() )
        self.dict_path = self.__build_dict_path__(self.dict_edges) #IT'S NOT BEING USED
        self.min_gap = min_gap

def main():
    w,h=4,6
    g = mockGraph(w,h)
    gm = GraphMesh(g,0.1)    

    return gm

if __name__=='__main__':
    main()