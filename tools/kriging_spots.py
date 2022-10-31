import pandas as pd
import numpy as np
from pykrige.ok import OrdinaryKriging
import plotnine
from plotnine import *
import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cmaps
from matplotlib.path import Path
from matplotlib.patches import PathPatch


data = [{"lon": 114.5383, "lat": 32.2075, "tmp": 12}, {"lon": 115.3156, "lat": 34.4867, "tmp": 5},
        {"lon": 115.2414, "lat": 36.0581, "tmp": 14}, {"lon": 112.7564, "lat": 34.9139, "tmp": 22.5},
        {"lon": 112.3717, "lat": 32.5825, "tmp": 26.5}, {"lon": 112.3958, "lat": 34.4214, "tmp": 15},
 
        {"lon": 113.7156, "lat": 34.3778, "tmp": 19},{"lon": 114.8497, "lat": 34.0744, "tmp": 16},
        {"lon": 112.4697, "lat": 34.1603, "tmp": 8},{"lon": 114.2947, "lat": 34.8022, "tmp": 15},
        ]


def main():
    
    df_data= pd.read_csv("C:\\Users\Jarvis\Desktop\henan_geojson\\tmps.csv")
    
    # 读取站点经度
    lons = df_data['lon']
    # 读取站点纬度
    lats = df_data['lat']
    tmps = df_data['tmp']

    # tmps = list()
    # for d in data:
    #     lons.append(float(d["lon"]))
    #     # 读取站点纬度
    #     lats.append(float(d["lat"]))
    #     # 读取梅雨量数据
    #     tmps.append(float(d["tmp"]))


    # 生成经纬度网格点
    grid_lon = np.linspace(110.21, 116.39,480)
    grid_lat = np.linspace(31.23, 36.22,240)

    gaussian_kriging = OrdinaryKriging(lons, lats, tmps, variogram_model='gaussian', nlags=6)
    z1, ss1 = gaussian_kriging.execute('grid', grid_lon, grid_lat)
    print(z1.shape)

    # 转换成网格
    xgrid, ygrid = np.meshgrid(grid_lon, grid_lat)

    # 将插值网格数据整理
    df_grid = pd.DataFrame(dict(long=xgrid.flatten(), lat=ygrid.flatten()))
    # 插值结果
    df_grid["Krig_gaussian"] = z1.flatten()

    # sh = gpd.read_file('./tools/410000.shp')
    # sh.plot()
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([110.21, 116.39, 31.23, 36.22], crs=ccrs.PlateCarree())

    province = shpreader.Reader('./tools/410000.shp')
    ax.add_geometries(province.geometries(), crs=ccrs.PlateCarree(), linewidths=0.5,edgecolor='k',facecolor='none')

    print(xgrid)
    cf = ax.contourf(xgrid, ygrid, z1, levels=np.linspace(0,30,10), cmap=cmaps.MPL_rainbow, transform=ccrs.PlateCarree())

    def shp2clip(originfig, ax, shpfile):
        sf = shapefile.Reader(shpfile)
        vertices = []
        codes = []
        for shape_rec in sf.shapeRecords():
            pts = shape_rec.shape.points
            prt = list(shape_rec.shape.parts) + [len(pts)]
            for i in range(len(prt) - 1):
                for j in range(prt[i], prt[i + 1]):
                    vertices.append((pts[j][0], pts[j][1]))
                codes += [Path.MOVETO]
                codes += [Path.LINETO] * (prt[i + 1] - prt[i] - 2)
                codes += [Path.CLOSEPOLY]
            clip = Path(vertices, codes)
            clip = PathPatch(clip, transform=ax.transData)
        for contour in originfig.collections:
            contour.set_clip_path(clip)
        return contour

    shp2clip(cf, ax, './tools/410000.shp')

    cb = plt.colorbar(cf)
    cb.set_label('temperature (℃)',fontsize=15)

    plt.show()
    


if __name__ == '__main__':
    main()
