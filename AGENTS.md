# Project context

This is a beginner's Rust learning project aimed at developing database-engineering foundations relevant to companies such as turbopuffer. The learner is new to Rust and has older C++ experience.

## How to help

- Use `docs/assignment-handbook.md` as the assignment specification and `docs/progress.md` to understand the current checkpoint.
- Favor small, explained steps and questions that check understanding when the user asks for tutoring.
- Let explicit user requests determine how much code to implement. Do not complete future assignments merely because they appear in the roadmap.
- Explain relevant ownership, borrowing, error handling, and storage behavior in practical terms.
- Distinguish implemented features, planned behavior, measured evidence, and assumptions.
- Preserve meaningful learner work and keep the README's status accurate.

## Implementation checks

Once Rust is installed and implementation begins, use the relevant tests plus `cargo fmt --check` and `cargo clippy --all-targets -- -D warnings` at checkpoints. Follow the failure model and format in the handbook.

## Documentation

The Markdown handbook is authoritative. Rebuild its PDF with `.venv-docs/bin/python scripts/build_handbook.py` after changes. See README for the isolated Python environment setup.
