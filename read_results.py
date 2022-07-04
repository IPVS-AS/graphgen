from __future__ import annotations

import os
import sys
import itertools
from typing import Any, Dict, List, Set

import pandas as pd

from node import Node, ntype_sad_serialize_rev, dtype_sad_serialize_rev
from generate import graph_to_set


def dict_to_str(d : Dict[Any, Any], ignore_empty : bool = False, level : int = 0) -> str:
    """
    Creates a neat string representation of the passed dictionary.

    Parameters
    ----------
    d : dict
        Dictionary to format.
    ignore_empty : bool, optional
        Whether to skip sequences of length < 1 or print them empty. False by default.
    level : int, optional
        Current level of indentation, by default 0.

    Returns
    -------
    str
        Passed dictionary formatted as single string.
    """
    INDENT : str = '    '
    SPACE  : str = ' '
    SPACE_SEP : str = '{space}->'
    SPACE_SEP_ESCAPE : str = '::SPACE_SEP_ESCAPE::'

    if not d:
        if ignore_empty:
            return ''
        return '{indent}(empty dict)'.format(indent=INDENT * level)
    s : List[str] = []
    l : List[int] = []
    for k, v in d.items():
        #if ignore_empty and len(v) < 1:
        #    continue
        if isinstance(v, dict):
            v = '...{endl}{v}'.format(endl=os.linesep, v=dict_to_str(v, ignore_empty, level + 1)) # type: ignore
        elif isinstance(v, pd.DataFrame):
            v = '(pandas.DataFrame){endl}{v}'.format(endl=os.linesep, v=str(v))
        else:
            v = repr(v)
        prefix = '{indent}{symbol}'.format(indent=INDENT * level, symbol='| ' if level > 0 else '')
        k = str(k)
        l.append(len(k))
        s.append('{pref}{k} {sep} {v}'.format(pref=prefix, k=k, sep=SPACE_SEP, v=v))
    m = min(max(l), 60)
    for i, e in enumerate(s):
        # In case the strings here also contain some curly brakcets {} it's possible that format()
        # will throw a KeyError as it considers all {} as tokens to replace. Specifically happens
        # to serialized DataFrames as they are JSON objects in one single string.
        try:
            s[i] = e.format(space=SPACE * (m - l[i]))
        except KeyError:
            s[i] = e.replace(SPACE_SEP, SPACE_SEP_ESCAPE) \
                    .replace('{', '{{') \
                    .replace('}', '}}') \
                    .replace(SPACE_SEP_ESCAPE, SPACE_SEP) \
                    .format(space=SPACE * (m - l[i])) \
                    .replace('{{', '{') \
                    .replace('}}', '}')
    return os.linesep.join(s)




def parse_node(current_graph : Dict[int, Node], line : str) -> None:
    id, type_str = line[len('v '):].split(' ', maxsplit=1)
    ntype_str, dtype_str = type_str[0], type_str[1]
    n = Node()
    n.id = int(id)
    try:
        n.ntype = ntype_sad_serialize_rev[int(ntype_str)]
    except:
        print(f'Fatal parse error at line: {line}'.rstrip())
        print(f'   Could not determine NType from: {ntype_str}'.rstrip())
        sys.exit(1)
    #if ntype_str == 'A':
    #    n.ntype = NType.ACTIVITY
    #elif ntype_str == 'D':
    #    n.ntype = NType.DATA
    #else:
    #    print(f'Fatal parse error at line: {line}'.rstrip())
    #    print(f'   Could not determine NType from: {ntype_str}'.rstrip())
    #    sys.exit(1)
    try:
        n.dtype = dtype_sad_serialize_rev[int(dtype_str)]
    except:
        print(f'Fatal parse error at line: {line}'.rstrip())
        print(f'   Could not determine DType from: {dtype_str}'.rstrip())
        sys.exit(1)
    #dtype_match = False
    #for a in DType:
    #    if dtype_str == a.value:
    #        n.dtype = a
    #        dtype_match = True
    #if not dtype_match:
    #    print(f'Fatal parse error at line: {line}'.rstrip())
    #    print(f'   Could not determine DType from: {dtype_str}'.rstrip())
    #    sys.exit(1)
    if n.id in current_graph:
        print(f'Fatal parse error at line: {line}'.rstrip())
        print(f'   Node already exists in graph. Incomplete node: {n}')
        print(f'   Current graph: \n{dict_to_str(current_graph)}'.rstrip())
        sys.exit(1)
    current_graph[n.id] = n



def parse_edge(current_graph : Dict[int, Node], line : str) -> None:
    id_a, id_b, _ = line[len('e '):].split(' ', maxsplit=2)
    id_a = int(id_a)
    id_b = int(id_b)
    if id_a == id_b:
        print(f'Fatal parse error at line: {line}'.rstrip())
        print(f'   IDs not allowed. id_a: {id_a}, id_b: {id_b}. Current graph: \n{dict_to_str(current_graph)}'.rstrip())
        sys.exit(1)
    if id_a not in current_graph or id_b not in current_graph:
        print(f'Fatal parse error at line: {line}'.rstrip())
        print(f'   IDs not in current graph. id_a: {id_a in current_graph}, id_b: {id_b in current_graph}. Current graph: \n{dict_to_str(current_graph)}'.rstrip())
        sys.exit(1)
    if current_graph[id_b] in current_graph[id_a].outgoing:
        print(f'Fatal parse error at line: {line}'.rstrip())
        print(f'   Nodes are already connected. id_a: {id_a}, id_b: {id_b}. \n{dict_to_str(current_graph)}'.rstrip())
    current_graph[id_a].outgoing.append(current_graph[id_b])



def parse_gspan_file(file : str) -> List[Node]:
    graphs : List[Node] = []
    current_graph : Dict[int, Node] = {}

    with open(file) as f:
        for line in f:
            line = line.rstrip()

            # Empty line
            if not line.strip():
                continue
            # Start of new graph
            elif line.startswith('t # '):
                if len(current_graph) > 0:
                    print(f'Fatal parse error at line: {line}'.rstrip())
                    print(f'   New graph starts but current is not committed. Current graph: \n{dict_to_str(current_graph)}'.rstrip())
                    sys.exit(1)
                    #incoming : Set[Node] = set()
                    #for _, v in current_graph.items():
                    #    v.metadata['len'] = len(current_graph)
                    #    for n in v.outgoing:
                    #        incoming.add(n)
                    #roots = set(current_graph.values()) - incoming
                    #if len(roots) != 1:
                    #    print(f'Fatal parse error at line: {line}'.rstrip())
                    #    print(f'   Multiple or no roots: {roots}')
                    #    print(f'Current graph: \n{dict_to_str(current_graph)}'.rstrip())
                    #    sys.exit(1)
                    #graphs.append(roots.pop())
                    #current_graph.clear()
            # Commit current graph to list
            elif line.startswith('-----------------'):
                incoming : Set[Node] = set()
                for _, v in current_graph.items():
                    v.metadata['len'] = len(current_graph)
                    for n in v.outgoing:
                        incoming.add(n)
                roots = set(current_graph.values()) - incoming
                if len(roots) != 1:
                    print(f'Fatal parse error at line: {line}'.rstrip())
                    print(f'   Multiple or no roots: {roots}')
                    print(f'Current graph: \n{dict_to_str(current_graph)}'.rstrip())
                    sys.exit(1)
                graphs.append(roots.pop())
                current_graph.clear()
            # Add metadata to nodes
            elif line.startswith('Support: '):
                support = int(line[len('Support: '):])
                for k in current_graph:
                    current_graph[k].metadata['support'] = support
            # Add node
            elif line.startswith('v '):
                parse_node(current_graph, line)
            # Add edge
            elif line.startswith('e '):
                parse_edge(current_graph, line)
            # Ignored lines
            elif line.startswith('Read:') or line.startswith('Mine:') or line.startswith('Total:'):
                pass
            # Unknown lines
            else:
                print(f'Unknown line: {line}')
    return graphs



def parse_grami_file(file : str) -> List[Node]:
    graphs : List[Node] = []
    current_graph : Dict[int, Node] = {}

    with open(file) as f:
        for line in f:
            line = line.rstrip()

            # Empty line
            if not line.strip():
                continue
            # Commit current graph and "start" new instance
            elif ':' == line.rstrip()[-1]:
                # First graph, no current exists yet
                if len(current_graph) < 1:
                    continue
                # Determine root to commit current graph
                incoming : Set[Node] = set()
                for _, v in current_graph.items():
                    v.metadata['len'] = len(current_graph)
                    for n in v.outgoing:
                        incoming.add(n)
                roots = set(current_graph.values()) - incoming
                if len(roots) != 1:
                    dummy = Node('UnconnectedPattern')
                    dummy.metadata['len'] = len(current_graph)
                    graphs.append(dummy)
                else:
                    graphs.append(roots.pop())
                current_graph.clear()
            # Add node
            elif line.startswith('v '):
                parse_node(current_graph, line)
            # Add edge
            elif line.startswith('e '):
                parse_edge(current_graph, line)
            # Unknown lines
            #else:
            #    print(f'Unknown line: {line}')
    return graphs


def identical(n1 : Node, n2 : Node) -> bool:
    if n1.ntype != n2.ntype:
        return False
    if n1.dtype != n2.dtype:
        return False
    if set(n1.outgoing) != set(n2.outgoing):
        return False
    return True



# Filters for visualization
min_length_graphs = 7
max_length_graphs = 200
max_graphs_display = 10
branches_allowed = False

for file in sys.argv[1:]:
    print(f'Parsing "{file}"')

    # Parse file
    graphs : List[Node] = []
    for algo in ['gspan', 'grami']:
        if algo in file:
            graphs = globals()[f'parse_{algo}_file'](file)
            break
    print(f'Found {len(graphs)} graphs')


    for a, b in itertools.combinations(graphs, 2):
        if identical(a, b) and a.name != 'UnconnectedPattern' and b.name != 'UnconnectedPattern':
            graphs.remove(b)
            print(f'Warning: Duplicate found')


    # Histogram
    # [len(graph), #occurrences]
    hist : Dict[int, int] = {}
    for g in graphs:
        if g.metadata['len'] in hist:
            hist[g.metadata['len']] += 1
        else:
            hist[g.metadata['len']] = 1
    print(f'Histogram: \nlen(graph) -> #occurrences\n{dict_to_str(dict(sorted(hist.items())))}')
    #print(f'        %{file}')
    #print(f'        \\addplot coordinates {{')
    #for k, v in sorted(hist.items()):
    #    print(f'            ({k}, {v})')
    #print(f'        }};')

    # Visualization
    if min_length_graphs > 0:
        filtered_graphs : List[Node] = []
        for g in graphs:
            if g.metadata['len'] >= min_length_graphs and g.metadata['len'] <= max_length_graphs:
                if branches_allowed:
                    filtered_graphs.append(g)
                else:
                    branches = False
                    for s in graph_to_set(g)[0]:
                        if len(s.outgoing) > 1:
                            branches = True
                            break
                    if not branches:
                        filtered_graphs.append(g)

        print(f'After filter: {len(filtered_graphs)} graphs')
        if len(filtered_graphs) < max_graphs_display + 1:
            for g in filtered_graphs:
                g.view()
        else:
            for g in filtered_graphs:
                if max_graphs_display < 1:
                    break
                max_graphs_display -= 1
                g.view()
