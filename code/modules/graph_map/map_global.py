#coding: utf-8

import os

FOLDER_SAVINGS = "%s/maps_read" % ("input",)
FEW_VERTICES = "%s/%s" % (FOLDER_SAVINGS,"few_vertices")
FULL_VERTICES = "%s/%s" % (FOLDER_SAVINGS,"full_vertices")

DRAW_IMAGES_SAVINGS = "%s/images" % ("output",)
EDGE_BETWEENNESS_IMG_FOLDER = "%s/%s" % (DRAW_IMAGES_SAVINGS,"edge_betweenness")
NODE_BETWEENNESS_IMG_FOLDER = "%s/%s" % (DRAW_IMAGES_SAVINGS,"node_betweenness")

def setup():
    if not os.path.exists(FEW_VERTICES):
        os.makedirs(FEW_VERTICES)

    if not os.path.exists(FULL_VERTICES):
        os.makedirs(FULL_VERTICES)

    if not os.path.exists(EDGE_BETWEENNESS_IMG_FOLDER):
        os.makedirs(EDGE_BETWEENNESS_IMG_FOLDER)        

    if not os.path.exists(NODE_BETWEENNESS_IMG_FOLDER):
        os.makedirs(NODE_BETWEENNESS_IMG_FOLDER)        

setup()