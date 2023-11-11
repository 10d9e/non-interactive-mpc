# Reference:
# Paper: "Evaluation of Arithmetic Sum-of-Products Expressions in Linear Secret Sharing Schemes with a Non-Interactive Computation Phase"
# Authors: Miguel de Vega, Andrei Lapets, Stanislaw Jarecki, Wicher Malten, Mehmet Ugurbil, Wyatt Howe
# URL: https://nillion.pub/sum-of-products-lsss-non-interactive.pdf

import random

class SecureNode:
    def __init__(self, node_id, p, g):
        self.node_id = node_id
        self.p = p
        self.g = g
        self.shared_values = {}
        self.gamma_values = {}
        self.partial_products = {}

    def receive_input(self, input_id, value, lambda_value):
        self.shared_values[input_id] = (value * pow(g, -lambda_value, self.p)) % self.p

    def compute_gamma_value(self, term_id, lambda_values):
        self.gamma_values[term_id] = sum(lambda_values) % (self.p-1)

    def compute_partial_product(self, term_id, input_id):
        self.partial_products[(term_id, input_id)] = self.shared_values[input_id]

# Secure parameters: large prime and suitable generator
p = 982451653
g = 2

# Reinitialize secure nodes
secure_nodes = [SecureNode(i, p, g) for i in range(4)]

# Inputs and lambda values for simulation
x = [random.randint(1, 100) for _ in range(4)]
lambda_values = [random.randint(1, p-1) for _ in range(4)]

# Expected z value calculation - verify with this
expected_z = (x[0] * x[1] + x[2] * x[3]) % p

# Preprocessing Phase
for i, node in enumerate(secure_nodes):
    node.receive_input(i, x[i], lambda_values[i])

gamma_values_term1 = [lambda_values[0], lambda_values[1]]
gamma_values_term2 = [lambda_values[2], lambda_values[3]]
secure_nodes[0].compute_gamma_value('term1', gamma_values_term1)
secure_nodes[2].compute_gamma_value('term2', gamma_values_term2)

# Computation Phase
for i, node in enumerate(secure_nodes):
    term_id = 'term1' if i < 2 else 'term2'
    node.compute_partial_product(term_id, i)

y_values = [1, 1]
for term_id in ['term1', 'term2']:
    for node in secure_nodes:
        partial_product = node.partial_products.get((term_id, node.node_id))
        if partial_product is not None:
            y_values[0 if term_id == 'term1' else 1] *= partial_product
            y_values[0 if term_id == 'term1' else 1] %= p
    y_values[0 if term_id == 'term1' else 1] *= pow(g, secure_nodes[0 if term_id == 'term1' else 2].gamma_values[term_id], p)
    y_values[0 if term_id == 'term1' else 1] %= p

z = sum(y_values) % p

# Printing expected and real z values
expected_z, z, [node.shared_values for node in secure_nodes], [secure_nodes[0].gamma_values, secure_nodes[2].gamma_values]

assert expected_z == z
print(f"expected: {expected_z} actual: {z}")
print('shares: ', [node.shared_values for node in secure_nodes])
print('gamma values on node 0, 2', [secure_nodes[0].gamma_values, secure_nodes[2].gamma_values])
