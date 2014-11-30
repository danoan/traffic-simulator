#!/usr/bin/python
#coding:utf-8

import open_to_netx as libopen
import pickle
import os

import graph_global as gg

class OpenMapRequest:
	def __init__(self,left,bottom,right,top,name):		
		self.left = float(left)
		self.bottom = float(bottom)
		self.right = float(right)
		self.top = float(top)
		self.name = name.strip()
	
	def resolve(self,coordinate=False,xml_folder=gg.MAP_FOLDER_INPUT):
		print_warning( "Wait while request for map %s is in process" % (self.name,))
		if coordinate:
			f = libopen.download_osm(self.left,self.bottom,self.right,self.top)
		else:
			f = open("%s/%s" % (xml_folder,self.name),"r")

		print_warning( "Map %s downloaded with success. Start to convert into a Graph" % (self.name,))
		G = libopen.read_osm(f)
		if G is not None:
			print_success( "Graph for map %s was created with success!" % (self.name,))
			return G
		else:
			print_fail( "Error creating Graph for map %s" % (self.name,))
			return None

def print_success(s):
	print "***SUCCESS: %s\n" % (s,)

def print_fail(s):
	print "XXX FAIL: %s\n" % (s,)

def print_warning(s):
	print "!!! WARN: %s\n" % (s,)

def print_question(s):
	print "???INPUT: %s" % (s,)

def interactive(map_name,left,bottom,right,top,output_folder=gg.MAP_FOLDER_OUTPUT):
	omr = OpenMapRequest(left,bottom,right,top,map_name)
	G = omr.resolve(coordinate=True)

	display = raw_input("Display Figure(y/n)? ")
	if display=='y':
		pass

	after_request(G,map_name,output_folder)	

def read_file(filename,coordinate=True,output_folder=gg.MAP_FOLDER_OUTPUT,xml_folder=gg.MAP_FOLDER_INPUT):
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
		G = orm.resolve(coordinate=coordinate,xml_folder=xml_folder)
		after_request(G,l[4].strip(),output_folder)

def after_request(G,map_name,output_folder):
	pickle.dump(G,open( "%s/%s.nx" % (output_folder,map_name,), "wb") )
	print_success( "Map saved as %s/%s.nx" % (output_folder,map_name,))
			

def main():
	print "Hello! This is a interface for Networkx Graph creation from OpenStreetMaps osm files \n\n"
	print "-i \t :Create graphs interactively"
	print "-f \t :Create Graphs from a coordinate file"
	print "-x \t :Create Graphs from xml files"
	print "-q \t :Quit"

	while True:
		o = raw_input("Option: ")	
		if o=='i':
			while True:
				map_name = raw_input("Map name: ")
				left = raw_input("Left Coordinate: ")
				bottom = raw_input("Bottom Coordinate: ")
				right = raw_input("Right Coordinate: ")
				top = raw_input("Top Coordinate: ")

				interactive(map_name,left,bottom,right,top)				

				again = raw_input("Another one(y/n)? ")
				if again!='y':
					break				
		elif o=='f':
			while True:
				filename = raw_input("Filename: ")
				read_file(filename)
				again = raw_input("Another one(y/n)? ")
				if again!='y':
					break		
		elif o=='x':
			while True:
				filename = raw_input("Filename: ")
				read_file(filename,coordinate=False	)
				again = raw_input("Another one(y/n)? ")
				if again!='y':
					break	
		elif o=='q':
			break
		else:
			print_fail( "Not recognized option" )

	print "BYE!"

if __name__=='__main__':
	main()
