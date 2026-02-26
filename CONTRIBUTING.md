# Contributing to pii-detector-fr

## Setup

```bash
git clone https://github.com/Exahia/pii-detector-fr.git
cd pii-detector-fr
python -m pip install -e .
```

## Quality Checks

Run tests before opening a PR:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## How to Propose Changes

1. Open an issue describing the bug/feature.
2. Create a branch from `main`.
3. Add tests with your change.
4. Open a pull request with:
   - context
   - implementation details
   - before/after behavior

## Scope for Contributions

- New French PII patterns
- False-positive reduction
- Better anonymization policies
- Performance improvements
- Dataset and evaluation tooling

## Guidelines

- Keep runtime dependency-light when possible.
- Do not commit real personal data in tests or examples.
- Prefer deterministic behavior over hidden heuristics.

## Security

Do not open public issues with sensitive production data.
If needed, contact: admin@exahia.ia
