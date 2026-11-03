import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="HLZ Operations Map", page_icon="🚁", layout="wide")

DATA = [
    ["HLZ-001","Example Oval","Shoalhaven",-35.36,150.47,"Grass","35 m × 35 m","Suitable","No","Open vehicle access from main road.","None","Powerlines approximately 100 m north.","H145 / AW139","Fictional demo location.","06/10/2026"],
    ["HLZ-002","Example Showground","Shoalhaven",-35.42,150.52,"Grass","45 m × 40 m","Suitable","Portable lighting","Enter from eastern access road.","Locked gate","Trees along western boundary.","H145 / AW139","Fictional demo location.","01/10/2026"],
    ["HLZ-003","Example Field","Kiama",-34.67,150.86,"Short grass","30 m × 30 m","Suitable","No","Vehicle access via western track.","Combination lock","Overhead wires near southern approach.","H145","Fictional demo location.","28/09/2026"],
    ["HLZ-004","Example Reserve","Ulladulla",-35.36,150.47,"Grass","40 m × 35 m","Suitable","No","Ambulance access from northern entrance.","Open","Trees and fencing around perimeter.","H145 / AW139","Fictional demo location.","24/09/2026"],
    ["HLZ-005","Example School Field","Nowra",-34.88,150.60,"Grass","32 m × 32 m","Suitable","No","Large vehicle access from southern gate.","Locked — key required","Sports infrastructure on eastern edge.","H145","Fictional demo location.","20/09/2026"],
]
COLS = ["HLZ ID","Name","Area","Latitude","Longitude","Surface","Size","Day","Night","Access","Gate","Hazards","Aircraft","Notes","Last Verified"]
df = pd.DataFrame(DATA, columns=COLS)

st.title("🚁 HLZ Operations Map")
st.caption("Prototype — all locations and operational information are fictional.")

st.sidebar.header("Search & Filters")
search = st.sidebar.text_input("Search HLZs", placeholder="ID, name, area, access, hazard…")
areas = st.sidebar.multiselect("Area", sorted(df["Area"].unique()))
surfaces = st.sidebar.multiselect("Surface", sorted(df["Surface"].unique()))
night = st.sidebar.multiselect("Night capability", sorted(df["Night"].unique()))

filtered = df.copy()

if search:
    mask = filtered.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
    filtered = filtered[mask]

if areas:
    filtered = filtered[filtered["Area"].isin(areas)]

if surfaces:
    filtered = filtered[filtered["Surface"].isin(surfaces)]

if night:
    filtered = filtered[filtered["Night"].isin(night)]

c1, c2, c3 = st.columns(3)
c1.metric("HLZs shown", len(filtered))
c2.metric("Areas", filtered["Area"].nunique() if len(filtered) else 0)
c3.metric("Night capable", int(filtered["Night"].str.contains("Suitable|Portable", case=False, na=False).sum()))

map_col, detail_col = st.columns([2.2, 1])

with map_col:
    if len(filtered) > 0:
        center = [filtered["Latitude"].mean(), filtered["Longitude"].mean()]
        m = folium.Map(location=center, zoom_start=9, tiles="OpenStreetMap")

        for _, row in filtered.iterrows():
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                tooltip=f"{row['HLZ ID']} — {row['Name']}",
                popup=f"<b>{row['HLZ ID']} — {row['Name']}</b><br>{row['Area']}<br>{row['Surface']}<br>{row['Size']}",
                icon=folium.Icon(icon="plane", prefix="fa"),
            ).add_to(m)

        result = st_folium(m, width=None, height=600, returned_objects=["last_object_clicked"])
    else:
        st.warning("No HLZs match the current filters.")
        result = {}

selected_id = None
clicked = result.get("last_object_clicked")

if clicked and len(filtered) > 0:
    lat = clicked.get("lat")
    lon = clicked.get("lng")
    if lat is not None and lon is not None:
        distances = (filtered["Latitude"] - lat) ** 2 + (filtered["Longitude"] - lon) ** 2
        selected_id = filtered.loc[distances.idxmin(), "HLZ ID"]

with detail_col:
    st.subheader("HLZ Details")

    if selected_id:
        row = df[df["HLZ ID"] == selected_id].iloc[0]
        st.markdown(f"### {row['HLZ ID']} — {row['Name']}")
        st.caption(row["Area"])
        st.write("Coordinates:", f"{row['Latitude']:.6f}, {row['Longitude']:.6f}")
        st.write("Landing area:", f"{row['Size']} • {row['Surface']}")
        st.write("Aircraft:", row["Aircraft"])
        st.write("Access:", row["Access"])
        st.write("Gate / Entry:", row["Gate"])
        st.write("Hazards:", row["Hazards"])
        st.write("Day:", row["Day"])
        st.write("Night:", row["Night"])
        st.write("Last verified:", row["Last Verified"])
        url = f"https://www.google.com/maps/search/?api=1&query={row['Latitude']},{row['Longitude']}"
        st.link_button("📍 Open in Google Maps", url)
    else:
        st.info("Tap a pin on the map to view its details.")

st.divider()
st.subheader("HLZ Database")
st.dataframe(
    filtered[["HLZ ID","Name","Area","Surface","Size","Day","Night","Last Verified"]],
    use_container_width=True,
    hide_index=True,
)
