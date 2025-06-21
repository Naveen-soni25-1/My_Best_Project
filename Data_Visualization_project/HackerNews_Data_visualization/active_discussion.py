from operator import itemgetter
import requests
import plotly.express as px
import pandas as pd

# Step 1: Fetch top story IDs
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status Code: {r.status_code}")
submission_ids = r.json()

submission_dicts = []

# Step 2: Fetch top 10 stories
for submission_id in submission_ids[:10]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    if r.status_code != 200:
        continue
    response_dict = r.json()
    
    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict.get('descendants', 0),
            'author': response_dict['by'],
            'score': response_dict['score'],
            'time': pd.to_datetime(response_dict['time'], unit='s')
        }
        submission_dicts.append(submission_dict)
    except KeyError as e:
        print(f"Missing field {e} in story ID {submission_id}")
        continue

# Step 3: Sort by comment count
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# Step 4: Create DataFrame for Plotly
df = pd.DataFrame(submission_dicts)
df['link'] = df.apply(lambda row: f"<a href='{row.hn_link}'>{row.author}</a>", axis=1)

# Step 5: Plot
fig = px.bar(
    df,
    x='link',
    y='comments',
    title="Active HackerNews Discussions",
    labels={'link':'Author','comments': 'Discussion Count'},
    template="plotly_dark",
    hover_data=['time', 'score'],
    color='title'
)

fig.update_layout(
    title_font_size=28,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    legend_title_text="TITLE",
    legend=dict(
        font=dict(color="white", size=12),
        bgcolor='black',
        bordercolor="white",
        borderwidth=1,
    )
)

fig.update_traces(marker_opacity=0.6)

fig.show()