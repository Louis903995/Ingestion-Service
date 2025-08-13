import Levenshtein


def trouve_pattern_similaire(texte, pattern, seuil_similarite=0.85):
    n = len(pattern)
    for i in range(len(texte) - n + 1):
        substring = texte[i : i + n]
        distance = Levenshtein.distance(substring, pattern)
        similarity = 1 - distance / max(len(substring), len(pattern))
        if similarity >= seuil_similarite:
            return i, substring, similarity
    return -1, None, 0.0

def extrait_lignes_entre_patterns_similaires(texte, pattern1, pattern2, seuil_similarite=0.85):
    # Trouver pattern1
    i1, pattern_trouve, _ = trouve_pattern_similaire(texte, pattern1, seuil_similarite)
    if i1 == -1:
        return None
    # Aller à la fin de la ligne où pattern1 se trouve
    fin_pattern1 = texte.find('\n', i1 + len(pattern_trouve))
    if fin_pattern1 == -1:
        return None
    # Chercher pattern2 après la fin de pattern1
    i2, _, _ = trouve_pattern_similaire(texte[fin_pattern1:], pattern2, seuil_similarite)
    if i2 == -1:
        return None
    # Position absolue de pattern2
    i2_abs = fin_pattern1 + i2
    # Prendre le texte entre ces deux patterns
    contenu = texte[fin_pattern1:i2_abs]
    # Nettoyer pour retirer la première et dernière ligne (si pattern1/pattern2 sont sur des lignes séparées)
    lignes = contenu.splitlines()
    # On enlève les lignes vides en début/fin si besoin
    while lignes and not lignes[0].strip():
        lignes = lignes[1:]
    while lignes and not lignes[-1].strip():
        lignes = lignes[:-1]
    return "\n".join(lignes)

# # Exemple
# texte = """
# du texte avant
# |     |                      |     |       |
# | --- | -------------------- | --- | ----- |

# ici commence le tableau de données
# 7   | *100G NENTOS FESH H | 4  | 4.35€
# fin du tableau
# |   | footer |   |   |
# """

# pattern1 = "| --- | -------------------- | --- | ----- |"
# pattern2 = "|   | footer |   |   |"

# resultat = extrait_lignes_entre_patterns_similaires(texte, pattern1, pattern2, seuil_similarite=0.8)
# print(resultat)