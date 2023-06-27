import sys
import numpy as np
import random
from ConfigSpace import ConfigurationSpace
from ConfigSpace.hyperparameters import CategoricalHyperparameter
from smac import HyperparameterOptimizationFacade as SMAC, Scenario
from solver import apply_lane_expansion, apply_net_expansion, regenerate_network, start_simulation

src_folder = '65-PIN3/src/network_files/'

def create_configuration_space_nd():
    cs = ConfigurationSpace()

    combination = cs.add_hyperparameter(CategoricalHyperparameter('combination', ['lane_net', 'lane_lane', 'net_net']))
    laneA = cs.add_hyperparameter(CategoricalHyperparameter('laneA', ['AL;2', 'AE;2', 'EF;2', 'FL;2', 'FG;2', 'GH;2', 'HL;2', 'DE;2', 'DI;2', 'EI;2', 'IJ;2', 'IM;2', 'FJ;2', 'JK;2', 'GK;2', 'BK;2', 'BH;2', 'CM;2', 'CK;2']))
    laneB = cs.add_hyperparameter(CategoricalHyperparameter('laneB', ['AL;2', 'AE;2', 'EF;2', 'FL;2', 'FG;2', 'GH;2', 'HL;2', 'DE;2', 'DI;2', 'EI;2', 'IJ;2', 'IM;2', 'FJ;2', 'JK;2', 'GK;2', 'BK;2', 'BH;2', 'CM;2', 'CK;2']))
    connectionA = cs.add_hyperparameter(CategoricalHyperparameter('connectionA', ['AD', 'AF', 'BG', 'BC', 'CJ', 'EJ', 'EL', 'FK', 'FI', 'GJ', 'GL', 'HK', 'JM', 'KM']))
    connectionB = cs.add_hyperparameter(CategoricalHyperparameter('connectionB', ['AD', 'AF', 'BG', 'BC', 'CJ', 'EJ', 'EL', 'FK', 'FI', 'GJ', 'GL', 'HK', 'JM', 'KM']))
    net = cs.add_hyperparameter(CategoricalHyperparameter('net', ['nd']))

    return cs

def create_configuration_space_ow():
    cs = ConfigurationSpace()

    combination = cs.add_hyperparameter(CategoricalHyperparameter('combination', ['lane_net', 'lane_lane', 'net_net']))
    laneA = cs.add_hyperparameter(CategoricalHyperparameter('laneA', ['AB;2', 'AD;2', 'AC;2', 'EB;2', 'DB;2', 'DC;2', 'CF;2', 'GC;2', 'DE;2', 'GD;2', 'HD;2', 'GF;2', 'HE;2', 'GH;2', 'KH;2', 'KG;2', 'KM;2', 'JM;2', 'JK;2', 'JL;2', 'JG;2', 'FI;2', 'JI;2', 'LI;2']))
    laneB = cs.add_hyperparameter(CategoricalHyperparameter('laneB', ['AB;2', 'AD;2', 'AC;2', 'EB;2', 'DB;2', 'DC;2', 'CF;2', 'GC;2', 'DE;2', 'GD;2', 'HD;2', 'GF;2', 'HE;2', 'GH;2', 'KH;2', 'KG;2', 'KM;2', 'JM;2', 'JK;2', 'JL;2', 'JG;2', 'FI;2', 'JI;2', 'LI;2']))
    connectionA = cs.add_hyperparameter(CategoricalHyperparameter('connectionA', ['FJ', 'GI']))
    connectionB = cs.add_hyperparameter(CategoricalHyperparameter('connectionB', ['FJ', 'GI']))
    net = cs.add_hyperparameter(CategoricalHyperparameter('net', ['ow']))

    return cs

def run(configuration, instance, seed):

    combination = configuration['combination']
    laneA = configuration['laneA']
    laneB = configuration['laneB']
    connectionA = configuration['connectionA']
    connectionB = configuration['connectionB']
    net = configuration['net']

    original_file = f'{src_folder}/{net}/{net}.edg.xml'
    modified_file = f'{src_folder}/{net}/{net}.edg-modified.xml'

    if combination == 'lane_net':
        apply_lane_expansion(laneA, original_file, net, src_folder)
        apply_net_expansion(f"{connectionA};100;1;60", modified_file, net, src_folder)
    if combination == 'lane_lane':
        apply_lane_expansion(laneA, original_file, net, src_folder)
        apply_lane_expansion(laneB, modified_file, net, src_folder)
    if combination == 'net_net':
        apply_net_expansion(f"{connectionA};100;1;60", original_file, net, src_folder)
        apply_net_expansion(f"{connectionB};100;1;60", modified_file, net, src_folder)

    regenerate_network(int(instance), net, src_folder)
    return start_simulation(src_folder)

def optimize(net):
    if net == 'ow':
        cs = create_configuration_space_ow()
    else:    
        cs = create_configuration_space_nd()
    
    scenario = Scenario(
        cs,
        n_trials=200,
        min_budget=1,
        max_budget=45,
        instances=['50', '100', '150', '200', '250'],
    )

    smac = SMAC(scenario, target_function=run)
    incumbent = smac.optimize()

    try:
        best_configuration = incumbent[0]
        best_objective = incumbent[1]
    except:
        best_configuration = None
        best_objective = None

    print("Best configuration:", best_configuration)
    print("Best objective:", best_objective)

if __name__ == '__main__':
    optimize('ow')
