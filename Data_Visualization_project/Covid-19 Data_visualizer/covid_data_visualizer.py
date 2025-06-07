import pandas as pd

# Load live OWID data
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)

# Check available countries
print("Sample locations:", df["location"].unique()[:10])

# Filter for India
india_df = df[df["location"] == "India"]

# Show latest few rows
india_df = india_df[["date", "total_cases", "new_cases", "total_deaths"]].dropna()
print(india_df.tail())
