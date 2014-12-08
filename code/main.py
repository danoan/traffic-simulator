#!/usr/bin/python

import os
import pickle
import operator
import math

from modules.graph_routines import graph_create
from modules.graph_map import map_save_as_few_vertices as mfew 
from modules.graph_map import map_direct as md
from modules.graph_map import map_remove_middle as mr
from modules.graph_map import map_labeling as ml

from modules.graph_map import map_betweenness as mb
from modules.graph_map import map_streets_are_vertices as msar
from modules.graph_map import map_weight as mw


from modules.simulator import traf_mesh as tm
from modules.simulator import traf_events as te
from modules.simulator import traf_dynamic as td

import convert_graphtool as conv_gt

XML_MAP_FOLDER = "input/xml"
FULL_VERTICES_FOLDER = "output/maps_read/full_vertices"
FEW_VERTICES_FOLDER = "output/maps_read/few_vertices"
SIMULATION_RESULTS = "output/simulation_results"

def setup():
    if not os.path.exists(XML_MAP_FOLDER):
        os.makedirs(XML_MAP_FOLDER)

    if not os.path.exists(FULL_VERTICES_FOLDER):
        os.makedirs(FULL_VERTICES_FOLDER)        

    if not os.path.exists(FEW_VERTICES_FOLDER):
        os.makedirs(FULL_VERTICES_FOLDER)                

    if not os.path.exists(SIMULATION_RESULTS):
        os.makedirs(SIMULATION_RESULTS)              

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
    # mw.weight_graph(dg)

    return tm.GraphMesh(dg,min_gap), dict_endpoints_streets  

def simulacao(map_name,gm,total_time,densidade,endpoints_streets,gt_map,nx_index,w_prop,save=False):
    total_events = int( math.floor( densidade*len(gm.g.nodes()) ) )
    events = te.mockEvents(gm.g,gt_map,nx_index,total_time*0.4,total_events,w_prop,gm.nmid)

    tr_dyn = td.TrafficDynamic(gm,events,total_time=total_time,total_events=total_events)
    data = tr_dyn.run(save=save,mapname=map_name)    

    #TODO: Nao Esta funcionando
    streets_avg_speed = {}    
    streets_count = {}
    for edge in data["Street Average Speed"].keys():    
        e = edge
        if not endpoints_streets.has_key(e):                     
            e = (e[1],e[0])   
            if not endpoints_streets.has_key(e):
                continue
        sname = endpoints_streets[edge]

        if streets_avg_speed.has_key(sname):
            streets_avg_speed[sname] += data["Street Average Speed"][e]
            streets_count[sname]+=1
        else:
            streets_avg_speed[sname] = data["Street Average Speed"][e]
            streets_count[sname]=1

    for s in streets_avg_speed.keys():
        streets_avg_speed[s] /= (1.0*streets_count[s])

    data["Street Average Speed"] = streets_avg_speed

    return data

def runAll():
    maps = ["rio de janeiro menor", "london menor"]
    for m in maps:
        run(m)

def save_results(map_name,map_filename,d,tempo,endpoints_streets,data):
    sorted_list = sorted(data["Street Average Speed"].items(),key=operator.itemgetter(1))
    csv = "Mapa,%s\nDensidade,%s\nVelocidade Media,%s\nTempo,%s\n" % (map_name,d,data["Average Speed"],tempo)

    print "***RESULTADOS d=%s***" % (d,)
    print "VELOCIDADE MEDIA: %s" % (data["Average Speed"],)
    print "10 RUAS MAIS LENTAS"
    csv+="10+ Lentas\n"
    for s in sorted_list[:10]:
        csv += "%s,%s\n" % (s[0],s[1])
        print s
    print "10 RUAS MAIS RAPIDAS"
    csv+="10+ Rapidas\n"
    for s in sorted_list[-10:]:
        csv += "%s,%s\n" % (s[0],s[1])
        print s

    ebc,m = mb.compute(map_name,map_filename)
    ebc_sorted = sorted(ebc.items(),key=operator.itemgetter(1),reverse=True)
    c=0
    csv+="Betweenness de Aresta\n"
    for k in ebc_sorted:
        if endpoints_streets.has_key( k[0] ):
            st_name = endpoints_streets[ k[0] ]
            csv += "%s,%s\n" % (st_name,k[1])
            c+=1
        if c==10:
            break


    ebc,m = msar.compute(map_name,map_filename)
    ebc_sorted = sorted(ebc.items(),key=operator.itemgetter(1),reverse=True)
    c=0
    csv+="Betweenness de Vertice\n"
    while c<10:
        st_name = ebc_sorted[c][0]
        csv += "%s,%s\n" % (st_name,ebc_sorted[c][1])
        c+=1


    f = open("%s/%s_%s.csv" % (SIMULATION_RESULTS,map_name,d),"wb")
    f.write(csv.encode("utf-8","ignore"))

def run(map_name):
    map_filename = "%s/%s.nx" % (FEW_VERTICES_FOLDER,map_name)    
    gm,endpoints_streets = generate_mesh_from_map(map_filename)   
    gt_map,nx_index,gt_index,w_prop = conv_gt.convert(gm.g)

    for d in [0.5+0.25*i for i in xrange(0,5)]:
        tempo = 1000

        data_sum = { "Simulation Time": 0,
                     "Total Events": 0,
                     "Average Speed": 0,
                     "Street Average Speed":{},
                    }                    
        st_count = {}

        r=25
        for i in xrange(0,r):
            data = simulacao(map_name,gm,tempo,d,endpoints_streets,gt_map,nx_index,w_prop)
            data_sum["Average Speed"]+=data["Average Speed"]
            data_sum["Simulation Time"]+=data["Simulation Time"]
            data_sum["Total Events"]=data["Total Events"]
            for k in data["Street Average Speed"].keys():
                if data_sum.has_key(k):
                    data_sum["Street Average Speed"][k] += data["Street Average Speed"][k]
                    st_count[k] += 1
                else:
                    data_sum["Street Average Speed"][k] = data["Street Average Speed"][k]
                    st_count[k] = 1

        data_sum["Average Speed"]/=1.0*r
        for k in data_sum["Street Average Speed"].keys():
            data_sum["Street Average Speed"][k]/=1.0*st_count[k]

        print "SAVING"
        save_results( map_name,map_filename,d,tempo,endpoints_streets,data_sum)


def single_simulation(map_name):
    tempo = 2000

    map_filename = "%s/%s.nx" % (FEW_VERTICES_FOLDER,map_name)    
    gm,endpoints_streets = generate_mesh_from_map(map_filename)   
    gt_map,nx_index,gt_index,w_prop = conv_gt.convert(gm.g)
    d = 1.5

    simulacao(map_name,gm,tempo,d,endpoints_streets,gt_map,nx_index,w_prop,save=True)    

def main():
    map_name = raw_input("Enter map name: ")
    single_simulation(map_name)
    # run(map_name)

    # convert_to_few_vertices()
    # read_maps()
    pass


setup()
if __name__=='__main__':
    main()