from Parser import Parser
import numpy as np
from Display import Display
from Operations import Operations

class Data(object):

    def __init__(self, data_file, center_file, background_file):
        self.data_f = data_file
        if center_file not None:
            self.center_f = center_file
        if background_file not None:
            self.backgrd_f = background_file
        # self.config = config

    def get_data(self, p):
        get_data.detector_data = np.array(p.xpath_get("/SPICErack/Data/Detector/data"))
        get_data.distance_1 = p.xpath_get("/SPICErack/Motor_Positions/sample_det_dist/#text")
        get_data.distance_2 = p.xpath_get("/SPICErack/Header/sample_to_flange/#text")
        get_data.pixel_size_x = p.xpath_get("/SPICErack/Header/x_mm_per_pixel/#text")
        get_data.pixel_size_y = p.xpath_get("/SPICErack/Header/y_mm_per_pixel/#text")
        get_data.translation = p.xpath_get("/SPICErack/Motor_Positions/detector_trans/#text")
        get_data.dim_x = p.xpath_get("/SPICErack/Header/Number_of_X_Pixels/#text")
        get_data.dim_y = p.xpath_get("/SPICErack/Header/Number_of_Y_Pixels/#text")

    def setup(self):
        op = Operations()
        p_data = Parser(self.data_f)
        data = p_data.parse()
        self.translated_data = op.translate(data, p_data)
        if self.center_f:
            p_center = Parser(self.center_f)
            center_data = Data(p_center)
            self.translated_center = op.translate(center_data,detector_data, p_center)
        if self.backgrd_f:
            p_backgrd = Parser(self.background_f)
            backgdr_data = Data(p_backgrd)
            self.translated_backgrd = op.translate(backgrd_data, p_backgrd)
            self.subtracted_data = op.subtract(self.data_f, self.backgrd_f)

    def display1D(self):
        Operations.integrate(self.subtracted_data)

    def display2d(self):
        Display.plot2d(self.center_data,Operations.center_of_mass(center_data))


def main():
    pass
if __name__ == "__main__":
    main()
