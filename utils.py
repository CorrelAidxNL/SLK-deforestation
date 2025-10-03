import matplotlib.pyplot as plt
import numpy as np
import rasterio
import math

FILE_PATH = "./files/S2/"
FILE_SUFFIX = "Kosovo_S2_"  # "Kosovo_S2_"#"Kosovo_L8_B4B5_"

RESOLUTION = 10
NDVI_FOREST_TRESHOLD = 0.6


def get_file_name(year):
    return FILE_PATH + f'/{year}/' + FILE_SUFFIX + f'{year}' + ".tif"


def title_to_file_plot(title):
    return title.replace(" ", "") + ".jpg"


def save_boxplot(data, title):
    data_valid = data[~np.isnan(data)]
    plt.figure()
    plt.boxplot(data_valid)
    plt.title(title)
    plt.savefig(title_to_file_plot(title), dpi=300, bbox_inches='tight')


def ndvi_calc(nir, red):
    return (nir - red) / (nir + red + 1e-6)


def get_forests_ndvi(ndvi_map, forest_treshold=NDVI_FOREST_TRESHOLD):
    return np.where(ndvi_map > forest_treshold, ndvi_map, np.nan)


def get_forest_map(ndvi_map, forest_treshold=NDVI_FOREST_TRESHOLD):
    return np.where(ndvi_map > forest_treshold, 1, np.nan)


def get_stats_years(years_analysed):
    '''
    Ndvi rage and
    :param years_analysed:
    :return:
    '''

    stats_years = []

    for year_a in years_analysed:
        stats = get_ndvi_analysis(year_a)
        stats_years.append(stats)
    print(stats_years)


def get_red_nir_stats(year_analysed):
    '''
    :param year_analysed:
    :return:
    Opens file, plots the ndvi (full), returns ndvi
    '''
    src = rasterio.open(get_file_name(year_analysed))
    print("Bounds:", src.bounds)
    print("Bands:", src.count)

    red = src.read(1).astype('float32')
    nir = src.read(2).astype('float32')

    red_stats = (np.nanmin(red), np.nanmax(red), np.nanmean(red))
    nir_stats = (np.nanmin(nir), np.nanmax(nir), np.nanmean(nir))

    print("Red band stats:", red_stats)
    print("NIR band stats:", nir_stats)

    return (red_stats, nir_stats)


def get_ndvi(year_analysed):
    '''
    :param year_analysed:
    :return:
    '''
    src = rasterio.open(get_file_name(year_analysed))
    print("Opened file")
    red = src.read(1).astype('float32')
    nir = src.read(2).astype('float32')
    print("Start ndvi calculation")
    ndvi = ndvi_calc(nir, red)
    return ndvi


def get_ndvis(years):
    '''
    :param year_analysed:
    :return:
    '''
    data = []
    for year in years:
        src = rasterio.open(get_file_name(year))
        red = src.read(1).astype('float32')
        nir = src.read(2).astype('float32')
        ndvi = ndvi_calc(nir, red)
        data.append(ndvi)
    print("NDVI calculated")

    return data


def get_ndvi_analysis(year_analysed):
    '''

    :param ndvi:
    :param year_analysed:
    :return:
    '''
    ndvi = get_ndvi(year_analysed)
    print(f"{year_analysed} NDVI range:", np.nanmin(ndvi), np.nanmax(ndvi))
    save_boxplot(ndvi, f"S2_ndvi_boxplot_{year_analysed}")
    return (np.nanmin(ndvi), np.nanmax(ndvi))


##########PLOTIGNG
def get_subplots(years):
    n_years = len(years)

    # Calculate optimal grid layout (prefer wider layouts)
    if n_years == 1:
        nrows, ncols = 1, 1
    elif n_years == 2:
        nrows, ncols = 1, 2
    elif n_years <= 4:
        nrows, ncols = 2, 2
    elif n_years <= 6:
        nrows, ncols = 2, 3
    elif n_years <= 9:
        nrows, ncols = 3, 3
    else:
        ncols = 4
        nrows = math.ceil(n_years / ncols)

    # Create figure with subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 5 * nrows))
    return fig, axes


# G3

def pixels_to_ha(map, resolution=RESOLUTION):
    return np.count_nonzero(~np.isnan(map)) * (resolution ^ resolution) / 10000
