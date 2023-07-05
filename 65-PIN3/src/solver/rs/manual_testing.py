from utils import local_run
from statistics import mean

ow1 = local_run("lane_lane", "AB;1", "AB;1", "ow", 50) # -> 90
ow2= local_run("lane_lane", "AB;1", "AB;1", "ow", 100) # -> 431
ow3 = local_run("lane_lane", "AB;1", "AB;1", "ow", 150) # -> 253
ow4 = local_run("lane_lane", "AB;1", "AB;1", "ow", 200) # -> 843
ow5 = local_run("lane_lane", "AB;1", "AB;1", "ow", 250) # -> 860

print(ow1,ow2,ow3,ow4,ow5)
print(mean([ow1,ow2,ow3,ow4,ow5]))

nd1 = local_run("lane_lane", "AL;1", "AL;1", "nd", 50) # -> 119
nd2 = local_run("lane_lane", "AL;1", "AL;1", "nd", 100) # -> 751
nd3 = local_run("lane_lane", "AL;1", "AL;1", "nd", 150) # -> 1099
nd4 = local_run("lane_lane", "AL;1", "AL;1", "nd", 200) # -> 273
nd5 = local_run("lane_lane", "AL;1", "AL;1", "nd", 250) # -> 2128

print(nd1,nd2,nd3,nd4,nd5)
print(mean([nd1,nd2,nd3,nd4,nd5]))