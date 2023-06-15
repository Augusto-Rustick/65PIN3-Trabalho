import os
import time
import subprocess

file_path = f'65-PIN3/src/irace_files/nd/irace.Rdata'

if os.path.exists(file_path):
    subprocess.run(['65-PIN3\irace.bat'], shell=True)
    time.sleep(1)
    modification_time = os.path.getmtime(file_path)
    while True:
        new_modification_time = os.path.getmtime(file_path)
        if (modification_time != new_modification_time):
            pass        
else:
    print("File not found.")