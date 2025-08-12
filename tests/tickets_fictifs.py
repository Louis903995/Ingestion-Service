import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Paramètres
n_tickets = 10000
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
produits = [
    {"nom": "Eau", "cat": "Boisson"}, 
    {"nom": "Soda", "cat": "Boisson"},
    {"nom": "Bière", "cat": "Boisson"},
    {"nom": "Jus", "cat": "Boisson"},
    {"nom": "Pain", "cat": "Alimentaire"},
    {"nom": "Lait", "cat": "Alimentaire"},
    {"nom": "Fromage", "cat": "Alimentaire"},
    {"nom": "Pâtes", "cat": "Alimentaire"},
    {"nom": "Riz", "cat": "Alimentaire"},
    {"nom": "Chips", "cat": "Snack"},
    {"nom": "Chocolat", "cat": "Snack"},
    {"nom": "Bonbons", "cat": "Snack"},
]
clients = [f'C{str(i).zfill(3)}' for i in range(50)]

def seasonal_boisson_factor(date):
    if date.month in [6, 7, 8]:
        return 3
    else:
        return 1

tickets = []
for i in range(n_tickets):
    ticket_id = f"T{str(i).zfill(6)}"
    rand_days = random.randint(0, (end_date - start_date).days)
    date = start_date + timedelta(days=rand_days)
    client_id = random.choice(clients)
    # Nombre d'articles sur ce ticket
    n_lignes = random.randint(1, 6)
    # Pour éviter des doublons de produits sur le même ticket
    produits_ticket = random.sample(produits, k=n_lignes)
    for prod in produits_ticket:
        # Poids de saisonnalité pour les boissons en été
        if prod['cat'] == "Boisson":
            poids = seasonal_boisson_factor(date)
            if random.random() > 1/poids:  # On ajoute plus souvent des boissons en été
                pass  # On garde la boisson
            else:
                continue  # On saute cette boisson hors saison
        qte = np.random.randint(1, 5)
        if prod['cat'] == "Boisson":
            montant = np.round(qte * np.random.uniform(1, 3), 2)
        elif prod['cat'] == "Snack":
            montant = np.round(qte * np.random.uniform(1.5, 4), 2)
        else:
            montant = np.round(qte * np.random.uniform(2, 6), 2)
        tickets.append({
            'ticket_id': ticket_id,
            'date': date,
            'produit': prod['nom'],
            'catégorie': prod['cat'],
            'quantité': qte,
            'montant': montant,
            'client_id': client_id
        })

df = pd.DataFrame(tickets)
df.to_csv('tickets.csv', index=False)

print(df.head(10))
print(f"Nombre total de lignes (articles) : {len(df)}")
print(f"Nombre de tickets uniques : {df['ticket_id'].nunique()}")