def hachage_caractere(caractere : str) -> int :
    """fonction qui retourne le code binaire sur un octet 
    équivalent au nombre de l'encodage utf 8 d'un caractère"""
    nb_caractere : int
    binaire : int
    nb_caractere = ord(caractere)
    binaire = format(nb_caractere, '08b')
    return binaire

def hachage_caractere_v2(caractere : str) -> int :
    """fonction qui retourne le code binaire sur un octet 
    équivalent au nombre de l'encodage utf 8 d'un caractère 
    qui n'utilise pas les fonctions prédéfinies"""

    nb_caractere : int
    binaire : str
    i : int
    nb_caractere = ord(caractere)
    binaire = ""
    for i in range(8):
        if nb_caractere % 2 == 0:
            binaire = "0" + binaire
        else:
            binaire = "1" + binaire
        nb_caractere = nb_caractere // 2
    return binaire

if __name__ == "__main__":
    caractere : str 
    resultat : int
    resultat2 : int
    caractere=""

    while len(caractere) != 1 :
        caractere = input("Entrez un caractere : ")
        while ord(caractere)<20 or ord(caractere)>80 :
            caractere = input("Entrez un caractere :")
    resultat = hachage_caractere(caractere)
    resultat2 = hachage_caractere_v2(caractere)
    print("Le code binaire du caractere ", caractere, " est : ", resultat, " et ", resultat2)
    
