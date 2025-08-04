# apps/new_app.py

import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import matplotlib
import json

# Load credentials from secrets
service_account_info = st.secrets["gcp_account"]
credentials = ee.ServiceAccountCredentials(
    service_account_info["client_email"],
    key_data=json.dumps(dict(service_account_info))
)
ee.Initialize(credentials)

st.set_page_config(layout="wide", page_title="India's ONE | Thematic Map")

st.sidebar.title("Project Repository")
st.sidebar.info(
    """
    [https://github.com/openlandcover/one7types](https://github.com/openlandcover/one7types)
    """
)

st.sidebar.title("Terms of Use")
st.sidebar.markdown(
    """
    This map data and analysis code are available for free and open public use, under [MIT License](https://mit-license.org/).
    """
)

st.sidebar.title("[Contact Us](https://forms.gle/r4NiLoEjVRaHoTE48)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link("app.py", label="Home", icon="🏠", use_container_width=True)
with col2:
    st.page_link("pages/01_Thematic_Map.py", label="**Thematic Map**", use_container_width=True)
with col3:
    st.page_link("pages/02_Probabilistic_Map.py", label="**Probabilistic Map**", use_container_width=True)
with col4:
    st.page_link("pages/03_Data_License.py", label="**Code, Data & License**", use_container_width=True)
with col5:
    st.page_link("pages/99_Funding_and_Support.py", label="**Funding and Support**", use_container_width=True)

st.divider()

def app():
    st.title("Thematic Map of Open Natural Ecosystems", anchor = "landcovers-thematic")

    with st.expander("**See a brief description of the types of ONE**"):
        col11, col12 = st.columns([1, 4])
        col11.markdown("**_Others_**")
        col12.markdown("""
            Forests, tree plantations, agricultural areas, built-up areas,
            open water and wetlands.""")
        col21, col22 = st.columns([1, 4])
        col21.markdown("**_Dune_**")
        col22.markdown("""
            Areas where the soil substrate is predominantly sandy,
            with the vegetation being mostly short-statured, sparsely distributed
            and occurring in clumps.""")
        col31, col32 = st.columns([1, 4])
        col31.markdown("**_Ravine_**")
        col32.markdown("""
            Areas with deep gullies following substrate erosion patterns.
            Tree cover is sparse, if at all, and ground vegetation is
            shrub- and grass-dominated.""")
        col41, col42 = st.columns([1, 4])
        col41.markdown("**_Saline_**")
        col42.markdown("""
            Salt marshes of The Rann of Kutchch.""")
        col51, col52 = st.columns([1, 4])
        col51.markdown("**_Bare or sparsely vegetated_**")
        col52.markdown("""
            Areas with no trees and little or no ground vegetation.
            Ground vegetation, if it occurs, is sparsely distributed.""")
        col61, col62 = st.columns([1, 4])
        col61.markdown("**_Open Savanna_**")
        col62.markdown("""
            Areas with grasses and shrubs in the understorey and trees above.
            Tree cover is very sparse.""")
        col71, col72 = st.columns([1, 4])
        col71.markdown("**_Shrub Savanna_**")
        col72.markdown("""
            Areas with grasses and shrubs in the understorey and trees above.
            Tree cover is sparse. Understorey can include short-statured
            woody vegetation.""")
        col81, col82 = st.columns([1, 4])
        col81.markdown("**_Woodland Savanna_**")
        col82.markdown("""
            Areas with grasses and shrubs in the understorey and trees above.
            Tree cover is moderate. Large openings in the tree canopy cover remain,
            and the understorey is predominantly grasses.""")

    # Prepare Earth Engine Image and remap as before
    mapRaster = ee.Image("projects/ee-open-natural-ecosystems/assets/publish/onesWith7Classes/landcover_hier")
    l2Labels = mapRaster.select("l2LabelNum") \
        .remap([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
               [1, 1, 6, 1, 3, 2, 4, 5, 7,  8,  9,  1])
    # l1Labels = mapRaster.select("l1LabelNum").remap([200, 100], [1, 0])  # Not used below

    # Define palette using matplotlib colour names
    palette = [
        matplotlib.colors.cnames["black"],         # Others
        matplotlib.colors.cnames["darkgreen"],     # Forest
        matplotlib.colors.cnames["khaki"],         # Dune
        matplotlib.colors.cnames["fuchsia"],       # Ravine
        matplotlib.colors.cnames["lightsteelblue"],# Saline
        matplotlib.colors.cnames["beige"],         # Bare/sparsely veg.
        matplotlib.colors.cnames["yellow"],        # Open Savanna
        matplotlib.colors.cnames["goldenrod"],     # Shrub Savanna
        matplotlib.colors.cnames["greenyellow"],   # Woodland Savanna
    ]

    vis_params = {
        "min": 1,
        "max": 9,
        "palette": palette,
    }

    # Get EE map tile for folium
    map_id_dict = ee.Image(l2Labels).getMapId(vis_params)

    # Create folium map
    m = folium.Map(location=[21, 79], zoom_start=5, control_scale=True, tiles='CartoDB positron')

    # Add EE Image as tile layer to folium map
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name='ONE Types',
        overlay=True,
        control=True,
        opacity=0.7
    ).add_to(m)

    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google Satellite",
        name="SATELLITE",
        overlay=False,
        control=True
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Optional: Add legend manually via Streamlit
    with st.expander("Show map legend"):
        st.markdown("""
        <div style='display: flex; flex-direction: column; gap: 4px;'>
            <span><span style='background-color: black; display:inline-block; width:15px; height:15px;'></span> Others</span>
            <span><span style='background-color: darkgreen; display:inline-block; width:15px; height:15px;'></span> Forest</span>
            <span><span style='background-color: khaki; display:inline-block; width:15px; height:15px;'></span> Dune</span>
            <span><span style='background-color: fuchsia; display:inline-block; width:15px; height:15px;'></span> Ravine</span>
            <span><span style='background-color: lightsteelblue; display:inline-block; width:15px; height:15px;'></span> Saline</span>
            <span><span style='background-color: beige; display:inline-block; width:15px; height:15px;'></span> Bare or sparsely vegetated</span>
            <span><span style='background-color: yellow; display:inline-block; width:15px; height:15px;'></span> Open Savanna</span>
            <span><span style='background-color: goldenrod; display:inline-block; width:15px; height:15px;'></span> Shrub Savanna</span>
            <span><span style='background-color: greenyellow; display:inline-block; width:15px; height:15px;'></span> Woodland Savanna</span>
        </div>
        """, unsafe_allow_html=True)

    st_folium(m, height=768, width=1024)

app()