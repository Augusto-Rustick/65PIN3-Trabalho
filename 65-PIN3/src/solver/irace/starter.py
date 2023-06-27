import os
import subprocess
import sys

net = sys.argv[1]
try:
    max_experiments = sys.argv[2]
except:
    max_experiments = 200
folder_path = f'65-PIN3/src/solver/irace/irace_files/{net}'
os.chdir(folder_path)
subprocess.run(f'irace --max-experiments {int(max_experiments)}', shell=True)