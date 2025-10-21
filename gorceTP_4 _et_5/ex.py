import hashlib
import os
import itertools
import argon2

ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "ÀÂÄÇÉÈÊËÎÏÔÖÙÛÜàâäçéèêëîïôöùûü"
    "0123456789"
    ".,;:!?()[]{}+-*/=<>_\"'&%$#@^~|\\"
)

def is_valid_string(s: str) -> bool:
    """Vérifie que tous les caractères de la chaîne sont dans l'alphabet autorisé"""
    return all(char in ALPHABET for char in s)

def get_valid_input(prompt: str) -> str:
    """Demande à l'utilisateur une entrée et valide qu'elle contient uniquement des caractères autorisés"""
    while True:
        user_input = input(prompt)
        if is_valid_string(user_input):
            return user_input
        else:
            print("Erreur : La chaîne contient des caractères non autorisés. Veuillez réessayer.")
            print(f"Caractères autorisés : lettres, chiffres, accents, espaces et ponctuation de base.")

def hash_and_truncate(input : str, length : int) ->str :
    """hash the input string with sha256 and return the first x characters of the hexadecimal representation"""
    sha256_hash : str
    shortened_hash : str
    sha256_hash = hashlib.sha256(input.encode()).hexdigest()
    shortened_hash = sha256_hash[:length]
    return shortened_hash

def hash_and_truncate_v2(input : str, length :int ) ->str :
    """hash the input string with sha1 and return the first x characters of the hexadecimal representation"""
    sha1_hash : str
    shortened_hash : str
    sha1_hash = hashlib.sha1(input.encode()).hexdigest()
    shortened_hash = sha1_hash[:length]
    return shortened_hash

def ex1():
    """Exercice 1 : Des mots de passe tout simples  
    1 Demander à l'utilisateur de saisir un mot de passe et un tag
    2 hasher le mot de passe concaténé avec le tag avec sha"""
    mdp : str
    tag : str
    concatMdp :str
    hashedMdp : str
    hashedMdp_v2 : str
    wished_length : int
    wished_length = 8
    mdp = get_valid_input("Entrez votre mot de passe : ")
    tag = get_valid_input("Entrez votre tag : ")
    concatMdp = mdp + tag
    hashedMdp = hash_and_truncate(concatMdp, wished_length)
    hashedMdp_v2 = hash_and_truncate_v2(concatMdp, wished_length)
    print("Le mot de passe haché et tronqué avec sha1 est :", hashedMdp_v2)
    print("Le mot de passe haché et tronqué avec sha256 est :", hashedMdp)

def ex2():
    """Exercice 2 : Des mots de passe d'une taille demandée
    1 Demander à l'utilisateur de saisir un mot de passe et un tag
    2 Demander à l'utilisateur de saisir la taille du mot de passe haché
    3 hasher le mot de passe concaténé avec le tag avec sha"""
    N : int
    N = 0
    mdp : str
    tag : str
    concatMdp :str
    hashedMdp : str
    while N<1 or N>12:
        N = int(input("Entrez la taille souhaitée pour le mot de passe (entre 1 et 12 compris) : "))
    mdp = get_valid_input("Entrez votre mot de passe : ")
    tag = get_valid_input("Entrez votre tag : ")
    concatMdp = mdp + tag
    hashedMdp = hash_and_truncate(concatMdp, N)
    print("Le mot de passe haché et tronqué avec sha256 est :", hashedMdp)

def ex3():
    """Exercice 3 : Mot de passe maître
    1 va cherhcer le mot de passe maître dans le fichier mpwd.txt
    2 Demande à l'utilisateur de saisir la taille du mot de passe haché
    3 Demander à l'utilisateur de saisir un tag
    4 hasher le mot de passe concaténé avec le tag avec sha"""
    N : int
    N = 0
    mdp : str
    tag : str
    concatMdp :str
    hashedMdp : str
    choice : int 
    choice = 0
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mpwd_path = os.path.join(script_dir, "mpwd.txt")
    with open(mpwd_path, "r") as f:
        mdp = f.read().strip()
    if mdp == "" or not is_valid_string(mdp):
        mdp = get_valid_input("Le mot de passe maître est vide ou invalide. Veuillez entrer un mot de passe maître valide : ")
    else:
        while (choice != 1 and choice != 2):
            choice = int(input("Souhaitez vous garder le mot de passe maitre du fichier ou utiliser le votre:\n1-le mot de passe prévu\n2-Le votre\nVotre choix : "))
        if choice == 2:
            mdp = get_valid_input("Choisissez votre mot de passe maitre : ")

    while N<1 or N>12:
        N = int(input("Entrez la taille souhaitée pour le mot de passe (entre 1 et 12 compris) : "))
    tag = get_valid_input("Entrez votre tag : ")
    concatMdp = mdp + tag
    hashedMdp = hash_and_truncate(concatMdp, N)
    print("Le mot de passe haché et tronqué avec sha256 est :", hashedMdp)

def ex4():
    """Exercice 4 : Attaque sur des mots de passe
    Dans cet exercice vous allez tenter de trouver des préimages possibles pour le mot de passe maitre, c'est à dire, vous allez tenter de casser la sécurité de votre générateur de mots de passe.
    
    Votre tache sera de trouver un mot de passe valide en connaissant le tag utilisé mais pas le mot de passe maitre
    
    Assurez vous premièrement que votre fichier de mots de passe maitre contient un mot de passe maitre de 1à caractères (àvous de les choisir). Dans votre rapport discutez quelle est la probabilité qu'un attaquant retrouve ce mot de passe maitre par force brute.
    
    Générez, en utilisant votre générateur de mots de passe et le mot de passe maitre, des mots de passe d'un caractere(N=1) pour les tags suivants : Unilim, Amazon, Netflix
    
    Dans un premier temps votre attaque devra trouver un mot de passe maitre qui donnera le même mot de passe que celui produit par votre vrai mot de pass sur le tag Unilim
    
    La stratégie sera celle d'une attaque par dictionnaire. Votre dictionnaire doit contenir tous les mots de passe possibles sur 10 caractères, chaque caractère provenant de votre dictionnaire, jusqu'à trouver un mot de passe identique(pour le tag unilim) à celui produit par le gestionnaire de mots de passe. Combien de possibilités avez vous essayées? Quelle est la probabilité théorique de trouver un mot de passe maitre qui provoque une collision et comment votre nombre d'essais se compare à cette valeur ?
    
    Dans un deuxième temps, votre attaque devra retrouver un mot de passe maitre qui provoque une collision sur les 3 tags : Unilim, Amazon et Netflix. Comparez le nombre d'essais nécessaire pour votre attaque dans ce cas par rapport au cas précédent.
    
    Finalement essayez la même attaque pour N=2 et N=3 en enregistrant le nombre d'esssais"""
    
    
    
    # Lire le mot de passe maître réel
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mpwd_path = os.path.join(script_dir, "mpwd.txt")
    with open(mpwd_path, "r") as f:
        real_master_pwd = f.read().strip()
    
    # Lire le dictionnaire depuis un fichier
    dict_path = os.path.join(script_dir, "dictionary.txt")
    try:
        with open(dict_path, "r", encoding="utf-8") as f:
            dictionary = f.read().strip()
    except FileNotFoundError:
        print(f"Erreur : Le fichier 'dictionary.txt' n'a pas été trouvé.")
        print("Création d'un dictionnaire par défaut...")
        dictionary = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        # Créer le fichier dictionary.txt
        with open(dict_path, "w", encoding="utf-8") as f:
            f.write(dictionary)
        print(f"Fichier 'dictionary.txt' créé avec {len(dictionary)} caractères.")
    
    print("\n=== EXERCICE 4 : ATTAQUE PAR DICTIONNAIRE ===\n")
    print(f"Taille de l'alphabet du dictionnaire : {len(dictionary)} caractères")
    print(f"Longueur du mot de passe maître réel : {len(real_master_pwd)} caractères")
    
    # Générer les mots de passe cibles avec le vrai mot de passe maître
    tags = ["Unilim", "Amazon", "Netflix"]
    
    choice = 0
    while choice != 5:
        # Menu de choix pour l'attaque
        print("\n" + "="*60)
        print("Choisissez le type d'attaque :")
        print("1. Attaque sur un seul tag (Unilim) avec N=1")
        print("2. Attaque sur trois tags (Unilim, Amazon, Netflix) avec N=1")
        print("3. Attaque sur un tag avec N=2")
        print("4. Attaque sur un tag avec N=3")
        print("5. Retour au menu principal")
        print("="*60)
        
        choice = int(input("\nVotre choix : "))
        
        if choice == 1:
            # Attaque sur un seul tag
            N = 1
            target_tag = "Unilim"
            target_hash = hash_and_truncate(real_master_pwd + target_tag, N)
            
            print(f"\nHash cible pour '{target_tag}' avec N={N} : {target_hash}")
            print(f"\nRecherche d'une collision sur {N} caractère(s)...")
            print(f"Probabilité théorique de collision : 1/{16**N} = 1/{16**N}")
            
            attempts = 0
            found = False
            
            # Générer tous les mots de passe possibles de 10 caractères
            for candidate in itertools.product(dictionary, repeat=10):
                candidate_pwd = ''.join(candidate)
                candidate_hash = hash_and_truncate(candidate_pwd + target_tag, N)
                attempts += 1
                
                if candidate_hash == target_hash:
                    print(f"\n✓ COLLISION TROUVÉE !")
                    print(f"Mot de passe candidat : {candidate_pwd}")
                    print(f"Nombre d'essais : {attempts}")
                    print(f"Hash produit : {candidate_hash}")
                    found = True
                    break
                
                if attempts % 100000 == 0:
                    print(f"Essais : {attempts}...", end='\r')
            
            if not found:
                print(f"\nAucune collision trouvée après {attempts} essais.")
        
        elif choice == 2:
            # Attaque sur trois tags
            N = 1
            target_hashes = {tag: hash_and_truncate(real_master_pwd + tag, N) for tag in tags}
            
            print(f"\nHashes cibles avec N={N} :")
            for tag, h in target_hashes.items():
                print(f"  {tag}: {h}")
            
            print(f"\nRecherche d'une collision sur les 3 tags...")
            print(f"Probabilité théorique : 1/{16**(N*3)} = 1/{16**(N*3)}")
            
            attempts = 0
            found = False
            
            for candidate in itertools.product(dictionary, repeat=10):
                candidate_pwd = ''.join(candidate)
                attempts += 1
                
                # Vérifier si le candidat produit les mêmes hash pour tous les tags
                match = True
                for tag in tags:
                    if hash_and_truncate(candidate_pwd + tag, N) != target_hashes[tag]:
                        match = False
                        break
                
                if match:
                    print(f"\n✓ COLLISION TROUVÉE SUR LES 3 TAGS !")
                    print(f"Mot de passe candidat : {candidate_pwd}")
                    print(f"Nombre d'essais : {attempts}")
                    found = True
                    break
                
                if attempts % 100000 == 0:
                    print(f"Essais : {attempts}...", end='\r')
            
            if not found:
                print(f"\nAucune collision trouvée après {attempts} essais.")
        
        elif choice == 3:
            # Attaque avec N=2
            N = 2
            target_tag = "Unilim"
            target_hash = hash_and_truncate(real_master_pwd + target_tag, N)
            
            print(f"\nHash cible pour '{target_tag}' avec N={N} : {target_hash}")
            print(f"\nRecherche d'une collision sur {N} caractères...")
            print(f"Probabilité théorique de collision : 1/{16**N} = 1/{16**N}")
            
            attempts = 0
            found = False
            
            for candidate in itertools.product(dictionary, repeat=10):
                candidate_pwd = ''.join(candidate)
                candidate_hash = hash_and_truncate(candidate_pwd + target_tag, N)
                attempts += 1
                
                if candidate_hash == target_hash:
                    print(f"\n✓ COLLISION TROUVÉE !")
                    print(f"Mot de passe candidat : {candidate_pwd}")
                    print(f"Nombre d'essais : {attempts}")
                    print(f"Hash produit : {candidate_hash}")
                    found = True
                    break
                
                if attempts % 100000 == 0:
                    print(f"Essais : {attempts}...", end='\r')
            
            if not found:
                print(f"\nAucune collision trouvée après {attempts} essais.")
        
        elif choice == 4:
            # Attaque avec N=3
            N = 3
            target_tag = "Unilim"
            target_hash = hash_and_truncate(real_master_pwd + target_tag, N)
            
            print(f"\nHash cible pour '{target_tag}' avec N={N} : {target_hash}")
            print(f"\nRecherche d'une collision sur {N} caractères...")
            print(f"Probabilité théorique de collision : 1/{16**N} = 1/{16**N}")
            
            attempts = 0
            found = False
            
            for candidate in itertools.product(dictionary, repeat=10):
                candidate_pwd = ''.join(candidate)
                candidate_hash = hash_and_truncate(candidate_pwd + target_tag, N)
                attempts += 1
                
                if candidate_hash == target_hash:
                    print(f"\n✓ COLLISION TROUVÉE !")
                    print(f"Mot de passe candidat : {candidate_pwd}")
                    print(f"Nombre d'essais : {attempts}")
                    print(f"Hash produit : {candidate_hash}")
                    found = True
                    break
                
                if attempts % 100000 == 0:
                    print(f"Essais : {attempts}...", end='\r')
            
            if not found:
                print(f"\nAucune collision trouvée après {attempts} essais.")
        
        elif choice == 5:
            print("\nRetour au menu principal...")
        
        else:
            print("Choix invalide.")

def menu():
    print("\n-----------------------------------------------------------------------------------------")
    print("Bienvenue dans le programme de hachage de mot de passe\nVoici les exercices disponibles :")
    print("1. Des mots de passe tout simples")
    print("2. Des mots de passe d'une taille demandée")
    print("3. Mot de passe maître")
    print("4. Attaque sur des mots de passe")
    print("5. Sécuriser le mot de passe maître")
    print("6. Quitter")


if __name__ == "__main__":
    nb : int
    nb = 0
    while nb != 6:
        menu()
        nb = int(input("Entrez le numéro de l'exercice que vous voulez exécuter : "))
        match nb:
            case 1:
                ex1()
            case 2:
                ex2()
            case 3:
                ex3()
            case 4:
                ex4()
            case 5:
                pass
            case 6:
                print("Au revoir !")
            case _:
                print("Choix invalide, veuillez réessayer.")
    