# LTH 1.0 — Self-Hosting

## Status

LTH 1.0 is the first self-hosting foundation release.

## Frozen foundations

- LTH 0.8 Semantic Convergence
- LTH 0.9 Execution Acceleration
- LTH 0.9.1 Stable Bootstrap

## 1.0 architecture

Leather source
→ Lexer
→ Parser
→ Semantic layer
→ IR
→ Runtime

LTH 1.0 does not replace existing implementations.

It makes Leather source a first-class implementation artifact and
establishes the bootstrap boundary for progressively moving compiler
responsibility into Leather itself.

## Core concepts

- value
- rule
- base
- flow
- system

## Design rule

One canonical semantic contract.

Multiple implementations.

Progressive self-hosting.

## Performance

The execution acceleration contract from LTH 0.9 remains active.

Self-hosting must not sacrifice semantic equivalence or execution
performance.

## Release principle

> Leather should eventually be able to build Leather.
