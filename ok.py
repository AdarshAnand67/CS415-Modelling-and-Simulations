# Assignment 5 Markov Chains - Template
#
# This is an educational Python utility for analyzing and
# visualizing small Discrete-time Markov Chains.
#
# Author: Dr. Neha Karanjkar


import random
import math
import os
import numpy as np


def generate_a_markov_chain(num_states, sparseness=0.8):
    """ 
    A function that randomly generates a markov chain
given the number of states, and returns 
    its transition probability matrix.

    sparseness is the probability of an edge being absent.
    Its the fraction of entries in a row in the Transition Probability Matrix 
    that are zeros.
    """
    assert sparseness >= 0 and sparseness <= 1
    P = [[0 for j in range(num_states)] for i in range(num_states)]
    print(P)

    I = [i for i in range(num_states)]  # states
    random.shuffle(I)  # randomly permute this list
    J = [i for i in range(num_states)]  # states
    print("I=", I)
    for i in I:  # i denotes "from" state
        sum_row = 0
        random.shuffle(J)  # randomly permute this list
        print("J=", J)
        for j in J:  # j denotes "to" state
            if j == J[-1]:
                # adjust Prob of last edge so that all out-probs from state i sum to 1
                edge_weight = abs(round((1 - sum_row), 2))
            else:
                if random.random() < sparseness:
                    edge_weight = 0  # with Prob=sparseness, make the edge weight=0
                elif sum_row == 0 and random.random() < 0.15:
                    edge_weight = 1  # with Prob=0.1, make this an absorbing state
                else:
                    edge_weight = abs(round(random.uniform(0, (1 - sum_row)), 2))
            sum_row += edge_weight
            P[i][j] = edge_weight
        if not math.isclose(sum_row, 1):
            print("ERROR! sum_row=", sum_row)
    assert is_stochastic_matrix(P, verbose=True)
    return P


def is_stochastic_matrix(P, verbose=False):
    """ 
    A function that checks whether a given matrix
    is a valid stochastic matrix.
    A stochastic matrix is square, contains only
    non-negative elements and the sum of each row is 1.
    """
    # if ---this is a valid stochastic matrix---
    # Your code ...
    # return True
    # else:

    #     return False


def expected_holding_time(P, s):
    """
    Given the transition probability matrix P, and a state s,
    this routine computes the expected holding time for state s.
    """
    # your code
    return exp_holding_time


def get_subset_of_P(P, list_of_states):
    """
    returns a subset of the original transition 
    probability matrix corresponding to a given 
    set of states.
    """
    P_subset = []
    for i in list_of_states:
        P_subset.append([])
        for j in list_of_states:
            P_subset[-1].append(P[i][j])
    return P_subset


def identify_recurrent_classes(P):
    """
    Given the transition probability matrix P, this function
    partitions the state space into transient states
    and recurrent classes (also known as closed communicating
    or irreducible classes).
    """
    transient_states = []
    recurrent_classes = []

    # Kosaraju's Algorithm or Tarjan's Algorithm:

    # ----- Your code here ------------------

    # print the results:
    print("connected_components=", connected_components)
    print("transient states:", transient_states)
    print("recurrent_classes:", recurrent_classes)
    return transient_states, recurrent_classes


def stationary_distribution(P):
    """
    computes the stationary distribution for
    a given transition probability matrix P
    Assuming P corresponds to an IRREDUCIBLE markov chain.
    (that is, all states belong to a 
    single recurrent class)
    """
    # your code here-------------
    return stationary_distr


def visualize_markov_chain(P, show_edge_labels=True, state_labels=None):
    """
    Given the transition probability matrix P,
    this function generates a visualization of the
    markov chain as a ".dot" file.

    NOTE: the ".dot" file can be viewed in a browser (http://www.webgraphviz.com/)
    OR converted into a pdf file using graphviz by running the command
            dot -Tpdf dot_file.dot -o plot.pdf
    """
    if state_labels == None:
        state_labels = [str(i) for i in range(len(P))]
    with open("dot_file.dot", "w") as f:
        print("digraph  {", file=f)
        for i in range(len(P)):
            print(state_labels[i] + ";", file=f)
        for i in range(len(P)):
            for j in range(len(P)):
                if P[i][j] > 0:
                    if show_edge_labels:
                        print(
                            f'{state_labels[i]} -> {state_labels[j]}  [weight={P[i][j]}, label="{P[i][j]}"];',
                            file=f,
                        )
                    else:
                        print(
                            f"{state_labels[i]} -> {state_labels[j]}  [weight={P[i][j]}];",
                            file=f,
                        )
        print("}", file=f)
    # ---- optional-----
    os.system("dot -Tpdf dot_file.dot -o plot.pdf")
    # -------------------


# ==================================================================
# Here's a sample transition matrix that
# could be visited for testing our routines:

sample_P = [  # 0    1    2    3    4    5    6    7    8
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 0
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 1
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0],  # 2
    [0.0, 0.0, 0.1, 0.1, 0.0, 0.1, 0.7, 0.0, 0.0],  # 3
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],  # 4
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # 5
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  # 6
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0],  # 7
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],  # 8
]


# Either use the sample matrix or randomly generate a transition Probability Matrix P.
# Comment out one of these:
# P = sample_P
P = generate_a_markov_chain(num_states=8, sparseness=0.9)

print("Transition Probability Matrix P = \n", np.array(P), "\n")
visualize_markov_chain(P)
transient_states, recurrent_classes = identify_recurrent_classes(P)
for r in recurrent_classes:
    p = get_subset_of_P(P, r)
    V = stationary_distribution(p)
    print("------------------")
    print("recurrent_class = ", r, " stationary_distribution:", V)
    print("transition matrix:\n", np.array(p))


# Expected solution for the Sample Matrix Given:
# ------------------------------------------------------
#
# 	   Transition Probability Matrix P =
# 	    [[ 1.   0.   0.   0.   0.   0.   0.   0.   0. ]
# 	    [ 0.   0.   1.   0.   0.   0.   0.   0.   0. ]
# 	    [ 0.   0.   0.   0.5  0.5  0.   0.   0.   0. ]
# 	    [ 0.   0.   0.1  0.1  0.   0.1  0.7  0.   0. ]
# 	    [ 0.   0.   0.   0.   0.   1.   0.   0.   0. ]
# 	    [ 0.   0.   0.   0.   1.   0.   0.   0.   0. ]
# 	    [ 0.   0.   0.   0.   0.   0.   1.   0.   0. ]
# 	    [ 0.   0.   0.   0.   0.   0.   0.5  0.5  0. ]
# 	    [ 0.   0.   0.   0.   0.   0.   0.   1.   0. ]]
#
# 	   connected_components= [[0], [1], [2, 3], [4, 5], [6], [7], [8]]
# 	   transient states: [1, 2, 3, 7, 8]
# 	   recurrent_classes: [[0], [4, 5], [6]]
# 	   ------------------
# 	   recurrent_class =  [0]  stationary_distribution: [[ 1.]]
# 	   transition matrix:
# 	    [[ 1.]]
# 	   ------------------
# 	   recurrent_class =  [4, 5]  stationary_distribution: [[ 0.5  0.5]]
# 	   transition matrix:
# 	    [[ 0.  1.]
# 	    [ 1.  0.]]
# 	   ------------------
# 	   recurrent_class =  [6]  stationary_distribution: [[ 1.]]
# 	   transition matrix:
# 	    [[ 1.]]
#


# ==================================================================
# Here's a sample transition matrix that
# could be visited for testing our routines:

sample_P = [  # 0    1    2    3    4    5    6    7    8
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 0
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 1
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0],  # 2
    [0.0, 0.0, 0.1, 0.1, 0.0, 0.1, 0.7, 0.0, 0.0],  # 3
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],  # 4
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # 5
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  # 6
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0],  # 7
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],  # 8
]


# Either use the sample matrix or randomly generate a transition Probability Matrix P.
# Comment out one of these:
# P = sample_P
P = generate_a_markov_chain(num_states=8, sparseness=0.9)

print("Transition Probability Matrix P = \n", np.array(P), "\n")
visualize_markov_chain(P)
transient_states, recurrent_classes = identify_recurrent_classes(P)
for r in recurrent_classes:
    p = get_subset_of_P(P, r)
    V = stationary_distribution(p)
    print("------------------")
    print("recurrent_class = ", r, " stationary_distribution:", V)
    print("transition matrix:\n", np.array(p))


# Expected solution for the Sample Matrix Given:
# ------------------------------------------------------
#
# 	   Transition Probability Matrix P =
# 	    [[ 1.   0.   0.   0.   0.   0.   0.   0.   0. ]
# 	    [ 0.   0.   1.   0.   0.   0.   0.   0.   0. ]
# 	    [ 0.   0.   0.   0.5  0.5  0.   0.   0.   0. ]
# 	    [ 0.   0.   0.1  0.1  0.   0.1  0.7  0.   0. ]
# 	    [ 0.   0.   0.   0.   0.   1.   0.   0.   0. ]
# 	    [ 0.   0.   0.   0.   1.   0.   0.   0.   0. ]
# 	    [ 0.   0.   0.   0.   0.   0.   1.   0.   0. ]
# 	    [ 0.   0.   0.   0.   0.   0.   0.5  0.5  0. ]
# 	    [ 0.   0.   0.   0.   0.   0.   0.   1.   0. ]]
#
# 	   connected_components= [[0], [1], [2, 3], [4, 5], [6], [7], [8]]
# 	   transient states: [1, 2, 3, 7, 8]
# 	   recurrent_classes: [[0], [4, 5], [6]]
# 	   ------------------
# 	   recurrent_class =  [0]  stationary_distribution: [[ 1.]]
# 	   transition matrix:
# 	    [[ 1.]]
# 	   ------------------
# 	   recurrent_class =  [4, 5]  stationary_distribution: [[ 0.5  0.5]]
# 	   transition matrix:
# 	    [[ 0.  1.]
# 	    [ 1.  0.]]
# 	   ------------------
# 	   recurrent_class =  [6]  stationary_distribution: [[ 1.]]
# 	   transition matrix:
# 	    [[ 1.]]
#


visited = [False for i in range(100)]
order = []
component = []
adj = [[] for i in range(100)]
adj_rev = [[] for i in range(100)]

# First dfs to get the order of the out time of vertices


def dfs1(v):
    global visited, order, component, adj, adj_rev

    visited[v] = True
    for i in adj[v]:
        if visited[i] == False:
            dfs1(i)
    order.append(v)


# Second dfs to get the strongly connected components
def dfs2(v):
    global visited, order, component, adj, adj_rev

    visited[v] = True
    component.append(v)
    for i in adj_rev[v]:
        if visited[i] == False:
            dfs2(i)


def identify_recurrent_classes(P):
    global visited, order, component, adj, adj_rev
    """
  Given the transition probability matrix P, this function
  partitions the state space into transient states
  and recurrent classes (also known as closed communicating
  or irreducible classes).
  """
    transient_states = []
    recurrent_classes = []
    connected_components = []

    # Kosaraju's Algorithm or Tarjan's Algorithm:

    # ----- Your code here ------------------

    # Converting the matrix to adjacency list
    for i in range(len(P)):
        for j in range(len(P[i])):
            if P[i][j] > 0 and i != j:
                adj[i].append(j)
                adj_rev[j].append(i)

    # print("Adjacency List::\n\n")
    # print(adj)

    # First DFS to get the order of the out time of vertices
    for i in range(len(P)):
        if visited[i] == False:
            dfs1(i)

    visited = [False for i in range(len(P))]

    # Reverse to traverse adj_rev
    order.reverse()

    for i in order:
        if visited[i] == False:
            dfs2(i)
            connected_components.append(component)
            component = []

    # Differentiate transient and recurrent states
    flag = 0
    for component in connected_components:
        flag = 0
        for i in component:
            for j in range(len(P[i])):
                if P[i][j] > 0 and j not in component:
                    flag = 1
                    break
            if flag == 1:
                for c in component:
                    transient_states.append(c)

                break
        if flag == 0:
            recurrent_classes.append(component)

    # print the results:
    print("connected_components=", connected_components)
    print("transient states:", transient_states)
    print("recurrent_classes:", recurrent_classes)
    return transient_states, recurrent_classes
