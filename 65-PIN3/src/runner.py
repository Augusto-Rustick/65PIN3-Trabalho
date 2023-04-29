import sys
from parameter_loader import apply_net_expansion, apply_lane_expansion, regenerate_network
from simulation_tools import start_simulation

def run():

    net = "ow"
    combination = sys.argv[1]
    param1 = sys.argv[2]
    param2 = sys.argv[3]

    # Original file is used for restoring the original file
    original_file = f'./network_files/{net}.edg.xml'
    modified_file = f'./network_files/{net}.edg-modified.xml'

    if combination == 'lane_net':
        apply_lane_expansion(param1, original_file, net)
        apply_net_expansion(f"{param2};100;1;60", modified_file, net)
    if combination == 'lane_lane':
        apply_lane_expansion(param1, original_file, net)
        apply_lane_expansion(param2, modified_file, net)
    if combination == 'net_net':
        apply_net_expansion(f"{param1};100;1;60", original_file, net)
        apply_net_expansion(f"{param2};100;1;60", modified_file, net)

    regenerate_network(100, net)
    print(start_simulation())

run()