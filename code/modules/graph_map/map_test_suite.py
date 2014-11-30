#coding: utf-8:

import map_global as mg

import map_betweenness as mb
import map_direct as md
import map_labeling as ml
import map_remove_middle as mr
import map_streets_are_vertices as msv
import map_weight as mw

def main():
    map_filename = "%s/%s" % ("few_vertices","meier.nx")

    print "***map_betweenness.py***"
    mb.run(map_filename)    

    print "\n***map_direct.py***"
    md.run(map_filename)

    print "\n***map_labeling.py***"
    ml.run(map_filename)

    print "\n***map_remove_middle.py***"
    mr.run(map_filename)    

    print "\n***map_streets_are_vertices.py***"
    msv.run(map_filename)    

    print "\n***map_weight.py***"
    mw.run(map_filename)    

if __name__=='__main__':
    main()