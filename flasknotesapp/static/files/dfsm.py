Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from graphviz import Digraph

# Create a Digraph object
dot = Digraph()

# Define DFA states and transitions
dfa_states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
start_state = 'q0'
accept_states = ['q5']
transitions = [('q0', 'a', 'q1'), ('q0', 'b', 'q1'), ('q1', 'a', 'q2'), ('q1', 'b', 'q2'),
               ('q2', 'a', 'q3'), ('q2', 'b', 'q3'), ('q3', 'a', 'q4'), ('q3', 'b', 'q4'),
               ('q4', 'a', 'q5'), ('q4', 'b', 'q5')]

# Add all nodes and mark the start and accept states
for state in dfa_states:
    if state == start_state:
        # Start state with doublecircle
        dot.node(state, state, shape='circle')
    elif state in accept_states:
        # Accept states with doublecircle
        dot.node(state, state, shape='doublecircle')
    else:
        dot.node(state, state, shape='circle')

# Add initial invisible edge for starting arrow
dot.edge('', start_state, style='invisible')

# Add all transitions
for (src, label, dest) in transitions:
    dot.edge(src, dest, label=label)

# Render the image
dot.render('/mnt/data/dfa', format='png', cleanup=True)

'/mnt/data/dfa.png'  # Filepath for the output image
