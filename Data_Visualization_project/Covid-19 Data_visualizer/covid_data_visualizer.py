import streamlit as st
import pandas as pd
import plotly.express as px

# Page title
st.title("COVID-19 Daily Cases Visualizer")
st.markdown("Built with Plotly + Streamlit") # subtitle 

# Load Data
@st.cache_data # caching the functuon data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    return pd.read_csv(url, parse_dates=["date"])

df = load_data()

# Country selector
countries = df["location"].dropna().unique()
selected_country = st.selectbox("Select Country:", sorted(countries))

# Metric selector
# st.radio: Lets the user choose one metric
metric = st.radio(
    "Select Metric to Visualize:",
    options=["new_cases", "total_cases", "total_deaths"],
    index=0,
    format_func=lambda x: x.replace("_", " ").title()
)

# Filter data for selected country
country_df = df[df["location"] == selected_country].copy()

# dropna(subset=[metric]) 
# Tells pandas: "Only drop rows where the value for metric is missing (NaN)."
country_df = country_df.dropna(subset=[metric])

# Check if data is available
if not country_df.empty:
    # Plotting
    fig = px.line(
        country_df,
        x="date",
        y=metric,
        title=f"{metric.replace('_', ' ').title()} in {selected_country}",
        labels={metric: metric.replace('_', ' ').title(), "date": "Date"},
        template="plotly_dark"
    )

    fig.update_layout(xaxis_title="Date", yaxis_title=metric.replace("_", " ").title(), title_x=0.5)

    # Show chart
    st.plotly_chart(fig, use_container_width=True)

    # Show raw data
    with st.expander("Show raw data"):
        st.dataframe(country_df[["date", metric]].tail(30))

else:
    st.warning("No data available for this country and metric.")