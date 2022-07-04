
This repository comprises the prototype for the publication *A Graph Structure to Discover Patterns in Unstructured Processes of Product Development* at the 2022 IEEE 23rd International Conference on Information Reuse and Integration for Data Science (IRI).

## Graph Generation

A list of graphs can be generated through `generate.py`, specifically the following function.

`generate.create_graph_list(pattern : Callable[[], Node], num : int = 1000, dist_max_nodes : int = 4000) -> List[Node]`

Creates a list of `num` connected graphs.
The returned list contains the first node of each graph.
Each graph is individually grown in random fashion, based on the supplied base `pattern`.

To grow a graph, internally we distinguish between *active* and *inactive* nodes (in `generate.grow_graph()`).
Initially, all nodes with no outgoing edge are considered active.
Each active node continuously goes through three consecutive decisions: termination, splitting, and growth.

In *termination*, each node makes a binary choice whether to be active and proceed with the other two decisions.
When a node decides not to be active anymore, it is no longer processed, i.e., the generation of new outgoing edges ends for this inactive node.
The probability for termination, i.e., for a node deciding to be inactive, is calculated with `max(0.2, \sqrt{{new_nodes}/{max_new_nodes}})`, where `new_nodes` is the number of newly created nodes for this graph so far and `max_new_nodes` is a constant limiting the maximum size of a graph.
Termination limits the size of a graph and depends on the number of generated nodes.
The probability of termination is at least 20%.
Its gradient increases rapidly at the beginning and decreases as the number of created nodes increases, similar to a logistic function.
This results in longer graphs.
Termination and splitting influence how long paths in our graph can get and how often a graph branches out.
The choice of probabilities here favors longer, less broad graphs.

In *splitting*, each active node decides on the number of outgoing edges that are subsequently created for this node.
We draw the number of edges from a folded normal distribution with mean `\mu = 0` and standard deviation `\sigma = 1` and subsequently add 1 to this number of edges.
This makes one outgoing edge the most likely case, with decreasing probabilities for higher numbers of edges, while the maximum number of edges per active node is 5.

In *growth*, each node decides which new node to create for each previously created outgoing edge.
If the currently growing node is a data node, we create a new activity node.
If the currently growing node is an activity, we create a data node with the same type of the activity.
Newly created nodes are active by default, so that our algorithm for generating new nodes is applied iteratively on them.
The generation of the whole graph is finished once no active node remains.

Use the following to create a list of random graphs, add noise, and write them to disk:

    # Replace parameters as you like
    g = create_graph_list(pattern_a, num=100, dist_max_nodes=2000)
    # Probability for (leaf addition, leaf deletion, inner node addition, inner node deletion)
    probability = (0.05, 0.05, 0.05, 0.05)
    g = [add_noise(i, probability) for i in g]
    write_out(g, file_prefix=f'combined-err-{probability[0]}', gspan=True)
    write_out(g, file_prefix=f'combined-err-{probability[0]}', gspan=False)

Note that gSpan and GraMi use different file and graph formats so we need two files.

## Subgraph Mining

Our findings can be replicated with the included shell scripts:

* `run_gspan.sh`
* `run_grami.sh`
* `run_grami_approx-d1.sh`
* `run_grami_approx-d2.sh`
* `run_grami_approx-d3.sh`

They run the respective FSM algorithms with the parameters we chose and store their results in a directory called `output`.
The input files are expected in a directory called `graphs` with a specific naming scheme.
When generated as specified above, the names will be as expected.
Consult the `.sh` files in case you would like more information or change the file names.

`read_results.py` can parse and visualize the result files in `output` through graphviz.
Call this file with an arbitrary amount of result files as argument.
The following variables within `read_results.py` can be used to tweak the selection:

    min_length_graphs = 7 # A graph must be at least this long
    max_length_graphs = 200 # A graph must be at most this long
    max_graphs_display = 10 # Only show the first x graphs

Unfortunately those variables cannot be set through CLI parameters.
