from Parser import Parser
import numpy as np
from scipy import ndimage
import os.path
from abc import ABCMeta
import plotly.offline as py
import plotly.graph_objs as go

class Display():

    def __init__(self, filename):
            p = Parser(filename)
            self.dict_data = p.parse()
            self.data = np.array(p.xpath_get("/SPICErack/Data/Detector/data"))


    def get_center_of_mass(self):
        com = ndimage.center_of_mass(self.data)
        com = [x for x in com]
        return com



class PlotlyDisplay (Display):
    def __init__(self, filename):
        super().__init__(filename)
        self.center_of_mass = super().get_center_of_mass()

    def plot2d(self, write_file):
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
                    size=11,
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
        if write_file == "none":
            plot_url = py.plot(fig)
        else:
            plot_url = py.plot(fig, filename= write_file)

pl = PlotlyDisplay("Data Examples/BioSANS.xml")
pl.plot2d(write_file = "none")
