#coding: utf-8

import networkx as nx
import matplotlib.pyplot as plt

import map_global as mg

def draw_edge_betweenness(g,street_nodes_order,ebc,max_ebc,save_img=False,save_name="saida.png"):
    pos = {node_id:(g.node[node_id]['data'].lat,g.node[node_id]['data'].lon) for node_id in g.nodes()}

    edge_colors = []
    street_to_label = {}
    for e in g.edges():
        edge_colors.append( -ebc[e]/(1.0*max_ebc) )
        
        if ebc[e]>=(max_ebc*0.4):
            if g.edge[e[0]][e[1]]['data'].tags.has_key('name'):
                street_to_label.update({g.edge[e[0]][e[1]]['data'].tags['name']:True})
            #else NONAME

    edge_labels = {e:"" for e in g.edges()}
    for s in street_to_label.keys():
        nodes = street_nodes_order[s]
        m = ( len(nodes)/2 ) -1

        if g[nodes[m]].has_key(nodes[m+1]):
            edge_labels.update( { (nodes[m],nodes[m+1]):s} )         
        else:
            edge_labels.update( { (nodes[m+1],nodes[m]):s} )

    nx.draw_networkx(g,pos=pos,font_size=8,with_labels=False,node_size=0,arrows=False,edge_color=edge_colors,edge_cmap=plt.cm.RdYlGn, edge_vmin=-1.0, edge_vmax=0.0)
    nx.draw_networkx_edge_labels(g,font_size=8,alpha=0.5,label_pos=0.5,pos=pos,edge_labels=edge_labels)

    if save_img:
        plt.savefig("%s/%s" % (mg.EDGE_BETWEENNESS_IMG_FOLDER,save_name),dpi=1200)
    else:
        plt.show()

def draw_streets_as_vertices(g,ebc,max_ebc,save_img=False,save_name="saida.png"):
    node_colors = []
    nodes_to_label = {n:"" for n in g.nodes()}
    for n in g.nodes():
        node_colors.append( -ebc[n]/(1.0*max_ebc) )
        
        if ebc[n]>=(max_ebc*0.4):
            print n
            nodes_to_label.update({n:n})

    nx.draw_networkx(g,pos=nx.fruchterman_reingold_layout(g),font_size=12,with_labels=True,labels=nodes_to_label,linewidths=None,node_size=30,arrows=False,node_color=node_colors,cmap=plt.cm.RdYlGn, vmin=-1.0, vmax=0.0)
    if save_img:
        plt.savefig("%s/%s" % (mg.NODE_BETWEENNESS_IMG_FOLDER,save_name),dpi=1200)
    else:
        plt.show()
