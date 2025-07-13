# Immigration Insights

**Immigration Insights** is my Python-based project for visualizing recent immigration trends across Canadian geographic areas. By combining census demographic data with spatial shapefiles, this project generates interactive maps using [Folium](https://python-visualization.github.io/folium/), enabling users to explore Canadian immigration trends.

---

## Features

- **Interactive Mapping:** Generates HTML maps with color-coded regions based on recent immigrant counts.
- **Spatial Data Processing:** Merges census data with Canadian geographic boundaries.
- **Geometry Simplification:** Optimizes map performance by simplifying geometries outside major cities.
- **Customizable Visualization:** Easily adjust color schemes, quantiles, and tooltips.
- **Reproducible Workflow:** Simple, script-based pipeline for data loading, processing, and visualization.

---

## Project Structure

```
immigration-insights/
├── data/           # Raw and processed data files (excluded by .gitignore)
├── dashboard.py    # Main script for data processing and map generation
├── requirements.txt # Python dependencies
├── README.md       # Project documentation
├── .gitignore      # Git ignore rules
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NumeralTiger/immigration-insights.git
cd immigration-insights
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Data

- Download the latest **Census Data** (CSV) from [Statistics Canada](https://www12.statcan.gc.ca/census-recensement/index-eng.cfm).
- Download **Geographic Shapefiles** (e.g., .shp, .dbf, .shx, etc.) from [Statistics Canada GeoSuite](https://www150.statcan.gc.ca/n1/en/catalogue/92-150-X).
- Place your census CSV and shapefile components in the `data/` directory.
- Check the filenames and if needed change them in `dashboard.py` if your files have different names.

### 4. Run the Dashboard Script

```bash
python dashboard.py
```

This will generate an interactive map as `ada_map.html` in your project root.

---

## Data Sources

- **Census Data:** Downloaded from Statistics Canada
- **Geographic Shapefiles:** Downloaded from Statistics Canada GeoSuite

---

## Customization

- **Cities List:** Edit the `cities` variable in `dashboard.py` to change which cities are excluded from geometry simplification.
- **Colormap:** Adjust the color palette and quantile breaks in the `StepColormap` section.
- **Tooltip Fields:** Modify the fields and aliases in the `GeoJsonTooltip` for different popup information.
