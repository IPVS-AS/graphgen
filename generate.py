from __future__ import annotations

import sys
import math
import random
from collections import deque
from copy import deepcopy
from statistics import mean, median
from typing import Any, Callable, Dict, List, Sequence, Set, Tuple

import matplotlib.pyplot as plt

from node import ANode, DNode, DType, Node, NType



def test_graph2() -> Node:
    tree1 = Node('A CAD').out(
        Node('D Model').out(
            Node('A CAE').out(
                Node('D DHC'),
                Node('D dP1'),
                Node('D dP2'),
                Node('D dP3'),
            ),
            Node('A Prot').out(
                Node('D Prod').out(
                    Node('A CAT').out(
                        Node('D DHC'),
                        Node('D dP1'),
                        Node('D dP2'),
                        Node('D dP3'),
                    )
                )
            )
        )
    )

    root = Node('D Spec').out(
        tree1,
        Node('A CAD').out(
            Node('D Model').out(
                Node('A CAE').out(
                    Node('D DHC'),
                    Node('D dP1'),
                    Node('D dP2'),
                    Node('D dP3'),
                ),
                Node('A Prot').out(
                    Node('D Prod').out(
                        Node('A CAT').out(
                            Node('D DHC'),
                            Node('D dP1'),
                            Node('D dP2'),
                            Node('D dP3'),
                        ),
                        Node('A ManPlan').out(
                            Node('D ManPlan'),
                            deepcopy(tree1)
                        )
                    )
                )
            )
        ),
        Node('A CAD').out(
            Node('D Model').out(
                Node('A CAE').out(
                    Node('D DHC'),
                    Node('D dP'),
                ),
            )
        ),
    )
    return root



def test_graph1() -> Node:
    a = Node('A')
    b1, b2, b3 = Node('B1'), Node('B2'), Node('B3')
    a.outgoing = [b1, b2, b3]
    c1, c2, c3 = Node('C1'), Node('C2'), Node('C3')
    b2.outgoing = [c1, c2, c3]
    d1, d2, d3 = Node('D1'), Node('D2'), Node('D3')
    c1.outgoing = [d1, d2, d3]
    d1, d2, d3 = Node('E1'), Node('E2'), Node('E3')
    c3.outgoing = [d1, d2, a]
    return a



def pattern_a() -> Node:
    return ANode('P_1', DType.PLANNING).out(
        DNode('D_{P_{1},1}', DType.PLANNING).out(
            ANode('S_1', DType.SIMULATION).out(
                DNode('D_{S_{1},1}', DType.SIMULATION),
                DNode('D_{S_{1},2}', DType.SIMULATION),
            ),
        ),
        DNode('D_{P_{1},2}', DType.PLANNING).out(
            ANode('S_2', DType.SIMULATION).out(
                DNode('D_{S_{2},1}', DType.SIMULATION),
                DNode('D_{S_{2},2}', DType.SIMULATION),
            ),
        ),
        DNode('D_{P_{1},3}', DType.PLANNING).out(
            ANode('S_3', DType.SIMULATION).out(
                DNode('D_{S_{3},1}', DType.SIMULATION),
                DNode('D_{S_{3},2}', DType.SIMULATION),
            ),
        )
    )



def pattern_b() -> Node:
    return ANode('P_1', DType.PLANNING).out(
            DNode('D_{P_{1},1}', DType.PLANNING).out(
                ANode('S_1', DType.SIMULATION).out(
                    DNode('D_{S_{1},1}', DType.SIMULATION).out(
                        ANode('P_2', DType.PLANNING).out(
                            DNode('D_{P_{2},1}', DType.PLANNING).out(
                                ANode('S_2', DType.SIMULATION).out(
                                    DNode('D_{S_{2},1}', DType.SIMULATION).out(
                                        ANode('P_3', DType.PLANNING).out(
                                            DNode('D_{P_{3},1}', DType.PLANNING).out(
                                                ANode('S_3', DType.SIMULATION).out(
                                                    DNode('D_{S_{3},1}', DType.SIMULATION)
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
    )



def graph_to_set(root : Node) -> Tuple[Set[Node], Set[Node]]:
    s : Set[Node] = set()
    s_leaves : Set[Node] = set()
    Q : deque[Node] = deque([root])
    while Q:
        u = Q.popleft()
        if u in s:
            continue
        Q.extend(u.outgoing)
        s.add(u)
        if not u.outgoing:
            s_leaves.add(u)
    return s, s_leaves



def calculate_dists(root : Node) -> Dict[Node, int]:
    dist : Dict[Node, int] = {}
    Q : deque[Node] = deque([root])
    dist[root] = 0
    while Q:
        u = Q.popleft()
        #u.label = f'{u.label} hops={dist[u]}'
        for v in u.outgoing:
            if v in dist:
                continue
            dist[v] = dist[u] + 1
            Q.append(v)
    return dist



def add_noise(root : Node, probs : Tuple[float, float, float, float]) -> Node:
    if all(p < sys.float_info.epsilon for p in probs):
        return root

    leaf_addition_prob  : float = probs[0]
    leaf_deletion_prob  : float = probs[1]
    inner_addition_prob : float = probs[2]
    inner_deletion_prob : float = probs[3]

    Q : deque[Node] = deque([root])
    visited : Set[Node] = set(Q)
    while Q:
        u = Q.popleft()

        # Random inner addition
        if u.outgoing:
            if random.random() < inner_addition_prob:
                node : Node = Node('')
                node.ntype = random.choice(list(NType))
                node.dtype = random.choice(list(DType))
                i = random.randint(0, len(u.outgoing) - 1)
                child = u.outgoing[i]
                u.outgoing[i] = node
                node.outgoing.append(child)
        # Random leaf addition
        else:
            if random.random() < leaf_addition_prob:
                node : Node = Node('')
                node.ntype = random.choice(list(NType))
                node.dtype = random.choice(list(DType))
                u.outgoing.append(node)

        for child in u.outgoing:
            if child in visited:
                continue
            visited.add(child)

            # Random inner deletion
            if child.outgoing:
                if random.random() < inner_deletion_prob:
                    i = random.randint(0, len(child.outgoing) - 1)
                    grandchild = child.outgoing[i]
                    e = u.outgoing.index(child)
                    u.outgoing[e] = grandchild
                    Q.append(grandchild)
                    continue
            # Random leaf deletion
            else:
                if random.random() < leaf_deletion_prob:
                    u.outgoing.remove(child)
                    continue
            Q.append(child)
    return root



def grow_graph(root : Node, dist_max_nodes : int = 4000) -> Tuple[Node, int, int]:
    leaves : Set[Node]
    _, leaves = graph_to_set(root)

    new_nodes : int = 0
    min_new_nodes : int = 20
    max_new_nodes : int = dist_max_nodes
    termination_prob : float
    Q : deque[Node] = deque(leaves)

    while Q:
        termination_prob = max(0.2, math.sqrt(new_nodes / max_new_nodes)) # strong rise initially, tapers off towards the end -> deeper trees
        #termination_prob = max(0.2, math.pow(new_nodes / max_new_nodes, 2)) # exponential rise -> broader trees
        u = Q.popleft()

        # Do we terminate this node?
        if random.random() < termination_prob and new_nodes > min_new_nodes:
            continue

        # Determine number of splits with folded normal distribution
        #splits = round(0.5 + abs(random.normalvariate(0, 2))) # broader trees
        splits = round(0.5 + abs(random.normalvariate(0, 1))) # deeper trees
        new_nodes += splits
        for _ in range(splits):
            node : Node
            if u.ntype is NType.ACTIVITY:
                node = DNode(f'D {u.dtype.value}', u.dtype)
            if u.ntype is NType.DATA:
                dtype = random.choice(list(DType))
                node = ANode(f'A {dtype.value}', dtype)
            else:
                raise RuntimeError('Unknown u.ntype:', str(u.ntype))
            u.outgoing.append(node)
            Q.append(node)
    return root, new_nodes, max(calculate_dists(root).values())



def plot_hist(x : Sequence[Any], bins : Sequence[int] = range(0, 10)):
    print(f'Hist min: {min(x)} | Hist max: {max(x)}')
    plt.hist(x, bins=bins) # type: ignore
    plt.show()
#plot_hist([round(0.5 + abs(random.normalvariate(0, 1))) for i in range(10000)])



def create_graph_list(pattern : Callable[[], Node], num : int = 1000, dist_max_nodes : int = 4000) -> List[Node]:
    avg_new : List[int] = []
    avg_dist : List[int] = []

    graphs = [pattern() for _ in range(num)]
    for g in graphs:
        g, *stats = grow_graph(g, dist_max_nodes=dist_max_nodes)
        avg_new.append(stats[0])
        avg_dist.append(stats[1])

    r = round
    print(f'Graphs: {num} ({pattern.__name__})')
    print(f'   New nodes mean: {r(mean(avg_new)):4}  | median: {r(median(avg_new)):4}  | min: {r(min(avg_new)):4}  | max: {r(max(avg_new)):4}')
    print(f'   Max dist mean : {r(mean(avg_dist)):4}  | median: {r(median(avg_dist)):4}  | min: {r(min(avg_dist)):4}  | max: {r(max(avg_dist)):4}')
    return graphs



def write_out(graphs : Sequence[Node], file_prefix : str, file_location : str = './graphs/graphs', gspan : bool = True):
    output : List[str] = []
    gnum : int = 0 if gspan else 1

    if not gspan:
        new_root : Node = Node('Connector')
        for g in graphs:
            new_root.outgoing.append(g)
        graphs = [new_root]

    for g in graphs:
        output.append(f't # {gnum}\n')
        gnum += 1

        nodes, _ = graph_to_set(g)
        vnum : int = 0
        # Assign new, monotonous IDs to pluck holes created by deletions
        for n in nodes:
            n.id = vnum
            vnum += 1
        # GraMi requires sorted node IDs
        nodes = list(nodes)
        nodes.sort(key=lambda x: x.id)
        for n in nodes:
            output.append(f'{n.serialize_vertex()}\n')
        for n in nodes:
            edges = n.serialize_edges().strip()
            if edges:
                output.append(f'{edges}\n')

    if gspan:
        output.append('t # -1\n')
    with open(f'{file_location}-{file_prefix}-{"gspan" if gspan else "grami"}', 'w') as f:
        f.writelines(output)


def __main__():
    g = create_graph_list(pattern_a, num=100, dist_max_nodes=2000) + create_graph_list(pattern_b, num=100, dist_max_nodes=2000)
    for prob in [
            (0.00, 0.00, 0.00, 0.00),
            ]:
        g = [add_noise(i, prob) for i in g]
        write_out(g, file_prefix=f'combined-err-{prob[0]}', gspan=True)
        write_out(g, file_prefix=f'combined-err-{prob[0]}', gspan=False)
