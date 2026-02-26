"""Unit tests for pii-detector-fr."""

from __future__ import annotations

import unittest

from pii_detector import PIIDetector


class PIIDetectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = PIIDetector(language="fr")

    def test_detect_email_phone_and_iban(self) -> None:
        text = (
            "Contact: marie.dupont@example.fr, téléphone +33 6 12 34 56 78, "
            "IBAN FR76 3000 6000 0112 3456 7890 189."
        )
        kinds = {m.entity_type for m in self.detector.detect(text)}
        self.assertIn("EMAIL", kinds)
        self.assertIn("PHONE_NUMBER", kinds)
        self.assertIn("IBAN", kinds)

    def test_anonymize_replaces_detected_values(self) -> None:
        text = "Mon email est contact@exemple.fr et ma plaque est AB-123-CD."
        result = self.detector.anonymize(text)
        self.assertIn("[EMAIL]", result)
        self.assertIn("[IMMATRICULATION]", result)
        self.assertNotIn("contact@exemple.fr", result)

    def test_prefers_longest_overlap_between_siren_and_siret(self) -> None:
        text = "SIRET: 802 954 785 00028"
        matches = self.detector.detect(text)
        self.assertEqual(1, len(matches))
        self.assertEqual("SIRET", matches[0].entity_type)

    def test_rejects_invalid_iban(self) -> None:
        text = "Iban invalide FR00 3000 6000 0112 3456 7890 189"
        matches = self.detector.detect(text)
        kinds = {m.entity_type for m in matches}
        self.assertNotIn("IBAN", kinds)


if __name__ == "__main__":
    unittest.main()
