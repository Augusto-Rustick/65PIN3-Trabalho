import os
import re
import sys
import time
import subprocess
from bs4 import BeautifulSoup

trip_generator = '../shared/sumo/tools/randomTrips.py'
src_folder = './network_files/'

def extract_all_elites(net):

    file_path = f"./65-PIN3/src/irace_files/{net}/allElites.txt"
    r_script = f"""
        load('./65-PIN3/src/irace_files/{net}/irace.RData')
        allElites <- iraceResults$allElites
        dump('allElites', file="{file_path}")
    """

    with open('script.R', 'w') as f:
        f.write(r_script)

    subprocess.call(['Rscript', 'script.R'])
    time.sleep(1)

    with open('allElites.txt', "r") as file:
        contents = file.read()

    matches = re.findall(r"c\((.*?)\)", contents)
    result = [list(map(int, match.split(", "))) for match in matches]

    return result

def get_all_elites_params(net):

    elites = extract_all_elites(net)
    file_path = "configurations.txt"

    configurations = {f'iteration_{i+1}' : [] for i in range(len(elites))}
    configurations_pool = {}

    with open(file_path, "r") as file:
        configurations_pool = {int(line_dict['Configuration_ID']): line_dict for line_dict in (eval(line) for line in file)}

    for counter, elite_set in enumerate(elites, start=1):
        for elite_config in elite_set:
            configurations[f'iteration_{counter}'].append(configurations_pool[elite_config]['Configuration'])

        
    return configurations

def clean_all_configurations():
    file_path = "65-PIN3/src/irace_files/ow/configurations.txt"

    with open(file_path, "w") as file:
        file.truncate()

    file_path = "65-PIN3/src/irace_files/nd/configurations.txt"

    with open(file_path, "w") as file:
        file.truncate()


def start_simulation():

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

def regenerate_network(number_of_vehicles, net):

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

def apply_lane_expansion(params, file, net):

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

def apply_net_expansion(params, file, net):

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

def run():

    combination = sys.argv[1]
    param1 = sys.argv[2]
    param2 = sys.argv[3]
    net = sys.argv[4]
    instance = sys.argv[5]
    instance = instance[::-1][0:instance[::-1].index("/")][::-1]

    # Original file is used for restoring the original file
    original_file = f'./network_files/{net}/{net}.edg.xml'
    modified_file = f'./network_files/{net}/{net}.edg-modified.xml'

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
    print(start_simulation())
