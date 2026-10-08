# LTH 1.0 — Self-Hosting Foundation

LTH 1.0 begins the transition from implementations of Leather
toward Leather implementing Leather.

## Core Rule

Leather source becomes a first-class implementation artifact.

## Foundation

- values
- rules
- bases
- flows
- systems
- modules
- execution
- verification
- performance-aware execution
- native escape hatch

## Compatibility

LTH 0.8 semantic convergence remains authoritative.

LTH 0.9 execution acceleration remains authoritative.

LTH 0.9.1 stable bootstrap remains authoritative.

## Self-Hosting Strategy

LTH 1.0 is incremental.

Existing Python, C++, and Rust implementations remain available
as bootstrap implementations.

Leather gradually takes ownership of:

1. language definitions
2. semantic rules
3. execution descriptions
4. runtime components
5. compiler components
6. eventually the compiler itself

## Principle

> Leather should eventually be able to build Leather.

This release begins that transition without breaking the frozen
semantic contract.
