# Authors: Conrad
# Associations: Indie Academy Discord Server
# License: MIT

import pickle


class Node:

    def __init__(self, name, parent=None):

        # The primary identifier for a node
        self.name = name

        # The node which this node is a subnode of
        self.parent = parent

        # Child nodes
        self.nodes = {}

        # The contents of the node
        self.content = []

    def __getitem__(self, item):
        return self.nodes[item]

    def __iter__(self):
        return iter(self.nodes)

    def __str__(self):
        out = self.name + ":\n"
        for node in self:
            out += "\t" + self[node].name + ": {" + ",".join(self[node].nodes.keys()) + "}\n"
            out += "\t\t" + self[node].format_content()
            out += "\n"
        out += "\n"

        return out

    def add_new_node(self, name):
        """
        Create a new node with the given name
        """
        if name in self:
            raise ValueError(f"Cannot create node; node with the name {name} already exists in {self.get_address()}.")
        else:
            self.nodes.update({name: Node(name, self)})

    def add_existing_node(self, node):
        """
        Add a subnode to the node
        """
        if node.name in self:
            raise ValueError(f"Cannot add existing node; node with the name {name} already exists in {self.get_address()}.")
        else:
            self.nodes.update({node.name: node})
            self.propogate_parent()

    def add_content(self, content):
        """
        Add node contents to the stack
        """
        self.content.append(content)

    def copy(self, copy_parent=False):
        """
        Create a copy of the node

        :param copy_parent: Whether to keep the copy's parent the same
        """
        out = Node(self.name, self.parent if copy_parent else None)
        out.nodes = self.nodes
        out.content = self.content
        return out

    def format_content(self):
        """
        For use with the __str__ function
        """
        return "\n\t\t".join(self.content)

    def get(self, directions):
        """
        Get the subnode which accords to the given directions
        """
        if len(directions) == 0:
            return self
        if directions[0] not in self:
            raise ValueError(f"Cannot find {directions[0]} in {self.get_address()}")
        else:
            if len(directions) == 1:
                return self[directions[0]]
            else:
                return self[directions[0]].get(directions[1:])

    def get_address(self):
        """
        Construct a list of directions to get to the node
        """
        if not self.parent:
            return [self.name]
        else:
            return self.parent.get_address() + [self.name]

    def get_path(self):
        """
        Generate a relative save path for the node
        """
        return "/".join(self.get_address())

    def propogate_parent(self):
        """
        Ensure that every subnode is properly parented
        """
        for node in self:
            self[node].parent = self
            self[node].propogate_parent()

    def remove_node(self, name):
        """
        Remove a node with the given name
        """
        if name not in self:
            raise ValueError(f"Cannot remove node; node with the name {name} does not exist in {self.get_address()}")
        else:
            self.nodes.pop(name)

    def save(self, optional_filename=""):
        """
        Save the node with pickle

        :param optional_filename: use this to save to a different path
        """
        if optional_filename:
            path_to_use = optional_filename
        else:
            path_to_use = self.get_path() + ".node"
        with open(path_to_use, "wb") as f:
            pickle.dump(self, f)
        return True

    @staticmethod
    def load(filename):
        """
        Load the node in the given file
        """
        with open(filename, "rb") as f:
            out = pickle.load(f)
        return out

