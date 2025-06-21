import requests

import plotly.express as px
import pandas as pd  

# Make an API call
url = "https://api.github.com/search/repositories"
url += "?q=stars:>10000&sort=stars&per_page=100&page=1"
headers = {"Accept": "application/vnd.github.v3+json"}

r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

response_dict = r.json()

# Process results
print(f"Total repositories: {response_dict['total_count']}")
print(f"Complete Results: {not response_dict['incomplete_results']}")

repo_dicts = response_dict["items"]
df = pd.DataFrame(repo_dicts)
df['link'] = df.apply(lambda row: f"<a href='{row['html_url']}' >{row['name']}</a>", axis=1)
# ...existing code...
df['data'] = df.apply(lambda row: f"{row['name']}<br />{row['owner']['login']} <br />{row['description']}",axis=1)
# ...existing code...


fig = px.bar(
    df,
    x='link',
    y='stargazers_count',
    title="Most-Starred Python Projects on GitHub",
    labels={"link":"Repository", "stargazers_count":"Stars"},
    color='name',
    color_continuous_scale="viridis",
    template="plotly_dark",
    hover_data=['data'])

fig.update_layout(
    title_font_size=28,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    legend_title_text="Repository Name",  # Change legend title
    legend=dict(
        font=dict(size=12, color="white"),  # Change legend font color and size
        bgcolor="black",                    # Background color
        bordercolor="white",                # Border color
        borderwidth=1,))

fig.update_traces(marker_opacity=1)
# In Plotly, a trace refers to a collection of data on a chart. 
# The update _traces() method can take a number of different arguments;

fig.show()