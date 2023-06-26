#file for storing common scripts shared between all solvers

import os
import re
import sys
import time
import subprocess
from bs4 import BeautifulSoup

trip_generator = '../shared/sumo/tools/randomTrips.py'
src_folder = '65-PIN3/src/network_files/'

def start_simulation(src_folder=src_folder):

    def create_command():
        cfg = f' -c {src_folder}net.sumo.cfg'
        dumps = f' --netstate-dump {src_folder}sumoTrace.xml  --summary {src_folder}summary.xml '
        configuration = ' --no-step-log --netstate-dump.empty-edges false --no-warnings '
        return f'sumo {cfg} {dumps} {configuration} '

    def run_command():
        return_code = subprocess.call(create_command(), shell=False)

        if return_code != 0:
            print('Command at start_simulation returned code <' + str(return_code) + '>.')
            sys.exit(1)

    def load_file():
        run_command()
        with open(f'{src_folder}summary.xml', 'r') as f:
            data = f.read()
        return data

    def objective_function():

        Bs_edges_data = BeautifulSoup(load_file(), "xml")
        simulated_steps = Bs_edges_data.findAll('step')

        steps = 0
        total_step_halt = 0
        for step in simulated_steps:
            steps += 1
            total_step_halt += int(step['halting'])

        return steps
    
    return objective_function()

def regenerate_network(number_of_vehicles, net, src_folder=src_folder):

    commands = [
        f'netconvert --node-files {src_folder}{net}/{net}.nod.xml --edge-files {src_folder}{net}/{net}.edg-modified.xml -o {src_folder}net.net.xml',
        # f'python {trip_generator} -n {src_folder}net.net.xml -e {number_of_vehicles} -o {src_folder}{net}/trips/{net}{number_of_vehicles}output.trips.xml',
        f'duarouter -n {src_folder}net.net.xml --route-files {src_folder}{net}/trips/{net}{number_of_vehicles}output.trips.xml -o {src_folder}net.rou.xml --ignore-errors',
    ]

    for command in commands:
        return_code = subprocess.call(command, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        if return_code != 0:
            print('Command at regenerate_network returned code <' + str(return_code) + '>.')
            sys.exit(1)

def apply_lane_expansion(params, file, net, src_folder=src_folder):

    id, value = params.split(";")

    with open(file, 'r') as f:
        data = f.read()

    xml = BeautifulSoup(data, 'xml')

    edgeA = xml.find('edge', {'id': id})
    edgeA['numLanes'] = value
    edgeB = xml.find('edge', {'id': id[::-1]})
    edgeB['numLanes'] = value

    output_path = f'{src_folder}{net}/{net}.edg-modified.xml'

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pretty_xml_output = xml.prettify()

    with open(output_path, 'wb') as f:
        f.write(pretty_xml_output.encode())

def apply_net_expansion(params, file, net, src_folder=src_folder):

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

    output_path = f'{src_folder}{net}/{net}.edg-modified.xml'

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pretty_xml_output = xml.prettify()

    with open(output_path, 'wb') as f:
        f.write(pretty_xml_output.encode())

def local_run(combination=None, param1=None, param2=None, net=None, instance=None):

    # for allowing parameters to be passed in by sys args or by python function call
    if  combination == None:
        combination = sys.argv[1]
        param1 = sys.argv[2]
        param2 = sys.argv[3]
        net = sys.argv[4]
        instance = sys.argv[5]
        instance = instance[::-1][0:instance[::-1].index("/")][::-1]

    original_file = f'{src_folder}/{net}/{net}.edg.xml'
    modified_file = f'{src_folder}/{net}/{net}.edg-modified.xml'

    if combination == 'lane_net':
        apply_lane_expansion(param1, original_file, net)
        apply_net_expansion(f"{param2};100;1;60", modified_file, net)
    if combination == 'lane_lane':
        apply_lane_expansion(param1, original_file, net)
        apply_lane_expansion(param2, modified_file, net)
    if combination == 'net_net':
        apply_net_expansion(f"{param1};100;1;60", original_file, net)
        apply_net_expansion(f"{param2};100;1;60", modified_file, net)

    regenerate_network(int(instance), net)
    return start_simulation()
