"""
Exercice 2 — Collisions et préimages
Utilise la fonction de l'exercice 1 : hachage_caractere_v2 et ALPHABET
"""

import random
import statistics
from collections import Counter
from typing import Tuple, Optional, List

from exercice1 import hachage_caractere_v2, ALPHABET  
def trouver_collision(alphabet: str = ALPHABET) -> Optional[Tuple[str, str, str]]:
    """
    Cherche deux caractères distincts ayant le même hash.
    Retourne (caractere1, caractere2, hash_binaire) si collision trouvée, sinon None.
    """
    table_hash: dict[str, str] = {}
    for caractere in alphabet:
        hash_binaire: str = hachage_caractere_v2(caractere)
        if hash_binaire in table_hash:
            if table_hash[hash_binaire] != caractere:
                return (table_hash[hash_binaire], caractere, hash_binaire)
        else:
            table_hash[hash_binaire] = caractere
    return None

def trouver_preimage(hash_cible: str, alphabet: str = ALPHABET, avec_remise: bool = True) -> Tuple[str, int]:
    """
    Cherche un caractère dont le hash est hash_cible.
    - avec_remise=True : tirages aléatoires i.i.d.
    - avec_remise=False : parcours d'une permutation aléatoire sans répétition
    Retourne (caractere_trouve, nombre_d_essais)
    """
    essais: int = 0
    deja_choisis: set[str] = set()
    while True:
        essais += 1
        caractere: str = random.choice(alphabet)
        if not avec_remise:
            if caractere in deja_choisis:
                continue
            deja_choisis.add(caractere)
        if hachage_caractere_v2(caractere) == hash_cible:
            return caractere, essais

def repetitions_preimages(n_repetitions: int = 100, avec_remise: bool = True) -> List[int]:
    """
    Répète n_repetitions fois la recherche de préimage pour des caractères aléatoires.
    Retourne la liste du nombre d'essais pour chaque répétition et affiche des statistiques.
    """
    resultats_essais: List[int] = []
    taille_alphabet: int = len(ALPHABET)

    for _ in range(n_repetitions):
        caractere_vrai: str = random.choice(ALPHABET)
        hash_cible: str = hachage_caractere_v2(caractere_vrai)
        _, essais = trouver_preimage(hash_cible, alphabet=ALPHABET, avec_remise=avec_remise)
        resultats_essais.append(essais)

    # Statistiques
    moyenne: float = statistics.mean(resultats_essais)
    mediane: float = statistics.median(resultats_essais)
    minimum: int = min(resultats_essais)
    maximum: int = max(resultats_essais)
    ecart_type: float = statistics.pstdev(resultats_essais)
    modes: List[Tuple[int, int]] = Counter(resultats_essais).most_common(3)

    print(f"\n--- Statistiques ({n_repetitions} répétitions, avec_remise={avec_remise}) ---")
    print(f"Moyenne : {moyenne:.2f}")
    print(f"Médiane : {mediane}")
    print(f"Min / Max : {minimum} / {maximum}")
    print(f"Écart-type : {ecart_type:.2f}")
    print(f"Valeurs les plus fréquentes (essais : occurrences) : {modes}")

    # Espérance théorique
    if avec_remise:
        esperance_theorique: float = taille_alphabet
    else:
        esperance_theorique = (taille_alphabet + 1) / 2
    print(f"Espérance théorique : {esperance_theorique:.2f} essais\n")

    return resultats_essais

if __name__ == "__main__":
    print("=== Exercice 2 : Collisions et préimages ===\n")

    # 1) Collision
    print("1️ Recherche de collision :")
    collision: Optional[Tuple[str, str, str]] = trouver_collision()
    if collision:
        c1, c2, h = collision
        print(f"Collision trouvée : '{c1}' et '{c2}' -> {h}")
    else:
        print("Aucune collision trouvée (attendu si hash = ord()).")

    # 2) Préimage pour un caractère aléatoire
    print("\n2️ Exemple de recherche de préimage :")
    caractere_vrai: str = random.choice(ALPHABET)
    hash_cible: str = hachage_caractere_v2(caractere_vrai)
    trouve, essais = trouver_preimage(hash_cible)
    print(f"Caractère choisi : '{caractere_vrai}', trouvé : '{trouve}' en {essais} essais")

    # 3) Répétitions
    print("\n3️ Répétitions de recherche de préimages :")
    repetitions_preimages(n_repetitions=1000, avec_remise=True)
    repetitions_preimages(n_repetitions=1000, avec_remise=False)
