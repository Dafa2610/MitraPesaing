import geopandas as gpd
import pandas as pd


def olahdata(data): #program untuk mengolah geom
    data_fix = gpd.GeoDataFrame(data, 
                       geometry=gpd.points_from_xy(data.lat, data.lng))


    return data_fix
