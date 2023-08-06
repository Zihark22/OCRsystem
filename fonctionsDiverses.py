from PIL.Image import *
try:
    from PIL import Image
except ImportError:
    import Image

from os.path import splitext, dirname, basename, join
import recadreFonctions as recadre
import recentreFonctions as recentre
import cv2
import numpy as np
from easyocr import Reader
import pytesseract

from PIL.PngImagePlugin import PngInfo
from datetime import datetime, timezone
import rfc3339

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.1.0/bin/tesseract'

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" # pas avoir erreur conflit librairies avec EasyOCR

## Métadonnées
# cette fonction écrit l'heure courante dans les metadonnées de l'image
def writeHeure(path):
    targetImage = Image.open(path)
    metadata = PngInfo()
    metadata.add_text('ha', getheure())
    targetImage.save(path, pnginfo=metadata) #sauvegarde des modifications

def getheure():
    n = datetime.now(timezone.utc).astimezone()
    n.isoformat('T')
    return rfc3339.rfc3339(n)

def writeMeta(path, ma_string):
    targetImage = Image.open(path)
    metadata = PngInfo()
    metadata.add_text('ha', ma_string)
    targetImage.save(path, pnginfo=metadata) # sauvegarde des modifications

def readHeure(path):
    targetImage = Image.open(path)
    return targetImage.text


## Decoupage de la video en frames
def save_frames(video_path: str, frame_dir: str,tpsEntreFrames: float, ext=str, name=""):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    #v_name = splitext(basename(video_path))[0]
    v_name = "decoupes"   # nom du dossier regroupant les frames
    if frame_dir[-1:] == "\\" or frame_dir[-1:] == "/":
        frame_dir = dirname(frame_dir)
    frame_dir_ = join(frame_dir, v_name)

    makedirs(frame_dir_, exist_ok=True)
    base_path = join(frame_dir_, name)
    idx = 0
    while cap.isOpened():
        idx += 1 # decalage au debut
        ret, frame = cap.read()
        if ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == 1:  #Enregistrer 0 seconde image
                cv2.imwrite("{}{}.{}".format(base_path, "00", ext),frame)
            elif idx < tpsEntreFrames*cap.get(cv2.CAP_PROP_FPS):
                continue
            else:  #Enregistrer l'image d'une seconde
                second = int(cap.get(cv2.CAP_PROP_POS_FRAMES)/idx)
                filled_second = str(second).zfill(2)
                cv2.imwrite("{}{}.{}".format(base_path, filled_second, ext),frame)
                idx = 0
        else:
            break
    return frame_dir_


## Binarisation
def binarise(img, seuil, couleur):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,th=cv2.threshold(gray,seuil,couleur,cv2.THRESH_BINARY)

    [n,p]=th.shape
    for i in range(n):
        for j in range(p):
            if th[i,j]>0:
                th[i,j]=1  # matrice complètement binaire 1(blanc) ou 0(noir)
            else :
                continue
    return th

## Retourne une image en 2 dimensions si l'image est en 3 dimensions
def matrix3Dto2D(img): # créer une matrice binaire à partir de l'image
    if(len(img.shape)>2):
        [n,p,k]=img.shape
        image2D=np.zeros((n,p))
        for i in range(n):
            for j in range(p):
                if img[i,j,0]: #si blanc
                    image2D[i,j]=0
                else:
                    image2D[i,j]=1
        return image2D
    else :
        return img

## Decoupage des frames
def reframe(img,x,y,h,w):
    x=int(x)
    y=int(y)
    h=int(h)-1
    w=int(w)-1
    crop_img=img[y:y+h, x:x+w]
    return crop_img


## Centrage sur le texte
def recadreETrecentre(Matrice):
    [n,p]=Matrice.shape

    matriceHaut=recadre.decoupHaut(Matrice)
    matriceBas=recadre.decoupBas(matriceHaut)
    matriceGauche=recadre.decoupGauche(matriceBas)
    matriceDroite=recadre.decoupDroite(matriceGauche)

    seuilNoTxt=0.05 # 5 % de noir = texte
    Matrice2=matriceDroite
    if getPourcentage(Matrice2)>seuilNoTxt :
        Matrice2=recentre.decoupGauche(Matrice2)    # Centrage sur le texte à gauche
    return Matrice2

## Pourcentage d'écriture
def getPourcentage(matrice):
    [n,p]=matrice.shape
    pixB=0
    pixN=0
    for i in range(n) :
        for j in range(p):
            if matrice[i,j]==0:
                pixN+=1
            else :
                pixB+=1
    pourcentage=pixN/(pixN+pixB)
    return pourcentage


## Matrice enregistrée en image
def MatriceToImage(matrice,chemin,nom,extension):
    [lignes,cols]=matrice.shape[:2]

    image = new('RGB', (cols,lignes))

    for i in range(cols) :
        for j in range(lignes):
            if matrice[j,i]==0:
                image.putpixel((i,j),(0,0,0))
            else :
                image.putpixel((i,j),(255,255,255))

    image.save(chemin+nom+"."+extension,"PNG")

## Agranissement de l'image pour la lecture PyTesseract

def Agrandissement(img):
    [n,p]=img.shape[:2]
    img=matrix3Dto2D(img)
    new_img=np.zeros((n*3,round(p+200)))
    new_img=new_img+255
    new_img[n:2*n,5:p+5]=img[:,:]
    return new_img

## Récupération des blocs d'un champ
def decoupeBande(img):
    img=Agrandissement(img)
    if(len(img.shape)>2):
        img=img[:,:,0]
    M = []
    n,p=img.shape[:2]
    # bascule = 0
    cpt2 = 0 #compteur pour les colones
    rtn = 0 #mémoire n° colone pour découper
    for k in range (p): #boucle sur les colonnes
        for i in range (n): #boucle sur les lignes
            if (img[i,k]==255 ): #on test que le pixel est blanc
                if (i==n-1): #on test une colone
                    if (cpt2 == 100): #on test les 100 colones blanches
                        M.append(img[:,rtn:k])
                        # bascule=1
                        rtn = k
                        cpt2=0
                    else:
                        cpt2 = cpt2+1
            elif(img[i,k]==0):
                cpt2 = 0
                # bascule=0
                break
    M.append(img[:,rtn:])
    return M

## Retourne les chaînes de caractères d'un champ en fonction des blocs du frame
def retour_fct(img):
    M=decoupeBande(img)
    N=[]
    cpt = 0
    for k in M:
        MatriceToImage(k,"","Img_Temp","png") # image temporaire
        reader = Reader(['fr'], gpu=False)
        if (cpt==1):
            try:
                string=pytesseract.image_to_string(Image.open("Img_Temp","png"))
                string=string[:len(string)-1]  # enleve le caractere \n de retour a la ligne ajouter automatiquement par pytesseract
                N.append(string)
                cpt = cpt+1
            except:
                try :
                    string=reader.readtext("Img_Temp.png",detail=0)
                    if(len(string)==0):
                        if(cpt>3):
                            break
                        else:
                            string=" "
                    else :
                        string=string[0]  # ne prendre que le string et pas la liste
                    N.append(string)
                    cpt = cpt+1
                except:
                    print("Erreur PyTesseract puis EasyOCR")
        else:
            try :
                string=reader.readtext("Img_Temp.png",detail=0)
                if(len(string)==0):
                    if(cpt>3):
                        break
                    else:
                        string=" "
                else :
                    string=string[0]  # ne prendre que le string et pas la liste
                N.append(string)
                cpt = cpt+1
            except:
                try:
                    string=pytesseract.image_to_string(Image.open("Img_Temp","png"))
                    string=string[:len(string)-1]  # enleve le caractere \n de retour a la ligne ajouter automatiquement par pytesseract
                    N.append(string)
                    cpt = cpt+1
                except :
                    print("Erreur EasyOCR puis Tesseract")
    try:
        os.remove("Img_Temp.png")
    except:
        print("Erreur suppression bloc")

    while(len(N)>3):
        N[2]=N[2]+" "+N[3]
        N.pop(3)
    if(len(N)<=2):
        N.insert(0," ")
    return N

