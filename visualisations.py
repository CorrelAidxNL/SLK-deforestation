import numpy as np
from utils import *
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import math


def plot_forests_multi_year(years):
    """
    Plot forest areas for multiple years in subplots

    Parameters:
    -----------
    years : list
        List of years to analyze and plot
    """
    n_years = len(years)

    fig, axes = get_subplots(years)

    if n_years == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    # Create colormaps
    solid_cmap = ListedColormap(['gray'])
    solid_cmap_y = ListedColormap(['yellow'])

    # Plot each year
    for idx, year in enumerate(years):
        ax = axes[idx]
        ndvi_ = get_ndvi(year)
        forests = get_forests_ndvi(ndvi_)

        ndvi_plot = ax.imshow(ndvi_, cmap=solid_cmap)
        forest_layer = ax.imshow(forests, cmap=solid_cmap_y, alpha=0.5)

        ax.set_title(f"{str(year)}")
        ax.axis("off")

    # Hide any unused subplots
    for idx in range(n_years, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.savefig("forest_transformation.jpg", dpi=300, bbox_inches='tight')
    return fig, axes


def get_change(map1, map2):
    return map1 - map2


def plot_changes(data_over_years, labels):
    """
    """
    n_years = len(years)
    print(f"Plotting {n_years}")

    fig, axes = get_subplots(years)

    # Ensure axes is always a flat array for consistent indexing
    if n_years == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    changes = []
    for i in range(len(data_over_years) - 1):
        lable = (labels[i], labels[i + 1])

        # prev_forests
        prev_forests = get_forest_map(data_over_years[i], NDVI_FOREST_TRESHOLD)
        # current forests
        curr_forests = get_forest_map(data_over_years[i + 1], NDVI_FOREST_TRESHOLD)

        change_map = np.full(prev_forests.shape, np.nan)
        anytime_tree_presence = ~np.isnan(prev_forests) | ~np.isnan(curr_forests)
        print(np.count_nonzero(~np.isnan(anytime_tree_presence)))
        # where at least one timestamp has forest
        change_map[anytime_tree_presence] = np.nan_to_num(curr_forests[anytime_tree_presence]) - np.nan_to_num(
            prev_forests[anytime_tree_presence])

        changes.append((lable, change_map))

    for idx, (label, change_map) in enumerate(changes):
        ax = axes[idx]
        ax.set_title(f"{label[0]} - {label[1]}")
        ax.axis("off")

        plot_change(ax, change_map)

    for idx in range(len(changes)):
        axes[idx].axis('off')

    plt.tight_layout()

    return fig, axes


def plot_change(ax, change_map):
    cmap = ListedColormap(['red', 'white', 'green'])
    ax.imshow(change_map, cmap=cmap, vmin=-1, vmax=1)
    plt.title('Change map')


# 1. raw forests for visualisation
# does not seem correct
years = [2021, 2022, 2023, 2024, 2025]

# fig, axes = plot_forests_multi_year(years)
# plt.savefig("forest_visualiser.jpg", dpi=300, bbox_inches='tight')


# boxplots
# get_stats_years(years)


# 2. change ->  why nulls?
ndvis = get_ndvis(years)

fig, axes = plot_changes(ndvis, years)
plt.savefig("change_binary.jpg", dpi=300, bbox_inches='tight')

# 3. Pixels to surfaces

# def get_forest_surface_Ha(ndvi_map, forest_treshold):
#     forests = get_forests_ndvi(ndvi_map,forest_treshold)
#     return pixels_to_ha(forests)
#
# def get_forest_pixels_percent(ndvi_map, forest_treshold, resolution=10):
#     '''
#
#     :param ndvi_map:
#     :param foret_treshold:
#     :param resolution:
#     :return:
#     '''
#
#     #Why 27 2755 286? ~27 k^2 instead of 10
#     land_pixels = np.count_nonzero(~np.isnan(ndvi_map))
#
#     forests = get_forests_ndvi(ndvi_map)
#
#     return np.count_nonzero(~np.isnan(forests)) / land_pixels * 100


#### forest % , surface in real  measurements

# years = [2020,2021,2022,2023,2024,2025]
# maps = get_ndvis(years)
#
# print(maps[0].shape)

# for mp in maps:
#     print("Year ", years)
#     print(get_forest_pixels_percent(mp, NDVI_FOREST_TRESHOLD))
