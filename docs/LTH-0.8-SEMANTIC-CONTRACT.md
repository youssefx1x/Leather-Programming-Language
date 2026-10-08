# LTH 0.8 Semantic Contract

## Status

LTH 0.8 — Semantic Convergence
Contract baseline: initial draft
Frozen implementations preserved: LTH 0.6 C++, LTH 0.7 Rust

## Purpose

LTH 0.8 defines one canonical semantic contract shared by all LTH
implementations.

The contract is language-level behavior, not implementation detail.

Implementations may differ internally in memory layout, optimization,
compiler strategy, and execution engine, but equivalent LTH programs
must produce equivalent observable results.

## Core Value Model

The canonical value model contains:

- None
- Bool
- Int
- Float
- Str
- List
- Map

Numeric values:

- Int uses signed integer semantics.
- Float uses IEEE-754 floating-point semantics.
- Mixed Int/Float numeric operations produce Float when the operation
  requires a floating result.

## Equality

Numeric equality is value-based across Int and Float.

Examples:

    1 == 1.0 -> true

Structured equality is recursive for Lists and Maps.

## Truthiness

Core false-like values include:

- None
- false
- integer zero
- floating-point zero
- empty string
- empty list
- empty map

Other supported values are truth-like.

## Boolean Operators

`and` and `or` are operand-returning operators.

Examples:

    0 and 7 -> 0
    0 or 7  -> 7

They are not required to return Bool values.

## Numeric Semantics

Integer floor division follows mathematical floor semantics.

Examples:

    -5 // 2  -> -3
    5 // -2  -> -3

Modulo is defined consistently with floor division.

Examples:

    -5 % 2   -> 1
    5 % -2   -> -1

Division by zero and modulo by zero are errors.

## Floating-Point Conformance

Implementations must preserve the same mathematical operation.

Conformance comparison for Float results uses a tolerance of:

    abs(actual - expected) < 1e-12

No implementation may add arbitrary rounding merely to satisfy the
conformance harness.

## Strings

String concatenation preserves left-to-right order.

## Collections

Lists preserve element order.

Maps preserve key/value associations.

Collection equality is structural and recursive.

## Canonical Error Classes

The initial contract recognizes:

- division by zero
- modulo by zero
- stack underflow
- invalid operation
- invalid operand

Exact implementation-specific error text is not required to match unless
explicitly designated by a conformance case.

## Canonical IR Direction

LTH 0.8 introduces a common execution representation for future
cross-implementation convergence.

Initial canonical operation families:

    CONST
    LOAD
    STORE
    LOAD_MEMBER
    LOAD_INDEX
    BUILD_LIST
    BUILD_MAP
    UNARY
    BINARY
    CALL
    JUMP_IF_FALSE
    JUMP
    POP
    HALT

The IR is semantic infrastructure. It does not require every implementation
to use the same internal VM.

## Conformance Rule

A case passes when:

    Python result == canonical result
    C++ result    == canonical result
    Rust result   == canonical result

For Float values, the LTH 0.8 tolerance applies.

For errors, the canonical error class must match.

## Compatibility Rule

LTH 0.8 does not intentionally change the semantics established by the
validated LTH 0.6 and LTH 0.7 implementations.

If a conflict is discovered, the conflict becomes a conformance failure
that must be resolved explicitly before an 0.8 freeze.

## Performance Rule

Optimization may change execution strategy and performance, but must not
change observable LTH semantics.

## Design Principle

One Language Semantics.
Multiple Implementations.
One Canonical Behavior.
