import pysmile
import smile_license.pysmile_license
from utils import str_join


class BayesianNetwork:
    def __init__(self, numMines, size, fileName="Minesweeper.xdsl"):
        self.net = pysmile.Network()
        self.fileName = fileName
        self.numMines = numMines
        self.generate_network(size)

    def generate_network(self, size):
        # generate network with size^2 X and Y nodes and one MinesAmount node
        all_x_nodes = []

        for x_coord in range(0, size):
            for y_coord in range(0, size):
                x_node_id = str_join('X', x_coord, '_', y_coord)
                mine_probability = float(self.numMines) / (float (size * size))
                self.create_cpt_node(x_node_id, x_node_id, ["NoMine", "Mine"], [1-mine_probability, mine_probability], (x_coord+1)*10, (y_coord+1)*10)
                all_x_nodes.append(x_node_id)

        for x_coord in range(0, size):
            for y_coord in range(0, size):

                # list of IDs of nodes, which are parents of currently processed node
                y_parents = []

                for x in range(max(0, x_coord - 1), min(x_coord + 2, size)):
                    for y in range(max(0, y_coord - 1), min(y_coord + 2, size)):
                        if (x_coord, y_coord) != (x, y):
                            y_parents.append(str_join('X', x, '_', y))

                y_node_id = str_join('Y', x_coord, '_', y_coord)
                self.create_equation_node(y_node_id, y_node_id, y_parents, (x_coord+1)*10 + 5, (y_coord+1)*10 + 5)


        # update the network
        self.net.update_beliefs()

        # write the network to the xdsl file
        self.net.write_file("Minesweeper.xdsl")

    def create_cpt_node(self, id, name, outcomes, definitions, x_pos, y_pos):
        handle = self.net.add_node(pysmile.NodeType.CPT, id)

        self.net.set_node_name(handle, name)
        self.net.set_node_position(handle, x_pos, y_pos, 85, 55)

        initial_outcome_count = self.net.get_outcome_count(handle)

        for i in range(0, initial_outcome_count):
            self.net.set_outcome_id(handle, i, outcomes[i])

        for i in range(initial_outcome_count, len(outcomes)):
            self.net.add_outcome(handle, outcomes[i])

        self.net.set_node_definition(handle, definitions)
        return handle

    def create_equation_node(self, id, name, parents, x_pos, y_pos):
        handle = self.net.add_node(pysmile.NodeType.EQUATION, id)

        self.net.set_node_name(handle, name)
        self.net.set_node_position(handle, x_pos, y_pos, 85, 55)

        for parent_id in parents:
            self.net.add_arc(parent_id, id)

        # set the bounds of the equation node
        self.net.set_node_equation_bounds(handle, 0, len(parents))

        boundaries = [(i+1) * (float(len(parents)) / float(len(parents) + 1)) for i in range(0, len(parents)+1)]
        intervals = [pysmile.DiscretizationInterval(str_join("State", i), boundaries[i]) for i in range(0, len(parents)+1)]

        self.net.set_node_equation_discretization(handle, intervals)
        return handle

    def read_from_file(self):
        # read the topology of the network
        self.net.read_file(self.fileName)

        # update the network
        self.net.update_beliefs()

    def set_x_evidence(self, x_coord, y_coord, fieldValue):
        node_id = str_join('X', x_coord, '_', y_coord)
        self.net.set_evidence(node_id, fieldValue)

    def set_y_evidence(self, x_coord, y_coord, fieldValue):
        node_id = str_join('Y', x_coord, '_', y_coord)
        self.net.set_cont_evidence(node_id, fieldValue)

    def reveal_fields_without_mine(self, fields):
        for (x, y), val in fields:
            self.reveal_field_without_mine(x, y, val)

    def reveal_field_without_mine(self, x_coord, y_coord, fieldValue):
        # fieldValue is an integer, shown on the revealed field
        self.set_x_evidence(x_coord, y_coord, "NoMine")
        self.set_y_evidence(x_coord, y_coord, fieldValue)

        # update the network
        self.net.update_beliefs()

    def get_no_mine_probability(self, x_coord, y_coord):
        node = str_join('X', x_coord, '_', y_coord)
        return self.net.get_node_value(node)[0]

    def find_best_nodes(self):
        # returns a list(!) of coordinates of fields with the lowest probability of finding a mine

        x_nodes = [node for node in self.net.get_all_node_ids() if node.startswith('X')]       # print x_nodes

        # filter out the already revealed fields
        not_revealed = list(filter(lambda nodeId: not self.net.is_evidence(nodeId), x_nodes))

        # sort the fields according to the probability of finding a mine in them
        # (the first node in the list has the highest probability of not finding mine)

        def key(nodeId):
            return -self.net.get_node_value(nodeId)[0]

        not_revealed.sort(key=key)

        if len(not_revealed) > 0:
            best = self.net.get_node_value(not_revealed[0])[0]
            return [map(lambda x: int(x), node.strip('X').split('_')) for node in not_revealed if abs(self.net.get_node_value(node)[0] - best) < 0.0005]
        else:
            return []
