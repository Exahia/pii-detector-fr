# Contribuer à pii-detector-fr

Merci de votre intérêt pour ce projet ! Voici comment contribuer.

## Signaler un bug

Ouvrez une [issue GitHub](https://github.com/Exahia/pii-detector-fr/issues) en décrivant :
- Le comportement observé
- Le comportement attendu
- Un exemple de texte reproduisant le problème (sans données personnelles réelles)

## Proposer une amélioration

1. Ouvrez une issue pour discuter de la fonctionnalité avant de coder
2. Obtenez un accord de l'équipe Exahia
3. Soumettez une Pull Request

## Processus de Pull Request

1. Forkez le repo
2. Créez une branche : `git checkout -b feat/ma-fonctionnalite`
3. Committez vos changements : `git commit -m "feat: description courte"`
4. Pushez : `git push origin feat/ma-fonctionnalite`
5. Ouvrez une Pull Request sur `main`

## Standards de code

- **Python** : PEP8, formatage avec `black`
- **Tests** : Toute nouvelle entité détectée doit être couverte par des tests
- **Documentation** : Mettre à jour le README si nécessaire
- **Langue** : Commentaires et PR en français ou anglais

## Ajouter un nouveau type d'entité

Pour ajouter la détection d'un nouveau type de PII français :

1. Créer un reconnaisseur dans `pii_detector/recognizers/`
2. L'enregistrer dans `pii_detector/registry.py`
3. Ajouter des tests dans `tests/`
4. Documenter l'entité dans le README

## Contact

Pour toute question : [admin@exahia.ia](mailto:admin@exahia.ia)

Projet maintenu par [Exahia](https://exahia.com).
