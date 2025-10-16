import hashlib
import os

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
    mdp = input("Entrez votre mot de passe : ")
    tag = input("Entrez votre tag : ")
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
    mdp = input("Entrez votre mot de passe : ")
    tag = input("Entrez votre tag : ")
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
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mpwd_path = os.path.join(script_dir, "mpwd.txt")
    with open(mpwd_path, "r") as f:
        mdp = f.read().strip()
    while N<1 or N>12:
        N = int(input("Entrez la taille souhaitée pour le mot de passe (entre 1 et 12 compris) : "))
    tag = input("Entrez votre tag : ")
    concatMdp = mdp + tag
    hashedMdp = hash_and_truncate(concatMdp, N)
    print("Le mot de passe haché et tronqué avec sha256 est :", hashedMdp)


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
                pass
            case 5:
                pass
            case 6:
                print("Au revoir !")
            case _:
                print("Choix invalide, veuillez réessayer.")
    