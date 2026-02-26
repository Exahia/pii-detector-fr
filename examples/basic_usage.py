"""Basic usage example for pii-detector-fr."""

from pii_detector import PIIDetector


def main() -> None:
    detector = PIIDetector(language="fr")

    text = (
        "Bonjour, je suis Jean Dupont. "
        "Mon email est jean.dupont@entreprise.fr, "
        "mon téléphone est 06 12 34 56 78 et mon IBAN FR76 3000 6000 0112 3456 7890 189."
    )

    print("=== Detections ===")
    for match in detector.detect(text):
        print(f"{match.entity_type}: {match.text} ({match.start}:{match.end})")

    print("\n=== Anonymized ===")
    print(detector.anonymize(text))


if __name__ == "__main__":
    main()
