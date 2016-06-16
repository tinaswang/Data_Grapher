from Parser import Parser
from Operations import Operations
from Display import Display

class Data(object):

    def __init__(self, data_file, center_file, background_file):
        self.data_f = data_file
        if center_file is not "none":
            self.center_f = center_file
        if background_file is not "none":
            self.backgrd_f = background_file
        #self.config = config

    def setup(self): # sets up the data for the three files
        op = Operations()
        p_data = Parser(self.data_f)
        self.data = Operations.get_data(p_data)[0]
        if self.center_f:
            p_center = Parser(self.center_f)
            self.center_data = Operations.get_data(p_center)[0]
            self.center_of_mass = Operations.get_center_of_mass(self.center_data)
        if self.backgrd_f:
            p_backgrd = Parser(self.backgrd_f)
            self.backgrd_data = Operations.get_data(p_backgrd)[0]
            self.subtracted_data = op.subtract(self.data, self.backgrd_data)

    def display1d(self): # Graphs a plotly line graph
        if (self.subtracted_data.any()):
            p = Parser(self.data_f)
            Display.plot1d(parser= p,
                                difference= self.subtracted_data,
                                 com =  self.center_of_mass)
        else:
             raise NameError("Data not found.")


    def display2d(self): # Graphs a plotly contour plot
        if (self.center_data.any()):
            Display.plot2d(self.center_data, self.center_f, self.center_of_mass)
        else:
             raise NameError("Data not found.")

def main():
    d = Data(data_file="Data Examples/BioSANS_exp253_scan0015_0001.xml",
            center_file = "Data Examples/BioSANS_exp253_scan0010_0001.xml",
            background_file="Data Examples/BioSANS_exp253_scan0011_0001.xml")
    d.setup()
    d.display1d()
if __name__ == "__main__":
    main()
