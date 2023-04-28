import os
from bs4 import BeautifulSoup

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

    output_path = './ow-network/ow.edg-modified.xml'

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

    new_edge_tag = xml.new_tag('edge', attrs={'from': id[0], 'to': id[1], 'id': id, 'length': length, 'numLanes': nLanes, 'speed': speed})
    edges_tag.append(new_edge_tag)

    new_edge_tag_reverse = xml.new_tag('edge', attrs={'from': id[1], 'to': id[0], 'id': id[::-1], 'length': length, 'numLanes': nLanes, 'speed': speed})
    edges_tag.append(new_edge_tag_reverse)

    output_path = './ow-network/ow.edg-modified.xml'

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pretty_xml_output = xml.prettify()

    with open(output_path, 'wb') as f:
        f.write(pretty_xml_output.encode())

# usage example
apply_net_expansion("FJ;100;1;60", './ow-network/ow.edg.xml')
apply_lane_expansion("FJ;2", './ow-network/ow.edg-modified.xml')
