
#Considerações... O arquivo está levando em consideração que está na mesma pasta que as imagens

import json
import ntpath
from select import select
from sys import stderr
import uuid
import matplotlib.pyplot as plt
from matplotlib import patches
import pydicom  
import numpy as np




class ProcessDicom:
    ''' Cria um array com a escala de hounsfield e realiza cinco cortes de acordo com as posições passadas
     e calcula a media e desvio padrao desses cortes.
        
    Parametros
        path: caminho para o aquivo 
        pos: vetor de posições
        width: comprimento do corte
        height: Altura do corte
    '''

    def __init__(self, file_path, pos,width, height): 
        self.pos =  pos
        self.width =  width
        self.height =  height
        self.filepath = file_path
        self.dataset = pydicom.dcmread(file_path)
        self.rescale_intercept = self.dataset[0x0028, 0x1052].value
        self.rescale_slope = self.dataset[0x0028, 0x1053].value
        self.pixel_array = self.dataset.pixel_array
        
        #Calcula matriz de housefild  
        self.housefield_units_pixel_array = self.pixel_array * self.rescale_slope + self.rescale_intercept

        #Realiza os crops e calcula médias e desvio padrão para cada
        self.top_left =     self.housefield_units_pixel_array[pos[0][0]:pos[0][0]+ width,pos[0][1]:pos[0][1]+height]
        self.top_left_mean = np.mean(self.top_left)
        self.top_left_std = np.std(self.top_left)
        
        self.top_right =    self.housefield_units_pixel_array[pos[1][0]:pos[1][0]+ width,pos[1][1]:pos[1][1]+height]
        self.top_right_mean = np.mean(self.top_left)
        self.top_right_std = np.std(self.top_left)
        
        self.center =       self.housefield_units_pixel_array[pos[2][0]:pos[2][0]+ width,pos[2][1]:pos[2][1]+height]
        self.center_mean = np.mean(self.center)
        self.center_std = np.std(self.center)
        
        self.botton_left =  self.housefield_units_pixel_array[pos[3][0]:pos[3][0]+ width,pos[3][1]:pos[3][1]+height]
        self.botton_left_mean = np.mean(self.botton_left)
        self.botton_left_std = np.std(self.botton_left)
        
        self.botton_right = self.housefield_units_pixel_array[pos[4][0]:pos[4][0]+ width,pos[4][1]:pos[4][1]+height]
        self.botton_right_mean = np.mean(self.botton_right)
        self.botton_right_std = np.std(self.botton_right)
        

        self.positions = [
            'Centro \n média: {:.2f}'.format(self.center_mean) +'\n std: {:.2f}'.format(self.center_std),
            'Superior esquerda \n média: {:.2f}'.format(self.top_left_mean) +'\n std: {:.2f}'.format(self.top_left_std),
            'Superior direita \n média: {:.2f}'.format(self.top_right_mean) +'\n std: {:.2f}'.format(self.top_right_std),
            'Inferior esquerda \n média: {:.2f}'.format(self.botton_left_mean) +'\n std: {:.2f}'.format(self.botton_left_std),
            'Inferior direita \n média: {:.2f}'.format(self.botton_right_mean) +'\n std: {:.2f}'.format(self.botton_right_std)
        ]
    #Metodo para mostrar as informações basicas do arquivo e localização e dados de cada corte
    def ShowInfo(self):
        
        print("filepath.........:", self.filepath)

        pat_name = self.dataset.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print("Patient's name...:", display_name)       
        print("Rescale Intercept.......:", self.rescale_intercept)
        print("Rescale Slope.......:", self.rescale_slope)

        print("Patient id.......:", self.dataset.PatientID)
        print("Modality.........:", self.dataset.Modality)
        print("Study Date.......:", self.dataset.StudyDate) 
        print("Localização ",self.positions[0])
        print("Localização ",self.positions[1])
        print("Localização ",self.positions[2])
        print("Localização ",self.positions[3])
        print("Localização ",self.positions[4])
        print("\n")

    #Metodo para mostrar as imagens e a localização dos cortes
    def ShowImage(self):
        
        fig,ax = plt.subplots(1)
        ax.imshow(self.pixel_array,cmap=plt.cm.bone)
        crop1 = patches.Rectangle(self.pos[0],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        crop2 = patches.Rectangle(self.pos[1],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        crop3 = patches.Rectangle(self.pos[2],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        crop4 = patches.Rectangle(self.pos[3],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        crop5 = patches.Rectangle(self.pos[4],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')

        ax.add_patch(crop1)
        ax.add_patch(crop2)
        ax.add_patch(crop3)
        ax.add_patch(crop4)
        ax.add_patch(crop5)
        plt.show()

    def GetInfo(self):    
        file_info = {
        "title":ntpath.basename(self.filepath),
        "id":str(uuid.uuid4().hex),
        "regioes":{
            "superior_esquerda":{
                    "media":(self.top_left_mean),
                    "std":(self.top_left_std)
                    },
                    "superior_direita":{
                    "media":(self.top_right_mean),
                    "std":(self.top_right_std)
                    },
                    "centro":{
                    "media":(self.center_mean),
                    "std":(self.center_std)
                    },
                    "inferior_esquerda":{
                    "media":(self.botton_left_mean),
                    "std":(self.botton_left_std)
                    },
                    "inferior_direita":{
                    "media":(self.botton_right_mean),
                    "std":(self.botton_right_std)
                    }
                }
            }

class ProcessFiles:
    __info = {
        "PatientID":{
        "IMG1":{
        },
        "IMG2":{
        },
        "IMG3":{
        },
        "IMG4":{   
        }
        }
    }
    
    def __init__(self, files, pos,width, height):  
        results=[]
        for file in files:
            results.append(ProcessDicom(file,pos,width,height))

        count = 1
        for result in results:
            result.ShowInfo()
            result.ShowImage()
            self.__info["PatientID"]["IMG" + str(count)] = result.GetInfo()
            count+=1
    
    def GetInfo(self):
        '''Return extracted files information in json format.'''
        return json.dumps(self.__info)   



files = ["CT.CP600.Image 1.dcm","CT.CP600.Image 2.dcm","CT.CP600.Image 3.dcm","CT.CP600.Image 4.dcm"]
pos = [(155,155),(300,155),(225,225),(155,300),(300,300)]
width=45
height=45
data = ProcessFiles(files,pos,width,height)
print(data.GetInfo())

