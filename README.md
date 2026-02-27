# pii-detector-fr

Detect and anonymize French PII (RGPD-sensitive data) with a lightweight Python library and CLI.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- French-oriented detection for:
  - email
  - phone numbers
  - French postal addresses
  - IBAN
  - NIR (numero de securite sociale)
  - SIREN / SIRET
  - payment card numbers (Luhn validated)
  - French license plates
  - dates (`dd/mm/yyyy`)
- Deterministic anonymization with placeholders (`[EMAIL]`, `[IBAN]`, etc.)
- Optional deterministic hash pseudonymization (`[EMAIL#d41d8cd98f00]`)
- No mandatory runtime dependency (stdlib only)
- CLI for quick scans and pipelines

## Installation

```bash
git clone https://github.com/Exahia/pii-detector-fr.git
cd pii-detector-fr
python -m pip install -e .
```

## Python Usage

```python
from pii_detector import PIIDetector

detector = PIIDetector(language="fr")

text = "Contact: marie.dupont@example.fr, +33 6 12 34 56 78, 12 rue de la Paix, 75002 Paris"

for match in detector.detect(text):
    print(match.entity_type, match.text, match.start, match.end)

print(detector.anonymize(text))
# Contact: [EMAIL], [TELEPHONE], [ADRESSE]

print(detector.anonymize(text, strategy="hash", hash_key="my-org-key"))
# Contact: [EMAIL#...], [PHONE_NUMBER#...], [ADDRESS_FR#...]
```

## CLI Usage

Scan text and return JSON:

```bash
pii-detector scan --text "Mon email est jean@exemple.fr"
```

Anonymize a file:

```bash
pii-detector anonymize --file ./document.txt
```

Hash pseudonymization mode:

```bash
pii-detector anonymize --file ./document.txt --strategy hash --hash-key "my-org-key"
```

Pipe via stdin:

```bash
cat document.txt | pii-detector scan --pretty
```

## Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Limitations

- This release is a regex-first baseline.
- For critical production use, you should validate detections on your own corpus and add project-specific rules.

## Roadmap

- Add confidence calibration by entity
- Add enterprise allowlist/denylist dictionaries
- Add optional Presidio/spaCy backend
- Publish benchmark dataset for French PII precision/recall

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT.
