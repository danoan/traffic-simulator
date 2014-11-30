#!usr/bin/python

#coding:utf-8

import math
import pickle
import networkx as nx

FOLDER_SAVINGS = "maps_read"
EARTH_RADIUS = 6367

def haversine(lat1,lon1,lat2,lon2):
	lat1,lon1,lat2,lon2 = map(math.radians,[lat1,lon1,lat2,lon2])

	diff_lat = lat2-lat1
	diff_lon = lon2-lon1
	a = math.sin(diff_lat/2.0)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(diff_lon/2.0)**2
	c = 2*math.asin(math.sqrt(a))

	return EARTH_RADIUS*c

def weight_graph(g):
	for u,v in g.edges():
		ulat = g.node[u]['data'].lat
		ulon = g.node[u]['data'].lon

		vlat = g.node[v]['data'].lat
		vlon = g.node[v]['data'].lon

		g[u][v]['weight'] = haversine(ulat,ulon,vlat,vlon)

def main():
	filename = raw_input("Enter the map filename: ")
	g = pickle.load(open("%s/%s" % (FOLDER_SAVINGS,filename),"rb"))	
	weight_graph(g)

if __name__=='__main__':
	main()
