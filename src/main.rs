use num_bigint::{BigInt, ToBigInt, RandBigInt};
use num_traits::One;
use std::collections::HashMap;

struct Node {
    node_id: usize,
    p: BigInt,
    g: BigInt,
    shared_values: HashMap<usize, BigInt>,
    gamma_values: HashMap<String, BigInt>,
    partial_products: HashMap<(String, usize), BigInt>,
}

impl Node {
    fn new(node_id: usize, p: BigInt, g: BigInt) -> Node {
        Node {
            node_id,
            p,
            g,
            shared_values: HashMap::new(),
            gamma_values: HashMap::new(),
            partial_products: HashMap::new(),
        }
    }

    fn receive_input(&mut self, input_id: usize, value: BigInt, lambda_value: BigInt) {
        let g_inv = self.g.modpow(&(&self.p - 2.to_bigint().unwrap()), &self.p); // Corrected modular inverse calculation
        let shared_value = (value * g_inv.modpow(&lambda_value, &self.p)) % &self.p;
        self.shared_values.insert(input_id, shared_value);
    }  

    fn compute_gamma_value(&mut self, term_id: String, lambda_values: &[BigInt]) {
        let gamma_value = lambda_values.iter().sum::<BigInt>() % (&self.p - BigInt::one());
        self.gamma_values.insert(term_id, gamma_value);
    }

    fn compute_partial_product(&mut self, term_id: String, input_id: usize) {
        if let Some(shared_value) = self.shared_values.get(&input_id) {
            self.partial_products.insert((term_id, input_id), shared_value.clone());
        }
    }
}

fn main() {
    
    let mut rng = rand::thread_rng();
    let p = 982451653.to_bigint().unwrap();
    let g = 2.to_bigint().unwrap();

    let mut secure_nodes = (0..4)
        .map(|i| Node::new(i, p.clone(), g.clone()))
        .collect::<Vec<_>>();

    // Randomly generate x and lambda values
    let x: Vec<BigInt> = (0..4).map(|_| rng.gen_bigint_range(&BigInt::one(), &p)).collect();
    let lambda_values: Vec<BigInt> = (0..4).map(|_| rng.gen_bigint_range(&BigInt::one(), &p)).collect();

    // Expected z value calculation
    let expected_z = (&x[0] * &x[1] + &x[2] * &x[3]) % &p;

    // Preprocessing Phase
    for (i, node) in secure_nodes.iter_mut().enumerate() {
        node.receive_input(i, x[i].clone(), lambda_values[i].clone());
    }

    let gamma_values_term1 = vec![lambda_values[0].clone(), lambda_values[1].clone()];
    let gamma_values_term2 = vec![lambda_values[2].clone(), lambda_values[3].clone()];
    secure_nodes[0].compute_gamma_value("term1".to_string(), &gamma_values_term1);
    secure_nodes[2].compute_gamma_value("term2".to_string(), &gamma_values_term2);

    // Computation Phase
    for (i, node) in secure_nodes.iter_mut().enumerate() {
        let term_id = if i < 2 { "term1" } else { "term2" }.to_string();
        node.compute_partial_product(term_id, i);
    }

    let mut y_values = vec![BigInt::one(), BigInt::one()];
    for term_id in ["term1", "term2"].iter() {
        for node in &secure_nodes {
            if let Some(partial_product) = node.partial_products.get(&((*term_id).to_string(), node.node_id)) {
                let index = if *term_id == "term1" { 0 } else { 1 };
                y_values[index] = (&y_values[index] * partial_product) % &p;
            }
        }
        if let Some(gamma_value) = secure_nodes[if *term_id == "term1" { 0 } else { 2 }].gamma_values.get(*term_id) {
            let index = if *term_id == "term1" { 0 } else { 1 };
            y_values[index] = (&y_values[index] * g.modpow(gamma_value, &p)) % &p;
        }
    }

    let z = (&y_values[0] + &y_values[1]) % &p;

    // Printing expected and real z values
    assert_eq!(expected_z, z);
    println!("expected: {} actual: {}", expected_z, z);
    println!("shares: {:?}", secure_nodes.iter().map(|node| &node.shared_values).collect::<Vec<_>>());
    println!("gamma values on node 0, 2: {:?}", secure_nodes.iter().map(|node| &node.gamma_values).collect::<Vec<_>>());
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::ToBigInt;

    #[test]
    fn test_secure_node_operation() {
        let p = 101.to_bigint().unwrap();
        let g = 3.to_bigint().unwrap();

        let mut rng = rand::thread_rng();

        let mut secure_nodes = (0..4)
            .map(|i| Node::new(i, p.clone(), g.clone()))
            .collect::<Vec<_>>();

        let x: Vec<BigInt> = vec![5, 3, 7, 4].into_iter().map(|num| num.to_bigint().unwrap()).collect();
        let lambda_values: Vec<BigInt> = (0..4).map(|_| rng.gen_bigint_range(&BigInt::one(), &p)).collect();

        let expected_z = (&x[0] * &x[1] + &x[2] * &x[3]) % &p;

        for (i, node) in secure_nodes.iter_mut().enumerate() {
            node.receive_input(i, x[i].clone(), lambda_values[i].clone());
        }

        let gamma_values_term1 = vec![lambda_values[0].clone(), lambda_values[1].clone()];
        let gamma_values_term2 = vec![lambda_values[2].clone(), lambda_values[3].clone()];
        secure_nodes[0].compute_gamma_value("term1".to_string(), &gamma_values_term1);
        secure_nodes[2].compute_gamma_value("term2".to_string(), &gamma_values_term2);

        for (i, node) in secure_nodes.iter_mut().enumerate() {
            let term_id = if i < 2 { "term1" } else { "term2" }.to_string();
            node.compute_partial_product(term_id, i);
        }

        let mut y_values = vec![BigInt::one(), BigInt::one()];
        for term_id in ["term1", "term2"].iter() {
            for node in &secure_nodes {
                if let Some(partial_product) = node.partial_products.get(&((*term_id).to_string(), node.node_id)) {
                    let index = if *term_id == "term1" { 0 } else { 1 };
                    y_values[index] = (&y_values[index] * partial_product) % &p;
                }
            }
            if let Some(gamma_value) = secure_nodes[if *term_id == "term1" { 0 } else { 2 }].gamma_values.get(*term_id) {
                let index = if *term_id == "term1" { 0 } else { 1 };
                y_values[index] = (&y_values[index] * g.modpow(gamma_value, &p)) % &p;
            }
        }

        let z = (&y_values[0] + &y_values[1]) % &p;
        assert_eq!(expected_z, z);
    }


    #[test]
    fn test_gamma_value_computation() {
        let p = 101.to_bigint().unwrap();
        let mut node = Node::new(0, p.clone(), 3.to_bigint().unwrap());

        let lambda_values = vec![2.to_bigint().unwrap(), 3.to_bigint().unwrap()]; // Example lambda values
        let expected_gamma_value = lambda_values.iter().sum::<BigInt>() % (&p - BigInt::one());

        node.compute_gamma_value("test_term".to_string(), &lambda_values);
        assert_eq!(node.gamma_values.get("test_term"), Some(&expected_gamma_value));
    }

}
