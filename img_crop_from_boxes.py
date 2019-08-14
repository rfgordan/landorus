import os
import csv
import argparse as ap
from os import path
import os
import xml.etree.ElementTree as ET
import cv2

parser = ap.ArgumentParser(description = 'Generate crops from boxes in xml format')
parser.add_argument('--boxes', type=str, dest = 'input_boxes', default = './board_labels/', help = "path to directory with xml defining boxes")
parser.add_argument('--images', type=str, dest= 'input_images', default = './board_images/', help = "path to directory with images of boards")
parser.add_argument('--crops', type=str, dest= 'crop_images', default = './crops/', help = "path to directory for crop outputs")
args = parser.parse_args()

xmls = []
for f_path in os.listdir(args.input_boxes):
    if f_path.endswith('.xml'):
        xmls += [ET.parse(os.path.join(args.input_boxes, f_path))]

# box = xmin, ymin, xmax, ymax
boxes = []
for xml in xmls:
    root = xml.getroot()
    for box in root.iter("bndbox"):
        coords = []
        for child in box:
            coords += [int(child.text)]
        boxes += [coords]

for i_path in os.listdir(args.input_images):
    if i_path.endswith('.png'):
        img = cv2.imread(os.path.join(args.input_images, i_path))
        for i, box in enumerate(boxes):
            img_crop = img[box[1]:box[3], box[0]:box[2]].copy()
            cv2.imwrite(os.path.join(args.crop_images, 'img_' + path.split(i_path)[0] + 'box_' + str(i) + '.png') , img_crop)