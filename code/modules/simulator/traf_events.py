#coding:utf-8

import random

import networkx as nx

def mockEvents(g,t,n,nmid):
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

        TrafficEvent.event_id+=1

    def finish(self,t_end):
        self.t_end = t_end

    def __str__(self):
        return "START: %s \nBEGIN: %s \nEND: %s \nPATH: %s \n" % (self.t_start,self.nmid_start,self.nmid_end,self.path)
