import sys
import subprocess
import time
from bs4 import BeautifulSoup

key = time.time()
command = f'sumo -c net.sumo.cfg --netstate-dump sumoTrace.xml --no-step-log --netstate-dump.empty-edges false --summary summary.xml --output-prefix {key}'

return_code = subprocess.call(command, shell = True)

if return_code != 0:
    print('Command returned code <' + str(return_code) + '>.')
    sys.exit(1)
 
with open(f'{key}summary.xml', 'r') as f:
    data = f.read()
 
Bs_edges_data = BeautifulSoup(data, "xml")

all_steps = Bs_edges_data.findAll('step')
simulated_steps = list(filter(lambda edge : ('running="0"' not in edge.__str__()), all_steps))

steps = 0
total_step_halt = 0
for step in simulated_steps:
    steps += 1
    total_step_halt += int(step['halting'])

print(total_step_halt/steps)
