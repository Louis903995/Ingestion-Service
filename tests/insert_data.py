from config_connexion import get_connection

conn, cursor = get_connection()

### Exemple de data fictives

# 1. Tailles d’enseigne
tailles = ["Petite", "Moyenne", "Grande"]
taille_ids = []
for taille in tailles:
    cursor.execute("""
        INSERT INTO taille_enseigne (libelle_taille_enseigne)
        OUTPUT INSERTED.taille_enseigne_id
        VALUES (?)
    """, (taille,))
    taille_ids.append(cursor.fetchone()[0])
conn.commit()

# 2. Enseignes
enseignes = [
    ("Carrefour", "12 rue du Marché", taille_ids[2]),
    ("Lidl", "45 avenue des Champs", taille_ids[1]),
    ("Auchan", "78 boulevard du Nord", taille_ids[2]),
    ("Aldi", "3 impasse des Lilas", taille_ids[0]),
    ("Intermarché", "99 route de Paris", taille_ids[1])
]
enseigne_ids = []
for enseigne in enseignes:
    cursor.execute("""
        INSERT INTO enseigne (enseigne_nom, enseigne_adresse, taille_enseigne_id)
        OUTPUT INSERTED.enseigne_id
        VALUES (?, ?, ?)
    """, enseigne)
    enseigne_ids.append(cursor.fetchone()[0])
conn.commit()

# 3. Clients
clients = [
    ("Dupont", "Victor", "victor.dupont@email.com", "1 rue des Fleurs", 200.00),
    ("Martin", "Sophie", "sophie.martin@email.com", "2 rue des Lilas", 300.00),
    ("Lemoine", "Claire", "claire.lemoine@email.com", "3 rue des Violettes", 150.00),
    ("Moises", "Louis", "louis.moises@email.com", "4 rue des Marguerites", 162.00),
    ("Brad", "Pitt", "brad.pitt@email.com", "5 rue des Tulipes", 89.00)
]
client_ids = []
for client in clients:
    cursor.execute("""
        INSERT INTO client (nom_client, prenom_client, email_client, adresse_client, budget_client)
        OUTPUT INSERTED.client_id
        VALUES (?, ?, ?, ?, ?)
    """, client)
    client_ids.append(cursor.fetchone()[0])
conn.commit()

# 4. Tickets
tickets = [
    (client_ids[0], enseigne_ids[0], 25.50),
    (client_ids[1], enseigne_ids[1], 40.00),
    (client_ids[2], enseigne_ids[2], 15.75),
    (client_ids[3], enseigne_ids[3], 60.20),
    (client_ids[4], enseigne_ids[4], 32.10)
]
ticket_ids = []
for ticket in tickets:
    cursor.execute("""
        INSERT INTO ticket_entete (client_id, enseigne_id, montant_total_ticket)
        OUTPUT INSERTED.ticket_id
        VALUES (?, ?, ?)
    """, ticket)
    ticket_ids.append(cursor.fetchone()[0])
conn.commit()

# 5. Catégories de produit
categories = ["Boissons", "Viandes", "Eau", "Épicerie sucrée", "Surgelés"]
categorie_ids = []
for cat in categories:
    cursor.execute("""
        INSERT INTO categorie_produit (nom_categorie_produit)
        OUTPUT INSERTED.categorie_produit_id
        VALUES (?)
    """, (cat,))
    categorie_ids.append(cursor.fetchone()[0])
conn.commit()

# 6. Lignes de ticket
ticket_lignes = [
    (ticket_ids[0], "Coca-Cola", 2, categorie_ids[0], 1.50),
    (ticket_ids[1], "Steaks hachés", 1, categorie_ids[1], 5.00),
    (ticket_ids[2], "Eau minérale", 6, categorie_ids[2], 0.75),
    (ticket_ids[3], "Maltesers", 3, categorie_ids[3], 2.00),
    (ticket_ids[4], "Frites surgelées", 2, categorie_ids[4], 3.50)
]
for ligne in ticket_lignes:
    cursor.execute("""
        INSERT INTO ticket_ligne (ticket_id, libelle_produit, quantite, categorie_produit_id, prix_unitaire)
        VALUES (?, ?, ?, ?, ?)
    """, ligne)
conn.commit()

cursor.close()
conn.close()

print("Données fictives insérées avec succès.")
