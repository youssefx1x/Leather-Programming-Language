#![allow(dead_code)]
#[path = "../src/lth07/lib.rs"]
mod lth07;

use lth07::{Compiler, Runner};
use std::collections::HashMap;

fn main() {
    let program = Compiler::demo_program();

    let result = Runner::new(1_000_000)
        .run(&program, &HashMap::new())
        .expect("LTH 0.7 demo failed");

    println!("LTH 0.7 Rust Demo");
    println!("values = {:?}", result.values);
    println!("instructions = {}", result.profile.instructions);
    println!("max_stack = {}", result.profile.max_stack);
    println!(
        "specialization_hits = {}",
        result.profile.specialization_hits
    );
}
