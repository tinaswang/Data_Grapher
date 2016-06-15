from Parser import Parser
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import scipy.optimize as opt
import numpy as np

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
    def translate(data, parser):
        translation = data.translation
        translation_pixels = translation / data.pixel_size_x

    @staticmethod
    def integrate(data):
        Z = data.distance_1 + data.distance_2
        z = np.full((data.dim_x*atadim_y), Z)

        xx_pixels, yy_pixels = np.mgrid[0:dim_x, 0:dim_y]
        dist = np.hypot(xx_pixels, yy_pixels)  # Linear distance from point 0,0
        values = np.square(5*np.cos(dist/200.0))

        x_coords = np.linspace(0.0, (pixel_size_x/1000) * dim_x, dim_x)
        y_coords = np.linspace(0.0, (pixel_size_y/1000) * dim_y, dim_y)
        xx_coords, yy_coords = np.meshgrid(x_coords, y_coords)

        v = np.stack((xx_coords.flatten(), yy_coords.flatten(), z), axis=-1)
        u = np.stack((np.zeros(dim_x*dim_y), np.zeros(dim_x*dim_y), z), axis=-1)
        theta = np.arccos(np.sum (u*v, axis=1) / (np.linalg.norm(u,axis=1) * np.linalg.norm(v , axis=1)))

        # Integration
        n_bins = 100
        bin_means, bin_edges, binnumber = stats.binned_statistic(theta, values.flatten(), statistic='mean', bins=n_bins)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width/2
        plt.figure()
        plt.plot(bin_centers,bin_means)

def main():
    pass
if __name__ == "__main__":
    main()
