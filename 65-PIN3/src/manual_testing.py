from parameter_loader import *
from simulation_tools import *

net = "ow"

original_file = f'./network_files/{net}.edg.xml'
modified_file = f'./network_files/{net}.edg-modified.xml'

apply_lane_expansion('JG;1', original_file, net)
apply_lane_expansion('KM;1', modified_file, net)
apply_net_expansion("FJ;100;1;60", modified_file, net)
regenerate_network(100, net)

# 62   --c lane_net  JG;2  GI
# 111  --c lane_lane  JL;2  KM;2