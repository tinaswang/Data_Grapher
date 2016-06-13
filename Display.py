from Parser import Parser
import numpy as np
from scipy import ndimage
import os.path
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import abc

class Display(object):

    def __init__(self, filename):
        __metaclass__  = abc.ABCMeta
        self.filename = filename

    @classmethod
    @abc.abstractmethod
    def get_data(self, filename):
        p = Parser(filename)
        dict_data = p.parse()
        self.data = np.array(p.xpath_get("/SPICErack/Data/Detector/data"))
        return self.data

    @classmethod
    @abc.abstractmethod
    def get_center_of_mass(self, data):
        com = ndimage.center_of_mass(data)
        com = [x for x in com]
        return com

    @abc.abstractmethod
    def plot2d(self):
         pass
    @abc.abstractmethod
    def plot1d (self):
        pass

class PlotlyDisplay (Display):
    def __init__(self, filename):
        super().__init__(filename)
        self.center_of_mass = self.get_center_of_mass(self.get_data(filename))

    def get_data(self, filename):
        return super().get_data(self.filename)

    def get_center_of_mass(self, data):
        return super().get_center_of_mass(data);

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
                    arrowwidth=3,
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
        self.center_of_mass = self.get_center_of_mass(self.get_data(filename))

    def get_data(self, filename):
        return super().get_data(self.filename)

    def get_center_of_mass(self, data):
        return super().get_center_of_mass(data);

    def plot2d(self):
        #fig = fig = plt.figure(figsize=(6, 6))
        #ax = fig.add_subplot(111)
        plt.imshow(self.data)
        plt.scatter(self.center_of_mass[1], self.center_of_mass[0], c= 'g', s= 100)
        #ax.annotate('', xy=(self.center_of_mass[1], self.center_of_mass[0]), xytext=(3, 1.5),
            #arrowprops=dict(facecolor='black', shrink= 1),
            #)

        plt.show()

    def plot1d (self):
        pass

def main():
    #pl = MatPlotLibDisplay("Data Examples/CG2.xml")
    pl2 = PlotlyDisplay("Data Examples/CG2.xml")
    #pl.plot2d()
    pl2.plot2d()
if __name__ == "__main__":
    main()
