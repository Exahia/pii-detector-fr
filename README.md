# PII Detector FR — Détection de Données Personnelles Françaises

> Détection et anonymisation automatique de données personnelles (PII) dans les textes français — propulsé par Presidio et spaCy.

[![Made in France](https://img.shields.io/badge/Made%20in-France-blue)](https://exahia.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![RGPD](https://img.shields.io/badge/RGPD-Compliant-green)](https://exahia.com)

---

## Pourquoi ?

Les entreprises françaises utilisant l'IA doivent **filtrer les données personnelles** avant tout traitement. Le RGPD impose des obligations strictes, avec des amendes pouvant atteindre **35M€ ou 7% du CA mondial** (EU AI Act, août 2026).

PII Detector FR détecte et anonymise automatiquement les données personnelles dans les textes français, **avant** qu'elles ne soient envoyées à un modèle de langage.

## Entités Détectées

| Entité | Exemples | Précision |
|--------|----------|-----------|
| **Noms** | Jean Dupont, Marie-Claire Lefèvre | Haute |
| **Adresses** | 12 rue de la Paix, 75002 Paris | Haute |
| **Téléphones** | 01 23 45 67 89, +33 6 12 34 56 78 | Très haute |
| **Emails** | jean.dupont@entreprise.fr | Très haute |
| **Numéro de Sécu** | 1 85 12 75 108 042 36 | Très haute |
| **IBAN** | FR76 3000 6000 0112 3456 7890 189 | Très haute |
| **SIRET/SIREN** | 802 954 785 00028 | Haute |
| **Numéro de carte** | 4970 1012 3456 7890 | Très haute |
| **Dates de naissance** | 15/03/1985, 15 mars 1985 | Haute |
| **Plaques d'immatriculation** | AB-123-CD | Haute |

## Installation

```bash
pip install pii-detector-fr
```

Ou depuis les sources :
```bash
git clone https://github.com/Exahia/pii-detector-fr.git
cd pii-detector-fr
pip install -r requirements.txt
python -m spacy download fr_core_news_lg
```

## Utilisation rapide

```python
from pii_detector import PIIDetector

detector = PIIDetector(language="fr")

texte = """
Bonjour, je suis Jean Dupont, habitant au 12 rue de la Paix, 75002 Paris.
Mon numéro de téléphone est le 01 23 45 67 89 et mon email est jean.dupont@mail.fr.
Mon numéro de sécurité sociale est 1 85 12 75 108 042 36.
"""

# Détecter les PII
resultats = detector.detect(texte)
for entite in resultats:
    print(f"{entite.type}: {entite.text} (confiance: {entite.score:.2f})")

# Anonymiser
texte_anonymise = detector.anonymize(texte)
print(texte_anonymise)
# → "Bonjour, je suis [NOM], habitant au [ADRESSE]..."
```

## Architecture

```
Texte brut
    │
    ▼
┌──────────────┐
│   spaCy NER  │ ← fr_core_news_lg (noms, lieux, organisations)
│   (français) │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Presidio    │ ← Reconnaisseurs custom (Sécu, IBAN, SIRET, etc.)
│  Analyzer    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Presidio    │ ← Remplacement, masquage, ou hachage
│  Anonymizer  │
└──────────────┘
       │
       ▼
  Texte anonymisé
```

## Performance

| Métrique | Valeur |
|----------|--------|
| **Latence** | <2ms par requête (texte court) |
| **Précision moyenne** | >95% sur les entités françaises |
| **Rappel** | >90% |
| **Langues** | Français (principal), extensible |

## Cas d'usage

- **Middleware IA** : Filtrer les PII avant envoi à un LLM
- **Anonymisation de documents** : RGPD, archivage, partage
- **Audit de conformité** : Scanner des corpus pour détecter des PII non protégées
- **Pipeline de données** : ETL avec anonymisation intégrée

## Lié à

Ce projet est développé par [Exahia](https://exahia.com), infrastructure IA souveraine B2B. La détection PII est un composant clé de notre middleware de sécurité.

## Licence

MIT — voir [LICENSE](LICENSE)
