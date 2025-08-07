# apps/new_app.py

import streamlit as st
import ee
import geemap.foliumap as geemap
import matplotlib

st.set_page_config(layout="wide", page_title="India's ONE | Probabilistic Map")

st.sidebar.title("Project Repository")
st.sidebar.info(
    """
    [https://github.com/openlandcover/one7types](https://github.com/openlandcover/one7types)
    """
)

# st.sidebar.title("Contact")
# st.sidebar.info(
#     """
#     """
# )

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
    st.title("Probabilistic Map of Open Natural Ecosystems", anchor = "landcovers-probabilistic")

    m = geemap.Map(center=(21, 79), zoom=5.2, control_scale=True)

    mapRaster = ee.Image("projects/ee-open-natural-ecosystems/assets/publish/onesWith7Classes/landcover_hier")
    l2OneProbs = mapRaster.select(["prob_one_.*"]).divide(1e4)
    l2NononeProbs = mapRaster.select(["prob_nonone_.*"]).divide(1e4)
    l1Probs = mapRaster.select(["prob_one", "prob_nonone"]).divide(1e4)

    oneProb = l2OneProbs.reduce(ee.Reducer.sum()).rename("one")
    agrProb = l2NononeProbs.select(["prob_nonone_agri_.*"]).reduce(ee.Reducer.sum()).rename("agr")
    othProb = l2NononeProbs.select("prob_nonone_forest").rename("oth")
    oneAgrOthRgb = ee.Image.cat([agrProb, oneProb, othProb])

    m.add_basemap("SATELLITE")
    # left_layer = geemap.ee_tile_layer(l1Probs, {"bands": ["prob_one"], "min": 0, "max": 1, "palette": ["1a2b2b", matplotlib.colors.cnames["navajowhite"]]}, name = "ONE probabilities")
    # right_layer = geemap.ee_tile_layer(oneAgrOthRgb, {"min": 0, "max": 1}, name = "Agri-ONE-Forest probabilities")
    # m.split_map(left_layer, right_layer)

    # st.markdown(
    #     """
    #     In the map above, the left panel shows the probability of Open Natural Ecosystems (ONE) at the 
    #     Level-1 classification (ONE / Non-ONE), while the right panel aggregates the probability of Agriculture (Red), 
    #     ONEs (Green), and Forest (Blue) at the Level-2 classification. The brighter and greener a pixel 
    #     in the right panel, the higher the probability that it is an ONE; likewise, brighter and redder 
    #     a pixel, the higher the probability that it is Agriculture, and the brighter and bluer a pixel, 
    #     the higher the probability that it is Forest.
    #     """
    # )

    m.addLayer(oneAgrOthRgb, {"min": 0, "max": 1}, "Agri-ONE-Forest probabilities")

    m.to_streamlit(height = 768, width=1024)

    st.markdown(
        """
        The map above illustrates the probabilistic component of the map dataset. It visualizes aggregates the
        probability of Agriculture (Red), ONEs (Green), and Forest (Blue) at once. The brighter and greener a pixel,
        the higher the probability that it is an ONE; likewise, brighter and redder 
        a pixel, the higher the probability that it is Agriculture, and the brighter and bluer a pixel, 
        the higher the probability that it is Forest.
        """
    )
app()