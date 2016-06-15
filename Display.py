from Parser import Parser
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from Operations import Operations
from Data import Data

class Display(object):

    def __init__(self, filename):
        pass
    def get_data(self, filename):
        self.p = Parser(filename)
        self.dict_data = Data(self.p)
        self.data = self.dict_data.detector_data
        return self.data

    @staticmethod
    def plot2d(data, center_of_mass):
         graph_data = [go.Contour(z = data)]
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


def main():
    pass
if __name__ == "__main__":
    main()
