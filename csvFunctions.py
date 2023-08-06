import csv

def print(file, tabinput, local_time_str):
    with open(file, 'a', newline='', encoding='utf-8') as fichierecriture:
        writer = csv.writer(fichierecriture)
        writer=csv.writer(fichierecriture)
        writer.writerow([local_time_str, tabinput[0], tabinput[1], tabinput[2]])

def clear(file):
    with open(file,'w',newline='', encoding='utf-8') as fichiercsv:
        writer=csv.writer(fichiercsv)
        writer.writerow('')