from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def lane_param(file):

    with open(file, 'r') as f:
        data = f.read()
    
    Bs_edges_data = BeautifulSoup(data, "xml")

    modifiable_edges = Bs_edges_data.findAll('edge')

    param_list = []
    for i in range(0, len(modifiable_edges), 2):
        elem = modifiable_edges[i]
        param_list.append((elem['from'] + elem['to'] + ";" + str(int(elem['numLanes']) + 1)))

    return param_list

def network_param(nodeFile, edgeFile):

    tree_node = ET.parse(nodeFile)
    root_node = tree_node.getroot()
    nodes = {}
    for node in root_node.findall('node'):
        node_id = node.get('id')
        x = float(node.get('x'))
        y = float(node.get('y'))
        nodes[node_id] = (x, y)

    tree_edge = ET.parse(edgeFile)
    root_edge = tree_edge.getroot()
    edges = {}
    for edge in root_edge.findall('edge'):
        edge_id = edge.get('id')
        from_node = edge.get('from')
        to_node = edge.get('to')
        edges[edge_id] = (from_node, to_node)


    def distance(node1, node2):
        return max(abs(node1[0] - node2[0]), abs(node1[1] - node2[1]))

    def not_crossroads(node, node_to=None):
        from_connections = {k: v for k, v in edges.items() if node in k}
        clean_connections = []
        for key, value in from_connections.items():
            val = key.replace(node, '')
            if val not in clean_connections:
                clean_connections.append(val)

        if (node_to is not None):
            adj = []
            for key in clean_connections:
                adj.append(not_crossroads(key))
            adj_forbidden = []
            counter = 0
            for set in adj:
                if node_to in set:
                    adj_forbidden.append(clean_connections[counter])
                counter += 1
            return edges.get(adj_forbidden[0] + adj_forbidden[1]) is None

        return clean_connections


    initial_network_connection = {}
    for node_id, (from_node, to_node) in edges.items():
        node1 = nodes[from_node]
        node2 = nodes[to_node]
        initial_network_connection[node_id] = distance(node1, node2)

    valid_suggestions = initial_network_connection.copy()
    return_params = []
    for nodeFrom in nodes.items():
        from_, (from_x, from_y) = nodeFrom
        for nodeTo in nodes.items():
            to, (to_x, to_y) = nodeTo
            if from_ != to:
                node_id = from_ + to
                distance_ = distance((to_x, to_y), (from_x, from_y))
                if (int(distance_) <= 100 and valid_suggestions.get(node_id) is None):
                    if (not_crossroads(from_, to)):
                        valid_suggestions[node_id] = distance_
                        return_params.append(node_id)

    return return_params

# usage example
print(lane_param('./ow-network/ow.edg.xml'))
print(network_param('./ow-network/ow.nod.xml', './ow-network/ow.edg.xml'))