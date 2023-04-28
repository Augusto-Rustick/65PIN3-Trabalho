import os
import sys
import subprocess
from bs4 import BeautifulSoup

src_folder = './network_files/'

def regenerate_network(number_of_vehicles):

    trip_generator = '../shared/sumo/tools/randomTrips.py'
    commands = [
        f'netconvert --node-files {src_folder}ow.nod.xml --edge-files {src_folder}ow.edg-modified.xml -o {src_folder}net.net.xml',
        f'python {trip_generator} -n {src_folder}net.net.xml -e {number_of_vehicles} -o {src_folder}output.trips.xml',
        f'duarouter -n {src_folder}net.net.xml --route-files {src_folder}output.trips.xml -o {src_folder}net.rou.xml --ignore-errors',
    ]

    for command in commands:
        return_code = subprocess.call(command, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        if return_code != 0:
            print('Command at regenerate_network returned code <' + str(return_code) + '>.')
            sys.exit(1)

# ID, Lanes
def apply_lane_expansion(params, file):

    id, value = params.split(";")

    with open(file, 'r') as f:
        data = f.read()

    xml = BeautifulSoup(data, 'xml')

    edgeA = xml.find('edge', {'id': id})
    edgeA['numLanes'] = value
    edgeB = xml.find('edge', {'id': id[::-1]})
    edgeB['numLanes'] = value

    output_path = f'{src_folder}ow.edg-modified.xml'

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pretty_xml_output = xml.prettify()

    with open(output_path, 'wb') as f:
        f.write(pretty_xml_output.encode())

# ID, Distance, Lanes, Speed
def apply_net_expansion(params, file):

    id, length, nLanes, speed = params.split(';')

    with open(file, 'r') as f:
        data = f.read()

    xml = BeautifulSoup(data, 'xml')

    edges_tag = xml.find('edges')

    new_edge_tag = xml.new_tag('edge', attrs={
                               'from': id[0], 'to': id[1], 'id': id, 'length': length, 'numLanes': nLanes, 'speed': speed})
    edges_tag.append(new_edge_tag)

    new_edge_tag_reverse = xml.new_tag('edge', attrs={
                                       'from': id[1], 'to': id[0], 'id': id[::-1], 'length': length, 'numLanes': nLanes, 'speed': speed})
    edges_tag.append(new_edge_tag_reverse)

    output_path = f'{src_folder}ow.edg-modified.xml'

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pretty_xml_output = xml.prettify()

    with open(output_path, 'wb') as f:
        f.write(pretty_xml_output.encode())
