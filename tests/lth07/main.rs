#![allow(dead_code)]
#[path = "../../src/lth07/lib.rs"]
mod lth07;

use lth07::{
    benchmark, Compiler, Op, Optimizer, Program, Runner, Value, Vm,
};
use std::collections::HashMap;

fn binary(left: Value, right: Value, op: &str) -> Value {
    let mut program = Program::new();

    program.constants = vec![left, right];
    program.names = vec!["result".to_string()];

    program.instructions = vec![
        Op::Const(0),
        Op::Const(1),
        Op::Binary(op.to_string()),
        Op::Store(0),
        Op::Halt,
    ];

    let result = Vm::new(1000)
        .run(&program, &HashMap::new())
        .expect("binary execution failed");

    result.values["result"].clone()
}

fn test_arithmetic() {
    assert_eq!(
        binary(Value::Int(2), Value::Int(3), "+"),
        Value::Int(5)
    );

    assert_eq!(
        binary(Value::Int(8), Value::Int(3), "-"),
        Value::Int(5)
    );

    assert_eq!(
        binary(Value::Int(4), Value::Int(3), "*"),
        Value::Int(12)
    );

    assert_eq!(
        binary(Value::Int(5), Value::Int(2), "//"),
        Value::Int(2)
    );

    assert_eq!(
        binary(Value::Int(-5), Value::Int(2), "//"),
        Value::Int(-3)
    );

    assert_eq!(
        binary(Value::Int(-5), Value::Int(2), "%"),
        Value::Int(1)
    );

    assert_eq!(
        binary(Value::Int(5), Value::Int(-2), "//"),
        Value::Int(-3)
    );

    assert_eq!(
        binary(Value::Int(5), Value::Int(-2), "%"),
        Value::Int(-1)
    );

    assert_eq!(
        binary(Value::Int(5), Value::Int(2), "/"),
        Value::Float(2.5)
    );
}

fn test_strings() {
    assert_eq!(
        binary(
            Value::Str("Leather ".to_string()),
            Value::Str("LTH".to_string()),
            "+"
        ),
        Value::Str("Leather LTH".to_string())
    );

    assert_eq!(
        binary(
            Value::Str("a".to_string()),
            Value::Str("b".to_string()),
            "<"
        ),
        Value::Bool(true)
    );
}

fn test_collections() {
    let mut program = Program::new();

    program.constants = vec![
        Value::Int(10),
        Value::Int(20),
    ];

    program.names = vec!["items".to_string()];

    program.instructions = vec![
        Op::Const(0),
        Op::Const(1),
        Op::BuildList(2),
        Op::Store(0),
        Op::Halt,
    ];

    let result = Vm::new(1000)
        .run(&program, &HashMap::new())
        .expect("list execution failed");

    assert_eq!(
        result.values["items"],
        Value::List(vec![Value::Int(10), Value::Int(20)])
    );

    let mut map = HashMap::new();
    map.insert("price".to_string(), Value::Int(150));

    assert_eq!(
        Value::Map(map.clone()),
        Value::Map(map)
    );
}

fn test_builtins() {
    let mut program = Program::new();

    program.constants = vec![
        Value::Str("Leather".to_string()),
    ];

    program.names = vec!["length".to_string()];

    program.instructions = vec![
        Op::Const(0),
        Op::Call("len".to_string(), 1),
        Op::Store(0),
        Op::Halt,
    ];

    let result = Vm::new(1000)
        .run(&program, &HashMap::new())
        .expect("builtin execution failed");

    assert_eq!(
        result.values["length"],
        Value::Int(7)
    );
}

fn test_truthiness_and_logic() {
    assert_eq!(
        binary(Value::Int(0), Value::Int(9), "or"),
        Value::Int(9)
    );

    assert_eq!(
        binary(Value::Int(5), Value::Int(9), "and"),
        Value::Int(9)
    );

    assert_eq!(
        binary(Value::Int(0), Value::Int(9), "and"),
        Value::Int(0)
    );
}

fn test_optimizer() {
    let mut program = Program::new();

    program.constants = vec![
        Value::Int(2),
        Value::Int(3),
    ];

    program.instructions = vec![
        Op::Nop,
        Op::Const(0),
        Op::Const(1),
        Op::Binary("+".to_string()),
        Op::Halt,
    ];

    let optimized = Optimizer::optimize(&program);

    assert!(
        optimized.instructions.len() < program.instructions.len()
    );

    let runner = Runner::new(1000);
    let result = runner
        .run(&program, &HashMap::new())
        .expect("optimized execution failed");

    assert_eq!(
        result.profile.instructions,
        2
    );
}

fn test_demo() {
    let program = Compiler::demo_program();

    let result = Runner::new(1000)
        .run(&program, &HashMap::new())
        .expect("demo execution failed");

    match &result.values["price"] {
        Value::Float(price) => {
            assert!((*price - 135.45).abs() < 1e-12);
        }
        other => panic!("expected Float price, got {:?}", other),
    }
}

fn test_errors() {
    let mut program = Program::new();

    program.instructions = vec![
        Op::Pop,
        Op::Halt,
    ];

    assert!(
        Vm::new(100)
            .run(&program, &HashMap::new())
            .is_err()
    );

    let mut loop_program = Program::new();

    loop_program.instructions = vec![
        Op::Jump(0),
    ];

    let error = Vm::new(20)
        .run(&loop_program, &HashMap::new())
        .expect_err("step limit should fail");

    assert!(error.contains("step limit"));
}

fn main() {
    test_arithmetic();
    test_strings();
    test_collections();
    test_builtins();
    test_truthiness_and_logic();
    test_optimizer();
    test_demo();
    test_errors();

    let elapsed = benchmark(20_000);

    println!("LTH 0.7 RUST TESTS: PASS");
    println!("BENCHMARK ITERATIONS: 20000");
    println!("BENCHMARK TIME US: {}", elapsed);
}
