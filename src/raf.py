from dataclasses import dataclass
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Reaction:
    name: str
    reactants: frozenset
    products: frozenset


def initialize():
    # case 1: RAF sample from Hordijk & Steel 2004.
    # F = {"a", "b"}
    # r1 = Reaction(name="r1", reactants=frozenset(["a", "b"]), products=frozenset(["c"]))
    # r2 = Reaction(name="r2", reactants=frozenset(["b", "c"]), products=frozenset(["d"]))
    # r3 = Reaction(
    #     name="r3", reactants=frozenset(["c", "d"]), products=frozenset(["e", "f"])
    # )
    # r4 = Reaction(name="r4", reactants=frozenset(["a", "e"]), products=frozenset(["g"]))
    # R = {r1, r2, r3, r4}
    # C = {("d", r1), ("a", r2), ("f", r4)}

    # case 2: a reaction set is RA, but not F-generated.
    # F = {"a", "b"}
    # r1 = Reaction(name="r1", reactants=frozenset(["a"]), products=frozenset(["b"]))
    # r2 = Reaction(name="r2", reactants=frozenset(["c"]), products=frozenset(["d"]))
    # r3 = Reaction(name="r3", reactants=frozenset(["d"]), products=frozenset(["e"]))
    # R = {r1, r2, r3}
    # C = {("c", r1), ("a", r2), ("b", r3)}

    # case 3: removing a catalysts "d" from case 1.
    F = {"a", "b"}
    r1 = Reaction(name="r1", reactants=frozenset(["a", "b"]), products=frozenset(["c"]))
    r2 = Reaction(name="r2", reactants=frozenset(["b", "c"]), products=frozenset(["d"]))
    r3 = Reaction(
        name="r3", reactants=frozenset(["c", "d"]), products=frozenset(["e", "f"])
    )
    r4 = Reaction(name="r4", reactants=frozenset(["a", "e"]), products=frozenset(["g"]))
    R = {r1, r2, r3, r4}
    C = {("a", r2), ("f", r4)}

    display_graph(F, R, C)
    while True:
        R_size = len(R)
        reduce_to_RA(R, C)
        W = compute_closure(F, R)
        reduce_to_F_generated(R, W)
        if R_size == len(R) or len(R) == 0:
            break
    display_graph(F, R, C)

    return 0


def display_graph(F, R, C):
    G = nx.DiGraph()

    # add Food as nodes.
    for food in F:
        G.add_node(food, color="pink", type="molecule", is_food=True)

    # add remaining molecules as nodes.
    supp_R = {m for r in R for m in r.reactants | r.products}
    target_molecules = supp_R - F
    for molecule in target_molecules:
        G.add_node(molecule, color="cyan", type="molecule", is_food=False)

    # add reactions.
    catalysts_by_reaction = defaultdict(set)
    for x, reaction in C:
        catalysts_by_reaction[reaction].add(x)
    for r in R:
        G.add_node(r, color="orange", type="reaction")
        for reactant in r.reactants:
            G.add_edge(reactant, r, relation="reactant")
        for product in r.products:
            G.add_edge(r, product, relation="reactant")
        # add catalysts.
        for x in catalysts_by_reaction[r]:
            if not x in target_molecules | F:
                G.add_node(x, type="molecule", color="silver")
            G.add_edge(x, r, relation="catalyst", style="dashed")

    # create labels. display "name" if they have.
    labels = {}
    for n in G.nodes:
        if hasattr(n, "name"):
            labels[n] = n.name
        else:
            labels[n] = str(n)
    # extract colors.
    colors = [G.nodes[n]["color"] for n in G.nodes]

    # plot a NetworkX graph.
    pos = nx.spring_layout(G, seed=42)
    reaction_edges = [
        (u, v) for u, v, d in G.edges(data=True) if d.get("style") != "dashed"
    ]
    catalyst_edges = [
        (u, v) for u, v, d in G.edges(data=True) if d.get("style") == "dashed"
    ]
    nx.draw_networkx_nodes(G, pos, node_color=colors)
    nx.draw_networkx_edges(G, pos, edgelist=reaction_edges, style="solid")
    nx.draw_networkx_edges(G, pos, edgelist=catalyst_edges, style="dashed")
    nx.draw_networkx_labels(G, pos, labels=labels)
    plt.show()


def reduce_to_RA(R, C):
    """
    reduce a reaction set to an RA set.
    Parameters:
        R: a set of class Reaction
        C: a set of catalysts
    """
    catalysts_by_reaction = defaultdict(set)
    for x, reaction in C:
        catalysts_by_reaction[reaction].add(x)

    while True:
        supp_R = {m for r in R for m in r.reactants | r.products}
        total_reactions = len(R)
        reactions_to_remove = set()
        for r in R:
            catalysts = catalysts_by_reaction.get(r, set())
            if catalysts.isdisjoint(supp_R):
                reactions_to_remove.add(r)
        R -= reactions_to_remove
        if len(R) == total_reactions:
            break


def compute_closure(F, R):
    W = F.copy()
    while True:
        is_found = False
        for r in R:
            if r.reactants <= W and not r.products <= W:
                W = W | r.products
                is_found = True
        if not is_found:
            break
    return W


def reduce_to_F_generated(R, W):
    reactions_to_remove = set()
    for r in R:
        if not r.reactants <= W:
            reactions_to_remove.add(r)
    R -= reactions_to_remove


def main():
    initialize()
    return 0


if __name__ == "__main__":
    main()
