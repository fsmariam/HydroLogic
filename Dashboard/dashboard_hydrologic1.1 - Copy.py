# Import
import streamlit as st
import pandas as pd
import base64 # To encode images for HTML embedding
import plotly.express as px # To create interactive charts and maps

# Before Start
# Load dataset
df = pd.read_csv("../data/processed/Merged_Training_Set_Updated.csv")

# convert image to base64 for embedding in HTML
def image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

# page setup - Sets layout to full-width for more screen space
st.set_page_config(layout="wide")

#  Header
st.markdown("###")
st.image("back.png", use_container_width=True)

st.markdown("""
    <h1 style="text-align: center; font-size: 2.5em; color: white; margin-top: 10px;">
        Smart Monitoring of Water Pump Functionality in Tanzania
    </h1>
""", unsafe_allow_html=True)
# st.title("""Smart Monitoring of Water Pump Functionality in Tanzania""")

st.markdown("This dashboard presents the predicted functionality status of water pumps across Tanzania using machine learning. It helps identify which pumps are working, need repair, or are non-functional, supporting data-driven water infrastructure decisions.")
# st.markdown("<hr style='border: 1px solid #bbb;'>", unsafe_allow_html=True)

# Filter out invalid ages (like negative values or zero)
valid_ages_df = df[df["pump_age"] >= 1]

# Now compute the min and max based on only valid values
min_age = int(valid_ages_df["pump_age"].min())
max_age = int(valid_ages_df["pump_age"].max())

# Pump Slider
st.markdown("### 📅 Pump Age Slider")
# Pump Age Slider
age_range = st.slider(
    "Select Pump Age Range (Years)",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age),
    step=1
)


# Apply filters
filtered_df = df[
    (df["pump_age"] >= age_range[0]) & (df["pump_age"] <= age_range[1])
]

# KPI Cards (Total, % functional, etc.)
# Claculates counts and percentages of pupm statuses
total_pumps = len(filtered_df)
status_counts = filtered_df['status_group'].value_counts()
working = status_counts.get("functional", 0)
repair = status_counts.get("functional needs repair", 0)
non_functional = status_counts.get("non functional", 0)

# Calculate percentages
working_percent = (working / total_pumps) * 100
repair_percent = (repair / total_pumps) * 100
non_functional_percent = (non_functional / total_pumps) * 100

# Define card style
card_style = """
    background-color: #ACD1E3;
    border: 2px solid #O57B9F;
    border-radius: 7px;
    padding: 14px;
    text-align: center;
"""

# Load icons
icon_total = image_to_base64("logos/tt.png")
icon_func = image_to_base64("logos/tf.png")
icon_repair = image_to_base64("logos/tr.png")
icon_nonfunc = image_to_base64("logos/tn.png")

# Create KPI columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col2:
    st.markdown(f"""
        <div style="{card_style}">
            <img src="{icon_total}" style="height:40px;"><br>
            <h3 style="color:#15262E">Total Pumps</h3>
            <h2 style="color:#15262E">{total_pumps:,}</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="{card_style}">
            <img src="{icon_func}" style="height:40px;"><br>
            <h3 style="color:#15262E"> % Functional</h3>
            <h2 style="color:#15262E">{working_percent:.1f}%</h2>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div style="{card_style}">
            <img src="{icon_repair}" style="height:40px;"><br>
            <h3 style="color:#15262E"> % Need Repair</h3>
            <h2 style="color:#15262E">{repair_percent:.1f}%</h2>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div style="{card_style}">
            <img src="{icon_nonfunc}" style="height:40px;"><br>
            <h3 style="color:#15262E"> % Non-Functional</h3>
            <h2 style="color:#15262E">{non_functional_percent:.1f}%</h2>
        </div>
    """, unsafe_allow_html=True)

# Horizontal split: map | filters
st.markdown("### Filter Panel")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    selected_region = st.selectbox("Region", ["All"] + sorted(df["region"].dropna().unique()))
with col2:
    selected_lga = st.selectbox("District (LGA)", ["All"] + sorted(df["lga"].dropna().unique()))
with col3:
    selected_ward = st.selectbox("Ward", ["All"] + sorted(df["ward"].dropna().unique()))
with col4:
    selected_pump_type = st.selectbox("Pump Type", ["All"] + sorted(df["waterpoint_type"].dropna().unique()))
with col5:
    selected_quality = st.selectbox("Quality", ["All"] + sorted(df["quality_group"].dropna().unique()))
with col6:
    selected_status = st.selectbox("Status", ["All"] + sorted(df["status_group"].dropna().unique()))
with col7:
    selected_quantity = st.selectbox("Quantity", ["All"] + sorted(df["quantity"].dropna().unique()))

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_lga != "All":
    filtered_df = filtered_df[filtered_df["lga"] == selected_lga]
if selected_ward != "All":
    filtered_df = filtered_df[filtered_df["ward"] == selected_ward]
if selected_pump_type != "All":
    filtered_df = filtered_df[filtered_df["waterpoint_type"] == selected_pump_type]
if selected_quality != "All":
    filtered_df = filtered_df[filtered_df["quality_group"] == selected_quality]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["status_group"] == selected_status]
if selected_quantity != "All":
    filtered_df = filtered_df[filtered_df["quantity"] == selected_quantity]


# Interactive Map
# Map Section
st.subheader("Pump Locations by Functionality")

map_df = filtered_df.dropna(subset=["latitude", "longitude"])
fig_map = px.scatter_mapbox(
    map_df,
    lat="latitude",
    lon="longitude",
    color="status_group",
    color_discrete_map={
        "functional": "#0098BD",
        "functional needs repair": "#69A1A4",
        "non functional": "#FF9870"
    },
    zoom=5,
    height=700,
    mapbox_style="carto-positron",
    hover_name="region",
    hover_data=["status_group", "pump_age", "water_quality"]
)

fig_map.update_layout(legend_title_text="Pump Status")
st.plotly_chart(fig_map, use_container_width=True, key="map_chart")

# Determine which filters are active
with st.container():
    # Compose dynamic filter summary
    active_filters = []
    if age_range != (min_age, max_age):
        active_filters.append(f"Pump Age: {age_range[0]}–{age_range[1]}")
    if selected_region != "All":
        active_filters.append(f"Region: {selected_region}")
    if selected_lga != "All":
        active_filters.append(f"LGA: {selected_lga}")
    if selected_ward != "All":
        active_filters.append(f"Ward: {selected_ward}")
    if selected_pump_type != "All":
        active_filters.append(f"Pump Type: {selected_pump_type}")
    if selected_quality != "All":
        active_filters.append(f"Quality: {selected_quality}")
    if selected_status != "All":
        active_filters.append(f"Status: {selected_status}")
    if selected_quantity != "All":
        active_filters.append(f"Quantity: {selected_quantity}")
    

# Compose filter summary
if active_filters:
    filter_note = "Filtered by: " + ", ".join(active_filters)
else:
    filter_note = "No filters applied (showing all data)."

# Report Summary Box BELOW the map
status_filtered = filtered_df["status_group"].value_counts()
functional_f = status_filtered.get("functional", 0)
repair_f = status_filtered.get("functional needs repair", 0)
nonfunctional_f = status_filtered.get("non functional", 0)

st.markdown(f"""
<div style="background-color: #1c1c1c; color: white; border-radius: 10px; padding: 16px; margin-top: 15px; border: 1px solid #444;">
    <h4 style="margin-bottom: 10px;">📍 Filtered Report Summary</h4>
    <p style="margin: 0;">
        ✅ <strong>{functional_f:,}</strong> functional &nbsp;&nbsp;
        ⚠️ <strong>{repair_f:,}</strong> need repair &nbsp;&nbsp;
        ❌ <strong>{nonfunctional_f:,}</strong> non-functional
    </p>
    <p style="margin-top: 10px; font-size: 0.9rem; color: #ccc;">
        {filter_note}
    </p>
</div>
""", unsafe_allow_html=True)



# Pie/Donut Chart of Status Breakdown (based on filtered_df)
fig_status_donut = px.pie(
    names=["Functional", "Need Repair", "Non-Functional"],
    values=[functional_f, repair_f, nonfunctional_f],
    hole=0.4,
    color=["Functional", "Need Repair", "Non-Functional"],
    color_discrete_map={
        "Functional": "#0098BD",
        "Need Repair": "#69A1A4",
        "Non-Functional": "#FF9870"
    }
)

fig_status_donut.update_traces(textinfo='label+percent', textfont_size=14)
fig_status_donut.update_layout(
    margin=dict(t=10, b=10, l=10, r=10),
    height=300,
    showlegend=False
)


# Render the chart under the report
st.plotly_chart(fig_status_donut, use_container_width=True, key="status_donut")


# Group selector + bar chart
# Stacked Bar Chart
st.subheader("Pump Status by Location")
group_by = st.selectbox("Group status by:", ["region", "lga", "ward"])
if group_by in filtered_df.columns:
    grouped = filtered_df.groupby([group_by, "status_group"]).size().reset_index(name="count")
    fig_bar = px.bar(
        grouped,
        x=group_by,
        y="count",
        color="status_group",
        barmode="stack",
        color_discrete_map={
            "functional": "#0098BD",
            "functional needs repair": "#69A1A4",
            "non functional": "#FF9870"
        },
        height=450
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)



# Footer
st.markdown("""
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f2f2f2;
            text-align: center;
            padding: 10px 0;
            font-size: 0.85rem;
            color: #444444;
            border-top: 1px solid #cccccc;
            z-index: 100;
        }
        .footer a {
            color: #2A9FC3;
            text-decoration: none;
            margin: 0 10px;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>

    <div class="footer">
        Developed by Farzaneh Gerami, Mariam Farda & Subaye Opoku-Acquah<br>
        as part of a <a href="https://www.redi-school.org/" target="_blank">ReDI School</a> Data Circle course, June 2025.
        &nbsp;·&nbsp;<br>
        <a href="https://github.com/fsmariam/HydroLogic" target="_blank">GitHub</a>
        <a href="https://github.com/ReDI-School/data-circle/tree/main/projects/water_pumps" target="_blank">About the Project</a>
    </div>
""", unsafe_allow_html=True)


# Longitude slider to filter and explore longitude effects
st.markdown("### 🌍 Longitude Range Slider")

min_lon = float(df["longitude"].min())
max_lon = float(df["longitude"].max())

longitude_range = st.slider(
    "Select Longitude Range",
    min_value=min_lon,
    max_value=max_lon,
    value=(min_lon, max_lon),
    step=0.01
)

# Apply longitude filter
filtered_df = filtered_df[
    (filtered_df["longitude"] >= longitude_range[0]) &
    (filtered_df["longitude"] <= longitude_range[1])
]

st.subheader("📈 Functionality vs Longitude")

if filtered_df.empty:
    st.warning("No pump data found for the selected filters.")
else:

# Prepare data: group longitude into bins for clarity
    lon_bins = pd.cut(filtered_df["longitude"], bins=30)
    lon_grouped = filtered_df.groupby(lon_bins)["status_group"].value_counts(normalize=True).unstack().fillna(0)

# Reset index to plot
lon_grouped = lon_grouped.reset_index()
lon_grouped["longitude_mid"] = lon_grouped["longitude"].apply(lambda x: x.mid)

# Plot functionality rate
fig_lon = px.line(
    lon_grouped,
    x="longitude_mid",
    y="functional",
    title="Percentage of Functional Pumps by Longitude",
    labels={"longitude_mid": "Longitude", "functional": "Functional (%)"}
)
fig_lon.update_traces(mode="lines+markers")
fig_lon.update_layout(height=400)

st.plotly_chart(fig_lon, use_container_width=True)

