import pydicom
import json
import os
import uuid
import matplotlib.pyplot as plt
from matplotlib import patches

class Image:
    def __init__(self, path, file):
        '''
        path = DICOM files directory
        '''
        self.path = path
        self.file = file

    def ds(self): 
        '''
        Reads dicom file on path and return its dataset
        '''
        return read_dicom(self.path, self.file)
        
    def crops_info(self):
        '''
        Returns hu mean and std as a dictionary
        '''
        crops_data = hounsfield(self.path, self.file)
        data = {'title': self.file, 'id': f'{uuid.uuid4()}', 'regions': {}}
        data['regions']['top left'] = {'mean': crops_data[1]['HU'], 'std': crops_data[1]['std']}
        data['regions']['top right'] = {'mean': crops_data[2]['HU'], 'std': crops_data[2]['std']}
        data['regions']['center'] = {'mean': crops_data[3]['HU'], 'std': crops_data[3]['std']}
        data['regions']['lower left'] = {'mean': crops_data[4]['HU'], 'std': crops_data[4]['std']}
        data['regions']['lower right'] = {'mean': crops_data[5]['HU'], 'std': crops_data[5]['std']}

        return data

    def json_data(self):
        '''
        Returns hu mean and std as json object
        '''
        data = Image.crops_info(self)
        data_json = json.dumps(data, indent=2)
        return data_json

    def plot(self):
        dataset = read_dicom(self.path, self.file)
        coordinates = crops_coordinates()
        fig, ax = plt.subplots()
        ax.imshow(dataset.pixel_array, cmap=plt.cm.bone)

        for coord in coordinates:
            rect = patches.Rectangle((coord[0], coord[1]), coord[3], coord[2], linewidth=1, edgecolor='r', facecolor='none') 
            ax.add_patch(rect)
        plt.show()

def main():
    '''
    Reads all the dicom files in the given folder and return a json object. User must confirm directory's name
    '''
    path = ask_path()
    files = os.listdir(path)
    patient_data = {}
    
    for file in files:
        dataset = Image(path, file)
        patient_data[f'IMG{files.index(file)+1}'] = dataset.crops_info()
        dataset.plot()
    patient_data = {dataset.ds().PatientID: patient_data}
    print(json.dumps(patient_data, indent=2))

def ask_path():
    path = directory() # \\python_file_directory\\img\\
    answer = input(f'Is the directory you want to consult: "{path}"? [y/n] ')
    if answer not in ['y', 'Y', 'n', 'N']:
        print('Not a valid answer')
        main()
    if answer in ['n', 'N']:
        path = input('Enter path name: ')
    return path

def directory():
    '''
    Returns '\\python_file_directory'\\img
    '''
    path = __file__
    pos = 0
    for i in range(len(path)):
        if path[i] == '\\':
            pos = i
    path = (path[:pos+1])+'img\\'

    return path

def read_dicom(path, file):
    dataset = pydicom.dcmread(path + file)
    return dataset

def crops_coordinates():
    '''
    User can change the coordinates. [x, y, height, widht]
    '''
    tl = [161, 161, 27, 74] #top left
    tr = [296, 177, 32, 51] #top right
    ct = [211, 244, 34, 86] #center
    ll = [153, 313, 36, 54] #lower left
    lr = [321, 308, 32, 35] #lower right
    coord = [tl, tr, ct, ll, lr]
    return coord

def image_crops(img):
    coord = crops_coordinates()
    top_left = img[coord[0][1]:coord[0][1]+coord[0][2], coord[0][0]:coord[0][0]+coord[0][3]]
    top_right = img[coord[1][1]:coord[1][1]+coord[1][2], coord[1][0]:coord[1][0]+coord[1][3]]
    center = img[coord[2][1]:coord[2][1]+coord[2][2], coord[2][0]:coord[2][0]+coord[2][3]]
    lower_left = img[coord[3][1]:coord[3][1]+coord[3][2], coord[3][0]:coord[3][0]+coord[3][3]]
    lower_right = img[coord[4][1]:coord[4][1]+coord[4][2], coord[4][0]:coord[4][0]+coord[4][3]]
    crops = [top_left, top_right, center, lower_left, lower_right]
    return crops

def hounsfield(path, file):
    dataset = read_dicom(path, file)
    img = dataset.pixel_array
    crops = image_crops(img)
    i=1
    crops_data = {}
    slope = dataset.RescaleSlope
    intercept = dataset.RescaleIntercept

    for crop in crops:
        hu = crop * slope + intercept
        media_hu = hu.mean()
        dp = hu.std()
        crops_data[i] = {'HU': media_hu, 'std': dp}
        i +=1

    return crops_data
    
main()













