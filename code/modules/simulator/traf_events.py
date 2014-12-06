#coding:utf-8

import random

import networkx as nx
import graph_tool.topology as gt_top

def mockEventsNX(g,t,n,nmid):
    events = []
    for i in xrange(0,n):
        while True:
            b = random.sample(g.nodes(),1)[0]
            e = random.sample(g.nodes(),1)[0]

            if nx.has_path(g,b,e):
                break

        start = random.randint(0,t)
        events.append( TrafficEvent(b,e,nx.shortest_path(g,b,e), start) )
        print i

    return events

def mockEvents(nx_map,gt_map,nx_index,t,n,w,nmid):
    #WAY FASTER
    events = []
    for i in xrange(0,n):
        while True:
            b = gt_map.vertex( random.randint(0,gt_map.num_vertices()-1) )
            e = gt_map.vertex( random.randint(0,gt_map.num_vertices()-1) )

            b1 = nx_index[b]
            e1 = nx_index[e]
            if nx.has_path(nx_map,b1,e1) and b1!=e1:
                break

        start = random.randint(0,t)
        events.append( TrafficEvent(b,e, map(lambda x: nx_index[x], gt_top.shortest_path(gt_map,b,e,weights=w)[0] ), start) )
        print i

    return events    

class TrafficEvent:
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2

    event_id = 0

    def __init__(self,nmid_start,nmid_end,path,t_start):
        self.nmid_start = nmid_start
        self.nmid_end = nmid_end
        self.path = path

        self.t_start = t_start      

        self.pos = 0
        self.vel = None
        self.status = TrafficEvent.NOT_STARTED
        self.t_end = t_start
        self.id = TrafficEvent.event_id

        self.avg_speed = 0
        self.last_5_avg_speed = 0

        TrafficEvent.event_id+=1

    def finish(self,t_end):
        self.t_end = t_end

    def __str__(self):
        return "START: %s \nBEGIN: %s \nEND: %s \nPATH: %s \n" % (self.t_start,self.nmid_start,self.nmid_end,self.path)
