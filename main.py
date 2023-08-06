from time import time

start_time = time()

from PIL.Image import *
try:
    from PIL import Image
except ImportError:
    import Image
import imageio
import cv2
from os.path import splitext, dirname, basename, join
import easyocr

import csvFunctions as fctCSV
import fonctionsDiverses as fctDIV
import supprimeFrameRedondante as supFRAM

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" # pas avoir erreur conflit librairies avec EasyOCR

chemin="/Users/badajozj/Desktop/PTransFinal/"  #  chemin du projet à modifier
dossier= "decoupes/"        # contiendra les frames de la video
extension="png"             # definition de l'extension pour les images enregistrees
nom_video="officiel.mp4"    # nom de la video a traite
tpsEntreFrames = 1.7        # temps entre 2 frames decoupes de la video en secondes

## Création des dossiers nécessaires
os.makedirs(dossier[:len(dossier)-1], exist_ok=True)

## Découpage de la video en frames sans tri des frames reondants
# fctDIV.save_frames(chemin+nom_video, chemin, tpsEntreFrames,extension)

## Suppression des frames redondants + découpage
# supFRAM.extractImages(chemin+nom_video,extension,dossier,tpsEntreFrames)

## Boucle sur tout les frames

# vidage du fichier de résultat
fctCSV.clear('log.csv')
frames = os.listdir(dossier)
frames.sort()
i=0
for image in frames:
    if image!=".DS_Store" and i==0:  # problème fichier caché sur Mac OS

        ## Lecture du frame
        decoupe_img = dossier + image
        img=cv2.imread(decoupe_img)
        cv2.imshow('PRET POUR LECTURE',img);
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        ## Binarisation
        seuil=130
        couleur=255
        imgBinaire=fctDIV.binarise(img,seuil,couleur)

        cv2.imshow('PRET POUR LECTURE',imgBinaire);
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        imgBinaire=fctDIV.matrix3Dto2D(imgBinaire) # si l'image est de dimension 3, elle est transformée en dimension 2
        [n,p]=imgBinaire.shape
        date = fctDIV.readHeure(decoupe_img)

        ## Decoupage des frames en 3 sous images (blocs)
        x=0
        y=0
        l=0.23*n # limite du premier champ en verticale

        imgHaut=fctDIV.reframe(imgBinaire,x,y,l,p)
        imgCentre=fctDIV.reframe(imgBinaire,x,l,l,p)
        imgBas=fctDIV.reframe(imgBinaire,x,n/2,n,p)

        cv2.imshow('PRET POUR LECTURE',imgHaut);
        cv2.waitKey(0)
        cv2.imshow('PRET POUR LECTURE',imgCentre);
        cv2.waitKey(0)
        cv2.imshow('PRET POUR LECTURE',imgBas);
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        ## Recadrage et Recentrage sur le texte + sauvegarde si nécessaire de l'image pour la lecture
        for i in range(3):
            if i==0:
                position = 'Haut'
                img = imgHaut
            elif i==1:
                position = 'Centre'
                img = imgCentre
            else:
                position = 'Bas'
                img = imgBas

            img = fctDIV.recadreETrecentre(img)

            cv2.imshow('PRET POUR LECTURE',img);
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            ## Lecture du texte de chaque champ
            try:
                result = fctDIV.retour_fct(img)
                print(result)
            except :
                print("Erreur lecture image : %s" % image.split(".")[0]+position)

            ## Ecriture dans le fichier csv
            try:
                fctCSV.print('log.csv', result, date['ha'])
            except:
                print("Erreur écriture fichier .CSV")

        ## Destruction du frame
        # os.remove(chemin+decoupe_img)
        i=i+1

## Suppresion des dossiers
# if os.path.exists(chemin+dossier):
#     try :
#         os.rmdir(chemin+dossier[:len(dossier)-1])
#     except :
#         print("Erreur suppression dossier decoupe")
# else :
#     print("Dossier decoupe inexistant")


## Traitement temps d'execution
tempsExec = time()-start_time

s=0
min=0
if tempsExec>=60 :
   min=tempsExec//60
   s=tempsExec%60
else :
    s=tempsExec

print(f"Execution en {tempsExec:.2f} secondes ({min:.0f} min {s:.2f} sec).")