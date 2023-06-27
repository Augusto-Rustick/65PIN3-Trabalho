import json
import random
from utils import *
from rich.console import Console
from rich.table import Table
from rich.live import Live
from graph import *

parameters = None

def resetTable():
    global table 
    table = Table(title="Instances")
    columns = ["Configuration", "Value"]

    for column in columns:
        table.add_column(column)

resetTable()

def loadParameters(filename):
    with open(filename, "r") as file:
        return json.load(file)
    
def getRandomStart(net):
    parameters = loadParameters('65-PIN3/src/solver/rs/params.json')[f'{net}']
    combination = random.choice(parameters['combination'])
    param1 = random.choice(parameters[f'{combination.split("_")[0]}'])
    param2 = random.choice(parameters[f'{combination.split("_")[1]}'])
    return (combination, param1, param2)

def getInstances():
    parameters = loadParameters('65-PIN3/src/solver/rs/params.json')
    instances = parameters['instances']
    return instances

def calculateRepetitions(maxBudget, costPerConfiguration):
    repetitions = int(maxBudget / costPerConfiguration)
    if repetitions == 0:
        repetitions = 1
    return repetitions


def start(net=None, maxBudget=None, bulk=False):
    instances = getInstances()
    total_configurations = calculateRepetitions(maxBudget, len(instances))
    best_known_configurations = []
    lowest_value = sys.maxsize
    lowest_value_index = None   
    for i in range(total_configurations):
        combination, param1, param2 = getRandomStart(net)
        configurationAverage = 0
        for instance in instances:
            current_val = local_run(combination, param1, param2, net, instance)
            configurationAverage += (current_val/len(instances))
        if len(best_known_configurations) < total_configurations:
            best_known_configurations.append({'value' : configurationAverage, 'parameters': [combination, param1, param2]})
        else:
            for known_configuration in best_known_configurations:
                if known_configuration['value'] > configurationAverage:
                    known_configuration['value'] = configurationAverage
                    known_configuration['parameters'] = [combination, param1, param2]
                    break
        if lowest_value > configurationAverage:
            lowest_value = configurationAverage
            lowest_value_index = i

        if not bulk:
            resetTable()
            for counter, configuration in enumerate(best_known_configurations):
                color = '[red]'
                if (counter == lowest_value_index):
                    color = '[green]'
                row = [str(configuration['parameters']), color + str(configuration['value'])]
                table.add_row(*row)
            console = Console()
            os.system('cls||clear')
            console.print(table, end='')

    sorted_list = sorted(best_known_configurations, key=lambda conf: conf['value'], reverse=False)
    if not bulk:
        draw_graph(net, sorted_list)
    return sorted_list

try:
    net = sys.argv[1]
    maxBudget = sys.argv[2]
    try:
        bulk = eval(sys.argv[3])
    except:
        bulk = False
        pass
except:
    pass
start(net, int(maxBudget), bulk)
