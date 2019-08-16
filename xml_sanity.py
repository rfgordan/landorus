import os
import csv
import argparse as ap
from os import path
import os
import xml.etree.ElementTree as ET
import cv2

x = ET.parse("./board_labels/board_labels8.xml")
root = x.getroot()
i = 0
box1dims = []
for box in root.iter("bndbox"):
    i += 1
    if i == 1:
        box1dims = [int(child.text) for child in box]
        print("default boxdims: " + str(box1dims))
    elif i == 2:
        boxdims = [int(child.text) for child in box]
        if not (boxdims[3] - boxdims[1]) == (box1dims[3] - box1dims[1]) or not (boxdims[2] - boxdims[0]) == (box1dims[3] - box1dims[1]):
            print("box {0} does not match dimensions: width off {1}, height off {2}", i, (boxdims[3] - boxdims[1]) - (box1dims[3] - box1dims[1]), (boxdims[2] - boxdims[0]) - (box1dims[2] - box1dims[0]))
    else:
        boxdims = [int(child.text) for child in box]
        if not (boxdims[3] - boxdims[1]) == (box1dims[3] - box1dims[1]) or not (boxdims[2] - boxdims[0]) == (box1dims[3] - box1dims[1]):
            print("box {0} does not match dimensions: width off {1}, height off {2}", i, (boxdims[3] - boxdims[1]) - (box1dims[3] - box1dims[1]), (boxdims[2] - boxdims[0]) - (box1dims[2] - box1dims[0]))

if i != 42:
    print("instead of 42 boxes, found: {0}", i)




