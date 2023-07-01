import time
import sys
def update_params_ow():

    if len(sys.argv) == 2:
        timee = 0
    else:
        timee = int(time.time())
    
    updated_params = f'''# name		    switch              type       values
combination     "--c "              c          ("lane_net", "lane_lane", "net_net")
laneA           " "                 c          ("AB;2", "AD;2", "AC;2", "EB;2", "DB;2", "DC;2", "CF;2", "GC;2", "DE;2", "GD;2", "HD;2", "GF;2", "HE;2", "GH;2", "KH;2", "KG;2", "KM;2", "JM;2", "JK;2", "JL;2", "JG;2", "FI;2", "JI;2", "LI;2") | combination %in% c("lane_net", "lane_lane")
laneB           " "                 c          ("AB;2", "AD;2", "AC;2", "EB;2", "DB;2", "DC;2", "CF;2", "GC;2", "DE;2", "GD;2", "HD;2", "GF;2", "HE;2", "GH;2", "KH;2", "KG;2", "KM;2", "JM;2", "JK;2", "JL;2", "JG;2", "FI;2", "JI;2", "LI;2") | combination %in% c("lane_lane")
connectionA     " "                 c          ("FJ", "GI")  | combination %in% c("lane_net", "net_net")
connectionB     " "                 c          ("FJ", "GI")  | combination %in% c("net_net")
net             " "                 c          ("ow")
time             " "                c          ("{timee}")
'''

    file_path = f'65-PIN3/src/solver/irace/irace_files/ow/parameters.txt'

    with open(file_path, 'w') as file:
        file.write(updated_params)

    return timee

print(update_params_ow())