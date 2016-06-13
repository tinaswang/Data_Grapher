from Parser import Parser
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy import stats
from Display import PlotlyDisplay


class Integrator(object):

    def __init__(self, data_file, background_file):
        self.filename = data_file
        self.p = Parser(data_file)
        self.parsed_data = self.p.parse()
        self.data = np.array(self.p.xpath_get("/SPICErack/Data/Detector/data"))
        self.com = self.get_center_of_mass(self.data)
        self.subtract(background_file)

    def get_center_of_mass(self, data):
        plotly = PlotlyDisplay(self.filename)
        com = plotly.get_center_of_mass(plotly.get_data(self.filename))
        return com

    def subtract(self, background_file):
        p2 = Parser(background_file)
        background_data = np.array(p2.xpath_get("/SPICErack/Data/Detector/data"))
        difference = self.data - background_data
        return difference

    def integrate(self):
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

        n_bins = 100
        bin_means, bin_edges, binnumber = stats.binned_statistic(theta, values.flatten(), statistic='mean', bins=n_bins)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width/2
        plt.figure()
        plt.plot(bin_centers , bin_means)
        plt.show()

def main():
    integrator = Integrator("Data Examples/HiResSANS_exp9_scan0030_0001.xml"
                            , "Data Examples/HiResSANS_exp9_scan0038_0001.xml")
    integrator.integrate()

if __name__ == "__main__":
    main()
