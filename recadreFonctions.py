import numpy as np

## Decoupe haut
def getHaut(matrice): # ligne du haut a supprimer
    [n,p]=matrice.shape
    lignesDelete=0
    for i in range(n):
        compteur=0
        for j in range(p):
            if matrice[i,j]==0:
                compteur+=1
        if compteur>p/4 :
            lignesDelete+=1
        else :
            break
    return lignesDelete+5

def decoupHaut(matrice): # enleve les lignes du haut (laisse 2 lignes)
    [n,p]=matrice.shape
    i=0
    nbrLignesAsup=getHaut(matrice)
    matriceDecoupe=np.zeros(((n-nbrLignesAsup),p))+1
    [l,c]=matriceDecoupe.shape
    for i in range(n):
        for j in range(p):
            if i>=nbrLignesAsup:
                matriceDecoupe[i-nbrLignesAsup,j]=matrice[i,j]
    return matriceDecoupe


## Decoupe bas
def getBas(matrice): # ligne du haut a supprimer
    [n,p]=matrice.shape
    lignesDelete=0
    for i in range(n):
        compteur=0
        delete=False
        for j in range(p):
            if matrice[n-1-i,p-1-j]==0:
                compteur+=1
        if compteur>0.35*p :
            lignesDelete+=1
    return lignesDelete

def decoupBas(matrice): # enleve les lignes du bas(laisse 2 lignes)
    [n,p]=matrice.shape
    i=0
    nbrLignesAsup=getBas(matrice)
    matriceDecoupe=np.zeros(((n-nbrLignesAsup),p))+1
    [l,c]=matriceDecoupe.shape
    for i in range(l):
        for j in range(c):
            matriceDecoupe[i,j]=matrice[i,j]
    return matriceDecoupe


## Decoupe gauche
def getGauche(matrice):
    [n,p]=matrice.shape
    colDelete=0
    for j in range(p):
        compteur=0
        for i in range(n):
            if matrice[i,j]==0:
                compteur+=1
        if compteur>10 :
            colDelete+=1
        else :
            break
    return colDelete+3

def decoupGauche(matrice): # enleve les lignes de gauche
    [n,p]=matrice.shape
    i=0
    nbrColAsup=getGauche(matrice)
    matriceDecoupe=np.zeros((n,(p-nbrColAsup)))+1
    [l,c]=matriceDecoupe.shape
    for j in range(p):
        for i in range(n):
            if j>=nbrColAsup:
                matriceDecoupe[i,j-nbrColAsup]=matrice[i,j]
            else :
                matriceDecoupe[i,j]=1
        j+=1
    return matriceDecoupe

## Decoupe droite
def getDroite(matrice):
    [n,p]=matrice.shape
    colDelete=0
    for j in range(p):
        compteur=0
        for i in range(n):
            if matrice[i,p-j-1]==0:
                compteur+=1
        if compteur>n/10 :
            colDelete+=1
        if compteur>0.3*n :
            break
    return colDelete+2

def decoupDroite(matrice): # enleve les lignes de droite
    [n,p]=matrice.shape
    i=0
    nbrColAsup=getDroite(matrice)
    matriceDecoupe=np.zeros(((n,(p-nbrColAsup))))+1
    [l,c]=matriceDecoupe.shape
    for j in range(p-nbrColAsup):
        for i in range(n):
            if j<c:
                matriceDecoupe[i,j]=matrice[i,j]
        j+=1
    return matriceDecoupe

