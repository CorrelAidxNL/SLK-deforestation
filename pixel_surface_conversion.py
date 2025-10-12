from utils import *

RESOLUTION = 10


def count_non_nulls(map):
    return np.count_nonzero(~np.isnan(map))


def pixels_to_ha(map, resolution=RESOLUTION):
    pixel_area_ha = (resolution ** 2) / 10_000.0
    return count_non_nulls(map) * pixel_area_ha


def pixels_to_km(map, resolution=RESOLUTION):
    pixel_area_km2 = (resolution ** 2) * 1e-6
    return count_non_nulls(map) * pixel_area_km2


def class_pixels_to_km(map, class_label, resolution=RESOLUTION):
    pixel_area_km2 = (resolution ** 2) * 1e-6
    return count_non_nulls(np.where(map == class_label, map, np.nan)) * pixel_area_km2

