# -*- coding: utf-8 -*-s
from os import path
import os
from  dicomFarm import ProcessDicom
import json


#Caminho para os arquivos dicom
path = './img'
data_paths = [i for i in (os.path.join(path, f) for f in os.listdir(path)) if os.path.isfile(i)]

#dict para armazenar os retornos 
data_info = {"PatientID":{}}


#looping para carragar os dados dos arquivos
i=1
for data_path in data_paths:
    data = ProcessDicom(data_path)
    data.PlotDicomImage()
    
    data_info['PatientID'].update(data.GetInfo(i))
    i+= 1

#json com as informaçoes extraidas
data_json = json.dumps(data_info)
print(data_json)
