from Parser import Parser
from Operations import Operations
from Display import Display
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go

class Data(object):

    def __init__(self, data_file, center_file, background_file):
        self.data_f = data_file
        if center_file is not "none":
            self.center_f = center_file
        if background_file is not "none":
            self.backgrd_f = background_file

    def setup(self):  # sets up the data for the three files
        p_data = Parser(self.data_f)
        # self.data = Operations.get_data(p_data)[0]
        self.data = np.rot90(Operations.get_data(p_data)[0])
        if self.center_f:
            p_center = Parser(self.center_f)
            # self.center_data =  Operations.get_data(p_center)[0]
            self.center_data =  np.rot90(Operations.get_data(p_center)[0])
            self.center = Operations.find_center(self.center_data, p_center)
        if self.backgrd_f:
            p_backgrd = Parser(self.backgrd_f)
            # self.backgrd_data = Operations.get_data(p_backgrd)[0]
            self.backgrd_data = np.rot90(Operations.get_data(p_backgrd)[0])
            self.subtracted_data = self.data - self.backgrd_data

    def display1d(self):  # Graphs a plotly line graph
        if (self.subtracted_data.any()):
            p = Parser(self.data_f)
            Display.plot1d(parser=p, com=self.center,
                           difference=self.subtracted_data)
        else:
            raise NameError("Data not found.")

    def display2d(self):  # Graphs a plotly contour plot of the beam center
        if (self.subtracted_data.any()):
            Display.plot2d(data=self.subtracted_data, filename=self.data_f,
                           center=self.center)
        else:
            raise NameError("Data not found.")

def main():
    # d = Data(data_file="Data Examples/BioSANS_exp253_scan0015_0001.xml",
    #         center_file="Data Examples/BioSANS_exp253_scan0010_0001.xml",
    #         background_file="Data Examples/BioSANS_exp253_scan0011_0001.xml")
    d = Data(data_file="Data Examples/test_0032.xml",
        center_file="Data Examples/test_0032_trans_0001.xml",
        background_file="Data Examples/test_bg_0032.xml")
    # d = Data(data_file="Data Examples/HiResSANS_exp9_scan0030_0001.xml",
    #     center_file="Data Examples/HiResSANS_exp9_scan0006_0001.xml",
    #     background_file="Data Examples/HiResSANS_exp9_scan0038_0001.xml")
    d.setup()
#     graph_data = [
#     go.Surface(
#         z=d.subtracted_data
#     )
# ]
#     fig = go.Figure(data=graph_data)
#     py.plot(fig)
    d.display1d()
    #d.display2d()
if __name__ == "__main__":
    main()
