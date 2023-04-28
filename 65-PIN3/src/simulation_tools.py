import sys
import subprocess
from bs4 import BeautifulSoup


def start_simulation():

    src_folder = './network_files/'

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

        # Open files
        Bs_edges_data = BeautifulSoup(load_file(), "xml")
        # Loads Simulated Steps
        simulated_steps = Bs_edges_data.findAll('step')

        # Objective function body
        steps = 0
        total_step_halt = 0
        for step in simulated_steps:
            steps += 1
            total_step_halt += int(step['halting'])

        # return total_step_halt
        return steps
    
    return objective_function()
