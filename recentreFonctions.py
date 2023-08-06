import numpy as np

marge = 4 # contour blanc de 4 pixels

## Decoupe bas
def getBas(matrice): # ligne du bas a supprimer
    [n,p]=matrice.shape
    lignesDelete=0
    for i in range(n):
        compteur=0
        for j in range(p):
            if matrice[n-i-1,j]!=0:
                compteur+=1
        if compteur>p-50 :
            lignesDelete+=1
        else :
            break
    if(lignesDelete>marge):
        lignesDelete-=marge # pour avoir de la marge
    # print("Nombre de lignes à supprimer en bas :",lignesDelete)
    return lignesDelete

def decoupeBas(matrice): # enleve les lignes du bas (laisse 5 lignes)
    [n,p]=matrice.shape
    i=0
    nbrLignesAsup=getBas(matrice)
    matriceDecoupe=np.zeros(((n-nbrLignesAsup),p))+1
    [l,c]=matriceDecoupe.shape
    while i<n-nbrLignesAsup:
        for j in range(p):
            matriceDecoupe[i,j]=matrice[i,j]
        i+=1
    return matriceDecoupe

## Decoupe haut
def getHaut(matrice): # ligne du haut a supprimer
    [n,p]=matrice.shape
    lignesDelete=0
    for i in range(n):
        compteur=0
        for j in range(p):
            if matrice[i,j]!=0:
                compteur+=1
        if compteur>p-50 :
            lignesDelete+=1
        else :
            break
    if(lignesDelete>marge):
        lignesDelete-=marge # pour avoir de la marge
    # print("Nombre de lignes à supprimer en haut :",lignesDelete,".\n")
    return lignesDelete

def decoupHaut(matrice): # enleve les lignes du haut (laisse 2 lignes)
    [n,p]=matrice.shape
    i=0
    nbrLignesAsup=getHaut(matrice)
    matriceDecoupe=np.zeros(((n-nbrLignesAsup),p))
    [l,c]=matriceDecoupe.shape
    for i in range(n-nbrLignesAsup):
        for j in range(p):
            if i>=nbrLignesAsup:
                matriceDecoupe[i-nbrLignesAsup,j]=matrice[i,j]
        i+=1
    return matriceDecoupe

## Decoupe gauche
def getGauche(matrice):
    [n,p]=matrice.shape
    colDelete=0
    for j in range(p):
        compteur=0
        for i in range(n):
            if matrice[i,j]!=0:
                compteur+=1
        if compteur>n-10 :
            colDelete+=1
        else :
            break
    if colDelete > marge :
        colDelete-= marge
    return colDelete

def decoupGauche(matrice): # enleve les lignes du haut (laisse 2 lignes)
    [n,p]=matrice.shape
    i=0
    nbrColAsup=getGauche(matrice)
    matriceDecoupe=np.zeros((n,(p-nbrColAsup)))
    [l,c]=matriceDecoupe.shape
    for j in range(p):
        for i in range(n):
            if j>nbrColAsup:
                matriceDecoupe[i,j-nbrColAsup]=matrice[i,j]
        j+=1
    return matriceDecoupe

## Decoupe droite
def getDroite(matrice):
    [n,p]=matrice.shape
    colDelete=0
    for j in range(p):
        compteur=0
        for i in range(n):
            if matrice[i,p-j-1]!=0:
                compteur+=1
        if compteur>n-10:
            colDelete+=1
        else :
            break
    if colDelete > marge :
        colDelete-= marge
    return colDelete

def decoupDroite(matrice): # enleve les lignes du haut (laisse 2 lignes)
    [n,p]=matrice.shape
    i=0
    nbrColAsup=getDroite(matrice)
    matriceDecoupe=np.zeros((n,(p-nbrColAsup)))
    [l,c]=matriceDecoupe.shape
    for j in range(p-nbrColAsup):
        for i in range(n):
            if j<c:
                matriceDecoupe[i,j]=matrice[i,j]
        j+=1
    return matriceDecoupe


