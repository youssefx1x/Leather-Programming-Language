# LTH 0.8 — Cross-Implementation Conformance

## Status

LTH 0.8 Semantic Convergence.

## Goal

LTH semantics are defined once and implemented independently by:

- Python
- C++
- Rust

All implementations consume the same canonical conformance corpus.

## Canonical Corpus

`tests/conformance/lth08_cases.tsv`

The corpus contains 18 semantic cases covering:

- numeric operations
- floor division
- modulo
- cross numeric equality
- truthiness
- operand-returning boolean operators
- strings
- collections
- canonical errors

## Conformance Rule

For every case:

`Python == C++ == Rust == Expected`

A case is conformant only when all four representations match.

## Numeric Rule

LTH uses Python-style floor division and modulo:

- `-5 // 2 = -3`
- `-5 % 2 = 1`
- `5 // -2 = -3`
- `5 % -2 = -1`

## Canonical Errors

- division by zero
- modulo by zero

## Canonical IR Direction

The convergence layer reserves these canonical operations:

`CONST`
`LOAD`
`STORE`
`LOAD_MEMBER`
`LOAD_INDEX`
`BUILD_LIST`
`BUILD_MAP`
`UNARY`
`BINARY`
`CALL`
`JUMP_IF_FALSE`
`JUMP`
`POP`
`HALT`

## Performance Principle

Conformance is semantic first.

Performance optimization is valid only when the observable semantic result remains canonical.

## Principle

> One Language Semantics. Multiple Implementations. One Canonical Behavior.
