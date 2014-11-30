#!/usr/bin/python

import os

from modules.graph_routines import graph_create
from modules.graph_map import map_save_as_few_vertices as mfew 

XML_MAP_FOLDER = "input/xml"
FULL_VERTICES_FOLDER = "output/maps_read/full_vertices"
FEW_VERTICES_FOLDER = "output/maps_read/few_vertices"

def setup():
    if not os.path.exists(XML_MAP_FOLDER):
        os.makedirs(XML_MAP_FOLDER)

    if not os.path.exists(FULL_VERTICES_FOLDER):
        os.makedirs(FULL_VERTICES_FOLDER)        

    if not os.path.exists(FEW_VERTICES_FOLDER):
        os.makedirs(FULL_VERTICES_FOLDER)                

def read_maps():
    '''
        Read maps as full-vertices
    '''
    xml_input_directions = "input/xml_file.txt"
    graph_create.read_file(xml_input_directions,coordinate=False,output_folder=FULL_VERTICES_FOLDER,xml_folder=XML_MAP_FOLDER)

def convert_to_few_vertices():
    maps_xml = [ os.path.join(FULL_VERTICES_FOLDER,f) for f in os.listdir(FULL_VERTICES_FOLDER) if os.path.isfile(os.path.join(FULL_VERTICES_FOLDER,f))]    
    mfew.run(maps_xml,output_folder=FEW_VERTICES_FOLDER)

def main():
    convert_to_few_vertices()
    # read_maps()
    pass


if __name__=='__main__':
    main()