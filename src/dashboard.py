# dashboard.py

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# -------------------------------
# Step 1: Load normalized data
# -------------------------------
df = pd.read_csv("../data/mlb_stats_all_years_normalized.csv")

# -------------------------------
# Step 1a: Clean up Statistic column for dropdown
# -------------------------------
invalid_keywords = [
    "click", "navigation", "previous", "next", "All Star", "World Series",
    "Team", "Red", "White", "Blue", "Astros", "Angels", "Yankees", "Giants",
    "Indians", "Cubs", "Cardinals", "Dodgers", "Braves", "Philadelphia",
    "Boston", "Chicago", "New York", "Cleveland", "Baltimore", "Pittsburgh",
    "Milwaukee", "St. Louis", "Kansas City", "Detroit", "Los Angeles", "Houston",
    "San Francisco", "Montreal", "Toronto", "Anaheim", "Oakland", "Seattle",
    "Florida", "Colorado", "Texas", "Arizona", "Buffalo", "Brooklyn", "Altoona",
    "Wilmington", "Hartford", "Providence", "Troy", "Syracuse", "Richmond",
    "Columbus", "Toledo", "Cincinnati"
]

pattern = '|'.join(invalid_keywords)
df = df[~df["Statistic"].str.contains(pattern, case=False, na=False)]

# Ensure Year is integer
df["Year"] = df["Year"].astype(int)

# -------------------------------
# Step 2: Initialize Dash app
# -------------------------------
app = Dash(__name__)
app.title = "MLB Stats Dashboard"

# -------------------------------
# Step 3: Layout
# -------------------------------
app.layout = html.Div([
    html.H1("MLB Stats Interactive Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Statistic:"),
        dcc.Dropdown(
            id="stat-dropdown",
            options=[{"label": stat, "value": stat} for stat in sorted(df["Statistic"].unique())],
            value="Hits",
            clearable=False
        ),
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": year, "value": year} for year in range(df["Year"].min(), df["Year"].max() + 1)],
            value=df["Year"].min(),
            clearable=False
        ),
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="trend-chart"),
])

# -------------------------------
# Step 4: Callbacks
# -------------------------------
@app.callback(
    Output("bar-chart", "figure"),
    Output("trend-chart", "figure"),
    Input("stat-dropdown", "value"),
    Input("year-dropdown", "value")
)
def update_charts(selected_stat, selected_year):
    # Filter for selected year
    year_df = df[(df["Statistic"] == selected_stat) & (df["Year"] == selected_year)]
    bar_fig = px.bar(
        year_df.sort_values("Value", ascending=False).head(10),
        x="Player",
        y="Value",
        color="Team",
        title=f"Top 10 Players for {selected_stat} in {selected_year}"
    )

    # Trend over years
    trend_df = df[df["Statistic"] == selected_stat].groupby("Year")["Value"].mean().reset_index()
    trend_fig = px.line(
        trend_df,
        x="Year",
        y="Value",
        title=f"Average {selected_stat} Over Years"
    )

    return bar_fig, trend_fig

# -------------------------------
# Step 5: Run server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
