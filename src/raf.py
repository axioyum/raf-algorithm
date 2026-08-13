from dataclasses import dataclass
import networkx as nx
from collections import defaultdict


@dataclass(frozen=True)
class Reaction:
    name: str
    reactants: frozenset
    products: frozenset


def initialize():
    F = {"a", "b"}
    r1 = Reaction(name="r1", reactants=frozenset(["a", "b"]), products=frozenset(["c"]))
    r2 = Reaction(name="r2", reactants=frozenset(["b", "c"]), products=frozenset(["d"]))
    r3 = Reaction(name="r3", reactants=frozenset(["c", "d"]), products=frozenset(["e"]))
    R = {r1, r2, r3}
    C = {("d", r1), ("a", r2), ("g", r3)}

    print(R)
    reduce_to_RA(R, C)
    print(R)
    return 0


def reduce_to_RA(R, C):
    supp_R = {m for r in R for m in r.reactants | r.products}
    catalysts_by_reaction = defaultdict(set)
    for x, reaction in C:
        catalysts_by_reaction[reaction].add(x)

    while True:
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
    W = F
    while True:
        is_found = False
        for A, B in R:
            if A <= W and not B <= W:
                W = W + B
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
