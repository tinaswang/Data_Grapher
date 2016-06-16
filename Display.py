from Parser import Parser
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from Operations import Operations


class Display(object):

    def __init__(self):
        pass

    @staticmethod
    def plot2d(data, filename, center_of_mass):
        p = Parser(filename)
        detector_data, distance_1, distance_2,pixel_size_x,pixel_size_y, translation, dim_x, dim_y = Operations.get_data(p)
        x_units_centered,y_units_centered = Operations.get_axes_units(detector_data.shape,
                                            pixel_size=[pixel_size_x, pixel_size_y])
        X= x_units_centered + translation
        Y = y_units_centered
        Z = detector_data
        graph_data = [go.Contour(z = detector_data)]
        layout = go.Layout(
         xaxis=dict(range=[X[0], X[-1]]),
         yaxis=dict(range=[Y[0], Y[-1]]),
         showlegend= False,
         annotations=[
                 dict(
                     x= center_of_mass[1],
                     y= center_of_mass[0],
                     xref='x',
                     yref='y',
                     text= (round(center_of_mass[1],3), round(center_of_mass[0],3)),
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

    @staticmethod
    def plot1d(parser, com, difference):
        pixel_size_x = Operations.get_data(parser)[3]
        pixel_size_y =  Operations.get_data(parser)[4]
        translation = Operations.get_data(parser)[5]

        bin_centers, bin_means = Operations.integrate(parser, com, difference)
        x_units_centered,y_units_centered = Operations.get_axes_units(difference.shape,
                                            pixel_size=[pixel_size_x, pixel_size_y])
        X_axis= x_units_centered
        Y_axis = y_units_centered + translation
        y_vals = np.arange(Y_axis[0], Y_axis[-1], 6)
        y_vals = [y/pixel_size_y for y in y_vals]
        trace = go.Scatter(
            x = bin_centers,
            y = bin_means - translation,
            mode = 'lines')
        layout = go.Layout(

                            yaxis = dict( range=[Y_axis[0], Y_axis[-1]],
                                        tickvals = [i for i in y_vals] ),

        )
        graph_data = [trace]
        #fig = go.Figure(data=graph_data, layout=layout)
        fig = go.Figure(data = graph_data)
        py.plot(fig)

def main():
    pass
if __name__ == "__main__":
    main()
