import re
from datetime import datetime
from typing import List
from reconnaissance_tickets.extraction_fuzzy import (
    extraire_apres_pattern_flou,
    extraire_avant_pattern_flou,
)
from reconnaissance_tickets.model_ticket import LigneTicketInterpretee


def trouve_tel_enseigne(texte: str) -> str | None:
    pattern = (
        r"Tel:\s*"  # "Tel:" suivi d'espaces éventuels
        r"("  # Début de la capture du numéro
        r"[0-9]{2}"  # 2 chiffres
        r"(?:[ .]+[0-9]{2}){4}"  # 4 groupes de séparateur(s) (espace ou point) + 2 chiffres
        r")"  # Fin de la capture
        r"(?:\s+|\s*\n)"  # Après le numéro: un ou plusieurs espaces OU zéro+espace puis saut de ligne
    )
    match = re.search(pattern, texte)
    if match:
        return match.group(1)
    return None


def trouve_date_heure(texte: str) -> datetime | None:
    # Regex pour trouver le numéro après 'Tel' en fin de ligne
    # un numéro est composé de 4 séries de 2 chiffres espacés par des " "
    match = re.search(r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})", texte, re.MULTILINE)
    if match:
        date_str = match.group(1)
        dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
        return dt


def isole_lignes_tableau(texte: str) -> List[str]:
    texte_intermediaire = extraire_apres_pattern_flou(
        texte, "TVA DESCRIPTION QTE x P.U. MONTANT TTC"
    )
    texte_reduit = extraire_avant_pattern_flou(
        texte_intermediaire, "ARTICLE(S) TOTAL A PAYER"
    )
    if texte_reduit:
        return texte_reduit.splitlines()
    return []


def interprete_lignes(texte: str) -> List[LigneTicketInterpretee]:
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
    resultat = []
    for ligne in texte:
        m = pattern.match(ligne)
        if not m:
            continue  # ignore les lignes non valides

        taux_tva = m[1].strip()
        if taux_tva == "":
            taux_tva = None
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
            qte = 1
            pu = None
        resultat.append(
            LigneTicketInterpretee(
                taux_tva=taux_tva,
                libelle_produit=libelle_produit,
                qte=qte,
                pu=pu,
                montant=montant,
            )
        )
    return resultat
