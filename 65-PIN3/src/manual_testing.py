from parameter_loader import *
from simulation_tools import *

original_file = './network_files/ow.edg.xml'
modified_file = './network_files/ow.edg-modified.xml'

apply_lane_expansion('JL;2', original_file)
apply_lane_expansion('KM;2', modified_file)
# apply_net_expansion("GI;100;1;60", modified_file)
regenerate_network(100)

# 62   --c lane_net  JG;2  GI
# 111  --c lane_lane  JL;2  KM;2