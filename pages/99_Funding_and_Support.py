# Funding and Support page for India's Open Natural Ecosystems (ONE)
# Displays acknowledgments, funding sources, and technical support information
# Lists contributing organizations and open source tools used in the project

import streamlit as st

# Configure Streamlit page layout and metadata
st.set_page_config(layout="wide", page_title="India's ONE | Support")

# Navigation bar with page links
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link("app.py", label="Home", icon="🏠", width="stretch")
with col2:
    st.page_link("pages/01_Thematic_Map.py", label="**Thematic Map**", width="stretch")
with col3:
    st.page_link("pages/02_Probabilistic_Map.py", label="**Probabilistic Map**", width="stretch")
with col4:
    st.page_link("pages/03_Data_License.py", label="**Code, Data & License**", width="stretch")
with col5:
    st.page_link("pages/99_Funding_and_Support.py", label="**Funding and Support**", width="stretch")

st.divider()

# Sidebar content with project information
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

def app():
    """Main function to render the funding and support page"""
    st.title("Funding and support")

    # Financial support section
    st.markdown(
    """

    &nbsp;

    **Financial support for various aspects of this mapping work came from:**

    * 2019-2020: [ATREE](https://www.atree.org/)
    * 2020-2021: [Azim Premji University](https://azimpremjiuniversity.edu.in/) as part of the Research Funding Programme
    * 2020-2022: Nadathur Foundation
    * 2021-2022: [National Centre for Biological Sciences (NCBS)](https://www.ncbs.res.in/) via the [Archives at NCBS](https://archives.ncbs.res.in/), with the support of [TNQ Technologies](https://www.tnq.co.in/csr-activities/)
    * 2022 onwards: [The Habitats Trust](https://www.thehabitatstrust.org/)
    
    &nbsp;

    **Technical and Logistical Support:**
    * 2019 onwards: [Nature Conservation Foundation](https://www.ncf-india.org/)
    * 2021 onwards: [Mahesh Sankaran Lab](https://www.ncbs.res.in/faculty/mahesh), NCBS

    &nbsp;

    Further, our work would not be possible without the creativity and generosity of efforts of developers behind
    many free, public and open source scientific computation resources and software tools,
    chief among them being:
    * The [geemap](https://geemap.org/) package | Qiusheng Wu
    * [Spatial Thoughts](https://spatialthoughts.com/) | Ujaval Gandhi
    * [awesome-gee-community-catalog](https://gee-community-catalog.org/) | Samapriya Roy
    * [Google Earth Engine Developers Group](https://groups.google.com/g/google-earth-engine-developers)
    * [Google Earth Engine on Stack Exchange](https://gis.stackexchange.com/questions/tagged/google-earth-engine)
    * [QGIS](https://qgis.org/)
    * Yoni Gavish of [*Gavish et al. (2018)*](https://doi.org/10.1016/j.isprsjprs.2017.12.002)
    * Multiple publicly-funded central and state government portals and repositories

    These analyses were carried out on the [Google Earth Engine](https://earthengine.google.com/)
    cloud computing platform.
    """,
    unsafe_allow_html=True)

# Execute the main application function
app()