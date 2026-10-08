# Leather 0.5 — Accelerated Execution Layer

Leather 0.5 extends the frozen 0.4 execution foundation with a real
stack-based bytecode execution layer.

## Architecture

LTH source
-> LTH 0.3 parser
-> LTH 0.5 compiler
-> bytecode
-> optimizer
-> stack VM
-> specialization cache
-> execution profile

## Major capabilities

- Explicit bytecode instructions
- Constant pooling
- Stack-based execution
- Branch execution
- Runtime specialization
- Opcode profiling
- Execution tracing
- Constant folding
- Source-to-bytecode compilation
- Equivalence validation against LTH 0.3
- Reusable compiled execution for benchmarks

## Performance direction

0.5 is an execution-engine milestone.

It does not claim universal speed superiority over Python or native
languages. Its purpose is to establish a concrete optimized execution
layer that later versions can specialize further for compute-heavy
workloads such as search, evaluation, repeated computation, and
game-tree workloads.

## Baseline protection

LTH 0.4 remains untouched and frozen.

LTH 0.5 is implemented as a new layer under `src/lth05/`.
