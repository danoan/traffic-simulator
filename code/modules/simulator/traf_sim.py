#!/usr/bin/python
#coding:utf-8

import random
import math
import time
import os
import pickle

import networkx as nx
import matplotlib.pyplot as plt

import open_to_netx as onx

import map_weight as mp
import map_direct as md
import map_remove_middle as mr
import map_labeling as ml

def draw(g,vi_map=None,traffic_map=None,events=[],with_labels=False,save=False,filename="out.png"):
	pos = {node_id:(g.node[node_id]['data'].lon, g.node[node_id]['data'].lat) for node_id in g.nodes()}

	node_color = [-1 for i in g.nodes() ]
	if traffic_map!=None:
		for e in events:
			mesh_node = e.path[ e.pos ]
			if e.status == TrafficEvent.RUNNING:
				# print "PAINTING",e.id, e.pos, e.path[ e.pos ], g.nodes()[ e.path[ e.pos ] ]
				node_color[ mesh_node ] = e.id + 5
			elif e.status == TrafficEvent.FINISHED:
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

			g.node[nid]['data'] = onx.Node(nid,j*2,i*2)
			nid+=1

	mp.weight_graph(g)
	return g 

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

			d[0] = d[0]/length*min_gap
			d[1] = d[1]/length*min_gap
			
			if len(dict_edges[ (u,v) ])>2:
				n = int( math.floor(length/min_gap) )

				v0 = umap
				nmid = dict_edges[ (u,v) ][1]
				for i in xrange(1,n):					
					gmesh.add_node( nmid )
					gmesh.node[nmid]['data'] = onx.Node(nmid,lon0+i*d[0],lat0+i*d[1])
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
		for u,v in g.edges():
			umap = vi_map[u]
			vmap = vi_map[v]

			dict_edges.update({(u,v):[umap]})

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

		return dict_edges,nmid

	def __build_dict_path__(self,dict_edges):
		dict_path = {}
		for u,v in dict_edges.keys():
			nodes = dict_edges[(u,v)]
			nodes = nodes[1:len(nodes)-1]

			dict_path[u] = {}	#Director Node
			dict_path[v] = {}	#Director Node

			distance = len(nodes)
			for n in nodes:
				if not dict_path.has_key(n):
					dict_path[n] = {}
				dict_path[n].update({v:distance})

		return dict_path


	def __init__(self,g,min_gap=1.0):
		self.g = g

		self.vi_map, self.nmid_director = self.__build_vertex_index_map__(g)
		self.dict_edges, self.nmid = self.__build_dict_edges__(g,self.vi_map,self.nmid_director,min_gap)

		self.dict_path = self.__build_dict_path__(self.dict_edges) #IT'S NOT BEING USED
		self.min_gap = min_gap

		# draw( self.__draw_mesh__(self.g,self.dict_edges,self.nmid) )


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

class TrafficDynamic:
	def __init__(self,gmesh,total_time=20,total_events=10,vmax=10):
		self.gmesh = gmesh
		self.events = mockEvents(gmesh.g,int(total_time*0.4),total_events,gmesh.nmid)
		self.total_time = total_time
		self.vmax = vmax

		self.gmesh_draw = self.gmesh.__draw_mesh__(self.gmesh.g,self.gmesh.vi_map,self.gmesh.dict_edges,self.gmesh.nmid_director,gmesh.min_gap)
		self.traffic_map = {}

	def build_mesh_path(self,path,dict_edges):
		mesh_path = []
		for i in xrange(0,len(path)-1):
			u = path[i]
			v = path[i+1]
			if dict_edges.has_key( (u,v) ):
				mesh_path.extend( dict_edges[(u,v)][:-1] )
			else:
				mesh_path.extend( dict_edges[(v,u)][:-1] )
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
		draw( self.gmesh_draw, self.gmesh.vi_map, self.traffic_map, self.events,with_labels=False,save=True,filename="%s/%s.png" %(foldername,t,))

	def process_event(self,e):
		if e.status==TrafficEvent.NOT_STARTED:
			e.vel = 1.0
			e.status = TrafficEvent.RUNNING

			e.path = self.build_mesh_path(e.path,self.gmesh.dict_edges)
			self.traffic_map[ e.path[e.pos] ]=True

			self.log( "STARTING EVENT %d\n %s" % (e.id,e) )			

		elif e.status==TrafficEvent.RUNNING:
			if e.pos==len(e.path)-1:
				self.log("EVENT %d HAS FINISHED. POS: %d" % (e.id,e.pos))
				e.status = TrafficEvent.FINISHED
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
		elif e.status==TrafficEvent.FINISHED:
			e.status = None

	def run(self,save=True,mapname="mapa_semnome"):
		foldername = "%s/%s_SEG%s_CARROS%s_VMAX%s" % ("images_sim",mapname,self.total_time,len(self.events),self.vmax)
		if save:			
			if not os.path.exists(foldername):
				os.mkdir(foldername)		

		t = 0
		events_queue = []

		starting_times = {t:[] for t in xrange(0,self.total_time)}
		event_id = 0
		for e in self.events:
			starting_times[e.t_start].append(e)

		while t<self.total_time:
			self.log("\n****T=%d****\n" % (t,))
			for e in starting_times[t]:
				events_queue.append(e)

			for i in xrange(len(events_queue)-1,-1,-1):
				e = events_queue[i]
				if self.process_event(e)==TrafficEvent.FINISHED:
					events_queue.remove(e)

			if save:
				self.save_figure(t,foldername)
			# time.sleep(0.1)
			t+=1

		vm = 0
		total_events = len(self.events)
		for e in self.events:
			print "EVENT %d: DISTANCE: %d TIME: %d" % (e.id,len(e.path),e.t_end-e.t_start)
			travel_time = (e.t_end-e.t_start)
			if travel_time ==0:
				total_events-=1
			else:
				vm += len(e.path)/( 1.0*travel_time )
		print "TOTAL TIME: %s TOTAL EVENTS: %s AVERAGE SPEED: %s " % (self.total_time,len(self.events),vm/len(self.events))

def load_map(filename):
	g = pickle.load( open(filename,"rb") )	

	print "LABELING"
	dict_streets_nodes,street_end_points,street_nodes_order = ml.get_labeling_info(g)
	g = mr.map_remove_middle(g,street_nodes_order)		

	print "DIRECT"
	dg = md.map_direct(g,street_nodes_order)	

	return dg

def main():
	w,h=4,6

	# g = mockGraph(w,h)
	# gm = GraphMesh(g,0.1)

	g = load_map("maps_read/few_vertices/rio de janeiro menor.nx")
	gm = GraphMesh(g,0.00025)
	
	td = TrafficDynamic(gm,total_time=40,total_events=5000)
	td.run(save=True,mapname="rio de janeiro")

if __name__=='__main__':
	main()	
