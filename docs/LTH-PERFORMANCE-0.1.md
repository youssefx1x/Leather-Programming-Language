# Leather Performance Foundation 0.1

Leather now has an independent performance layer above the existing
semantic/IR/runtime pipeline.

## Core Idea

Leather performance optimization must preserve meaning.

A candidate optimization is valid only when:

1. Its meaning signature matches the source computation.
2. Semantic preservation is explicitly asserted.
3. Its performance cost strictly improves the source in the defined metrics.
4. The result can be represented as evidence.

## Performance Dimensions

Leather tracks:

- time
- memory
- states
- branching
- depth
- precision
- interactions

These dimensions are descriptive computational metrics.

They are not universal physical laws.

## Optimization

The optimizer treats a transformation as a candidate rather than assuming
that a transformation is automatically beneficial.

A candidate is selected only when it strictly Pareto-dominates the source cost.

## SEA Bridge

Leather and SEA share the same seven computational dimensions.

Leather costs can therefore be mapped into `SEAComplexity`.

This allows SEA optimization certificates to be used as a second-layer
complexity representation while Leather retains its own execution model.

## Runtime Evidence

The runtime layer can measure actual elapsed execution time.

Measurements are evidence for the tested workload only.

A fast result on one machine does not constitute a universal performance
theorem.

## Current Architecture

Source Intent
    ↓
Semantic Meaning
    ↓
Leather Performance Intent
    ↓
Performance Estimate
    ↓
Optimization Candidate
    ↓
Pareto Validation
    ↓
SEA Complexity View
    ↓
Runtime Measurement
    ↓
Performance Evidence

The existing Core 0.1 IR is intentionally unchanged in this layer.
