import numpy as np
import os
import copy
from math import *
import matplotlib.pyplot as plt
from functools import reduce

# reading in dicom files
import pydicom
from pydicom import dcmread
from pydicom.data import get_testdata_file

# plot libraries
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import json

class ImageProcessing:
    
    """
    Image Processing of DICOM file.
    
    Parameters  
        
    file_path: file path
    
        
    Methods
    
    description()
        Get basic information about the file
    define_crops()
        Define crops given their coordinates
    average()
        Calculate average value
    standard_deviation()
        Calculage standard deviation value
    """

    def __init__(self, file_path):
        
        self.path = file_path
        self.infodata = pydicom.dcmread(file_path)
        self.image = self.infodata.pixel_array
        self.intercept = self.infodata.RescaleIntercept
        self.slope = self.infodata.RescaleSlope        
        self.hounsfield_unit = self.image * self.slope + self.intercept
        
    def description(self):
        
        """
        File Description
        """
        
        print()
        print(f"File path........: {self.path}")
        print(f"SOP Class........: {self.infodata.SOPClassUID} ({self.infodata.SOPClassUID.name})")
        print()

        pat_name = self.infodata.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print(f"Patient's Name...: {display_name}")
        print(f"Patient ID.......: {self.infodata.PatientID}")
        print(f"Modality.........: {self.infodata.Modality}")
        print(f"Study Date.......: {self.infodata.StudyDate}")
        print(f"Image size.......: {self.infodata.Rows} x {self.infodata.Columns}")
        print(f"Pixel Spacing....: {self.infodata.PixelSpacing}")

        # use .get() if not sure the item exists, and want a default value if missing
        print(f"Slice location...: {self.infodata.get('SliceLocation', '(missing)')}")

        # plot the image using matplotlib
        plt.imshow(self.infodata.pixel_array, cmap=plt.cm.gray)
        plt.show()
        
    def define_crops(self, initial_pos_x, initial_pos_y, final_pos_x, final_pos_y):
        
        """
        Define crops through their coordinates and returns their average and their standard deviation
        """
        
        self.initial_pos_x = initial_pos_x
        self.initial_pos_y = initial_pos_y
        self.final_pos_x = final_pos_x
        self.final_pos_y = final_pos_y
        
        self.crop = self.hounsfield_unit[self.initial_pos_x:self.final_pos_x, self.initial_pos_y:self.final_pos_y]
        
        return (self.average(), self.standard_deviation())

    def visualization(self):
        
        """
        Crops Visualization
        """
        
        fig,ax = plt.subplots(1)
        ax.imshow(self.image,cmap=plt.cm.bone)  
            
        for value in positions:            
        
            rect = patches.Rectangle((value[0],value[1]),value[2]-value[0],value[3]-value[1], edgecolor = "y", facecolor = "none") 
            
            ax.add_patch(rect)
            
    
    def average(self):
        
        return np.mean(self.crop)
    
    def standard_deviation(self):
        
        return np.std(self.crop)
    

files = ["img/CT.CP600.Image 1.dcm","img/CT.CP600.Image 2.dcm","img/CT.CP600.Image 3.dcm","img/CT.CP600.Image 4.dcm"]

crops = {
    'superior_esquerda':(165,165,215,225),
    'superior_direita':(260,160,320,205),
    'centro':(226,226,286,286),
    'inferior_esquerda':(130,260,180,300),
    'inferior_direita':(300,300,350,350)
}

positions = []

for key, value in crops.items():

    positions.append(value)


    
    
"""
Display file images with their respective crops
"""
    
for file in files:
    image = ImageProcessing(file)
    image.visualization()

def create_patient_dict(image: ImageProcessing):
    
    """
    Create a patient dictionary containing all the required information
    """
    
    image_dict = {}

    image_dict['title'] = image.path

    image_dict['id'] = image.path.partition(" ")[2].partition(".")[0]

    image_dict['regioes'] = {}


    for key,value in crops.items():
        media, std = image.define_crops(*value)
    
        image_dict['regioes'][key] = {'media':media, 'std':std}
    
    patient_dict = {}
    
    patient_dict['IMG' + image_dict['id']] = image_dict
       
    return patient_dict, image.infodata.PatientID     
    
    
final_answer = {}

"""
Concatenate every information from each file
"""

for file in files:
  
    patient_dict, patient_id = create_patient_dict(ImageProcessing(file))

    if patient_id in final_answer:
        final_answer[patient_id].update(patient_dict)
    else:
        final_answer[patient_id] = patient_dict

        
json.dumps(final_answer)   