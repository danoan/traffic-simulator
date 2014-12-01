#!/usr/bin/python

import os
import pickle

from modules.graph_routines import graph_create
from modules.graph_map import map_save_as_few_vertices as mfew 
from modules.graph_map import map_direct as md
from modules.graph_map import map_remove_middle as mr
from modules.graph_map import map_labeling as ml

from modules.simulator import traf_mesh as tm
from modules.simulator import traf_events as te
from modules.simulator import traf_dynamic as td

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


def generate_mesh_from_map(filename,min_gap=0.00025):
    g = pickle.load( open(filename,"rb") )  

    print "LABELING"
    dict_streets_nodes,street_end_points,dict_endpoints_streets,street_nodes_order = ml.get_labeling_info(g)
    g = mr.map_remove_middle(g,street_nodes_order)      

    print "DIRECT"
    dg = md.map_direct(g,street_nodes_order)    

    return tm.GraphMesh(dg,min_gap), dict_endpoints_streets  

def simulacao(total_time,total_events):
    map_name = "rio de janeiro menor"
    map_filename = "%s/%s.nx" % (FEW_VERTICES_FOLDER,map_name)
    gm,endpoints_streets = generate_mesh_from_map(map_filename)    #Se calculo dict_endpoints street com o graph do gmesh, da erro. Parece que o grafo foi de alguma forma corrompido no GraphMesh

    events = te.mockEvents(gm.g,total_time*0.4,total_events,gm.nmid)

    tr_dyn = td.TrafficDynamic(gm,events,total_time=total_time,total_events=total_events)
    data = tr_dyn.run(save=False,mapname=map_name)    

    #TODO: Nao Esta funcionando
    streets_avg_speed = {}    
    for edge in data["Street Average Speed"].keys():
        e = edge
        if not endpoints_streets.has_key(e):                     
            e = (e[1],e[0])   
            if not endpoints_streets.has_key(e):
                continue
        sname = endpoints_streets[edge]

        if streets_avg_speed.has_key(sname):
            streets_avg_speed[sname] += data["Street Average Speed"][e]
            streets_avg_speed[sname] /= 2.0
        else:
            streets_avg_speed[sname] = data["Street Average Speed"][e]

    print len(data["Street Average Speed"].keys()), len(streets_avg_speed.keys())
    data["Street Average Speed"] = streets_avg_speed

    print data

def main():
    simulacao(40,20)
    # convert_to_few_vertices()
    # read_maps()
    pass


if __name__=='__main__':
    main()