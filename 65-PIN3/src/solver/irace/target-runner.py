import os
import sys
import subprocess
import random
import csv
import pandas as pd

# Get the parameters as command line arguments
configuration_id = sys.argv[1]
instance_id = sys.argv[2]
seed = sys.argv[3]
instance = sys.argv[4]
combination = ''.join(sys.argv[5])
conf_params = ' '.join(sys.argv[6:])
net = sys.argv[-2]
time = sys.argv[-1]

# Call Python scripts that start simulation
command = "python run.py " +  conf_params + " " + instance

# Define the stdout and stderr files
r = str(random.randint(1, 999999))
out_file = './c' + str(configuration_id) + '-' + str(instance_id) + '-' + r + '.stdout'
err_file = './c' + str(configuration_id) + '-' + str(instance_id) + '-' + r + '.stderr'

# Execute
outf = open(out_file, "w")
errf = open(err_file, "w")
return_code = subprocess.call(command, stdout=outf, stderr=errf, shell=True)
outf.close()
errf.close()

# Check return code
if return_code != 0:
    print('Command returned code <' + str(return_code) + '>.')
    sys.exit(1)

# Check output file
if not os.path.isfile(out_file):
    print('Output file <' + out_file  + '> not found.')
    sys.exit(1)

# Get result and print it
result = open(out_file)
lastLine = result.readlines()[-1]
result.close()
lastLine = int(float(lastLine.replace('\n', '')))
print(lastLine)

config_file = f'./irace_files/{net}/configurations.txt'
with open(config_file, 'a') as f:
    dict = {'Configuration_ID' : configuration_id, 'Configuration' : conf_params + " " + str(lastLine) + " " + configuration_id, 'Value' : str(lastLine)}
    f.write(str(dict) + "\n")

# Save configuration to file
if time != "0":

    csv_file = f'{time}_irace_optimization_{net}_results.csv'
    conf_params_list = conf_params.split(" ")
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([configuration_id, f'{conf_params_list[0]}-{conf_params_list[1]}-{conf_params_list[2]}', instance[::-1][0:instance[::-1].index("/")][::-1],
                            int(lastLine), 0])
        file.close()


    df = pd.read_csv(csv_file)
    df['Custo Medio'] = df.groupby('ID')['Custo Individual'].transform('mean')
    df = df.sort_values('Custo Medio', ascending=True)
    df.to_csv(csv_file, index=False)

# Clean files and exit
os.remove(out_file)
os.remove(err_file)
sys.exit(0)
