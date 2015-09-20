import networkx as nx
import matplotlib.pyplot as plt
import proja


def draw(g):
    nodes = g.get_nodes()
    edges = g.get_edges()

    # create networkx g
    G = nx.DiGraph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in edges:
        G.add_edge(edge[0], edge[1])

    # draw g
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    labels = dict(zip(nodes, nodes))
    nx.draw_networkx_labels(G, pos, labels=labels)

    # show g
    plt.show()

if __name__ == '__main__':
    agents = [
        proja.Agent('Alice'),
        proja.Agent('Bob'),
        proja.Agent('Charlie')
    ]

    G = proja.PolyForest(agents)

    alice = G.agents[0]
    bob = G.agents[1]
    node_cinema = proja.Node(author=alice, content='Want to go to the cinema?')
    alice.root.add_child(node_cinema)
    bob.root.add_child(node_cinema)

    draw(G)
