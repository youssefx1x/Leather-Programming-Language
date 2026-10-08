# Leather 0.6 — C++ Execution Layer

## Goal

LTH 0.6 introduces a native C++ execution foundation while preserving the
semantic model established by LTH 0.5.

## Principles

- Same semantic result.
- Same context/output separation.
- Stack-based execution.
- Specialized arithmetic.
- Explicit profiling.
- No replacement of the Python implementation.
- C++ is an additional execution backend.

## Architecture

LTH 0.5 Python
        |
        v
Semantic / bytecode contract
        |
        v
LTH 0.6 C++ VM
        |
        +-- Value
        +-- Program
        +-- Stack VM
        +-- Specialization
        +-- Profiler
        +-- Optimizer

## 0.6 Scope

- Native Value representation
- Native bytecode model
- Native stack VM
- Specialized numeric binary operations
- Context isolation
- Profiling
- C++ regression foundation

## Future

0.7 will deepen optimization and introduce stronger Python/C++ semantic
equivalence fixtures.

0.8+ can add lower-level execution strategies without changing LTH semantics.
