from Parser import Parser
from Operations import Operations
from Display import Display
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go

class Data(object):

    def __init__(self, data_file, center_file = None, background_file=None):
        self.data_f = data_file
        if center_file is not None:
            self.center_f = center_file
        if background_file is not None:
            self.backgrd_f = background_file

    @staticmethod
    def get_data(p):
        detector_data = np.array(p.xpath_get("/SPICErack/Data/Detector/data"))
        distance_1 = p.xpath_get("/SPICErack/Motor_Positions/sample_det_dist/#text")
        distance_2 = p.xpath_get("/SPICErack/Header/sample_to_flange/#text")
        pixel_size_x = p.xpath_get("/SPICErack/Header/x_mm_per_pixel/#text")
        pixel_size_y = p.xpath_get("/SPICErack/Header/y_mm_per_pixel/#text")
        translation = p.xpath_get("/SPICErack/Motor_Positions/detector_trans/#text")
        dim_x, dim_y = detector_data.shape
        return detector_data, distance_1, distance_2,pixel_size_x,pixel_size_y, translation, dim_x, dim_y

    def setup(self):  # sets up the data for the three files
        self.p_data = Parser(self.data_f)
        self.data = Data.get_data(self.p_data)[0]
        # self.data = np.rot90(Data.get_data(self.p_data)[0]) # for data that needs to be rotated 90 degrees
        try:
            p_center = Parser(self.center_f)
            pixel_size_x = Data.get_data(p_center)[3]
            pixel_size_y = Data.get_data(p_center)[4]
            self.size = (pixel_size_x, pixel_size_y)
            translation = Data.get_data(p_center)[5]
            self.center_data = Data.get_data(p_center)[0]
            # self.center_data =  np.rot90(Data.get_data(p_center)[0]) # for data that needs to be rotated 90 degrees
            self.center = Operations.find_center(center_data=self.center_data,
                                                size = self.size,
                                                translation=translation)
        except:
            pass
        try:
            p_backgrd = Parser(self.backgrd_f)
            self.backgrd_data = Data.get_data(p_backgrd)[0]
            # self.backgrd_data = np.rot90(Data.get_data(p_backgrd)[0]) # data that needs to be rotated
            self.subtracted_data = self.data - self.backgrd_data
        except:
            pass

    def display(self):  # Graphs a plotly line graph
        p = Parser(self.data_f)
        profile = Operations.integrate(size=(self.size),
                                            center=self.center,
                                            data = self.subtracted_data)


        Display.plot1d(com=self.center,
                           difference=self.subtracted_data,
                           profile=profile,
                           pixel_size=(self.size[0], self.size[1]))
        # except:
            # raise ValueError("Not enough data.")

    def display2d(self):
        # Graphs a plotly contour plot of the subtracted data
        # If there's no subtracted data, will graph data file
        all_data= Data.get_data(self.p_data)
        pixel_size_x, pixel_size_y = self.size
        units = Operations.get_axes_units(all_data[0].shape,
                                         pixel_size=[pixel_size_y, pixel_size_x])
        try:
            Display.plot2d(data=self.subtracted_data, parameters=all_data,
                           center=self.center, units=units)
        except:
            Display.plot2d(data=self.center_data, parameters=all_data,
                           center=self.center, units=units)

def main():
    # d = Data(data_file="Data Examples/BioSANS_exp253_scan0015_0001.xml",
            # center_file="Data Examples/BioSANS_exp253_scan0010_0001.xml",
            # background_file="Data Examples/BioSANS_exp253_scan0011_0001.xml")
    # d = Data(data_file="Data Examples/test_0032.xml",
    #     center_file="Data Examples/test_0032_trans_0001.xml",
    #     background_file="Data Examples/test_bg_0032.xml")
    d = Data(data_file="C:/Users/tsy/Documents/GitHub/Reducer/Data Examples/HiResSANS_exp9_scan0030_0001.xml",
         center_file="C:/Users/tsy/Documents/GitHub/Reducer/Data Examples/HiResSANS_exp9_scan0006_0001.xml",
        background_file="C:/Users/tsy/Documents/GitHub/Reducer/Data Examples/HiResSANS_exp9_scan0038_0001.xml")
    d.setup()
    d.display()
    # d.display2d()

if __name__ == "__main__":
    main()
