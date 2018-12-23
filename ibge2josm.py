#!/usr/bin/env python

"""ibge2josm.py: a small python app that converts IBGE data for JOSM"""

__author__ = 'Igor Eliezer'
__copyright__ = "Copyright 2018, Igor Eliezer ME"
__date__ = '2018/12/21'
__status__ = "Prototype"

# Imports
import re
import os
from tkinter import Tk
from tkinter import filedialog

# Messages
print("\nIBGE->JOSM: Converte dados do IBGE/CNEFE para JOSM/CSV.")
print("Criado por: " + __author__ + " (www.igoreliezer.com)")
print("Data: " + __date__)
print(
    "\nInstrução: após teclar ENTER, selecione um arquivo txt com os dados do IBGE/CNEFE e programa tentará convertê-lo.")
input("\nTecle ENTER para prosseguir: ")


# FUNCTIONS
def select_file():
    """
Select file
    :return: string
    """
    Tk().withdraw()
    filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo para converter",
                                          filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")))
    return filename


def dms(coord):
    """
Format DMS list (00 00 00 O) into DMS string with symbols ("00° 00' 00" W).
    :param coord: list
    :return: string
    """
    d = coord[0]
    m = coord[1]
    s = coord[2]
    c = coord[3]
    if c == 'O':
        c = 'W'
    return d + '° ' + m + '\' ' + s + '" ' + c


def dms2dd(coord):
    """
Convert DMS list (00 00 00 O) to decimal coord string ("-00.000000...").
    :param coord: list
    :return: string
    """
    d = coord[0]
    m = coord[1]
    s = coord[2]
    return '-' + str(float(d) + float(m) / 60 + float(s) / 3600)


# EXECUTION

# File 1: select and try to read the header
file = select_file()
try:
    f = open(file, 'r', encoding='utf-8')
    header = f.readline().split(';')
except UnicodeDecodeError:
    f = open(file, 'r', encoding='windows-1250')
    header = f.readline().split(';')

# File 2 - create and write the header
file_new = os.path.splitext(file)[0] + '.csv'
f_new = open(file_new, 'w', encoding="utf8")
f_new.write(','.join(header[0:5] + ['DMS_lat', 'DMS_lon', 'lat', 'lon'] + header[7:]))

# File 1 to file 2
# TODO: output number of lines
for line in f:
    if not re.match('\'C', line):  # skip
        data = line.split(';')
        lat = data[5].split(' ')
        lon = data[6].split(' ')
        if len(lat) == len(lon) == 4:
            line_new = ','.join(data[0:5] + [dms(lat)] + [dms(lon)] + [dms2dd(lat)] + [dms2dd(lon)] + data[7:])
            f_new.write(line_new)

# Close files
f.close()
f_new.close()

# Finish
print("\nSalvo em: " + file_new)
input("\nTecle ENTER para sair. ")
