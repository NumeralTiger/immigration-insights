import time, json 
import pandas as pd
import geopandas as gpd
import folium
from branca.colormap import StepColormap


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

start_total = time.time()

# 1) Load CSV
log("Loading CSV")
ada_df = pd.read_csv("ADA_profile_simplified(ada_profile_simplified).csv", encoding="latin1")
ada_df["recent_immigrants"] = ada_df["T1536"].fillna(0)
ada_df["ADA_code"] = ada_df["ADA_code"].astype(str)

# 2) Load shapefile and reproject
log("Loading shapefile")
ada_gdf = gpd.read_file("lada000b21a_e.shp").to_crs(epsg=4326)
ada_gdf["ADAUID"] = ada_gdf["ADAUID"].astype(str)

# 3) Merge
def style_function(feat):
    val = feat["properties"]["recent_immigrants"] or 0
    return {
        "fillColor": colormap(val),
        "color": "black",
        "weight": 0.1,
        "fillOpacity": 0.6
    }

log("Merging data")
ada_gdf = ada_gdf.merge(
    ada_df,
    left_on="ADAUID",
    right_on="ADA_code",
    how="inner"
)
log(f"Merged: {len(ada_gdf)} ADAs")

# 4) Simplify geometries
log("Simplifying geometries (outside major cities)")
t0 = time.time()

cities = ["Toronto", "Montréal", "Vancouver", "Calgary", "Ottawa", "Edmonton"]
mask = ada_gdf["CSDNAME"].isin(cities)

ada_gdf.loc[~mask, "geometry"] = ada_gdf.loc[~mask, "geometry"].simplify(
    tolerance=0.01, preserve_topology=True
)

log(f"Simplification done in {time.time() - t0:.1f}s")

# 5) GeoJSON
log("Serializing to GeoJSON")
t0 = time.time()
geojson_data = json.loads(ada_gdf.to_json())
log(f"Serialized {len(geojson_data['features'])} features in {time.time() - t0:.1f}s")

# 6) Build map
log("Building Folium map")
m = folium.Map(location=[56.13, -106.35], zoom_start=4)

# 7) Build quantile-based Viridis colormap (legend removed)
breaks = ada_gdf["recent_immigrants"].quantile([0, .2, .4, .6, .8, 1]).tolist()
colormap = StepColormap(
    # list of Viridis colors from branca
    ['#440154', '#414487', '#2A788E', '#22A884', '#7AD151'],
    index=breaks,
    vmin=breaks[0],
    vmax=breaks[-1]
)

# 8) Add layer with tooltips
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["CSDNAME", "recent_immigrants"],
        aliases=["Area:", "Recent immigrants:"]
    )
).add_to(m)

# 9) Save map without legend bar
m.save("ada_map.html")
log("Map saved to ada_map.html")
log(f"Total runtime: {time.time() - start_total:.1f}s")
