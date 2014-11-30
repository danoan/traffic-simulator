#coding:utf-8

import graph_create as gc
import graph_global as gg

def main():
    print "***Creating directly from coordinates***"

    gc.interactive("direct_coordinates",-43.2913,-22.9156,-43.2691,-22.8874)

    print "***Creating from a Coordinates directions input file***"
    filename = "%s/%s" % ("input","coordinate_file.txt")
    gc.read_file(filename)    

    print "***Creating from a XML directions input file***"
    filename = "%s/%s" % ("input","xml_file.txt")
    gc.read_file(filename,coordinate=False )    


if __name__=='__main__':
    main()