# GE images were splitted into multiple parts. Script for mergin the images into 1 .tiff file.

import rasterio
from rasterio.merge import merge
import glob
import os

year = 2025

tiff_folder = f"files/S2/{year}/"
tiff_files = glob.glob(os.path.join(tiff_folder, "*.tif"))

src_files_to_mosaic = [rasterio.open(f) for f in tiff_files]

mosaic, out_trans = merge(src_files_to_mosaic)

# Copy the metadata of one of the source files
out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans
})

output_path = f"files/S2/{year}/Kosovo_S2_{year}.tif"
with rasterio.open(output_path, "w", **out_meta) as dest:
    dest.write(mosaic)

print(f"Merged TIFF saved to: {output_path}")
