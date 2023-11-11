# Reference:
# Paper: "Evaluation of Arithmetic Sum-of-Products Expressions in Linear Secret Sharing Schemes with a Non-Interactive Computation Phase"
# Authors: Miguel de Vega, Andrei Lapets, Stanislaw Jarecki, Wicher Malten, Mehmet Ugurbil, Wyatt Howe
# URL: https://nillion.pub/sum-of-products-lsss-non-interactive.pdf

import random

class Node:
    def __init__(self, node_id, p, g):
        """ 
        Initialize a node with its ID, a prime number p, and a generator g. 
        The node maintains dictionaries for shared values, gamma values, and partial products.
        """
        self.node_id = node_id
        self.p = p
        self.g = g
        self.shared_values = {}  # Stores shared values for inputs
        self.gamma_values = {}   # Stores gamma values for terms
        self.partial_products = {}  # Stores partial products for terms

    def receive_input(self, input_id, value, lambda_value):
        """ 
        Receive an input along with its lambda value, and compute the shared value.
        The shared value is the input value masked by the negative power of lambda, modulo p.
        """
        self.shared_values[input_id] = (value * pow(g, -lambda_value, p)) % p

    def compute_gamma_value(self, term_id, lambda_values):
        """ 
        Compute and store the gamma value for a given term.
        Gamma is the sum of the lambda values for the term's inputs, modulo (p-1).
        """
        self.gamma_values[term_id] = sum(lambda_values) % (p-1)

    def compute_partial_product(self, term_id, input_id):
        """ 
        Compute and store the partial product for a term and an input.
        The partial product is simply the shared value of the input for this term.
        """
        self.partial_products[(term_id, input_id)] = self.shared_values[input_id]

# Setup
p = 101  # A small prime number for modular arithmetic
g = 3    # A generator for the multiplicative group modulo p

# Create nodes representing different participants in the protocol
nodes = [Node(i, p, g) for i in range(4)]

# Inputs and lambda values for the sum-of-products expression
x = [5, 3, 7, 4]  # Inputs x11, x12, x21, x22 respectively
lambda_values = [random.randint(1, p-1) for _ in range(4)]  # Random lambda values for masking

# Preprocessing Phase
# Distribute inputs and lambda values to nodes
for i, node in enumerate(nodes):
    node.receive_input(i, x[i], lambda_values[i])

# Compute gamma values for each term (sum of lambda values for inputs in each term)
gamma_values_term1 = [lambda_values[0], lambda_values[1]]  # For term1 (x11 * x12)
gamma_values_term2 = [lambda_values[2], lambda_values[3]]  # For term2 (x21 * x22)
nodes[0].compute_gamma_value('term1', gamma_values_term1)
nodes[2].compute_gamma_value('term2', gamma_values_term2)

# Nodes compute partial products for their inputs in each term
for i, node in enumerate(nodes):
    term_id = 'term1' if i < 2 else 'term2'  # Determine term based on input index
    node.compute_partial_product(term_id, i)

# Computation Phase
# Combine partial products to compute the full product terms
y_values = [1, 1]  # Initialize product terms for term1 and term2
for term_id in ['term1', 'term2']:
    for node in nodes:
        partial_product = node.partial_products.get((term_id, node.node_id))
        if partial_product is not None:
            # Multiply and mod the partial product to the product term
            y_values[0 if term_id == 'term1' else 1] *= partial_product
            y_values[0 if term_id == 'term1' else 1] %= p
    # Multiply the product term by g raised to the gamma value, then mod
    y_values[0 if term_id == 'term1' else 1] *= pow(g, nodes[0 if term_id == 'term1' else 2].gamma_values[term_id], p)
    y_values[0 if term_id == 'term1' else 1] %= p

# Final output - sum of the product terms mod p
z = sum(y_values) % p

z, [node.shared_values for node in nodes], [nodes[0].gamma_values, nodes[2].gamma_values]

print('result: ', z)
print('shares: ', [node.shared_values for node in nodes])
print('gamma values on node 0, 2', [nodes[0].gamma_values, nodes[2].gamma_values])
