#coding:utf-8
import os

MAP_FOLDER_OUTPUT = "output/maps_read"
MAP_FOLDER_INPUT = "input/xml"

def setup():
    if not os.path.exists(MAP_FOLDER_OUTPUT):
        os.makedirs(MAP_FOLDER_OUTPUT)

    if not os.path.exists(MAP_FOLDER_INPUT):        
        os.makedirs(MAP_FOLDER_INPUT)

setup()