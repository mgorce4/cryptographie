from exercice1 import hachage_caractere_v2, ALPHABET 


def XOR_string(s1 : str) -> str:
    """fonction qui transforme chaque caractere d'une string 
    en binaire puis fait un XOR entre chaque caractere"""

    resultat : str
    i : int
    resultat = ""
    for i in range(len(s1)):
        caractere : str
        caractere = s1[i]
        binaire : str
        binaire = hachage_caractere_v2(caractere)
        if i == 0 :
            resultat = binaire
        else :
            j : int
            temp : str
            temp = ""
            for j in range(8):
                if resultat[j] == binaire[j] :
                    temp = temp + "0"
                else :
                    temp = temp + "1"
            resultat = temp
    return resultat
    

if __name__ == "__main__":
    phrase : str
    resultat : int

    phrase = input("Entrez une phrase : ")
    resultat = XOR_string(phrase)
    print("Le code binaire de la phrase ", phrase, " est : ", resultat)