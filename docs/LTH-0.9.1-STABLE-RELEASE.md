# LTH 0.9.1 — Stable Bootstrap Release

## Identity

LTH 0.9.1 is the former LTH 1.0 scope.

It establishes the stable language/application boundary before the
future self-hosting stages.

## Scope

- Stable language contract
- Official runner
- Application/output/interaction boundary
- Module loading
- Leather-native errors
- LTH 0.1 compatibility guard
- Performance transparency
- Rust bootstrap verification
- Regression testing
- Integrity freeze

## Compatibility

The frozen LTH 0.1 semantic foundation remains authoritative.

LTH 0.9.1 adds stable application/runtime infrastructure without
replacing the foundational semantics.

## Performance

Performance observation is transparent:

- execution timing
- operation counts
- average execution cost

Observation must not change the semantic result.

## Rust Bootstrap

Rust is the stable implementation/bootstrap direction.

The bootstrap layer verifies the available Rust compiler and Rust
implementation boundary.

## Principle

> One language semantics. Multiple implementations. One canonical behavior.

## Release Rule

No semantic change from LTH 0.8 or LTH 0.9 is permitted merely for
implementation convenience.

LTH 0.9.1 is a stable bridge toward future LTH self-hosting.
