# Probabilistic Map page for India's Open Natural Ecosystems (ONE)
# Displays probability layers for different land cover types using RGB visualization
# Shows uncertainty and confidence in classification results

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
st.set_page_config(layout="wide", page_title="India's ONE | Probabilistic Map")

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
    """Main function to render the probabilistic map page"""
    st.title("Probabilistic Map of Open Natural Ecosystems", anchor = "landcovers-probabilistic")

    # Check Earth Engine initialization status before proceeding
    if not EE_INITIALIZED:
        st.info("Please configure Earth Engine authentication to view the interactive map.")
        return

    # Create interactive map centered on India with satellite basemap
    m = geemap.Map(center=(21, 79), zoom=5.2, control_scale=True)

    # Load Earth Engine imagery with probability bands
    mapRaster = ee.Image("projects/ee-open-natural-ecosystems/assets/publish/onesWith7Classes/landcover_hier")

    # Extract and normalize probability bands (from integers scaled by 1e4 to 0-1 range)
    l2OneProbs = mapRaster.select(["prob_one_.*"]).divide(1e4)      # ONE ecosystem probabilities
    l2NononeProbs = mapRaster.select(["prob_nonone_.*"]).divide(1e4) # Non-ONE probabilities
    l1Probs = mapRaster.select(["prob_one", "prob_nonone"]).divide(1e4) # Level-1 probabilities

    # Aggregate probabilities for RGB visualization
    # Sum all ONE ecosystem probabilities (green channel)
    oneProb = l2OneProbs.reduce(ee.Reducer.sum()).rename("one")
    # Sum agricultural probabilities (red channel)
    agrProb = l2NononeProbs.select(["prob_nonone_agri_.*"]).reduce(ee.Reducer.sum()).rename("agr")
    # Forest probabilities (blue channel)
    othProb = l2NononeProbs.select("prob_nonone_forest").rename("oth")
    # Create RGB composite: Red=Agriculture, Green=ONEs, Blue=Forest
    oneAgrOthRgb = ee.Image.cat([agrProb, oneProb, othProb])

    # Add satellite basemap and probability layer
    m.add_basemap("SATELLITE")
    # Note: Split map functionality commented out - using single RGB composite instead
    m.addLayer(oneAgrOthRgb, {"min": 0, "max": 1}, "Agri-ONE-Forest probabilities")

    # Display the interactive map in Streamlit
    m.to_streamlit(height = 768, width=1024)

    # Explanation of the RGB probability visualization
    st.markdown(
        """
        The map above illustrates the probabilistic component of the map dataset. It visualizes aggregates the
        probability of Agriculture (Red), ONEs (Green), and Forest (Blue) at once. The brighter and greener a pixel,
        the higher the probability that it is an ONE; likewise, brighter and redder
        a pixel, the higher the probability that it is Agriculture, and the brighter and bluer a pixel,
        the higher the probability that it is Forest.
        """
    )

# Execute the main application function
app()