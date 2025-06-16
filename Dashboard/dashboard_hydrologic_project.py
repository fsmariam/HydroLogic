# Import
import streamlit as st
import pandas as pd
import base64 # To encode images for HTML embedding
import plotly.express as px # To create interactive charts and maps

# Before Start
# Load dataset
df = pd.read_csv("../data/processed/pump_dataset_full_cleaned.csv")

df['predicted_status_group'] = my_model.predict(df[features])

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
    <h1 style="text-align: center; font-size: 2.5em; color: #15262E; margin-top: 10px;">
        Smart Monitoring of Water Pump Functionality in Tanzania
    </h1>
""", unsafe_allow_html=True)
# st.title("""Smart Monitoring of Water Pump Functionality in Tanzania""")

st.markdown("This dashboard presents the predicted functionality status of water pumps across Tanzania using machine learning. It helps identify which pumps are working, need repair, or are non-functional, supporting data-driven water infrastructure decisions.")
st.markdown("<hr style='border: 1px solid #bbb;'>", unsafe_allow_html=True)

# KPI Cards (Total, % functional, etc.)
# Claculates counts and percentages of pupm statuses
total_pumps = len(df)
status_counts = df['status_group'].value_counts()
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

st.markdown("###")
st.markdown("###")

st.markdown("### Pump Age Slider")
# Pump Age Slider
min_age = int(df["pump_age"].min())
max_age = int(df["pump_age"].max())
age_range = st.slider("Select Pump Age Range (Years)", min_age, max_age, (min_age, max_age))

st.markdown("###")

# Horizontal split: map | filters
st.markdown("### Filter Panel")
col1, col2, col3, col4, col5, col6 = st.columns(6)

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

# Apply filters
filtered_df = df[
    (df["pump_age"] >= age_range[0]) & (df["pump_age"] <= age_range[1])
]

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

# Add radio button to switch between Actual vs Predicted status
status_display_choice = st.radio("Show Status Based On:", ["Actual", "Predicted"])
# Define which column to use depending on the user's choice
status_column = "status_group" if status_display_choice == "Actual" else "predicted_status_group"


# Interactive Map
st.subheader("Pump Locations by Functionality")
map_df = filtered_df.dropna(subset=["latitude", "longitude"])
fig_map = px.scatter_mapbox(
    map_df,
    lat="latitude",
    lon="longitude",
    color="status_column",
    color_discrete_map={
        "functional": "#0098BD",
        "functional needs repair": "#69A1A4",
        "non functional": "#FF9870"
    },
    zoom=5,
    height=700,
    mapbox_style="carto-positron",
    hover_name="region",
    hover_data=[status_column, "pump_age", "water_quality"]
)

fig_map.update_layout(legend_title_text="Pump Status")
st.plotly_chart(fig_map, use_container_width=True)

#Update the title dynamically
st.subheader(f"Pump Locations by {'Predicted' if status_column == 'predicted_status_group' else 'Actual'} Functionality")

# Group selector + bar chart
# Stacked Bar Chart
st.subheader("Pump Status by Location")
group_by = st.selectbox("Group status by:", ["region", "lga", "ward"])
if group_by in filtered_df.columns:
    grouped = filtered_df.groupby([group_by, status_column]).size().reset_index(name="count")
    fig_bar = px.bar(
        grouped,
        x=group_by,
        y="count",
        color=status_column,,
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

# update the title
st.subheader(f"Pump Status by Location ({'Predicted' if status_column == 'predicted_status_group' else 'Actual'})")


# Pie chart (water quality)
st.subheader("Water Quality Distribution")
quality_counts = filtered_df["quality_group"].value_counts().reset_index()
quality_counts.columns = ["quality", "count"]
fig_pie = px.pie(
    quality_counts,
    names="quality",
    values="count",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Blues
)
st.plotly_chart(fig_pie, use_container_width=True)


# Prediction status_group
# we have to add the model 

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
