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

    def test_detects_five_valid_french_addresses(self) -> None:
        text = (
            "1) 12 rue de la Paix, 75002 Paris\n"
            "2) 8 avenue Victor Hugo 75016 Paris\n"
            "3) 45 bd Saint-Germain 75005 Paris\n"
            "4) 3 impasse des Lilas, 33000 Bordeaux\n"
            "5) 120 route de Lyon 13008 Marseille"
        )
        matches = [m for m in self.detector.detect(text) if m.entity_type == "ADDRESS_FR"]
        self.assertEqual(5, len(matches))

    def test_does_not_detect_incomplete_address_patterns(self) -> None:
        text = (
            "Adresse incomplete: 12 rue des Idees.\n"
            "Code postal seul: 75002.\n"
            "Ville seule: Paris."
        )
        kinds = {m.entity_type for m in self.detector.detect(text)}
        self.assertNotIn("ADDRESS_FR", kinds)

    def test_anonymize_replaces_address(self) -> None:
        text = "Retrouvez-nous au 12 rue de la Paix, 75002 Paris."
        result = self.detector.anonymize(text)
        self.assertIn("[ADRESSE]", result)
        self.assertNotIn("12 rue de la Paix, 75002 Paris", result)

    def test_summarize_counts_entities(self) -> None:
        text = "Email: a@b.fr et backup c@d.fr. Tel: +33 6 12 34 56 78."
        summary = self.detector.summarize(text)
        self.assertEqual(2, summary.get("EMAIL"))
        self.assertEqual(1, summary.get("PHONE_NUMBER"))


if __name__ == "__main__":
    unittest.main()
