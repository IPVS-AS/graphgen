from __future__ import annotations

import os, itertools, uuid
from typing import List, Set, Iterator, Dict, Any
from graphviz import Digraph # type: ignore
from copy import deepcopy
from datetime import datetime
from enum import Enum



class NType(Enum):
    ACTIVITY = 'A'
    DATA = 'D'

class DType(Enum):
    PLANNING = 'Planning'
    SIMULATION = 'Simulation'
    TESTING = 'Testing'
    CONSTRUCTION = 'Construction'
    #PLANNING1 = 'Planning1'
    #SIMULATION1 = 'Simulation1'
    #TESTING1 = 'Testing1'
    #CONSTRUCTION1 = 'Construction1'
    #PLANNING2 = 'Planning2'
    #SIMULATION2 = 'Simulation2'


class Node:
    id_pool : Iterator[int] = itertools.count()

    def __init__(self, name : str = 'Dummy') -> None:
        self.uuid : str = str(uuid.uuid4())
        self.id = next(Node.id_pool)
        self.name : str = name
        self.outgoing : List[Node] = []
        self.ntype = NType.ACTIVITY
        self.dtype = DType.PLANNING
        self.metadata : Dict[str, Any] = {}

    @property
    def label(self) -> str:
        return f'{self.ntype.value} {self.dtype.value}'

    def out(self, *nodes : Node) -> Node:
        self.outgoing = list(nodes)
        return self

    def serialize_vertex(self, sad : bool = True) -> str:
        return f'v {self.id} {ntype_sad_serialize[self.ntype]}{dtype_sad_serialize[self.dtype]}'

    def serialize_edges(self, sad : bool = True) -> str:
        s : List[str] = []
        for child in self.outgoing:
            s.append(f'e {self.id} {child.id} 1')
        return '\n'.join(s)

    def __copy__(self) -> Node:
        n : Node = type(self)(name='__copy__')
        n.name = self.name
        n.outgoing = self.outgoing
        n.ntype = self.ntype
        n.dtype = self.dtype
        n.metadata = self.metadata
        return n

    def __deepcopy__(self, memo : Dict[int, Node]) -> Node:
        n : Node = type(self)(name='__deepcopy__')
        n.name = self.name
        n.outgoing = self.outgoing
        n.ntype = self.ntype
        n.dtype = self.dtype
        n.metadata = deepcopy(self.metadata) # type: ignore
        memo[id(self)] = n
        n.outgoing = deepcopy(self.outgoing, memo)
        return n

    def __repr__(self) -> str:
        return f'Node("{self.label}"):{self.id}'

    def __str__(self) -> str:
        return f'({self.name} id:{self.id} {self.label})'

    def ascii(self, len_prev_pad : int = 0, visited : Set[Node] = set()) -> str:
        arrow_start : str = ' '
        arrow_end : str = '-> '
        arrow_mid : str = '--'
        arrow_branch : str = '|-'
        assert len(arrow_mid) == len(arrow_branch)

        label : str = self.label
        pad : str = (len_prev_pad + len(label) + len(arrow_start)) * ' '

        if self in visited:
            return f'go to: {label}'
        visited.add(self)

        if self.outgoing:
            l : List[str] = [label, arrow_start]
            for i, v in enumerate(self.outgoing):
                l.append(pad if i > 0 else "")
                l.append(arrow_branch if i > 0 else arrow_mid)
                l.append(arrow_end)
                l.append(v.ascii(len(pad) + len(arrow_end) + len(arrow_mid), visited))
                l.append(os.linesep if i < len(self.outgoing) - 1 else "")
            return ''.join(l)
        return label

    def view(self, folder : str = './graphviz'):
        g : Digraph = self.to_dot()
        g = g.unflatten(stagger=5) # type: ignore
        g.render(view=True, directory=folder, filename=f'{datetime.now()}-{self.label}-{self.uuid}.gz', cleanup=False) # type: ignore

    def plot(self, folder : str = './graphviz'):
        g : Digraph = self.to_dot()
        g = g.unflatten(stagger=5) # type: ignore
        g.render(view=False, directory=folder, filename=f'{datetime.now()}-{self.label}-{self.uuid}.gz', cleanup=False) # type: ignore

    def to_dot(self) -> Digraph:
        g = Digraph()
        g.node(name=str(self.uuid), label=f'{self.label} {self.id}') # type: ignore
        Node.__to_dot_acc(self, g)
        return g

    @classmethod
    def __to_dot_acc(cls, n : Node, g : Digraph, visited : Set[Node] = set()):
        if n in visited:
                return
        visited.add(n)
        if not n.outgoing:
            return
        for child in n.outgoing:
            g.node(name=str(child.uuid), label=f'{child.label} {child.id}') # type: ignore
            g.edge(str(n.uuid), str(child.uuid)) # type: ignore
            Node.__to_dot_acc(child, g, visited)


class DNode(Node):
    def __init__(self, name : str, dtype : DType) -> None:
        super().__init__(name)
        self.ntype = NType.DATA
        self.dtype = dtype

class ANode(Node):
    def __init__(self, name : str, dtype : DType) -> None:
        super().__init__(name)
        self.ntype = NType.ACTIVITY
        self.dtype = dtype


ntype_sad_serialize = {
    NType.ACTIVITY : 1,
    NType.DATA : 2,
}
ntype_sad_serialize_rev = {
    1 : NType.ACTIVITY,
    2 : NType.DATA,
}
dtype_sad_serialize = {
    DType.PLANNING : 1,
    DType.SIMULATION : 2,
    DType.TESTING : 3,
    DType.CONSTRUCTION : 4,
    #DType.PLANNING1 : 5,
    #DType.SIMULATION1 : 6,
    ##DType.TESTING1 : 7,
    #DType.CONSTRUCTION1 : 8,
    #DType.PLANNING2 : 9,
    #DType.SIMULATION2 : 0,
}
dtype_sad_serialize_rev = {
    1 : DType.PLANNING,
    2 : DType.SIMULATION,
    3 : DType.TESTING,
    4 : DType.CONSTRUCTION,
    #5 : DType.PLANNING1,
    #6 : DType.SIMULATION1,
    #7 : DType.TESTING1,
    #8 : DType.CONSTRUCTION1,
    #9 : DType.PLANNING2,
    #0 : DType.SIMULATION2,
}
