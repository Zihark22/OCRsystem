import sys
import argparse
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

import fonctionsDiverses as foncDIV

#Mean Squared Error
def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

#extraction of non-similar frames
def extractImages(file,extension,dossier,tpsEntreFrames):
    count = 0 #index of the saved frame
    step = 0 #time step (to get frames from the video)
    vidcap = cv2.VideoCapture(file) #Open the video (it must be saved in the same root folder of the project)
    success,image = vidcap.read() #image= the current frame (numéro n)
    imageprev=image  #last frame captured (n-1)
    imageprev1=imageprev #the frame before the last one (n-2)
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(step*tpsEntreFrames*1000))    # read a frame every tpsEntreFrames secondes
        success,image = vidcap.read()

        heure = foncDIV.getheure()
        if (success==False):
            break
        #filtrage du frame pour amélioration de calcul

        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

        print ('Read a new frame: ', success)

        if (count==0):
            cv2.imwrite(dossier+"%d."% count+extension , image)     # save the very first frame
            foncDIV.writeMeta(dossier+"%d." % count+extension, heure)
            #ajout du temps en metadonnée

            ######## os.setxattr("decoupes/%d.png" % count, 'user.bar', local_time_str)
            count = count + 1
        else:
            s = ssim(imageprev, blur) #Structural Similarity Index between current and previous frame
            m = mse(imageprev, blur) #Mean Squared Error between current and previous frame
            #print(m,s)
            if(count==1):
                if ((m>602) and (s<0.8761)):
                    cv2.imwrite(dossier+"%d."% count+extension , image)  # save frame
                    foncDIV.writeMeta(dossier+"%d." % count+extension, heure)
                    count = count + 1
            else:
                mprev=mse(imageprev, imageprev1) # Previous Mean Squared Error
                if (((m>602) and (s<0.8761)) or ((m>405)and (m/mprev>5))): # add another condition: if the mse is not very big but the change
                                                                           #is more important comparing to previous mse
                    cv2.imwrite(dossier+"%d."% count+extension , image)  # save frame
                    foncDIV.writeMeta(dossier+"%d." % count+extension, heure)
                    count = count + 1
        step=step+1
        imageprev1 = imageprev
        imageprev = blur
