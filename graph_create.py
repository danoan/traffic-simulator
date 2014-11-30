#!/usr/bin/python
#coding:utf-8

import open_to_netx as libopen
import pickle
import os
 
FOLDER_SAVINGS = "maps_read"

class OpenMapRequest:
	def __init__(self,left,bottom,right,top,name):		
		self.left = float(left)
		self.bottom = float(bottom)
		self.right = float(right)
		self.top = float(top)
		self.name = name.strip()
	
	def resolve(self):
		print_warning( "Wait while request for map %s is in process" % (self.name,))
		# f = libopen.download_osm(self.left,self.bottom,self.right,self.top)
		f = open("%s/xml/%s" % (FOLDER_SAVINGS,self.name),"r")
		print_warning( "Map %s downloaded with success. Start to convert into a Graph" % (self.name,))
		G = libopen.read_osm(f)
		if G is not None:
			print_success( "Graph for map %s was created with success!" % (self.name,))
			return G
		else:
			print_fail( "Error creating Graph for map %s" % (self.name,))
			return None

def setup():
	if not os.path.exists(FOLDER_SAVINGS):
		os.makedirs(FOLDER_SAVINGS)

def print_success(s):
	print "***SUCCESS: %s\n" % (s,)

def print_fail(s):
	print "XXX FAIL: %s\n" % (s,)

def print_warning(s):
	print "!!! WARN: %s\n" % (s,)

def print_question(s):
	print "???INPUT: %s" % (s,)

def interactive():
	while True:
		map_name = raw_input("Map name: ")
		left = raw_input("Left Coordinate: ")
		bottom = raw_input("Bottom Coordinate: ")
		right = raw_input("Right Coordinate: ")
		top = raw_input("Top Coordinate: ")
			
		omr = OpenMapRequest(left,bottom,right,top,map_name)
		G = omr.resolve()

		display = raw_input("Display Figure(y/n)? ")
		if display=='y':
			pass

		after_request(G,map_name)	
		again = raw_input("Another one(y/n)? ")
		if again!='y':
			return

def read_file():
	while True:
		filename = raw_input("Filename: ")
		f = open(filename,"r")
		if f is None:
			print_fail( "File could not be read" )
			return
		while True:
			s = f.readline()
			if len(s)==0:
				break
			l = s.split(",")
			orm = OpenMapRequest(*l)
			G = orm.resolve()
			after_request(G,l[4].strip())
			
		again = raw_input("Another one(y/n)? ")
		if again!='y':
			return

def after_request(G,map_name):
	pickle.dump(G,open( "%s/full_vertices/%s.nx" % (FOLDER_SAVINGS,map_name,), "wb") )
	print_success( "Map saved as %s/%s.nx" % (FOLDER_SAVINGS,map_name,))
			

def main():
	print "Hello! This is a interface for Networkx Graph creation from OpenStreetMaps osm files \n\n"
	print "-i \t :Create graphs interactively"
	print "-f \t :Create Graphs from a file"
	print "-q \t :Quit"

	while True:
		o = raw_input("Option: ")	
		if o=='i':
			interactive()		
		elif o=='f':
			read_file()
		elif o=='q':
			break
		else:
			print_fail( "Not recognized option" )

	print "BYE!"

if __name__=='__main__':
	setup()
	main()
