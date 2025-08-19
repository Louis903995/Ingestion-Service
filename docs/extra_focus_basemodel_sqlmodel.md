# Focus — Pourquoi et comment utiliser BaseModel et SQLModel

Objectifs distincts:
- BaseModel (Pydantic): validation, sérialisation, contrôle des contrats d’API, objets non persistés (ex: TicketInterprete issu OCR).
- SQLModel: persistance relationnelle, jointures, contraintes et relations ORM.

Bonnes pratiques de séparation:
- Ne pas exposer directement les entités SQLModel en réponse publique; préférer des DTO (ex: TicketEnteteResponse).
- Uniformiser les champs entre DTO et entités persistance uniquement si l’intention est de réutiliser le même schéma; sinon assumer des noms différents et écrire un mapping explicite.

Exemple de mapping contrôlé (pseudo-code):

```python
# De TicketInterprete (DTO) vers TicketEntete (SQLModel)
db_ticket = TicketEntete(
    client_id=client_id,
    enseigne_id=ti.enseigne_id,
    date_heure_ticket=ti.date_heure_ticket,
    montant_total_ticket=ti.montant_total_ticket or 0.0,
)
for l in ti.lignes:
    db_ligne = TicketLignes(
        ticket_id=db_ticket.ticket_id,  # après flush/commit
        libelle_produit=l.libelle_produit or "",
        quantite=l.qte or 1,
        categorie_produit_id=l.categorie_produit_id,
        prix_unitaire=l.pu,
        montant_total_ligne=l.montant,
    )
```

Erreurs courantes à éviter:
- Mélanger des DTO avec des entités persistées (risque d’exposer des colonnes internes).
- Supposer que from_orm gère des champs aux noms différents sans config/mapping; préférer un constructeur explicite si les noms divergent.

Liens:
- Modélisation générale: [03 — Modélisation](./03_modeles_donnees.md)
- Services: [06 — Services métiers](./06_services_metier.md)
- Points d’attention: [10 — Points d’attention](./10_points_attention.md)