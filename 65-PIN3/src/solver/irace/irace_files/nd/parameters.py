import time
import sys
def update_params_nd():

    if len(sys.argv) == 2:
        timee = 0
    else:
        timee = int(time.time())
    
    updated_params = f'''# name		    switch              type       values
combination     "--c "              c          ("lane_net", "lane_lane", "net_net")
laneA           " "                 c          ("AL;2", "AE;2", "EF;2", "FL;2", "FG;2", "GH;2", "HL;2", "DE;2", "DI;2", "EI;2", "IJ;2", "IM;2", "FJ;2", "JK;2", "GK;2", "BK;2", "BH;2", "CM;2", "CK;2") | combination %in% c("lane_net", "lane_lane")
laneB           " "                 c          ("AL;2", "AE;2", "EF;2", "FL;2", "FG;2", "GH;2", "HL;2", "DE;2", "DI;2", "EI;2", "IJ;2", "IM;2", "FJ;2", "JK;2", "GK;2", "BK;2", "BH;2", "CM;2", "CK;2") | combination %in% c("lane_lane")
connectionA     " "                 c          ("AD", "AF", "BG", "BC", "CJ", "EJ", "EL", "FK", "FI", "GJ", "GL", "HK", "JM", "KM")  | combination %in% c("lane_net", "net_net")
connectionB     " "                 c          ("AD", "AF", "BG", "BC", "CJ", "EJ", "EL", "FK", "FI", "GJ", "GL", "HK", "JM", "KM")  | combination %in% c("net_net")
net             " "                 c          ("nd")
time             " "                c          ("{timee}")
'''

    file_path = f'65-PIN3/src/solver/irace/irace_files/nd/parameters.txt'

    with open(file_path, 'w') as file:
        file.write(updated_params)

    return timee

print(update_params_nd())