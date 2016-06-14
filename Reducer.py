from Parser import Parser
import numpy as np
from scipy import ndimage
import os.path
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from Display import MatPlotLibDisplay

class Reducer(object):

    def __init__(self, data_file, background_file, center_file):
        self.data_f = data_file
        if center_file not None:
            self.center_f = center_file
        if background_file not None:
            self.backgrd_f = background_file

    def setup():
        op = Operations()
        p_data = Parser(self.data_f)
        data = p_data.parse()
        self.translated_data = op.translate(data, p_data)
        if self.center_f:
            p_center = Parser(self.center_f)
            center_data = p_center.parser()
            self.com = op.get_center_of_mass(center_data)
            self.translated_center = op.translate(center_data, p_center)
        if self.backgrd_f:
            p_backgrd = Parser(self.background_f)
            backgdr_data = p_background.parser()
            self.translated_backgrd = op.translate(backgrd_data, p_backgrd)
            self.difference = op.subtract(self.data_f, self.backgrd_f)

    def plot1d():
        pass


def main():
p = Parser("Data Examples/HiResSANS_exp9_scan0006_0001.xml")
if __name__ == "__main__":
    main()
