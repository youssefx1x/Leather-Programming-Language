# SEA CORE 0.4

## Purpose

SEA 0.4 extends the mathematical prototype into an explicit computational
structure for recurrence, graphs, equivalence, search, compression,
measurement, validation, and domain execution.

## New Layers

### 1. Recurrence Algebra

Represents finite recurrences:

T(n) = Σ a_i T(n-i-1) + F(n)

This provides a direct representation for recursive computational growth.

### 2. Graph / DAG Model

SEA states can be represented as graph nodes and transitions as directed edges.

Supported operations:

- node insertion
- edge insertion
- reachability
- cycle detection
- topological order
- graph statistics

### 3. Equivalence / Quotient

States can be grouped by an explicit equivalence key.

Original state population:

N

Quotient population:

N_q

Compression ratio:

N / N_q

The equivalence function is explicit and therefore inspectable.

### 4. Search Compression

SEA provides two comparable search modes:

- TREE: expansion without global deduplication
- GRAPH: expansion with explicit state equivalence

Measured quantities include:

- generated states
- expanded states
- unique states
- duplicate states
- depth
- runtime

### 5. Validation

SEA 0.4 validates:

- recurrence structure
- graph integrity
- search-result invariants

### 6. Domain Layer

A `SEADomain` packages:

- initial state
- state expansion
- goal predicate
- equivalence key
- metadata

### Scientific Boundary

SEA 0.4 does NOT claim a universal exponential-to-polynomial transformation.

It measures specific, explicit state-space reductions.

A reduction is meaningful only when:

1. The state equivalence is valid for the problem semantics.
2. The optimized computation preserves the required result.
3. The reduction is measured on the defined workload.

The graph/search comparison is therefore an experimental computational model,
not a theorem about all search problems.
