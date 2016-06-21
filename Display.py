from Parser import Parser
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from Operations import Operations
import matplotlib.pyplot as plt

class Display(object):

    def __init__(self):
        pass

    @staticmethod
    def plot2d(data, filename, center): # makes a 2d plotly graph of the center data

        p = Parser(filename)
        detector_data, distance_1, distance_2,pixel_size_y,pixel_size_x, translation, dim_x, dim_y = Operations.get_data(p)
        x_units_centered,y_units_centered = Operations.get_axes_units(detector_data.shape,
                                            pixel_size=[pixel_size_y,pixel_size_x])

        X = x_units_centered
        Y = y_units_centered + translation
        Z = data
        graph_data = [go.Contour(z = detector_data, x = X, y = Y)]

        layout = go.Layout(
         xaxis = dict(title = "Milimeters"),
         yaxis = dict(title = "Milimeters"),
         showlegend= False,
         annotations=[
                 dict(
                     x = center[0]/pixel_size_x - detector_data.shape[1]/2,
                     y = (center[1])/pixel_size_y,
                     xref='x',
                     yref='y',
                     text= "Center",
                     showarrow=True,
                     font=dict(
                         family='Courier New, monospace',
                         size=11,
                         color='#000000'
                     ),
                     align = 'center',
                     arrowhead=2,
                     arrowsize=1,
                     arrowwidth=2,
                     arrowcolor='#ffffff',
                     ax=20,
                     ay=-30,
                     bordercolor='#c7c7c7',
                     borderwidth=2,
                     borderpad=4,
                     bgcolor='#ffffff',
                     opacity=0.8
                 )
             ]
         )


        fig = go.Figure(data=graph_data, layout=layout)
        py.plot(fig)

    @staticmethod
    def plot1d(parser, com, difference): # Makes the plotly line graph

        bin_centers, bin_means = Operations.integrate(parser, com, difference)
        bin_centers = bin_centers
        bin_means = bin_means

        trace = go.Scatter(
            x = bin_centers,
            y = bin_means,
            mode = 'lines'
            )

        layout = go.Layout(
            xaxis = dict(title = "Angle"),
            yaxis = dict(title = "Intensity")

        )
        graph_data = [trace]
        fig = go.Figure(data=graph_data, layout = layout)
        py.plot(fig)


def main():
    pass
if __name__ == "__main__":
    main()
