import collections
from typing import Dict, Set, List, Tuple
import matplotlib.pyplot as plt


class CurriculumGraph:
    def __init__(self):
        self.adj: Dict[str, Set[str]] = {}

    def add_discipline(self, name: str):
        if name not in self.adj:
            self.adj[name] = set()

    def remove_discipline(self, name: str):
        if name in self.adj:
            del self.adj[name]
        for s in list(self.adj.keys()):
            self.adj[s].discard(name)

    def add_prereq(self, prereq: str, course: str):
        self.add_discipline(prereq)
        self.add_discipline(course)
        self.adj[prereq].add(course)

    def remove_prereq(self, prereq: str, course: str):
        if prereq in self.adj:
            self.adj[prereq].discard(course)

    def get_prereqs(self, course: str) -> List[str]:
        return [u for u, neigh in self.adj.items() if course in neigh]

    def _dfs_has_path(self, start: str, end: str, visited: Set[str]) -> bool:
        if start == end:
            return True
        visited.add(start)
        for v in self.adj.get(start, []):
            if v not in visited and self._dfs_has_path(v, end, visited):
                return True
        return False

    def has_dependency(self, a: str, b: str) -> Tuple[bool, str]:
        if a not in self.adj or b not in self.adj:
            return (False, '')
        if self._dfs_has_path(a, b, set()):
            return (True, f"{a} → {b}")
        if self._dfs_has_path(b, a, set()):
            return (True, f"{b} → {a}")
        return (False, '')

    def has_cycle(self) -> bool:
        state = {u: 0 for u in self.adj}

        def dfs(u):
            state[u] = 1
            for v in self.adj[u]:
                if state.get(v, 0) == 1:
                    return True
                if state.get(v, 0) == 0 and dfs(v):
                    return True
            state[u] = 2
            return False

        for u in self.adj:
            if state[u] == 0 and dfs(u):
                return True
        return False

    def topological_sort(self) -> List[str]:
        indeg = {u: 0 for u in self.adj}
        for u in self.adj:
            for v in self.adj[u]:
                indeg[v] = indeg.get(v, 0) + 1
        q = collections.deque([u for u in indeg if indeg[u] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in self.adj.get(u, []):
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        if len(order) != len(self.adj):
            raise ValueError("O grafo contém ciclos — não é possível ordenar.")
        return order

    def _collect_prereq_subgraph(self, target: str) -> Set[str]:
        rev = {u: set() for u in self.adj}
        for u in self.adj:
            for v in self.adj[u]:
                rev[v].add(u)

        visited = set()
        stack = [target]
        while stack:
            x = stack.pop()
            if x not in visited:
                visited.add(x)
                stack.extend(rev.get(x, []))
        return visited

    def progression_to(self, target: str) -> List[str]:
        nodes = self._collect_prereq_subgraph(target)
        sub_adj = {u: set(v for v in self.adj[u] if v in nodes) for u in nodes}

        indeg = {u: 0 for u in sub_adj}
        for u in sub_adj:
            for v in sub_adj[u]:
                indeg[v] = indeg.get(v, 0) + 1

        q = collections.deque([u for u in indeg if indeg[u] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in sub_adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order

    def visualize(self, target: str = None):
        import networkx as nx

        G = nx.DiGraph()
        for u in self.adj:
            for v in self.adj[u]:
                G.add_edge(u, v)

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, seed=10, k=1.5)

        if target and target in self.adj:
            subnodes = self._collect_prereq_subgraph(target)
            node_colors = ['lightgreen' if n in subnodes else 'lightgray' for n in G.nodes()]
            nx.draw(
                G, pos,
                with_labels=True,
                node_color=node_colors,
                arrows=True,
                arrowsize=18,
                node_size=3000,
                edgecolors="black",
                font_size=10,
                font_weight="bold"
            )
            nx.draw_networkx_edge_labels(G, pos, font_size=8, label_pos=0.5)
            plt.title(f"Progressão até '{target}' (verde = necessário)", fontsize=14, fontweight="bold")
        else:
            nx.draw(
                G, pos,
                with_labels=True,
                node_color="#a3c4f3",
                arrows=True,
                arrowsize=18,
                node_size=3000,
                edgecolors="black",
                font_size=10,
                font_weight="bold"
            )
            nx.draw_networkx_edge_labels(G, pos, font_size=8, label_pos=0.5)
            plt.title("Rede de Disciplinas e Pré-requisitos", fontsize=14, fontweight="bold")

        plt.axis("off")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    g = CurriculumGraph()

    disciplinas = [
        "Cálculo I", "Cálculo II", "Álgebra Linear",
        "Física I", "Física II",
        "Estrutura de Dados I", "Estrutura de Dados II",
        "Desenho Técnico",
        "Sistemas Operacionais", "Redes de Computadores",
        "Trabalho de Conclusão"
    ]
    for d in disciplinas:
        g.add_discipline(d)

    g.add_prereq("Cálculo I", "Cálculo II")
    g.add_prereq("Álgebra Linear", "Cálculo II")
    g.add_prereq("Física I", "Física II")
    g.add_prereq("Estrutura de Dados I", "Estrutura de Dados II")
    g.add_prereq("Estrutura de Dados II", "Redes de Computadores")
    g.add_prereq("Estrutura de Dados II", "Sistemas Operacionais")
    g.add_prereq("Redes de Computadores", "Trabalho de Conclusão")
    g.add_prereq("Sistemas Operacionais", "Trabalho de Conclusão")
    g.add_prereq("Desenho Técnico", "Trabalho de Conclusão")

    print("Pré-requisitos de Cálculo II:", g.get_prereqs("Cálculo II"))
    print("Estrutura de Dados I e Trabalho de Conclusão têm dependência?",
          g.has_dependency("Estrutura de Dados I", "Trabalho de Conclusão"))
    print("Há ciclos no grafo?", g.has_cycle())

    print("\nOrdem sugerida para cursar:")
    for i, d in enumerate(g.topological_sort(), 1):
        print(f"{i:2d}. {d}")

    print("\nProgressão até 'Trabalho de Conclusão':")
    print(g.progression_to("Trabalho de Conclusão"))

    g.visualize(target="Trabalho de Conclusão")

