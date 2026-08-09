from dataclasses import dataclass
import networkx as nx


@dataclass(frozen=True)
class Reaction:
  name: str
  reactants: frozenset
  products: frozenset


def initialize():
  F = {"a","b"}
  r1 = Reaction(name="r1", reactants=frozenset(["a","b"]), products=frozenset(["c"]))
  r2 = Reaction(name="r2", reactants=frozenset(["b","c"]), products=frozenset(["d"]))
  R = {r1,r2}
  C = {
    ("d", r1),
    ("a", r2)
  }
  X = F | {m for r in R for m in r.reactants | r.products}

  print(X)
  return 0


def main():
  initialize()
  return 0



if __name__ == "__main__":
  main()