"""
# Supprimer toutes les données des tables 
cursor.execute("DELETE FROM supermarche")
cursor.execute("DELETE FROM categorie")
cursor.execute("DELETE FROM ticket")
cursor.execute("DELETE FROM client")
conn.commit()

# Réinitialiser le compteur d'auto-incrément (IDENTITY) à 0 pour chaque table
# Cela garantit que les prochaines insertions repartiront de 1 et qu'en executant ce script 2 fois, on aura 2 fois les mêmes données 
cursor.execute("DBCC CHECKIDENT ('supermarche', RESEED, 0)")
cursor.execute("DBCC CHECKIDENT ('categorie', RESEED, 0)")
cursor.execute("DBCC CHECKIDENT ('ticket', RESEED, 0)")
cursor.execute("DBCC CHECKIDENT ('client', RESEED, 0)")
conn.commit()
"""

### Exemple de data fictives

# Insérer des clients fictifs et récupérer leurs IDs
clients_data = [
    ("Dupont", "Victor", "victor.dupont@email.com", 200.00),
    ("Martin", "Sophie", "sophie.martin@email.com", 300.00),
    ("Lemoine", "Claire", "claire.lemoine@email.com", 150.00),
    ("Moises", "Louis", "louis.moises@email.com", 162.00),
    ("Brad", "Pitt", "brad.pitt@email.com", 89.00)
]

client_ids = []
for client in clients_data:
    cursor.execute("""
        INSERT INTO client (nom, prenom, email, budget)
        OUTPUT INSERTED.client_id
        VALUES (?, ?, ?, ?)
    """, client)
    client_ids.append(cursor.fetchone()[0])

conn.commit()
print(f"{len(client_ids)} clients insérés avec succès.")


# Insérer les tickets liés aux bons client_id
tickets_data = [
    (client_ids[0], "coca-cola"),
    (client_ids[1], "steaks hachés"),
    (client_ids[2], "eau"),
    (client_ids[3], "maltesers"),
    (client_ids[4], "frites")
]

ticket_ids = []
for ticket in tickets_data:
    cursor.execute("""
        INSERT INTO ticket (client_id, libelle)
        OUTPUT INSERTED.id_ticket
        VALUES (?, ?)
    """, ticket)
    ticket_ids.append(cursor.fetchone()[0])
conn.commit()

# Insérer les catégories liées aux bons id_ticket
categorie_data = [
    (ticket_ids[0], "Coca-Cola", "boissons"),
    (ticket_ids[1], "steaks hachés", "viandes et charcuterie"),
    (ticket_ids[2], "eau", "eau"),
    (ticket_ids[3], "Maltesers", "épicerie sucrée"),
    (ticket_ids[4], "frites", "surgelés")
]
cursor.executemany("""
    INSERT INTO categorie (id_ticket, libelle, categorie)
    VALUES (?, ?, ?)
""", categorie_data)
conn.commit()

# Insérer les supermarchés liés aux bons id_ticket
supermarche_data = [
    (ticket_ids[0], "Carrefour", "2018-06-06", 200),
    (ticket_ids[1], "Aldi", "2018-06-06", 300),
    (ticket_ids[2], "Auchan", "2018-06-06", 400),
    (ticket_ids[3], "Lidl", "2018-06-06", 600),
    (ticket_ids[4], "Carrefour", "2018-06-06", 200)
]
cursor.executemany("""
    INSERT INTO supermarche (id_ticket, nom_magasin, date_achat, prix_total)
    VALUES (?, ?, ?, ?)
""", supermarche_data)
conn.commit()

cursor.close()
conn.close()
