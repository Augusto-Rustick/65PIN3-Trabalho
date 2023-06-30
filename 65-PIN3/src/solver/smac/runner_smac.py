import sys
import time
import csv
from statistics import mean
from collections import defaultdict
from ConfigSpace import ConfigurationSpace, InCondition, AndConjunction, NotEqualsCondition
from ConfigSpace.hyperparameters import CategoricalHyperparameter
from smac import AlgorithmConfigurationFacade as SMAC, Scenario
from smac_utils import apply_lane_expansion, apply_net_expansion, regenerate_network, start_simulation
from smac_graph import draw_graph

src_folder = '65-PIN3/src/solver/smac/network_files/'


def create_configuration_space_nd():
    cs = ConfigurationSpace()
    cs.add_hyperparameter(CategoricalHyperparameter('param1', ['AL;2', 'AE;2', 'EF;2', 'FL;2', 'FG;2', 'GH;2', 'HL;2', 'DE;2', 'DI;2', 'EI;2', 'IJ;2',
                          'IM;2', 'FJ;2', 'JK;2', 'GK;2', 'BK;2', 'BH;2', 'CM;2', 'CK;2', 'AD', 'AF', 'BG', 'BC', 'CJ', 'EJ', 'EL', 'FK', 'FI', 'GJ', 'GL', 'HK', 'JM', 'KM']))
    cs.add_hyperparameter(CategoricalHyperparameter('param2', ['AE;2', 'AL;2', 'EF;2', 'FL;2', 'FG;2', 'GH;2', 'HL;2', 'DE;2', 'DI;2', 'EI;2', 'IJ;2',
                          'IM;2', 'FJ;2', 'JK;2', 'GK;2', 'BK;2', 'BH;2', 'CM;2', 'CK;2', 'AD', 'AF', 'BG', 'BC', 'CJ', 'EJ', 'EL', 'FK', 'FI', 'GJ', 'GL', 'HK', 'JM', 'KM']))
    cs.add_hyperparameter(CategoricalHyperparameter('net', ['nd']))
    return cs


def create_configuration_space_ow():
    cs = ConfigurationSpace()
    cs.add_hyperparameter(CategoricalHyperparameter('param1', ['AB;2', 'AD;2', 'AC;2', 'EB;2', 'DB;2', 'DC;2', 'CF;2', 'GC;2', 'DE;2',
                          'GD;2', 'HD;2', 'GF;2', 'HE;2', 'GH;2', 'KH;2', 'KG;2', 'KM;2', 'JM;2', 'JK;2', 'JL;2', 'JG;2', 'FI;2', 'JI;2', 'LI;2', 'FJ', 'GI']))
    cs.add_hyperparameter(CategoricalHyperparameter('param2', ['AD;2', 'AB;2', 'AC;2', 'EB;2', 'DB;2', 'DC;2', 'CF;2', 'GC;2', 'DE;2',
                          'GD;2', 'HD;2', 'GF;2', 'HE;2', 'GH;2', 'KH;2', 'KG;2', 'KM;2', 'JM;2', 'JK;2', 'JL;2', 'JG;2', 'FI;2', 'JI;2', 'LI;2', 'FJ', 'GI']))
    cs.add_hyperparameter(CategoricalHyperparameter('net', ['ow']))
    return cs


def run(configuration, instance, seed):

    combination_bit1 = "lane" if (len(configuration['param1']) == 4) else "net"
    combination_bit2 = "lane" if (len(configuration['param2']) == 4) else "net"

    combination = combination_bit1 + "_" + combination_bit2
    net = configuration['net']

    original_file = f'{src_folder}/{net}/{net}.edg.xml'
    modified_file = f'{src_folder}/{net}/{net}.edg-modified.xml'

    param1 = configuration['param1']
    param2 = configuration['param2']

    if combination == 'net_lane':
        apply_net_expansion(f"{param1};100;1;60",
                            original_file, net, src_folder)
        apply_lane_expansion(param2, modified_file, net, src_folder)
    if combination == 'net_net':
        apply_net_expansion(f"{param1};100;1;60",
                            original_file, net, src_folder)
        apply_net_expansion(f"{param2};100;1;60",
                            modified_file, net, src_folder)
    if combination == 'lane_net':
        apply_lane_expansion(param1, original_file, net, src_folder)
        apply_net_expansion(f"{param2};100;1;60",
                            modified_file, net, src_folder)
    if combination == 'lane_lane':
        apply_lane_expansion(param1, original_file, net, src_folder)
        apply_lane_expansion(param2, modified_file, net, src_folder)

    regenerate_network(int(instance), net, src_folder)
    return start_simulation(src_folder)


def optimize(network, n_trials=200, bulk=False, instances=['50', '100', '150', '200', '250']):
    if len(sys.argv) == 5:
        instances = eval(sys.argv[4])
    if network == 'ow':
        cs = create_configuration_space_ow()
    else:
        cs = create_configuration_space_nd()
    scenario = Scenario(
        cs,
        n_trials=n_trials,
        instances=instances,
        deterministic=True
    )

    smac = SMAC(scenario, target_function=run)
    incumbent = smac.optimize()
    results, configs, incumbent = smac._runhistory._data, smac._runhistory._config_ids, incumbent
    if eval(bulk):
        save_results_to_csv(
            results, configs, f'65-PIN3/src/results/smac/smac_optimization_{n_trials}_{network}_results_{time.time()}.csv')
    else:
        print("as bulk option is false, printing results to a visual graph, wait a few seconds...")
        draw_graph(network, format_data(results, configs))
    return results, configs, incumbent


def save_results_to_csv(results, configs, filename):
    config_costs = defaultdict(list)
    all_known_configurations = []
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Configuracao', 'Qnt. Veiculos',
                        'Custo Individual', 'Custo Medio'])
        for result in results:
            result_execution = results[result]
            cost = result_execution.cost
            config_costs[result.config_id].append(int(cost))

        for result in results:
            result_execution = results[result]

            # Extract execution data
            config_id = result.config_id
            instance = result.instance
            cost = result_execution.cost

            configuration = dict(
                search_configuration_by_value(configs, config_id))
            combination_bit1 = "lane" if (
                len(configuration['param1']) == 4) else "net"
            combination_bit2 = "lane" if (
                len(configuration['param2']) == 4) else "net"

            combination = combination_bit1 + "_" + combination_bit2

            if combination == 'net_lane':
                combination = 'lane_net'

            configuration_str = f'{combination}-{configuration["param1"]}-{configuration["param2"]}'

            all_known_configurations.append({'ID': config_id, 'Configuracao': configuration_str, 'Qnt. Veiculos': instance, 'Custo Individual' : cost, 'Custo Medio' : mean(config_costs[config_id])})
            
        for result in sorted(all_known_configurations, key=lambda conf: conf['Custo Medio'], reverse=False):
            writer.writerow([result['ID'], result['Configuracao'], result['Qnt. Veiculos'],
                        result['Custo Individual'], result['Custo Medio']])
        


def search_configuration_by_value(dataset, target_value):
    for configuration, value in dataset.items():
        if value == target_value:
            return configuration
    return None


def format_data(results, configs):
    formatted_data = []
    config_costs = defaultdict(list)
    for result in results:
        result_execution = results[result]
        cost = result_execution.cost
        config_costs[result.config_id].append(int(cost))
        
    for result in results:
        result_execution = results[result]

        # Extract execution data
        config_id = result.config_id
        cost = result_execution.cost

        configuration = dict(search_configuration_by_value(configs, config_id))
        combination_bit1 = "lane" if (
            len(configuration['param1']) == 4) else "net"
        combination_bit2 = "lane" if (
            len(configuration['param2']) == 4) else "net"
        
        param1 = configuration['param1']
        param2 = configuration['param2']

        combination = combination_bit1 + "_" + combination_bit2

        if combination == 'net_lane':
            temp = param1
            param1 = param2
            param2 = temp 
            combination = 'lane_net'

        formatted_data.append({'value': mean(config_costs[result.config_id]), 'parameters': [
            combination, param1, param2]})
        
        
    unique_params = set()
    filtered_data = []

    for item in formatted_data:
        params = tuple(item['parameters'])
        if params not in unique_params:
            unique_params.add(params)
            filtered_data.append(item)
        
    return sorted(filtered_data, key=lambda conf: conf['value'], reverse=False)


optimize(sys.argv[1], int(sys.argv[2]), sys.argv[3])
