import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from spending import generate_spending_events

today = datetime.today()
start_date = today - timedelta(days=today.weekday())
start_date = pd.to_datetime(start_date.date())

spending_entries = generate_spending_events(start_date)

df_spending = pd.DataFrame(spending_entries)
df_spending['Day'] = df_spending['Timestamp'].dt.day_name()
df_spending['Hour'] = df_spending['Timestamp'].dt.hour

# --- Step 4: Create Pivot Table ---
heatmap_data = df_spending.pivot_table(
    index='Day',
    columns='Hour',
    values='Amount',
    aggfunc='sum',
    fill_value=0,
)

# Ensure all 7 days and 24 hours are present
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
full_hours = list(range(24))
heatmap_data = heatmap_data.reindex(index=ordered_days, columns=full_hours, fill_value=0)

# --- Step 5: Prepare for Plotly ---
heatmap_plotly = heatmap_data.reset_index().melt(
    id_vars='Day',
    var_name='Hour',
    value_name='Amount'
)

# --- Step 6: Create Plotly Heatmap ---
fig = px.density_heatmap(
    heatmap_plotly,
    x="Hour",
    y="Day",
    z="Amount",
    color_continuous_scale="YlOrRd",
    text_auto=".2f",
    nbinsx=24,
)

fig.update_traces(zmin=0, zmax=100)

fig.update_layout(
    title="Spending Heatmap: Amount Spent per Hour and Day",
    title_x=0.5,
    xaxis_title="Hour of Day",
    yaxis_title="Day of Week",
    width=1200,
    height=350,
    xaxis=dict(
        tickmode="array",
        tickvals=list(range(24)),    # 0,1,2,...,23
        ticktext=[f"{h}:00" for h in range(24)],   # '0:00', '1:00', ..., '23:00'
    ),
    yaxis=dict(
        scaleanchor="x",
        scaleratio=1,
        categoryorder='array',
        categoryarray=[
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]
    ),
)

fig.show()
