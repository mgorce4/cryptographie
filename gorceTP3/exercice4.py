"""
Exercice 4 - Attaque par dictionnaire avec fonction de hachage H*

Ce programme implémente une attaque par dictionnaire en utilisant une fonction de hachage H*
définie comme le XOR des hash individuels de chaque caractère d'un mot.
On réutilise la fonction hachage_caractere_v2 de l'exercice 1.

Auteur: [Votre nom]
Date: 2025
"""

from collections import defaultdict
from typing import Dict, List, Tuple, Set
import os

# Import des fonctions des exercices précédents
from exercice1 import hachage_caractere_v2, ALPHABET

def calculer_h_etoile(mot: str) -> int:
    """
    Calcule la fonction de hachage H*(mot) définie comme le XOR 
    des valeurs de hachage de chaque caractère du mot.
    
    Args:
        mot: Le mot dont on veut calculer le hash
        
    Returns:
        La valeur H*(mot) comprise entre 0 et 255
    """
    resultat = 0
    for caractere in mot:
        # Récupération du hash binaire du caractère
        hash_binaire = hachage_caractere_v2(caractere)
        # Conversion en entier et XOR avec le résultat précédent
        resultat ^= int(hash_binaire, 2)
    return resultat


def afficher_statistiques_alphabet():
    """
    Affiche des statistiques sur l'alphabet utilisé pour le hachage.
    Utile pour comprendre la distribution des caractères.
    """
    print(f"Alphabet utilisé: '{ALPHABET}'")
    print(f"Nombre de caractères dans l'alphabet: {len(ALPHABET)}")
    print(f"Plage des valeurs de hachage possibles: 0 à 255")
    print()

def generer_variantes_mot(mot: str) -> List[str]:
    """
    Génère différentes variantes d'un mot pour tester les collisions.
    
    Les variantes incluent:
    - Le mot original
    - Le mot en minuscules
    - Le mot en majuscules  
    - Le mot avec première lettre majuscule et le reste en minuscules
    
    Args:
        mot: Le mot d'origine
        
    Returns:
        Liste des variantes sans doublons
    """
    variantes_possibles = [
        mot,                                    # mot original
        mot.lower(),                           # tout en minuscules
        mot.upper(),                           # tout en majuscules
    ]
    
    # Ajout de la variante "titre" si le mot n'est pas vide
    if len(mot) > 0:
        variantes_possibles.append(mot[0].upper() + mot[1:].lower())
    
    # Suppression des doublons tout en préservant l'ordre
    variantes_uniques = []
    mots_deja_vus = set()
    
    for variante in variantes_possibles:
        if variante not in mots_deja_vus:
            mots_deja_vus.add(variante)
            variantes_uniques.append(variante)
            
    return variantes_uniques

def analyser_dictionnaire(chemin_fichier: str, fichier_sortie: str) -> Dict[int, List[Tuple[str, str]]]:
    """
    Analyse un dictionnaire de mots pour trouver des collisions avec la fonction H*.
    
    Pour chaque mot du dictionnaire, on génère ses variantes (majuscules, minuscules, etc.)
    et on calcule H* pour chacune. Les mots ayant la même valeur H* constituent une collision.
    
    Args:
        chemin_fichier: Chemin vers le fichier dictionnaire
        fichier_sortie: Chemin où écrire les résultats
        
    Returns:
        Dictionnaire des collisions (clé = valeur H*, valeur = liste des couples (mot_original, variante))
        
    Raises:
        FileNotFoundError: Si le fichier dictionnaire n'existe pas
    """
    # Vérification de l'existence du fichier
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Le fichier dictionnaire '{chemin_fichier}' n'a pas été trouvé")

    # Dictionnaire pour regrouper les mots par valeur de hash
    groupes_hash = defaultdict(list)
    
    # Lecture des mots du dictionnaire
    mots_dictionnaire = []
    with open(chemin_fichier, "r", encoding="utf-8") as fichier:
        for ligne in fichier:
            mot = ligne.strip()
            if mot:  # Ignorer les lignes vides
                mots_dictionnaire.append(mot)

    # Calcul des hash pour chaque variante de chaque mot
    total_variantes = 0
    for mot_original in mots_dictionnaire:
        for variante in generer_variantes_mot(mot_original):
            valeur_hash = calculer_h_etoile(variante)
            groupes_hash[valeur_hash].append((mot_original, variante))
            total_variantes += 1

    # Conservation uniquement des groupes avec collisions (2+ éléments)
    collisions_trouvees = {
        hash_val: liste_mots 
        for hash_val, liste_mots in groupes_hash.items() 
        if len(liste_mots) > 1
    }

    # Écriture des résultats dans le fichier de sortie
    with open(fichier_sortie, "w", encoding="utf-8") as sortie:
        sortie.write(f"=== Analyse du dictionnaire ===\n")
        sortie.write(f"Fichier analysé: {chemin_fichier}\n")
        sortie.write(f"Nombre de mots dans le dictionnaire: {len(mots_dictionnaire)}\n")
        sortie.write(f"Nombre total de variantes testées: {total_variantes}\n")
        sortie.write(f"Nombre de valeurs H* avec collisions: {len(collisions_trouvees)}\n\n")
        
        # Détail de chaque collision
        for hash_val in sorted(collisions_trouvees.keys()):
            liste_mots = collisions_trouvees[hash_val]
            sortie.write(f"H* = {hash_val} (0x{hash_val:02x}) -> {len(liste_mots)} collisions\n")
            for mot_original, variante in liste_mots:
                sortie.write(f"  '{mot_original}' (variante: '{variante}')\n")
            sortie.write("\n")
    
    return collisions_trouvees

def main():
    """
    Fonction principale du programme.
    
    Analyse le dictionnaire ODS5 pour trouver des collisions avec la fonction H*
    et affiche un résumé des résultats.
    """
    # Configuration des chemins de fichiers
    CHEMIN_DICTIONNAIRE = "ods5.txt"  # Chemin vers le dictionnaire
    FICHIER_RESULTATS = "ods5_collisions.txt"  # Fichier de sortie

    print("=== Exercice 4 - Attaque par dictionnaire ===")
    print("Recherche de collisions avec la fonction de hachage H*")
    print()
    
    # Affichage des informations sur l'alphabet
    afficher_statistiques_alphabet()
    
    print(f"Analyse du dictionnaire: {CHEMIN_DICTIONNAIRE}")
    
    try:
        # Analyse du dictionnaire
        collisions_detectees = analyser_dictionnaire(CHEMIN_DICTIONNAIRE, FICHIER_RESULTATS)

        # Affichage du résumé
        print("\n--- Résumé des résultats ---")
        print(f"Nombre de valeurs H* avec collisions: {len(collisions_detectees)}")
        
        if len(collisions_detectees) == 0:
            print("Aucune collision détectée dans ce dictionnaire.")
            return
        
        # Calcul de statistiques
        total_collisions = sum(len(mots) for mots in collisions_detectees.values())
        print(f"Nombre total de mots impliqués dans des collisions: {total_collisions}")
        
        # Affichage de quelques exemples
        print("\nExemples de collisions trouvées:")
        exemples_affiches = 0
        nombre_max_exemples = 8
        
        for hash_val in sorted(collisions_detectees.keys()):
            if exemples_affiches >= nombre_max_exemples:
                break
                
            liste_mots = collisions_detectees[hash_val]
            print(f"  H* = {hash_val} (0x{hash_val:02x}) -> {len(liste_mots)} mots en collision")
            
            # Afficher les premiers exemples de cette collision
            mots_exemple = liste_mots[:3]  # Afficher au maximum 3 exemples
            for mot_original, variante in mots_exemple:
                print(f"    • '{mot_original}' -> '{variante}'")
            
            if len(liste_mots) > 3:
                print(f"    ... et {len(liste_mots) - 3} autres")
            
            exemples_affiches += 1

        if len(collisions_detectees) > nombre_max_exemples:
            print(f"    ... et {len(collisions_detectees) - nombre_max_exemples} autres groupes de collisions")

        print(f"\nRésultats détaillés sauvegardés dans: {FICHIER_RESULTATS}")
        
    except FileNotFoundError as e:
        print(f"Erreur: {e}")
        print("Assurez-vous que le fichier dictionnaire existe dans le répertoire courant.")
        print("Vous pouvez télécharger le dictionnaire ODS5 depuis le site officiel.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")
        print("Vérifiez que le fichier dictionnaire est au bon format (un mot par ligne).")


if __name__ == "__main__":
    main()
