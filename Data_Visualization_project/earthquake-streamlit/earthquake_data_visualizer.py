import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date


st.set_page_config(page_title="Earthquake Map", layout="wide", page_icon="🌍")

st.sidebar.markdown("---")
st.sidebar.markdown("Created by **Naveen Soni**")
st.sidebar.markdown("[GitHub](https://github.com/Naveen-soni25-1)")

# App title
st.title("🌍 Live Earthquake Feed from USGS")
st.markdown("Visualize recent earthquake data from the [USGS Earthquake API](https://earthquake.usgs.gov/).")

# User inputs
start_date = st.date_input("Pick **start** date for earthquakes", date(2024, 1, 1))
end_date = st.date_input("Pick **end** date for earthquakes", date.today())
limited_eq = st.number_input("Limit the number of earthquakes", min_value=1, value=50)
min_mag = st.number_input("Minimum magnitude to show", min_value=0.0, value=4.5)

# Load data from API
@st.cache_data
def load_data(start_date, end_date, limited_eq, min_mag):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": min_mag,
        "orderby": "time",
        "limit": int(limited_eq)
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data

# Load and parse
data = load_data(start_date, end_date, limited_eq, min_mag)

# Extract earthquake data from GeoJSON
features = data.get("features", [])

if features:
    eq_data = []
    for feature in features:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        eq_data.append({
            "place": props["place"],
            "mag": props["mag"],
            "time": pd.to_datetime(props["time"], unit='ms'),
            "lon": coords[0],
            "lat": coords[1],
            "title": props["title"]
        })

    df = pd.DataFrame(eq_data)

    # Plotting map
    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        hover_name="title",
        size="mag",
        color="mag",
        color_continuous_scale="viridis",
        projection="natural earth",
        title="🌀 Earthquakes Map",
        height=600,
        width=800,
        template="plotly_dark",
        basemap_visible=False
    )
    fig.update_geos(
        resolution=110,
        showcoastlines=True, coastlinecolor="royalblue",
        showocean=True, oceancolor="LightBlue",
        showrivers=True, rivercolor="Blue",
        showcountries=True, countrycolor='lightcyan',
        showland=True, landcolor="forestgreen"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show raw data
    with st.expander("🔍 Show Raw Data"):
        st.dataframe(df[["time", "place", "mag"]].sort_values("time", ascending=False))

else:
    st.warning("No earthquake data found for the selected range and filters.")
