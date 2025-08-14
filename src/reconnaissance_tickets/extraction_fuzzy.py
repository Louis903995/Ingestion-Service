import re
import Levenshtein


def normalise_espaces_pipes(s):
    # Remplace pipes et espaces multiples par un seul espace, retire les bords
    return re.sub(r"[\s|]+", " ", s).strip()


def extraire_apres_pattern_flou(texte, pattern, seuil_similarite=0.85):
    """
    Retourne ce qui suit le pattern (suite de mots séparés par espaces/pipes, matching flou).
    """
    norm_texte = normalise_espaces_pipes(texte)
    norm_pattern = normalise_espaces_pipes(pattern)
    n = len(norm_pattern)
    for i in range(len(norm_texte) - n + 1):
        chunk = norm_texte[i : i + n]
        dist = Levenshtein.distance(chunk, norm_pattern)
        similarity = 1 - dist / max(len(chunk), len(norm_pattern))
        if similarity >= seuil_similarite:
            # Essaie de retrouver la position du dernier mot du pattern dans le texte d'origine
            mots = pattern.split()
            last_word = mots[-1]
            # Cherche tous les emplacements possibles de last_word
            regex = re.compile(re.escape(last_word), re.IGNORECASE)
            for m in regex.finditer(texte):
                # Approxime une correspondance de position
                if m.start() >= int(i * len(texte) / len(norm_texte)) - len(last_word):
                    return texte[m.end() :]
            # Si échec, retourne la fin du texte
            return texte
    return None


def extraire_avant_pattern_flou(texte, pattern, seuil_similarite=0.85):
    """
    Retourne ce qui précède le pattern (suite de mots séparés par espaces/pipes, matching flou).
    """
    norm_texte = normalise_espaces_pipes(texte)
    norm_pattern = normalise_espaces_pipes(pattern)
    n = len(norm_pattern)
    for i in range(len(norm_texte) - n + 1):
        chunk = norm_texte[i : i + n]
        dist = Levenshtein.distance(chunk, norm_pattern)
        similarity = 1 - dist / max(len(chunk), len(norm_pattern))
        if similarity >= seuil_similarite:
            # Essaie de retrouver la position du premier mot du pattern dans le texte d'origine
            mots = pattern.split()
            first_word = mots[0]
            regex = re.compile(re.escape(first_word), re.IGNORECASE)
            for m in regex.finditer(texte):
                if m.start() >= int(i * len(texte) / len(norm_texte)) - 5:  # tolérance
                    return texte[: m.start()]
            # Si échec, coupe au même pourcentage
            approx_idx = int(i * len(texte) / len(norm_texte))
            return texte[:approx_idx]
    return None
