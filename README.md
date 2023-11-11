# Non Interactive Multi Party Computation

The Python code provided is a simulation of a protocol described in the paper [Evaluation of Arithmetic Sum-of-Products Expressions in Linear Secret Sharing Schemes with a Non-Interactive Computation Phase](https://nillion.pub/sum-of-products-lsss-non-interactive.pdf). The protocol is designed for secure multi-party computation (MPC), particularly for evaluating arithmetic expressions in the form of sum-of-products within a linear secret sharing scheme (LSSS), without necessitating interactive communication during the computation phase.

### Overview
The protocol in the paper allows multiple parties (nodes) to jointly compute an arithmetic sum-of-products expression while keeping their individual input values secret. It achieves this through a combination of linear secret sharing, masked factors, and a non-interactive computation phase.

### The Math
Let's break down the key mathematical concepts and how they are applied:

1. **Linear Secret Sharing Schemes (LSSS)**:
   - **Basics**: In an LSSS, a secret $\( s \)$ is divided into $\( n \)$ shares, such that any $\( t \)$ shares (where $\( t $\) is the threshold) can reconstruct the secret, but fewer than $\( t $\) shares reveal no information about $\( s $\). The most common example is Shamir's Secret Sharing.
   - **Mathematical Representation**: If $\( \{s_1, s_2, ..., s_n\} $\) are the shares of the secret $\( s $\), then in a linear scheme, these shares satisfy a linear equation like $\( a_1s_1 + a_2s_2 + ... + a_ns_n = s $\) for some coefficients $\( \{a_1, a_2, ..., a_n\} $\).

2. **Sum-of-Products Expressions**:
   - **General Form**: These are expressions of the form $$\( \sum_{i=1}^{m} \prod_{j=1}^{n} x_{ij} \)$$, where $\( x_{ij} $\) are terms (constants or variables) and the expression involves summing up products of these terms.
   - **Application in LSSS**: The paper discusses evaluating these expressions under the constraints of LSSS, where direct multiplication might not be feasible or secure.

3. **Masked Factors**:
   - **Concept**: Masking involves hiding the actual value of a term using another value (the mask). For example, if $\( x $\) is a term, its masked version might be $\( x + r $\), where $\( r $\) is a random value known only to a specific participant.
   - **Purpose in LSSS**: This ensures that during the computation, the actual values remain hidden, preserving the security of the secret sharing scheme.

4. **Protocol Mathematics**:
   - **Preprocessing Phase**: In this phase, the participants compute 'sharings' of random elements. These sharings are then combined according to the structure of the sum-of-products expression.
   - **Computation Phase**: This involves evaluating the sum-of-products expression using the preprocessed data. The crucial aspect here is that this computation is non-interactive, meaning participants do not need to communicate with each other during this phase.

5. **Correctness and Security**:
   - **Correctness**: The mathematical correctness of the protocol ensures that the final computed value accurately represents the intended sum-of-products expression.
   - **Security**: The security analysis likely involves proving that no participant can deduce more information than intended from their shares or the computation process. This is crucial in preserving the confidentiality of the secret in a secret sharing scheme.

### Protocol

The "Protocol" section of the paper describes the procedure for evaluating arithmetic sum-of-products expressions in linear secret sharing schemes without requiring interactive communication during the computation phase. Let's dissect the math involved in both the preprocessing and computation phases:

### Preprocessing Phase
1. **Ideal Preprocessing Functionality (`FPREPROC`) for Sum of Products**: 
   - Sum of products is represented as $$\( z = \sum_{a=1}^{A} \prod_{m=1}^{M_a} x_{am} \)$$
   - `FPREPROC` generates a sharing $\( \lambda_{am} \)$ of a random element $\( \lambda_{am} \in \mathbb{Z}_{p-1} \)$ for each input at position $\( (a, m) \)$, where $\( a \in \{1, ..., A\} \)$ and $\( m \in \{1, ..., M_a\} \)$
   - For every addend term ( indexed by $\( a \)$ ), the parties compute a sharing $\( [g^{\gamma_a}] \)$ for an element $\( \gamma_a \in \mathbb{Z}_{p-1} \)$ such that:

   $$\( \gamma_a = \sum_{m=1}^{M_a} \lambda_{am} \)$$
   
### Computation Phase
1. **Expression for Sum of Products**: 
   - The sum of products is expressed as $$\( z = \sum_{a=1}^{A} y_a \), where \( y_a = \prod_{m=1}^{M_a} x_{am} \)$$

2. **Computation Protocol ($\( \pi \)$)**: 
   - **Input Stage**: 
     - Each party receives a sharing $\( \lambda_{am} \)$ of a mask exponent for every input $\( x_{am} \)$ they contribute to the computation.
     - They reconstruct $\( \lambda_{am} \)$ and then compute and broadcast $$\( \langle x_{am} \rangle_{\lambda_{am}} = x_{am} \cdot g^{-\lambda_{am}} \in \mathbb{Z}_p^* \)$$.
   - **Evaluation Stage**: 
     - For each product (addend term) having index $\( a \)$, parties locally compute $\( [y_a] = [g^{\gamma_a}] \cdot \langle x_{am} \rangle_{\lambda_{am}} \)$.
   - **Output Stage**: 
     - Parties reveal $\( z \in \mathbb{F}_p \)$ from its sharing $\( [z] \)$ and output $\( z \)$.

### Mathematical Concepts
- **Linear Secret Sharing**: The shares are combined linearly to reconstruct the secret.
- **Masked Factors**: These are used to securely mask the inputs during the computation phase.
- **Homomorphic Properties**: The protocol leverages the homomorphic properties of the cryptographic primitives to compute the sum-of-products without revealing individual masked factors.

This protocol demonstrates a sophisticated method to compute arithmetic expressions in a secure multi-party computation setting without the need for interactive communication during the computation phase. The math ensures that despite the complexity of the operations involved, the security and privacy of the participants' inputs are maintained throughout the computation.

### Simulation Details
The Python code simulates a simplified version of this protocol with the following components:

1. **Node Class**: Represents a participant in the computation. Each node can:
   - Receive inputs and corresponding lambda values (used for masking).
   - Compute shared values, gamma values, and partial products.

2. **Setup Phase**: Initializes the computational environment:
   - `p`: A prime number used for modular arithmetic to ensure computations stay within a finite field.
   - `g`: A generator for the multiplicative group modulo `p`.
   - Nodes: Participants in the computation are initialized.

3. **Preprocessing Phase**: 
   - **Input Distribution**: Each node is assigned an input and a corresponding lambda value. The lambda values are used to compute the shared values, effectively masking the original input values.
   - **Gamma Value Computation**: Each node computes the gamma value for each term of the expression. The gamma value is a sum of the lambda values for the inputs in a given term, modulated by `p-1`.

4. **Computation Phase**:
   - **Partial Product Computation**: Nodes calculate partial products for each term they contribute to. A partial product is the shared value of the input.
   - **Combining Partial Products**: The nodes combine their partial products to compute the full product terms of the sum-of-products expression. The final output (`z`) is the sum of these product terms, modulated by `p`.

5. **Output**: The final computed value (`z`) along with each node's shared values and the gamma values for each term are outputted, demonstrating the result of the distributed computation.

### Relation to the Paper
This code provides a practical example of the theoretical concepts presented in the paper. While the paper discusses a more complex and secure implementation suitable for real-world applications, this simulation offers an educational insight into how such a protocol operates. It demonstrates the key aspects of secure multi-party computation: maintaining the privacy of individual inputs while allowing a collective computation of a function. 

In summary, the authors of the [paper](https://nillion.pub/sum-of-products-lsss-non-interactive.pdf) have developed a sophisticated protocol that enhances the capabilities of linear secret sharing schemes while maintaining their security and non-interactivity. The math ensures both the operational feasibility and cryptographic security of the proposed scheme, which is essential for practical applications in secure multi-party computation. The code serves as an illustrative example, showing how the principles of linear secret sharing and non-interactive computation phases can be applied to securely compute sum-of-products expressions in a distributed manner, as described in the referenced paper.


### Reference
- **Paper**: "Evaluation of Arithmetic Sum-of-Products Expressions in Linear Secret Sharing Schemes with a Non-Interactive Computation Phase"
- **Authors**: Miguel de Vega, Andrei Lapets, Stanislaw Jarecki, Wicher Malten, Mehmet Ugurbil, Wyatt Howe
- **URL**: [Link to Paper](https://nillion.pub/sum-of-products-lsss-non-interactive.pdf)
