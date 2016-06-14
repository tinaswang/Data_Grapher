from Parser import Parser
import numpy as np
from scipy import ndimage
import os.path
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from Operations import Operations
import abc

class Display(object):

    def __init__(self, filename):
        __metaclass__  = abc.ABCMeta
        self.filename = filename

    @classmethod
    @abc.abstractmethod
    def get_data(self, filename):
        self.p = Parser(filename)
        dict_data = p.parse()
        self.data = np.array(p.xpath_get("/SPICErack/Data/Detector/data"))
        return self.data

    @abc.abstractmethod
    def plot2d(self):
         pass

    @classmethod
    @abc.abstractmethod
    def plot1d (self):
        distance_1 = self.p.xpath_get("/SPICErack/Motor_Positions/sample_det_dist/#text")
        distance_2 = self.p.xpath_get("/SPICErack/Header/sample_to_flange/#text")
        pixel_size_x = self.p.xpath_get("/SPICErack/Header/x_mm_per_pixel/#text")
        pixel_size_y = self.p.xpath_get("/SPICErack/Header/y_mm_per_pixel/#text")
        translation = self.p.xpath_get("/SPICErack/Motor_Positions/detector_trans/#text")
        Z = distance_1 + distance_2

        dim_x = self.p.xpath_get("/SPICErack/Header/Number_of_X_Pixels/#text")
        dim_y = self.p.xpath_get("/SPICErack/Header/Number_of_Y_Pixels/#text")
        z = np.full((dim_x*dim_y), Z)

        xx_pixels, yy_pixels = np.mgrid[0:dim_x, 0:dim_y]
        dist = np.hypot(xx_pixels, yy_pixels)  # Linear distance from point 0,0
        values = np.square(5*np.cos(dist/200.0))

        x_coords = np.linspace(0.0, pixel_size_x * dim_x, dim_x)
        y_coords = np.linspace(0.0, pixel_size_y * dim_y, dim_y)
        xx_coords, yy_coords = np.meshgrid(x_coords, y_coords)

        v = np.stack((xx_coords.flatten(), yy_coords.flatten(), z), axis=-1)
        u = np.stack((np.zeros(dim_x*dim_y), np.zeros(dim_x*dim_y), z), axis=-1)
        theta = np.arccos(np.sum (u*v, axis=1) / (np.linalg.norm(u,axis=1) * np.linalg.norm(v , axis=1)))

class PlotlyDisplay (Display):
    def __init__(self, filename):
        super().__init__(filename)
        op = Operations(filename, data_file= None, background_file= None)
        self.center_of_mass = op.get_center_of_mass(self.get_data(filename))

    def get_data(self, filename):
        return super().get_data(filename)

    def plot2d(self):
        graph_data = [go.Contour(z = self.data)]
        layout = go.Layout(
        showlegend=False,
        annotations=[
                dict(
                    x= self.center_of_mass[1],
                    y= self.center_of_mass[0],
                    xref='x',
                    yref='y',
                    text= (round(self.center_of_mass[1],3), round(self.center_of_mass[0],3)),
                    showarrow=True,
                    font=dict(
                        family='Courier New, monospace',
                        size=14,
                        color='#ffffff'
                    ),
                    align = 'center',
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='#ff7f0e',
                    ax=20,
                    ay=-30,
                    bordercolor='#c7c7c7',
                    borderwidth=2,
                    borderpad=4,
                    bgcolor='#ff7f0e',
                    opacity=0.8
                )
            ]
        )


        fig = go.Figure(data=graph_data, layout=layout)
        py.plot(fig)
    def plot1d (self):
        pass

class MatPlotLibDisplay (Display):
    def __init__(self, filename):
        super().__init__(filename)
        op = Operations(filename, data_file= None, background_file= None)
        self.center_of_mass = op.get_center_of_mass(self.get_data(filename))

    def get_data(self, filename):
        return super().get_data(self.filename)

    def plot2d(self):
        #fig = fig = plt.figure(figsize=(6, 6))
        #ax = fig.add_subplot(111)
        plt.imshow(self.data, origin = "lower")
        plt.scatter(self.center_of_mass[1], self.center_of_mass[0], c= 'g', s= 100)
        #ax.annotate('', xy=(self.center_of_mass[1], self.center_of_mass[0]), xytext=(3, 1.5),
            #arrowprops=dict(facecolor='black', shrink= 1),
            #)
        plt.show()

    def plot1d (self):
        pass

def main():
    #pl = MatPlotLibDisplay("Data Examples/BioSANS_exp253_scan0010_0001.xml")
    #pl2 = PlotlyDisplay("Data Examples/HiResSANS_exp9_scan0030_0001.xml")
    #pl.plot2d()
    #print(pl2.get_center_of_mass(pl2.get_data("Data Examples/HiResSANS_exp9_scan0030_0001.xml")))


if __name__ == "__main__":
    main()
