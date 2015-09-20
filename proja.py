import uuid


class Agent(object):

    def __init__(self, name, root=None):
        self.name = name
        self.root = root

    def get_nodes(self):
        return self.root.get_nodes()

    def get_childs(self):
        return self.root.get_childs()

    def get_outward_edges(self):
        return self.root.get_outward_edges()


class Node(object):

    def __init__(self, author, content='Content'):
        self.ident = uuid.uuid4()
        self.childs = []
        self.author = author
        self.content = content

    def add_child(self, node):
        self.childs.append(node)

    def get_childs(self):
        if not self.childs:
            return []
        cs = []
        for c in self.childs:
            cs += [c.content] + c.get_childs()
        return cs

    def get_outward_edges(self):
        if not self.childs:
            return []
        es = []
        for c in self.childs:
            es += [(self.ident, c.ident)] + c.get_outward_edges()
        return es


class PolyForest(object):

    def __init__(self, agents):
        self.agents = agents

        for agent in self.agents:
            agent.root = Node(agent, content='Root for {}'.format(agent.name))

    def add_agent(self, agent):
        self.agents.append(agent)

    def get_nodes(self):
        ns = []
        for agent in self.agents:
            ns += [agent.root.ident] + agent.get_childs()
        return set(ns)

    def get_edges(self):
        es = []
        for agent in self.agents:
            es += agent.get_outward_edges()
        return set(es)
