from Parser import Parser
import numpy as np
import matplotlib.pyplot as plt

class Operations(object):

    def __init__(self):
        pass
    def get_center_of_mass(self, center_data):
        hist, bins = np.histogram(center_data.ravel(), normed=False, bins=60000)
        threshold = bins[np.cumsum(bins) * (bins[1] - bins[0]) > 30000][0]
        mnorm2d = np.ma.masked_less(center_data, threshold)
        com = ndimage.measurements.center_of_mass(mnorm2d)
        return com

    def subtract(self, data, background_data):
        p1 = Parser(data_file)
        p2 = Parser(background_file)
        data = np.array(p1.xpath_get("/SPICErack/Data/Detector/data"))
        background_data = np.array(p2.xpath_get("/SPICErack/Data/Detector/data"))
        difference = data - background_data
        return difference

    def translate(self, data, parser):
        translation = parser.xpath_get("/SPICErack/Motor_Positions/detector_trans/#text")
        
