#!/usr/bin/python
#coding:utf-8

import os
import random
import time

import traf_events as te
import traf_draw as tdr

OUTPUT_IMAGES_FOLDER = "output/images"

def setup():
    if not os.path.exists(OUTPUT_IMAGES_FOLDER):
        os.makedirs(OUTPUT_IMAGES_FOLDER)

setup()

class TrafficDynamic:
    def __init__(self,gmesh,events,total_time=20,total_events=10,vmax=10):
        self.gmesh = gmesh
        self.events = events
        self.total_time = total_time
        self.vmax = vmax

        self.node_edge_map = {}
        self.edge_total_time = {}

        self.gmesh_draw = self.gmesh.__draw_mesh__(self.gmesh.g,self.gmesh.vi_map,self.gmesh.dict_edges,self.gmesh.nmid_director,gmesh.min_gap)
        self.traffic_map = {}

    def build_mesh_path(self,path,dict_edges):
        mesh_path = []
        for i in xrange(0,len(path)-1):
            u = path[i]
            v = path[i+1]
            umap = self.gmesh.vi_map[u]
            vmap = self.gmesh.vi_map[v]
            if dict_edges.has_key( (u,v) ):

                for node in dict_edges[(u,v)][:-1]:
                    mesh_path.append(node)
                    if node!=path[0]:
                        self.node_edge_map.update( {node:(umap,vmap)} )

        mesh_path.append( self.gmesh.vi_map[ path[-1] ] )       
        return mesh_path

    def update_position(self,e):
        self.traffic_map[ e.path[e.pos] ] = False
        e.pos += int(e.vel)
        self.traffic_map[ e.path[e.pos] ] = True

    def log(self,s):
        # print s
        pass

    def save_figure(self,t,foldername):
        tdr.draw( self.gmesh_draw, self.gmesh.vi_map, self.traffic_map, self.events,with_labels=False,save=True,filename="%s/%s.png" %(foldername,t,))

    def process_event(self,e):
        if e.status==te.TrafficEvent.NOT_STARTED:
            e.vel = 1.0
            e.status = te.TrafficEvent.RUNNING

            e.path = self.build_mesh_path(e.path,self.gmesh.dict_edges)
            self.traffic_map[ e.path[e.pos] ]=True

            self.log( "STARTING EVENT %d\n %s" % (e.id,e) )         

        elif e.status==te.TrafficEvent.RUNNING:
            current_node = e.path[e.pos]
            if self.node_edge_map.has_key(current_node): #If not, it is a director node, and I can`t say which edge it belongs to
                u,v = self.node_edge_map[current_node]
                if self.edge_total_time.has_key( (u,v) ):
                    self.edge_total_time[(u,v)] += 1
                else:
                    self.edge_total_time[(u,v)] = 1

            if e.pos==len(e.path)-1:
                self.log("EVENT %d HAS FINISHED. POS: %d" % (e.id,e.pos))
                e.status = te.TrafficEvent.FINISHED
                self.traffic_map[ e.path[e.pos] ] = False
            else:   
                    
                gaps_ahead = 0
                for i in xrange(e.pos+1,len(e.path)):
                    if self.traffic_map.has_key( e.path[i] ):
                        if self.traffic_map[e.path[i]]:
                            break
                    gaps_ahead += 1

                if e.vel<gaps_ahead:
                    self.update_position(e)
                    if e.vel<self.vmax:
                        e.vel+=1
                    self.log("EVENT %d WALKING INCREASE: Gaps: %d Velocity: %d Position: %d" % (e.id,gaps_ahead,e.vel,e.pos))
                else:
                    e.vel = gaps_ahead
                    self.update_position(e)
                    self.log("EVENT %d WALKING BREAKING: Gaps: %d Velocity: %d Position: %d" % (e.id,gaps_ahead,e.vel,e.pos))

                if e.vel>0:
                    if random.randint(0,5)==1:
                        e.vel -=1
                        self.log("EVENT %d SLOW DOWN: Gaps: %d Velocity: %d Position: %d" % (e.id,gaps_ahead,e.vel,e.pos))

                e.t_end+=1
        elif e.status==te.TrafficEvent.FINISHED:
            e.status = None

    def run(self,save=True,mapname="mapa_semnome"):
        foldername = "%s/%s_SEG%s_CARROS%s_VMAX%s" % (OUTPUT_IMAGES_FOLDER,mapname,self.total_time,len(self.events),self.vmax)
        if save:            
            if not os.path.exists(foldername):
                os.mkdir(foldername)        

        t = 0
        events_queue = []

        starting_times = {t:[] for t in xrange(0,self.total_time)}
        event_id = 0
        for e in self.events:
            starting_times[e.t_start].append(e)

        sim_start = time.time()
        while t<self.total_time:
            self.log("\n****T=%d****\n" % (t,))
            for e in starting_times[t]:
                events_queue.append(e)

            for i in xrange(len(events_queue)-1,-1,-1):
                e = events_queue[i]
                if self.process_event(e)==te.TrafficEvent.FINISHED:
                    events_queue.remove(e)

            if save:
                self.save_figure(t,foldername)
            t+=1
        sim_end = time.time()
        sim_total_time = sim_end-sim_start

        return self.generate_sim_stats(sim_total_time)

    def generate_sim_stats(self,sim_total_time):
        data = { "Simulation Time": sim_total_time,
                 "Total Events": len(self.events),
                 "Average Speed": 0,
                 "Street Average Speed":{},
                }
        avg_sp = 0
        total_events = len(self.events)
        for e in self.events:
            travel_time = (e.t_end-e.t_start)

            if e.status == te.TrafficEvent.FINISHED:
                avg_sp += len(e.path)/( 1.0*travel_time )
            else:
                total_events-=1
                
        if total_events>0:
            data["Average Speed"] = avg_sp/total_events

        for mesh_edge in self.edge_total_time.keys():
            data["Street Average Speed"].update( {self.gmesh.dict_mesh_edges[mesh_edge]:self.edge_total_time[mesh_edge]} )

        return data