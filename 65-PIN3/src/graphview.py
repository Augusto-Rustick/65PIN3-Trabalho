import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from matplotlib.widgets import Button
from solver import *

src_folder = '65-PIN3/src/network_files/'
titles = ["Grafo original"]

def visualize_graph(graph, connections=None):
    pos = nx.get_node_attributes(graph, 'pos')
    labels = nx.get_node_attributes(graph, 'id')

    edge_colors = ['black'] * graph.number_of_edges()  # Initialize all edge colors as black

    if connections:
        for connection, color in connections:
            path = list(connection)
            for i in range(len(path) - 1):
                edge = (path[i], path[i + 1])
                if graph.has_edge(*edge):
                    try:
                        edge_index = list(graph.edges()).index(edge)
                    except ValueError:
                        edge_index = list(graph.edges()).index(edge[::-1])
                    edge_colors[edge_index] = color

    nx.draw_networkx(graph, pos=pos, with_labels=True, node_size=500, font_size=10, edge_color=edge_colors)
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)

    # Add labels for duplicates (red) and new connections (green)
    duplicates = set()
    new_connections = set()

    if connections:
        for connection, color in connections:
            if color == 'red':
                duplicates.update(connection)
            elif color == 'green':
                new_connections.update(connection)

    red_labels = {node: node for node in duplicates}
    green_labels = {node: node for node in new_connections}

    nx.draw_networkx_labels(graph, pos, labels=red_labels, font_color='red', font_size=8)
    nx.draw_networkx_labels(graph, pos, labels=green_labels, font_color='green', font_size=8)

    plt.legend(handles=[
        plt.Line2D([], [], color='green', label='Novas conexões'),
        plt.Line2D([], [], color='red', label='Estradas ampliadas'),
        plt.Line2D([], [], color='red', label='Trânsito alto')
    ])

def parse_nodes_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    graph = nx.Graph()

    for node_elem in root.iter('node'):
        node_id = node_elem.attrib['id']
        x = float(node_elem.attrib['x'])
        y = float(node_elem.attrib['y'])
        pos = (x, y)
        graph.add_node(node_id, pos=pos)

    return graph

def parse_edges_file(file_path, graph):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for edge_elem in root.iter('edge'):
        source = edge_elem.attrib['from']
        target = edge_elem.attrib['to']
        edge_id = edge_elem.attrib['id']
        sorted_nodes = tuple(sorted((source, target)))
        graph.add_edge(*sorted_nodes, id=edge_id)

    return graph

class GraphVisualizer:
    def __init__(self, graphs, connections_list):
        self.graphs = graphs
        self.connections_list = connections_list
        self.current_graph_index = 0

        self.fig = plt.figure(figsize=(8, 6))

        self.button_prev = Button(plt.axes([0.3, 0.02, 0.1, 0.05]), 'Anterior')
        self.button_next = Button(plt.axes([0.6, 0.02, 0.1, 0.05]), 'Próximo')
        
        self.ax_graph = self.fig.add_subplot(111)

        self.button_prev.on_clicked(self.prev_graph)
        self.button_next.on_clicked(self.next_graph)

        self.update_graph()

    def update_graph(self):
        self.ax_graph.clear()
        graph = self.graphs[self.current_graph_index]
        connections = self.connections_list[self.current_graph_index]
        visualize_graph(graph, connections)
        self.ax_graph.set_title(f"{titles[self.current_graph_index]}")
        self.ax_graph.axis('off')  # Hide the axis for graph visualization
        self.fig.canvas.draw()

    def prev_graph(self, event):
        self.current_graph_index -= 1
        if self.current_graph_index < 0:
            self.current_graph_index = len(self.graphs) - 1
        self.update_graph()

    def next_graph(self, event):
        self.current_graph_index += 1
        if self.current_graph_index >= len(self.graphs):
            self.current_graph_index = 0
        self.update_graph()

def draw_graph(net):

    print(net)
    nodes_file = f"65-PIN3/src/network_files/{net}/{net}.nod.xml"
    edges_file = f"65-PIN3/src/network_files/{net}/{net}.edg.xml"
    edges_file2 = f"65-PIN3/src/network_files/{net}/{net}.edg-modified.xml"
    
    graphs = []
    connections_list = []

    # Add custom graphs and their connections to the lists
    graph = parse_nodes_file(nodes_file)
    graph = parse_edges_file(edges_file, graph)
    connections = []
    graphs.append(graph)
    connections_list.append(connections)

    iterations = get_all_elites_params(net)
    for iteration in iterations:  
        for count, modification in enumerate(iterations[iteration], start=1):
            parameters = modification.split(" ")
            combination = parameters[0] 
            param1 = parameters[1]
            param2 = parameters[2]
            param4 = parameters[4]
            param5 = parameters[5]

            titles.append(f"{iteration} solution number {count}, got {param4} ({combination, param1, param2}, instance n{param5})")

            original_file = f'65-PIN3/src/network_files/{net}/{net}.edg.xml'
            modified_file = f'65-PIN3/src/network_files/{net}/{net}.edg-modified.xml'

            if combination == 'lane_net':
                apply_lane_expansion(param1, original_file, net, src_folder)
                apply_net_expansion(f"{param2};100;1;60", modified_file, net, src_folder)
                connections = [[(f'{param1[0]}', f'{param1[1]}'), 'red'], [(f'{param2[0]}', f'{param2[1]}'), 'green']]
            if combination == 'lane_lane':
                apply_lane_expansion(param1, original_file, net, src_folder)
                apply_lane_expansion(param2, modified_file, net, src_folder)
                connections = [[(f'{param1[0]}', f'{param1[1]}'), 'red'], [(f'{param2[0]}', f'{param2[1]}'), 'red']]
            if combination == 'net_net':
                apply_net_expansion(f"{param1};100;1;60", original_file, net, src_folder)
                apply_net_expansion(f"{param2};100;1;60", modified_file, net, src_folder)
                connections = [[(f'{param1[0]}', f'{param1[1]}'), 'green'], [(f'{param2[0]}', f'{param2[1]}'), 'green']]

            regenerate_network(50, net, src_folder)

            graph = parse_nodes_file(nodes_file)
            graph = parse_edges_file(edges_file2, graph)
            graphs.append(graph)
            connections_list.append(connections)

    graph_visualizer = GraphVisualizer(graphs, connections_list)

    plt.show()

draw_graph("nd")