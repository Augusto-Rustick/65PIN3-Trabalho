import os
import subprocess
import sys
import time
import csv

net = sys.argv[1]
try:
    max_experiments = sys.argv[2]
except:
    max_experiments = 200
try:
    bulk = eval(sys.argv[3])
except:
    bulk = False
folder_path = f'65-PIN3/src/solver/irace/irace_files/{net}'

if not bulk:
    subprocess.run(f'python 65-PIN3/src/solver/irace/irace_files/{net}/parameters.py placeholder', capture_output=True).stdout
    os.chdir(folder_path)
    subprocess.run(f'irace --max-experiments {int(max_experiments)}', shell=True)
else:
    time = subprocess.run(f'python 65-PIN3/src/solver/irace/irace_files/{net}/parameters.py', capture_output=True).stdout
    time = str(time).replace("\\r\\n", "").replace("b", "").replace("'", "")

    csv_file = f'65-PIN3\src\solver\irace\{int(time)}_irace_optimization_{net}_results.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Configuracao', 'Qnt. Veiculos',
                        'Custo Individual', 'Custo Medio'])
        file.close()

    os.chdir(folder_path)
    process = subprocess.Popen(f'irace --max-experiments {int(max_experiments)}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

