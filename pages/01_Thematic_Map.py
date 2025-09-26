# Thematic Map page for India's Open Natural Ecosystems (ONE)
# Displays interactive classified land cover map using Google Earth Engine
# Shows discrete categories of land cover types with color-coded visualization

import streamlit as st
import ee
import geemap.foliumap as geemap
import matplotlib
import json

# Configuration for authentication fallback (set to False for production deployment)
ENABLE_LOCAL_AUTH_FALLBACK = True

# Global variable to track Earth Engine initialization status
EE_INITIALIZED = False

# Cloud-first authentication with optional local fallback
try:
    # Primary: Try service account from Streamlit secrets (for cloud deployment)
    if "gcp_account" in st.secrets:
        service_account_info = st.secrets["gcp_account"]
        credentials = ee.ServiceAccountCredentials(
            service_account_info["client_email"],
            key_data=json.dumps(dict(service_account_info))
        )
        ee.Initialize(credentials)
        EE_INITIALIZED = True
        st.success("✅ Authenticated with Google Earth Engine (Service Account)")

except Exception as cloud_auth_error:
    # Fallback: Try local authentication only if enabled
    if ENABLE_LOCAL_AUTH_FALLBACK:
        try:
            ee.Authenticate()  # This will prompt user to authenticate if needed
            ee.Initialize()
            EE_INITIALIZED = True
            st.success("✅ Authenticated with Google Earth Engine (Local Account)")

        except Exception as local_auth_error:
            st.error(f"""
            **Earth Engine Authentication Required**

            This page requires Google Earth Engine authentication to display maps.

            **For Local Development (Option 1 - Recommended):**
            1. Run `earthengine authenticate` in your terminal
            2. Follow the authentication flow in your browser
            3. Refresh this page

            **For Local Development (Option 2 - Service Account):**
            1. Create a `.streamlit/secrets.toml` file in your project directory
            2. Add your Google Earth Engine service account credentials:
            ```toml
            [gcp_account]
            type = "service_account"
            project_id = "your-project-id"
            private_key_id = "your-private-key-id"
            private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
            client_email = "your-service-account@your-project.iam.gserviceaccount.com"
            client_id = "your-client-id"
            auth_uri = "https://accounts.google.com/o/oauth2/auth"
            token_uri = "https://oauth2.googleapis.com/token"
            ```

            **For Cloud Deployment:**
            Add the credentials through Streamlit Cloud's secrets management.

            **Errors:**
            - Cloud auth: {str(cloud_auth_error)}
            - Local auth: {str(local_auth_error)}
            """)
            EE_INITIALIZED = False
    else:
        # Production mode: only show cloud authentication error
        st.error(f"""
        **Earth Engine Authentication Required**

        Service account authentication failed. Please configure Google Earth Engine
        credentials through Streamlit Cloud's secrets management.

        **Error:** {str(cloud_auth_error)}
        """)
        EE_INITIALIZED = False

# Configure Streamlit page layout and metadata
st.set_page_config(layout="wide", page_title="India's ONE | Thematic Map")

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

def app():
    """Main function to render the thematic map page"""
    st.title("Thematic Map of Open Natural Ecosystems", anchor = "landcovers-thematic")

    # Check Earth Engine initialization status before proceeding
    if not EE_INITIALIZED:
        st.info("Please configure Earth Engine authentication to view the interactive map.")
        return

    # Expandable section with descriptions of ONE ecosystem types
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

    # Load and process Earth Engine imagery for land cover classification
    mapRaster = ee.Image("projects/ee-open-natural-ecosystems/assets/publish/onesWith7Classes/landcover_hier")

    # Remap Level-2 classification labels to consolidated categories for visualization
    # Maps from detailed subcategories to main ecosystem types
    l2Labels = mapRaster.select("l2LabelNum") \
        .remap([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
               [1, 1, 6, 1, 3, 2, 4, 5, 7,  8,  9,  1])

    # Define color palette using matplotlib color names for each land cover type
    palette = [
        matplotlib.colors.cnames["black"],         # Others (non-natural areas)
        matplotlib.colors.cnames["darkgreen"],     # Forest
        matplotlib.colors.cnames["khaki"],         # Dune ecosystems
        matplotlib.colors.cnames["fuchsia"],       # Ravine systems
        matplotlib.colors.cnames["lightsteelblue"],# Saline areas
        matplotlib.colors.cnames["beige"],         # Bare/sparsely vegetated
        matplotlib.colors.cnames["yellow"],        # Open Savanna
        matplotlib.colors.cnames["goldenrod"],     # Shrub Savanna
        matplotlib.colors.cnames["greenyellow"],   # Woodland Savanna
    ]

    # Visualization parameters for Earth Engine layer
    vis_params = {
        "min": 1,
        "max": 9,
        "opacity": 0.7,
        "palette": palette,
    }

    # Legend dictionary mapping ecosystem types to colors
    oneTypeslegendDict = {  "Others": matplotlib.colors.cnames["black"],
                            "Forest": matplotlib.colors.cnames["darkgreen"],
                              "Dune": matplotlib.colors.cnames["khaki"],
                            "Ravine": matplotlib.colors.cnames["fuchsia"],
                            "Saline": matplotlib.colors.cnames["lightsteelblue"],
        "Bare or sparsely vegetated": matplotlib.colors.cnames["beige"],
                      "Open Savanna": matplotlib.colors.cnames["yellow"],
                     "Shrub Savanna": matplotlib.colors.cnames["goldenrod"],
                  "Woodland Savanna": matplotlib.colors.cnames["greenyellow"]
    }

    # Get Earth Engine map tile for visualization
    map_id_dict = ee.Image(l2Labels).getMapId(vis_params)

    # Create interactive map centered on India with satellite basemap
    m = geemap.Map(center=(21, 79), zoom=5.2, control_scale=True)
    m.add_basemap("SATELLITE")
    m.addLayer(ee.Image(l2Labels), vis_params, "ONE Types")
    # Note: m.add_legend() commented out due to missing template - using Streamlit legend instead



    # Render legend manually using Streamlit HTML (workaround for geemap template issue)
    st.markdown("### Map Legend")
    st.markdown("""
    <div style='display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;'>
        <span><span style='background-color: black; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Others</span>
        <span><span style='background-color: darkgreen; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Forest</span>
        <span><span style='background-color: khaki; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Dune</span>
        <span><span style='background-color: fuchsia; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Ravine</span>
        <span><span style='background-color: lightsteelblue; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Saline</span>
        <span><span style='background-color: beige; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Bare/Sparsely Vegetated</span>
        <span><span style='background-color: yellow; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Open Savanna</span>
        <span><span style='background-color: goldenrod; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Shrub Savanna</span>
        <span><span style='background-color: greenyellow; display:inline-block; width:15px; height:15px; margin-right: 5px;'></span> Woodland Savanna</span>
    </div>
    """, unsafe_allow_html=True)

    # Display the interactive map in Streamlit
    m.to_streamlit(height = 768, width=1024)

# Execute the main application function
app()