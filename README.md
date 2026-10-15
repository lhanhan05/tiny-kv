# tiny-kv

A self-directed, college-style systems programming project: learn Rust by building a small persistent key-value store, then prepare for [Mini-LSM](https://skyzh.github.io/mini-lsm/).

**Current status:** assignment and starter repository prepared; database implementation has not started. `src/main.rs` is an orientation program, not a working database.

## Assignment handbook

- **[Download / read the full PDF](docs/assignment-handbook.pdf)**
- [Read the editable Markdown version](docs/assignment-handbook.md)
- [Track milestones](docs/progress.md)
- [Keep engineering notes](notes/engineering-journal.md)
- [Write up measurements](results/performance-report.md)

The handbook contains prerequisites, setup, a suggested schedule, seven assignments, a precise storage-format specification, recovery rules, failure tests, performance and Linux labs, deliverables, a 100-point rubric, and a first-session checklist. It is an independent learning assignment, not an official turbopuffer or university course.

## Goal

Build enough understanding to explain how a single-process database stores data, what happens during a crash, and how measurements guide an optimization. The finished project should demonstrate correctness, explicit durability guarantees, recovery tests, and reproducible performance analysis.

## Start here

1. Install the current stable Rust toolchain using [rustup](https://www.rust-lang.org/tools/install).
2. Verify `rustc --version` and `cargo --version` in a new terminal.
3. In this project directory, run `cargo run`.
4. Read handbook sections 1-5, then complete Assignment 1.

This repository already contains `Cargo.toml` and `src/main.rs`; you can start editing it directly.

## Milestones

- [ ] Environment and basic Rust exercises
- [ ] A1: In-memory store
- [ ] A2: File-backed store and clean-restart persistence
- [ ] A3: Append-only log and a defined acknowledgement rule
- [ ] A4: Recovery, corruption checks, and failure testing
- [ ] A5: Crash-aware compaction
- [ ] A6: Performance study and Linux debugging lab
- [ ] A7: Mini-LSM readiness review and first chapter

## Intended final CLI

These commands are the assignment target; they become available as you implement it.

```bash
cargo run -- --db data/store.kv put name Alice
cargo run -- --db data/store.kv get name
cargo run -- --db data/store.kv delete name
cargo run -- --db data/store.kv compact
```

## Repository layout

```text
src/                          Rust starter; grow this during the assignment
docs/assignment-handbook.md    Authoritative, editable assignment
docs/assignment-handbook.pdf   Generated, printable assignment
docs/progress.md               Milestone checklist
notes/engineering-journal.md   Decisions, questions, and debugging notes
results/performance-report.md  Experiment template
results/raw/                  Local generated measurements (Git-ignored)
data/                         Local database files (Git-ignored)
scripts/build_handbook.py      Reproducible PDF generator
requirements-docs.txt          Python dependencies for rebuilding the PDF
```

## Rebuild the PDF

Python 3.10+ is needed only to generate the documentation. It is independent of the Rust database project.

```bash
python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install -r requirements-docs.txt
.venv-docs/bin/python scripts/build_handbook.py
```

## Working agreement

Make small commits, predict behavior before running code, and record what you learn. Use help to understand errors and review reasoning; make sure you can explain every piece of code you keep. Tag completed checkpoints as described in the handbook.

## References

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rustlings](https://github.com/rust-lang/rustlings)
- [Mini-LSM](https://skyzh.github.io/mini-lsm/)
- [PingCAP Talent Plan: Rust key-value store](https://github.com/pingcap/talent-plan/tree/master/courses/rust)

Original handbook prepared with AI assistance as a learning plan. Linked course materials retain their own authorship and licenses.
