
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pydicom
import numpy as np
import json
import ntpath
import uuid

class ProcessFile:
    '''Process givem DICOM file.

    Constructor arguments:
    :param file_path: file path
    :param pos: list of crop positions
    :param width: crop width
    :param height: crop height
    
    Methods
    -------
    GetInfo()
        Get extracted file information.
    ShowInfo()
        Show basic file informations.
    ShowImage()
        Show image and crop boxes.
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
        # Calc housefields mattrix according to: https://gist.github.com/somada141/df9af37e567ba566902e
        self.housefield_units_pixel_array = self.pixel_array * self.rescale_slope + self.rescale_intercept

        self.top_left =     self.housefield_units_pixel_array[pos[0][0]:pos[0][0]+ width,pos[0][1]:pos[0][1]+height]
        self.top_right =    self.housefield_units_pixel_array[pos[1][0]:pos[1][0]+ width,pos[1][1]:pos[1][1]+height]
        self.center =       self.housefield_units_pixel_array[pos[2][0]:pos[2][0]+ width,pos[2][1]:pos[2][1]+height]
        self.botton_left =  self.housefield_units_pixel_array[pos[3][0]:pos[3][0]+ width,pos[3][1]:pos[3][1]+height]
        self.botton_right = self.housefield_units_pixel_array[pos[4][0]:pos[4][0]+ width,pos[4][1]:pos[4][1]+height]
        
    def ShowInfo(self):
        ''''Show basic file informations.'''
        print("filepath.........:", self.filepath)
        print("Storage type.....:", self.dataset.SOPClassUID)

        pat_name = self.dataset.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print("Patient's name...:", display_name)       
        print("Rescale Intercept.......:", self.rescale_intercept)
        print("Rescale Slope.......:", self.rescale_slope)
        
        print("Patient id.......:", self.dataset.PatientID)
        print("Modality.........:", self.dataset.Modality)
        print("Study Date.......:", self.dataset.StudyDate)

        if 'PixelData' in self.dataset:
            rows = int(self.dataset.Rows)
            cols = int(self.dataset.Columns)
            print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
                rows=rows, cols=cols, size=len(self.dataset.PixelData)))
            if 'PixelSpacing' in self.dataset:
                print("Pixel spacing....:", self.dataset.PixelSpacing)

        print("Slice location...:", self.dataset.get('SliceLocation', "(missing)"))
        
    def ShowImage(self):
        ''''Show image and crop boxes.'''
        fig,ax = plt.subplots(1)
        ax.imshow(self.pixel_array,cmap=plt.cm.bone)
        rect1 = patches.Rectangle(self.pos[0],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        rect2 = patches.Rectangle(self.pos[1],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        rect3 = patches.Rectangle(self.pos[2],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        rect4 = patches.Rectangle(self.pos[3],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        rect5 = patches.Rectangle(self.pos[4],self.width,self.height,linewidth=1,edgecolor='y',facecolor='none')
        
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.add_patch(rect3)
        ax.add_patch(rect4)
        ax.add_patch(rect5)
        plt.show()


    def __CalcMean(self, img):
        ''''Calc mean.'''
        return img.mean()      

    def __CalcStd(self, img):
        ''''Calc standard deviation.'''
        return img.std()  

    def GetInfo(self):
        ''''Get extracted file information.'''
        file_info = {
        "title":ntpath.basename(self.filepath),
        "id":str(uuid.uuid4().hex),
        "regioes":{
        "superior_esquerda":{
        "media":self.__CalcMean(self.top_left),
        "std":self.__CalcStd(self.top_left)
        },
        "superior_direita":{
        "media":self.__CalcMean(self.top_right),
        "std":self.__CalcStd(self.top_right)
        },
        "centro":{
        "media":self.__CalcMean(self.center),
        "std":self.__CalcStd(self.center)
        },
        "inferior_esquerda":{
        "media":self.__CalcMean(self.botton_left),
        "std":self.__CalcStd(self.botton_left)
        },
        "inferior_direita":{
        "media":self.__CalcMean(self.botton_right),
        "std":self.__CalcStd(self.botton_right)
        }
        }
        }

        return file_info

class ProcessFiles:
    '''Process given DICOM files.

    Constructor arguments:
    :param files: list of files to be processed
    :param pos: list of crop positions
    :param width: crop width
    :param height: crop height
    
    Attributes
    ----------
    __info : str
        holds information about processed files
    
    Methods
    -------
    GetInfo()
        Get extracted files information in json format
    '''

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
            results.append(ProcessFile(file,pos,width,height))

        count = 1
        for result in results:
            result.ShowInfo()
            result.ShowImage()
            self.__info["PatientID"]["IMG" + str(count)] = result.GetInfo()
            count+=1
    def GetInfo(self):
        '''Return extracted files information in json format.'''
        return json.dumps(self.__info)


#set file paths
files = ["img/CT.CP600.Image 1.dcm","img/CT.CP600.Image 2.dcm","img/CT.CP600.Image 3.dcm","img/CT.CP600.Image 4.dcm"]
#set crop boxes
pos = [(155,155),(300,155),(225,225),(155,300),(300,300)]
width=50
height=50
#process files
data = ProcessFiles(files,pos,width,height)
print(data.GetInfo())





    