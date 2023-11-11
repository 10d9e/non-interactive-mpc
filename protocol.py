# Reference:
# Paper: "Evaluation of Arithmetic Sum-of-Products Expressions in Linear Secret Sharing Schemes with a Non-Interactive Computation Phase"
# Authors: Miguel de Vega, Andrei Lapets, Stanislaw Jarecki, Wicher Malten, Mehmet Ugurbil, Wyatt Howe
# URL: https://nillion.pub/sum-of-products-lsss-non-interactive.pdf

import random

# Toy example of the protocol

# Setup - using small numbers for simplicity
p = 101  # A small prime number for our toy example
g = 3    # A generator of the multiplicative group modulo p

# Assume we have 4 inputs for our sum-of-products expression
x = [5, 3, 7, 4]  # x11, x12, x21, x22 respectively

# Preprocessing Phase
# Generate random masks for each input
lambda_values = [random.randint(1, p-1) for _ in range(4)]

# Compute shared values for each input
shared_values = [(x[i] * pow(g, -lambda_values[i], p)) % p for i in range(4)]

# Compute gamma for each term
gamma_values = [sum(lambda_values[:2]) % (p-1), sum(lambda_values[2:]) % (p-1)]

# Computation Phase
# Compute each product term y_a
y_values = [(pow(g, gamma_values[0], p) * shared_values[0] * shared_values[1]) % p,
            (pow(g, gamma_values[1], p) * shared_values[2] * shared_values[3]) % p]

# Compute the sum z
z = sum(y_values) % p

# Output the result
z, shared_values, gamma_values, lambda_values

print(z, shared_values, gamma_values, lambda_values)
