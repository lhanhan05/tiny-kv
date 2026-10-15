# Project progress

Only check a milestone off after its acceptance criteria and evidence are complete. The assignment handout is in [assignment-handbook.md](assignment-handbook.md).

## Setup

- [ ] Install stable Rust and verify Cargo works.
- [ ] Run the starter program.
- [ ] Make and explain the first small code change.
- [ ] Complete the Rust preparation exercises in section 5.

## A1 - In-memory store

- [ ] Implement put/get/delete and the interactive command loop.
- [ ] Pass missing-key, overwrite, delete, empty-value, and validation tests.
- [ ] Explain ownership, borrowing, and `Option` using this code.
- [ ] Record a demo and create tag `a1-memory`.

## A2 - File-backed store

- [ ] Save and reload a versioned snapshot.
- [ ] Demonstrate put/get/delete across separate processes.
- [ ] Report malformed files and I/O errors clearly.
- [ ] Document clean-restart persistence and failure limitations.
- [ ] Create tag `a2-snapshot`.

## A3 - Append-only log

- [ ] Implement the handbook's v1 format and record codec.
- [ ] Rebuild state by replaying the log.
- [ ] Append and synchronize before acknowledging each mutation.
- [ ] Handle uncertain write outcomes and new-file initialization.
- [ ] Create tag `a3-log`.

## A4 - Recovery

- [ ] Test every byte cut within a final record.
- [ ] Test checksum, operation, length, header, and UTF-8 errors.
- [ ] Repair incomplete tails before accepting further writes.
- [ ] Test actual child-process termination and restart.
- [ ] Explain process-crash versus power-loss evidence.
- [ ] Create tag `a4-recovery`.

## A5 - Compaction

- [ ] Compact to a synchronized replacement on the same filesystem.
- [ ] Synchronize the parent directory and reopen the active file.
- [ ] Test each replacement boundary and subsequent writes.
- [ ] Explain delete handling and the single-writer assumption.
- [ ] Create tag `a5-compaction`.

## A6 - Measurements and Linux

- [ ] Implement a deterministic workload runner.
- [ ] Capture release-build baseline and CPU/memory evidence.
- [ ] Improve one measured bottleneck and repeat the same experiment.
- [ ] Complete the Linux syscall and debugging exercise.
- [ ] Fill in `results/performance-report.md`.
- [ ] Create tag `a6-performance`.

## A7 - Mini-LSM bridge

- [ ] Answer the readiness questions without copying a solution.
- [ ] Read the Mini-LSM overview and complete its first implementation chapter.
- [ ] Record the separate course repository and checkpoint.
- [ ] Submit the final design report and demo.
- [ ] Create tag `a7-ready`.
