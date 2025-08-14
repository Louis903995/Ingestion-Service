import re

from levenshtein import extrait_lignes_entre_patterns_similaires


def trouve_nom_enseigne(texte: str) -> str | None:
    # Recherche "#" suivi de 0 ou plusieurs espaces puis "market", insensible à la casse.
    # recherche toute ligne non vide après "market"
    # capture le début de la ligne jusqu'à "Tel" non inclus
    match = re.search(
        r"#\s*market.*?\n\s*\n*([^\n]+?)\s*Tel:", texte, re.IGNORECASE | re.DOTALL
    )
    if match:
        return match.group(1).strip()


def trouve_tel_enseigne(texte: str) -> str | None:
    # Regex pour trouver le numéro après 'Tel' en fin de ligne
    # un numéro est composé de 4 séries de 2 chiffres espacés par des " "
    match = re.search(r"Tel[:\s]*([0-9]{2}(?:\s[0-9]{2}){4})\s*$", texte, re.MULTILINE)
    if match:
        return match.group(1)


def isole_lignes_tableau(texte: str) -> str:
    texte_reduit = extrait_lignes_entre_patterns_similaires(
        texte,
        "TVA DESCRIPTION QTE x P.U. MONTANT TTC",
        "ARTICLE(S) TOTAL A PAYER",
        seuil_similarite=0.95,
    )
    # print(texte_reduit)

    pattern = re.compile(
        r"""
        ^\s*                  # début de ligne + espaces optionnels
        \|                    # pipe ouvrant
        (?:\s*-{3,}\s*\|){2,3}# 2 ou 3 groupes (pour 3 ou 4 colonnes)
        \s*-{3,}\s*           # dernière colonne : >=3 -
        \|                    # pipe fermant
        \s*$                  # espaces optionnels + fin de ligne
        """,
        re.MULTILINE | re.VERBOSE,
    )

    lignes = texte_reduit.splitlines()
    for i, ligne in enumerate(lignes):
        if pattern.match(ligne):
            # On avance après le pattern
            index = i + 1
            # On saute toutes les lignes blanches (espaces ou vide)
            while index < len(lignes) and lignes[index].strip() == "":
                index += 1
            # On retourne toutes les lignes à partir de la première ligne utile
            return lignes[index:]
    return []


def interprete_lignes(texte: str):
    pattern = re.compile(
        r"""
    ^\s*\|?\s*                 # Début ligne, pipe et espaces optionnels
    (\d*)                      # Col 1: quantité (peut être vide pour totaux)
    \s*\|\s*                   # Séparateur pipe
    ([^|]+?)                   # Col 2: nom produit
    (?:                        # Groupe optionnel pour Col3
        \s*\|\s*               # Séparateur pipe
        ([\dxX., ]*)           # Col 3: qte x PU ou vide (ex: '4 x 3.54')
    )?                         # <- OPTIONNEL !
    \s*\|\s*                   # Séparateur pipe
    (\d+[.,]\d+)\s*€?          # Col 4: prix avec ou sans le symbole euro
    \s*\|?\s*$                 # Pipe et espaces optionnels, fin de ligne
    """,
        re.VERBOSE,
    )
    for ligne in texte:
        m = pattern.match(ligne)
        if not m:
            continue  # ignore les lignes non valides

        taux_tva = m[1].strip()
        libelle_produit = m[2].strip()
        if m[3]:
            qte_par_pu = m[3].replace(",", ".").replace(" ", "").strip()
        else:
            qte_par_pu = None
        montant = m[4].replace(",", ".").strip()

        # Gestion de la troisème colonne optionnelle au format "q x pu"
        if qte_par_pu:
            if "x" in qte_par_pu.lower():
                try:
                    q_str, pu_str = re.split(r"x", qte_par_pu, flags=re.IGNORECASE)
                    qte = int(q_str)
                    pu = float(pu_str)
                except Exception:
                    # on ne fait rien, on se contente de ce qu'on a réussi à récupérer
                    pass
        else:
            qte = None
            pu = None
        z = {
            "taux_tva": taux_tva,
            "libelle_produit": libelle_produit,
            "qte": qte,
            "pu": pu,
            "montant": montant,
        }
        print(z)


# filename = "sample.md"
filename = "sample-modifié.md"
with open(filename, "r") as f:
    sample = f.read()
    print(trouve_nom_enseigne(sample))
    print(trouve_tel_enseigne(sample))
    lignes = isole_lignes_tableau(sample)
    # print(lignes)
    print(interprete_lignes(lignes))
