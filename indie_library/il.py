import pickle


# offers a way to display a Formula using latex string and a tite.
class Formula(object):
    def __init__(self, name: str = "", formulation: str = "") -> None:
        super().__init__()
        self.name = name
        self.formulation = formulation

    def display(self, **kwargs) -> str:
        return self.formulation.format(**kwargs)

    def get_formulation(self) -> str:
        return self.formulation

    def set_formulation(self, formulation: str) -> None:
        self.formulation = formulation


# offers an explanation to be attached to Formula
class WhimsicalFormula(Formula):
    def __init__(self, name: str, formulation: str, explanation: str) -> None:
        super().__init__(name=name, formulation=formulation)
        self.explanation = explanation


# offers a sequence of other formulas atop the whimsical explanation
class LogicalFormula(WhimsicalFormula):
    def __init__(self, name: str, formulation: str, explanation: str, sequence) -> None:
        super().__init__(name, formulation, explanation)
        self.sequence: list = sequence


# offers an index of subformulae for each formula contained within a logical formula
class Alphabet(LogicalFormula):
    def __init__(self, name: str, formulation: str, explanation: str, sequence) -> None:
        super().__init__(name, formulation, explanation, sequence)
        self.indices = {}
        i = 1
        for f in self.sequence:
            self.indices[f.name] = i
            i += 1

    def __init__(self, formula: LogicalFormula) -> None:
        super().__init__(formula.name, formula.formulation, formula.explanation, formula.sequence)
        self.indices = {}
        i = 1
        for f in self.sequence:
            self.indices[f.name] = i
            i += 1


# a node will be the primitive object for a DAG, capable of holding a sequence of other nodes and adding
class Node(object):
    def __init__(self, name: str, author="") -> None:
        super().__init__()
        self.address: list = []
        self.nodes: list = []
        self.name: str = name
        self.formula: LogicalFormula = None
        self.content: str = ""
        self.author: str = author

    # Method to check if a node is in this one by exhaustive name search.
    def has_node(self, name) -> bool:
        for node in self.get_nodes():
            if node.get_name() == name:
                return True
        return False

    def read(self) -> str:
        return "[" + self.get_name() + "]{" + self.get_content() + "\n}"

    def read_for_embed(self) -> str:
        return self.get_content()

    def write(self, text: str) -> None:
        self.set_content(self.get_content() + "\n" + text)

    def set_content(self, content: str) -> None:
        self.content = content

    def get_content(self) -> str:
        return self.content

    def copy(self, node):
        node: Node = node
        copy = Node(node.name)
        copy.set_address(node.get_address())
        copy.set_nodes(node.get_nodes())
        return copy

    def set_address(self, address) -> None:
        address: list = address
        self.address = address

    def get_order(self) -> int:
        return len(self.nodes)

    def get_address(self):
        return list(self.address)

    def get_nodes(self):
        return list(self.nodes)

    def set_nodes(self, nodes):
        self.nodes = nodes

    def add_node(self, node) -> None:
        for n in self.get_nodes():
            if node.get_name() == n.get_name():
                raise Exception("Name conflict when trying to add node.")
        add_node: Node = self.copy(node)
        address = self.get_address()
        address.append(self.get_order())
        add_node.set_address(address)
        for n in node.get_nodes():
            add_node.add_node(n)
        self.nodes.append(add_node)

    def kill_node(self, name: str):
        for n in self.get_nodes():
            if n.get_name() == name:
                self.nodes.remove(n)
                return
        raise Exception("Name not found.")

    def get_node(self, directions):
        if len(directions) == 0:
            return self
        if len(directions) == 1:
            if len(self.get_nodes()) >= directions[0] + 1:
                return self.get_nodes()[directions[0]]
        if len(self.get_nodes()) >= directions[0] + 1:
            return self.get_nodes()[directions[0]].get_node(directions[1:])
        raise Exception("Invalid address: " + str(directions) + ".")

    def get_node_in_node(self, name: str):
        if self.has_node(name):
            for n in self.get_nodes():
                if n.get_name() == name:
                    return n
        raise Exception("No node found with that name in this node when running get_node_in_node.")

    def get_node_address(self, directions):
        if len(directions) == 0:
            return self.get_name()
        if len(directions) == 1:
            if len(self.get_nodes()) >= directions[0] + 1:
                return self.get_name() + "\\" + self.get_nodes()[directions[0]].get_name()
        if len(self.get_nodes()) >= directions[0] + 1:
            return self.get_name() + "\\" + self.get_nodes()[directions[0]].get_node_address(directions[1:])
        raise Exception("Invalid address: " + str(directions) + ".")

    def get_node_by_name(self, node_name):
        for node in self.get_nodes():
            if node.get_name() == node_name:
                return node

        return None

    def get_name(self) -> str:
        return self.name

    def printname(self):
        print(self.name)

    def load(self, filename):
        with open(filename, 'rb') as load_file:
            return pickle.load(load_file)

    def save(self, filename=""):
        if filename == "":
            filename = self.get_name()
        with open(filename, 'wb') as save_file:
            pickle.dump(self, save_file)

