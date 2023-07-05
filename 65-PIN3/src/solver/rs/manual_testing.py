from utils import local_run
from statistics import mean

# local_run("lane_lane", "AB;1", "AB;1", "ow", 50) # -> 90
# local_run("lane_lane", "AB;1", "AB;1", "ow", 100) # -> 431
# local_run("lane_lane", "AB;1", "AB;1", "ow", 150) # -> 253
# local_run("lane_lane", "AB;1", "AB;1", "ow", 200) # -> 843
# local_run("lane_lane", "AB;1", "AB;1", "ow", 250) # -> 860

# print(mean([90,431,253,843,860]))

# local_run("lane_lane", "AL;1", "AL;1", "nd", 50) # -> 119
# local_run("lane_lane", "AL;1", "AL;1", "nd", 100) # -> 751
# local_run("lane_lane", "AL;1", "AL;1", "nd", 150) # -> 1099
# local_run("lane_lane", "AL;1", "AL;1", "nd", 200) # -> 273
# local_run("lane_lane", "AL;1", "AL;1", "nd", 250) # -> 2128

# print(mean([119, 751, 1099, 273, 2128]))