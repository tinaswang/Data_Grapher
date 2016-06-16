from Parser import Parser
import numpy as np
import scipy.ndimage as ndimage
import numpy as np
from scipy import stats


class Operations(object):

    def __init__(self):
        pass

    @staticmethod
    def get_center_of_mass(center_data):
        hist, bins = np.histogram(center_data.ravel(), normed=False, bins=49000)
        threshold = bins[np.cumsum(bins) * (bins[1] - bins[0]) > 30000][0]
        mnorm2d = np.ma.masked_less(center_data, threshold)
        com = ndimage.measurements.center_of_mass(mnorm2d)
        return com

    @staticmethod
    def subtract(data, background_data):
        difference = data - background_data
        return difference

    @staticmethod
    def get_data(p):
        detector_data = np.array(p.xpath_get("/SPICErack/Data/Detector/data"))
        distance_1 = p.xpath_get("/SPICErack/Motor_Positions/sample_det_dist/#text")
        distance_2 = p.xpath_get("/SPICErack/Header/sample_to_flange/#text")
        pixel_size_x = p.xpath_get("/SPICErack/Header/x_mm_per_pixel/#text")
        pixel_size_y = p.xpath_get("/SPICErack/Header/y_mm_per_pixel/#text")
        translation = p.xpath_get("/SPICErack/Motor_Positions/detector_trans/#text")
        dim_x = p.xpath_get("/SPICErack/Header/Number_of_X_Pixels/#text")
        dim_y = p.xpath_get("/SPICErack/Header/Number_of_Y_Pixels/#text")
        return detector_data, distance_1, distance_2,pixel_size_x,pixel_size_y, translation, dim_x, dim_y

    @staticmethod
    def integrate(parser, com, difference):
        ycom, xcom = com
        detector_data, distance_1, distance_2,pixel_size_x, pixel_size_y, translation, dim_x, dim_y = Operations.get_data(parser)
        Z = distance_1 + distance_2
        z = np.full((dim_x*dim_y), Z)

        xx_pixels, yy_pixels = np.mgrid[0:dim_x, 0:dim_y]
        dist = np.hypot(xx_pixels, yy_pixels)  # Linear distance from point 0,0

        x_coords = np.linspace(-xcom, (pixel_size_x *dim_x) - xcom, dim_x)
        y_coords = np.linspace(-ycom, (pixel_size_y * dim_y) - ycom, dim_y)
        xx_coords, yy_coords = np.meshgrid(x_coords, y_coords)

        v = np.stack((xx_coords.flatten(), yy_coords.flatten(), z), axis=-1)
        u = np.stack((np.zeros(dim_x*dim_y), np.zeros(dim_x*dim_y), z), axis=-1)
        theta = np.arccos(np.sum (u*v, axis=1) / (np.linalg.norm(u,axis=1) * np.linalg.norm(v , axis=1)))

        # Integration
        n_bins = 100
        bin_means, bin_edges, binnumber = stats.binned_statistic(theta, difference.flatten(), statistic='mean', bins=n_bins)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width/2

        return bin_centers, bin_means


    @staticmethod
    def get_axes_units(data_shape, pixel_size):
        """
        pixel_size in mm
        get default units with center as center of the images
        """
        i_center = data_shape[1]/2
        j_center = data_shape[0]/2
        x_axis_units = (np.arange(data_shape[1])-i_center) * pixel_size[1]
        y_axis_units = (np.arange(data_shape[0])-j_center) * pixel_size[0]
        return x_axis_units, y_axis_units

def main():
    pass
if __name__ == "__main__":
    main()
