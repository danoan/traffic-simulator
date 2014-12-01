#!/usr/bin/python
#coding:utf-8

import traf_mesh as tm
import traf_dynamic as td
import traf_events as te

def run(w,h,total_time,total_events):
	g = tm.mockGraph(w,h)
	gm = tm.GraphMesh(g,min_gap=0.25)

	events = te.mockEvents(gm.g,total_time*0.4,total_events,gm.nmid)

	tr_dyn = td.TrafficDynamic(gm,events,total_time=total_time,total_events=total_events)
	tr_dyn.run(save=False,mapname="%s_w%s_h%s" % ("lattice",w,h))

def main():	
	w = int( raw_input("Enter lattice map width:") )
	h = int( raw_input("Enter lattice map height:") )
	total_time = int( raw_input("Simulation Time:") )
	total_events = int( raw_input("Number of Events:") )

	run(w,h,total_time,total_events)

if __name__=='__main__':
	main()	
