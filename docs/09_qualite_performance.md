# 09 — Qualité, performances et bonnes pratiques

Bonnes pratiques appliquées:
- Séparation claire routers/services/models/schemas.
- Caches RAM pour mappings fréquents (enseignes, catégories).
- Compteurs métriques pour observabilité en prod.
- Relations SQLModel et propriétés dérivées (nom_categorie_produit) pour simplifier les DTO.

Recommandations supplémentaires:
- Validation et parsing des dates au niveau du router (ou service) pour éviter les ambiguïtés de type (string vs datetime).
- Timeout et gestion d’exception explicite pour les appels au microservice de catégorisation.
- Tests unitaires ciblant:
  - Regex et fuzzy extraction (golden files Markdown OCR).
  - Mapping catégories (sensibilité à la casse, valeurs par défaut).
  - Scénarios d’erreurs (OCR down, catégorisation down, enseigne non trouvée).

Performance:
- Préchargement de dictionnaires au startup pour éviter des requêtes répétitives.
- selectinload pour charger les catégories des lignes en une passe.
- Possibilité d’ajouter des index DB (ticket_id, categorie_produit_id, date_heure_ticket) pour accélérer les requêtes de rapports.

Sécurité/Robustesse:
- Vérifier la provenance et la taille des fichiers uploadés.
- Masquer les secrets (MISTRAL_API_KEY, App Insights) et configurer des rôles RBAC sur les environnements d’exécution.
- Journaliser les erreurs avec contexte (client_id, ens. détectée) en évitant tout PII.

Navigation:
- Points d’attention: [10 — Points d’attention](./10_points_attention.md)
- Annexes: [11 — Annexes](./11_annexes.md)

Voir aussi: [Sommaire](./00_navigation.md)