#coding:utf-8

import math

import networkx as nx
import matplotlib.pyplot as plt

import traf_events as te

def draw(g,vi_map=None,traffic_map=None,events=[],with_labels=False,save=False,filename="out.png"):
    pos = {node_id:(g.node[node_id]['data'].lon, g.node[node_id]['data'].lat) for node_id in g.nodes()}

    node_color = [(1,1,1) for i in g.nodes() ]
    if traffic_map!=None:
        for e in events:
            mesh_node = e.path[ e.pos ]
            if e.status == te.TrafficEvent.RUNNING:
                # print "PAINTING",e.id, e.pos, e.path[ e.pos ], g.nodes()[ e.path[ e.pos ] ]

                blue = math.floor(e.last_5_avg_speed)/2.0
                if blue>1:
                    blue = 1

                red=0
                if blue<1/20.0:
                    red = 1-10*blue

                node_color[ mesh_node ] = (red,0,blue)
            elif e.status == te.TrafficEvent.FINISHED:
                node_color[ mesh_node ] = (1,1,1)

    fig = plt.figure(frameon=False,dpi=90)
    ax = fig.add_axes( [0,0,2,2])
    ax.axis('off')
    nx.draw_networkx(g,pos=pos,arrows=False,node_size=18,with_labels=with_labels,linewidths=0.2,node_color=node_color,vmin=0,vmax=10)
    if save:
        plt.savefig(filename,dpi=70,bbox_inches='tight')       
    else:
        plt.show()
    plt.close(fig)  