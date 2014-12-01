#coding:utf-8

import networkx as nx
import matplotlib.pyplot as plt

import traf_events as te

def draw(g,vi_map=None,traffic_map=None,events=[],with_labels=False,save=False,filename="out.png"):
    pos = {node_id:(g.node[node_id]['data'].lon, g.node[node_id]['data'].lat) for node_id in g.nodes()}

    node_color = [-1 for i in g.nodes() ]
    if traffic_map!=None:
        for e in events:
            mesh_node = e.path[ e.pos ]
            if e.status == te.TrafficEvent.RUNNING:
                # print "PAINTING",e.id, e.pos, e.path[ e.pos ], g.nodes()[ e.path[ e.pos ] ]
                node_color[ mesh_node ] = e.id + 5
            elif e.status == te.TrafficEvent.FINISHED:
                node_color[ mesh_node ] = len(events)+10

    fig = plt.figure(frameon=False,dpi=150)
    ax = fig.add_axes( [0,0,2,2])
    ax.axis('off')
    nx.draw_networkx(g,pos=pos,arrows=False,node_size=18,with_labels=with_labels,linewidths=0.2,node_color=node_color,cmap=plt.cm.Blues,vmin=-1,vmax=len(events)+10)
    if save:
        plt.savefig(filename,dpi=150,bbox_inches='tight')       
    else:
        plt.show()
    plt.close(fig)  