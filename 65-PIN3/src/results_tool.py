import subprocess
import re

net = "nd"

def extract_all_elites(net):

    file_path = f"./65-PIN3/src/irace_files/{net}/allElites.txt"
    r_script = f"""
        load('./65-PIN3/src/irace_files/{net}/irace.RData')
        allElites <- iraceResults$allElites
        dump('allElites', file="{file_path}")
    """

    with open('script.R', 'w') as f:
        f.write(r_script)

    subprocess.call(['Rscript', 'script.R'])

    with open(file_path, "r") as file:
        contents = file.read()

    matches = re.findall(r"c\((.*?)\)", contents)
    result = [list(map(int, match.split(", "))) for match in matches]

    return result

def get_all_elites_params():
    pass

print(extract_all_elites(net))