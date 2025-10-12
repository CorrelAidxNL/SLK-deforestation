import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from utils import *
from rasterio.warp import reproject, Resampling
from pixel_surface_conversion import *


year = "2018"

sentinel_source_path = "files/S2_new/2018/Kosovo_S2_2018.tif"
sentinel_source = rasterio.open(sentinel_source_path)



ndvi_array = get_ndvi(year)

corine_path = "files/new_Forest_Mask_CORINE2018.tif"
corine = rasterio.open(corine_path)
corine_map = corine.read(1)



# Undersampling ndvi to match Corine size

ndvi_undersampled = np.empty((corine.height, corine.width), dtype=ndvi_array.dtype)

reproject(
    source=ndvi_array,
    destination=ndvi_undersampled,
    src_transform=sentinel_source.transform,
    src_crs='EPSG:4326',
    dst_transform=corine.transform,
    dst_crs='EPSG:4326',
    resampling=Resampling.bilinear
)



def plot_ndvi(data, title, cmap='RdYlGn', vmin=-1.0, vmax=1.0, figsize=(10, 8)):
    """
    Create and display an NDVI plot

    Parameters:
    - data: 2D array of NDVI values
    - title: plot title
    - cmap: colormap (default 'RdYlGn')
    - vmin: minimum value for colorbar
    - vmax: maximum value for colorbar
    - figsize: figure size tuple
    """
    fig, ax = plt.subplots(figsize=figsize)
    img = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_title(title)
    plt.colorbar(img, ax=ax, label='NDVI')
    return fig, ax

# # Plot 1: NDVI resampled
# plot_ndvi(ndvi_array, 'NDVI original')
# plt.show()
#
#
# # Plot 1: NDVI resampled
# plot_ndvi(ndvi_undersampled, 'NDVI resampled')
# plt.show()
#
# # Plot 2: NDVI for forests
# ndvi_corine_forests = np.where(corine_map == 1, ndvi_undersampled, np.nan)
# plot_ndvi(ndvi_corine_forests, 'NDVI with CORINE Land Cover Overlay - Forest')
# plt.show()
#
# # Plot 3: NDVI for non-forests
# ndvi_corine_non_forests = np.where(corine_map != 1, ndvi_undersampled, np.nan)
# plot_ndvi(ndvi_corine_non_forests, 'NDVI with CORINE Land Cover Overlay - Non Forest')
# plt.show()
#
# # Plot 4: Non-forest with NDVI higher than forest threshold
# ndvi_corine_non_forests_high_ndvi = np.where(ndvi_corine_non_forests >= 0.6, ndvi_corine_non_forests, np.nan)
# plot_ndvi(ndvi_corine_non_forests_high_ndvi, 'NDVI with CORINE Land Cover Overlay - Non Forest (High NDVI ≥ 0.6)')
# plt.show()
#







def print_nump_stats(data):
    print("================================")
    print("Mean:", np.nanmean(data))
    print("Median:", np.nanmedian(data))
    print("Standard Deviation:", np.nanstd(data))
    print("Variance:", np.nanvar(data))
    print("Minimum:", np.nanmin(data))
    print("Maximum:", np.nanmax(data))
    print("25th Percentile:", np.nanpercentile(data, 25))
    print("75th Percentile:", np.nanpercentile(data, 75))
    print("================================")



# print_nump_stats(ndvi_corine_forests)
# print_nump_stats(ndvi_corine_non_forests)


# Labelling pixels in S2 using Corine labelled pixels

corine_oversampled = np.empty((sentinel_source.height, sentinel_source.width), dtype=corine_map.dtype)
reproject(
    source=corine_map,
    destination=corine_oversampled,
    src_transform=corine.transform,
    src_crs='EPSG:4326',
    dst_transform=sentinel_source.transform,
    dst_crs='EPSG:3857',
    resampling=Resampling.nearest # important
)

print(corine_oversampled.shape)
corine_forest_surface = pixels_to_km(np.where(corine_oversampled == 0, np.nan, corine_oversampled))
print(corine_forest_surface)

corine_forest_percent = corine_forest_surface / pixels_to_km(ndvi_array)
print(corine_forest_percent)