# Performance report

Status: not started. Replace prompts with actual observations; leave missing measurements explicitly marked as missing.

## 1. Question and hypothesis

What is slow or memory-heavy? What evidence suggests a cause?

## 2. Environment

- Date:
- Commit:
- OS / kernel:
- CPU / core count:
- RAM:
- Storage device / filesystem:
- Rust version:
- Build mode and flags:
- Background load:

## 3. Workload

- Seed / dataset identity:
- Initial key count:
- Key and value sizes:
- Operation mix / hit rate:
- Warm-up and measured operation count:
- Number of repeated runs:
- Open / recovery included or excluded:
- Durability policy:
- Cache assumptions:
- Exact commands:

## 4. Baseline

- Operations per second:
- Per-operation p50 / p95 / p99, including sample count:
- Recovery time:
- File size:
- Peak resident memory, measurement tool, and units:
- CPU profile location and observed hot path:

## 5. Change

- Hypothesis:
- Implementation / commit:
- Correctness checks:
- Durability semantics before and after:

## 6. Comparison

Report individual runs or a summary plus variation. Compare the same workload and environment. Include regressions and results that did not improve.

## 7. Interpretation

What does the evidence support? What remains uncertain? Which cost moved elsewhere?

## 8. Reproduction

List the commands and small committed inputs needed to reproduce the result. Keep bulky raw profiles in `results/raw/` and summarize the useful evidence here.
