# Main entry point for India's Open Natural Ecosystems (ONE) mapping application
# This Streamlit app provides interactive visualization of land cover mapping
# in India's semi-arid Open Natural Ecosystems

import streamlit as st
import leafmap.foliumap as leafmap

# Configure the Streamlit page layout and title
st.set_page_config(layout="wide", page_title="India's ONE")

# Sidebar content with project information and navigation
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

# Create navigation bar with page links across 5 columns
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

# Main content section with project title and description
st.title("Open Land Cover Mapping of India's Semi-arid Open Natural Ecosystems (ONEs)")

# Project overview and context
st.markdown(
    """
    India is endowed with a diversity of terrestrial biomes. Barring
    forests—areas of closed tree canopies—they comprise diverse
    naturally open and often treeless habitats that support their own
    rich and unique complement of plant and animal life. Further,
    for centuries, such diversity has thrived alongside unique pastoral
    and agro-pastoral communities that have shared space with nature
    in this biome, while deriving identity, sustenance and livelihood from it.

    Together, these Open Natural Ecosystems stretch across a vast
    area comprising some 15% of the land area in India's semi-arid zone.
    The threats they face are vast too. Not only are they
    disregarded for their unique ecological, cultural and livelihood values,
    but they are also targets of huge government schemes and programmes for
    well-intentioned developmental purposes that lead to serious
    unintended negative consequences.

    A previous effort to map the extent of these ONEs can be seen
    [here](https://mdm.users.earthengine.app/view/open-natural-ecosystems),
    with its methods and data freely and publicly accessible
    in this [publication](https://doi.org/10.1111/jbi.14471).
    """
)

# Display representative image of India's ONEs
st.image("./ones_of_india.jpg")

# Project philosophy and open data principles
st.write("# Our Philosophy")
st.write("We are a generation witnessing unprecedented changes to our lands and waters, deeply impacting humans and other living beings that depend on them. We believe, therefore, that efforts to observe and map the changing fates and fortunes of earth's land cover should, as far as possible, be done in public interest. Hence, these data must not only be publicly and freely accessible, but the methods by which they are produced, too, must be open to public scrutiny. In this belief, we are making not only the outputs of our mapping public and free under a permissive MIT License, but also the input training data we have created, and the source code we have developed and used to produce our maps.")

