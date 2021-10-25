import uuid
import matplotlib.pyplot as plt
from matplotlib import patches
import pydicom  
import numpy as np



class ProcessDicom:
    ''' Classe que recebe um arquivo DICOM, cria um array com a escala de hounsfield,
    realiza cinco cortes e calcula a media e desvio padrao desses cortes.
        
    Param
        path: caminho para o aquivo dicom
    
    Methods
        PlotDicomImage()
            Gera uma visualizacao grafica com o arquivo dicom com os cortes nas cinco posicoes 
        
        GetInfoJson()
            Gera um objeto json com as informaçoes do arquivo dicom
    '''

    def __init__(self, path):
        self.path = path
        self.crop_size = 42
        self.data_set = pydicom.dcmread(path)
        self.rescale_intercept = self.data_set[0x0028, 0x1052].value
        self.rescale_slope = self.data_set[0x0028, 0x1053].value
        self.pixel_array = self.data_set.pixel_array
        self.arr_size = self.pixel_array.shape
        
        self.xy = [
            ( (int(self.arr_size[0] * 0.45)), (int(self.arr_size[1] * 0.45)) ), #center position
            ( (int(self.arr_size[0] * 0.3)), (int(self.arr_size[1] * 0.3)) ), #top_left position
            ( (int(self.arr_size[0] * 0.6)), (int(self.arr_size[1] * 0.3)) ), #top_right position
            ( (int(self.arr_size[0] * 0.3)), (int(self.arr_size[1] * 0.6)) ), #botton_left position
            ( (int(self.arr_size[0] * 0.6)), (int(self.arr_size[1] * 0.6)) ),  #botton_right position
        ]

        self.hounsfield_pixel_array = (
            self.pixel_array * self.rescale_slope + self.rescale_intercept
        )

        self.center = (
            self.hounsfield_pixel_array[
                self.xy[0][0]:self.xy[0][0] + self.crop_size, #x
                self.xy[0][1]:self.xy[0][1] + self.crop_size  #y
            ]
        )
        self.center_mean = np.mean(self.center)
        self.center_std = np.std(self.center)
        

        self.top_left = (
            self.hounsfield_pixel_array[
                self.xy[1][0]:self.xy[1][0] + self.crop_size,
                self.xy[1][1]:self.xy[1][1] + self.crop_size
            ]
        )
        self.top_left_mean = np.mean(self.top_left)
        self.top_left_std = np.std(self.top_left)

        self.top_right = (
            self.hounsfield_pixel_array[
                self.xy[2][0]:self.xy[2][0] + self.crop_size,
                self.xy[2][1]:self.xy[2][1] + self.crop_size
            ]
        )
        self.top_right_mean = np.mean(self.top_right)
        self.top_right_std = np.std(self.top_right)

        self.botton_left = (
            self.hounsfield_pixel_array[
                self.xy[3][0]:self.xy[3][0] + self.crop_size,
                self.xy[3][1]:self.xy[3][1] + self.crop_size
            ]
        )
        self.botton_left_mean = np.mean(self.botton_left)
        self.botton_left_std = np.std(self.botton_left)

        self.botton_right = (
            self.hounsfield_pixel_array[
                self.xy[4][0]:self.xy[4][0] + self.crop_size,
                self.xy[4][1]:self.xy[4][1] + self.crop_size
            ]
        )
        self.botton_right_mean = np.mean(self.botton_right)
        self.botton_right_std = np.std(self.botton_right)
    
    def PlotDicomImage(self):
        '''Class que exibe dicom com os crops'''
        positions = [
            'Centro \n média: {:.2f}'.format(self.center_mean) +'\n std: {:.2f}'.format(self.center_std),
            'Superior esquerda \n média: {:.2f}'.format(self.top_left_mean) +'\n std: {:.2f}'.format(self.top_left_std),
            'Superior direita \n média: {:.2f}'.format(self.top_right_mean) +'\n std: {:.2f}'.format(self.top_right_std),
            'Inferior esquerda \n média: {:.2f}'.format(self.botton_left_mean) +'\n std: {:.2f}'.format(self.botton_left_std),
            'Inferior direita \n média: {:.2f}'.format(self.botton_right_mean) +'\n std: {:.2f}'.format(self.botton_right_std)
        ]

        #__init__(xy, width, height, angle=0.0, **kwargs)
        fig, ax = plt.subplots()
        ax.imshow(self.hounsfield_pixel_array, cmap=plt.cm.bone)
        title = self.path.split("/")[-1]
        i = 0 #index
        for crop in self.xy:
            crop = patches.Rectangle(
                self.xy[i],
                self.crop_size, 
                self.crop_size,
                fc ='none',
                lw=0.9,
                ec='y')
            
            ax.add_patch(crop)
            ax.text(self.xy[i][0]+20, 
                    self.xy[i][1]-25,
                    positions[i], 
                    ha='center',
                    va='center',
                    size=6, 
                    alpha=.5,
                    color='r',
                    fontweight='bold')

            
            i+= 1
        ax.set_title(f'Imagem: '+ title)      
        plt.show()
    
    def GetInfo(self, i):
            
        patient_info = {
            "IMG"+str(i):{
                "title":self.path.split("/")[-1],
                "id":uuid.uuid4().hex,
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
        }
        return patient_info