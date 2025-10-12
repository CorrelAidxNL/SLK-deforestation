from rasterio.warp import reproject, Resampling

from pixel_surface_conversion import *

impact = rasterio.open("files/Data Impact observatory/2018 3a04cb6533_assets/kosovo_20180101-20181231_data.tif")
impact_map = impact.read(1)

unique_elements, counts = np.unique(impact_map, return_counts=True)
data_no_nan = unique_elements[~np.isnan(unique_elements)]
plt.figure(figsize=(8, 5))
plt.bar(unique_elements, counts, color='green', edgecolor='black')
plt.xlabel('IO Map  Class')
plt.ylabel('Count')
plt.xticks(unique_elements)
plt.show()

country_surface = pixels_to_km(np.where(impact_map == 0, np.nan, impact_map), resolution=10)
tree_surface = class_pixels_to_km(impact_map, 2) / country_surface

print(tree_surface)
# 44% trees


### corine check
corine_path = "files/new_Forest_Mask_CORINE2018.tif"  # replace with your path
corine = rasterio.open(corine_path)
corine_map = corine.read(1)

# Undersampling ndvi to match Corine size

impact_map_undersampled = np.empty((corine.height, corine.width), dtype=impact_map.dtype)

reproject(
    source=impact_map,
    destination=impact_map_undersampled,
    src_transform=impact.transform,
    src_crs=impact.crs,  # Use the actual CRS
    dst_transform=corine.transform,
    dst_crs=corine.crs,  # Use Corine CRS
    resampling=Resampling.nearest
)


unique_elements, counts = np.unique(impact_map_undersampled, return_counts=True)
country_surface = pixels_to_km(np.where(impact_map_undersampled == 0, np.nan, impact_map_undersampled), resolution=100)
print(class_pixels_to_km(impact_map_undersampled, 2, 100) / country_surface)

import numpy as np

def filter_by_flag(data_array, mask_array, map_flag):
    """
    Preserve values from data_array where mask_array equals map_flag,
    otherwise set to np.nan.

    Parameters:
        data_array (np.ndarray): Array to filter
        mask_array (np.ndarray): Array to check flags
        map_flag (int/float): Value in mask_array to preserve

    Returns:
        np.ndarray: Filtered array
    """
    # Create a new array filled with nan
    filtered = np.full_like(data_array, np.nan, dtype=float)

    # Preserve values where mask_array equals map_flag
    filtered[mask_array == map_flag] = data_array[mask_array == map_flag]

    return filtered


trees_from_corina_map = filter_by_flag(impact_map_undersampled, corine_map, 1)
data_no_nan = trees_from_corina_map[~np.isnan(trees_from_corina_map)]

unique_elements, counts = np.unique(data_no_nan, return_counts=True)

plt.figure(figsize=(8, 5))
plt.bar(unique_elements, counts, color='green', edgecolor='black')
plt.xlabel('IO Map  Class')
plt.ylabel('Count')
plt.title('IO Classess from Cortina Tree layer')
plt.xticks(unique_elements)  # show all unique elements on x-axis
plt.show()
