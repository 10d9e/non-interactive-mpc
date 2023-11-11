# Non Interactive Multi Party Computation

The Python code provided is a simulation of a protocol described in the paper [Evaluation of Arithmetic Sum-of-Products Expressions in Linear Secret Sharing Schemes with a Non-Interactive Computation Phase](https://nillion.pub/sum-of-products-lsss-non-interactive.pdf). The protocol is designed for secure multi-party computation (MPC), particularly for evaluating arithmetic expressions in the form of sum-of-products within a linear secret sharing scheme (LSSS), without necessitating interactive communication during the computation phase.

### Overview of the Protocol
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
