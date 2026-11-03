import html
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from pathlib import Path
import streamlit.components.v1 as components
from urllib.parse import quote
import math
import json
import urllib.request
import urllib.error

st.set_page_config(
    page_title="Shoalhaven Landing Zones",
    page_icon="shoalhaven_landing_zones_icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_location_component = components.declare_component(
    "hlz_location_permission",
    path=str(Path(__file__).parent),
)



# =========================
# Prototype settings
# =========================
APP_BLUE = "#1E5AA8"
# Prototype credentials. In the final version these will be stored securely,
# rather than in the application source code.
if "portal_pin" not in st.session_state:
    st.session_state.portal_pin = "1234"
if "admin_users" not in st.session_state:
    st.session_state.admin_users = {"admin": "1234"}

# Prototype data source.
# In the final version this will be replaced by the private OneDrive Excel connection.
DATA_FILE = "hlz_database.csv"

# =========================
# Styling
# =========================
APP_BLUE = "#EAF3FF"

# Use a high-contrast light theme by default, then switch to a matching dark
# palette when the phone/browser reports prefers-color-scheme: dark.
st.markdown(
    f"""
    <style>
        :root {{ color-scheme: light !important; }}
        html, body, .stApp {{
            color-scheme: light !important;
            background-color: {APP_BLUE} !important;
            color: #17212B !important;
        }}
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
        [data-testid="stMainBlockContainer"], .main, .block-container {{
            background-color: {APP_BLUE} !important;
            color: #17212B !important;
        }}
        .block-container {{
            padding-top: 3.5rem;
            padding-bottom: 2rem;
        }}
        /* Tighten the vertical gap between the Current Location info banner,
           the zero-height location component, and the desktop warning. */
        div[data-testid="stAlert"] {{
            margin-bottom: 0.25rem !important;
        }}
        div[data-testid="stElementContainer"]:has(iframe[title*="hlz_location_permission"]) {{
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            min-height: 0 !important;
        }}
        div[data-testid="stElementContainer"]:has(iframe[title*="hlz_location_permission"]) iframe {{
            display: block !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        /* The red desktop warning should sit close to the blue location banner. */
        div[data-testid="stElementContainer"]:has(iframe[title*="hlz_location_permission"]) + div[data-testid="stElementContainer"] {{
            margin-top: -0.6rem !important;
        }}
        /* Keep a little breathing room around the interactive map on phones,
           making it easier to begin a page scroll without touching the map. */
        @media (max-width: 768px) {{
            div[data-testid="stElementContainer"]:has(iframe[title*="streamlit_folium"]) {{
                width: 96% !important;
                max-width: 96% !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }}
            iframe[title*="streamlit_folium"] {{
                max-width: 100% !important;
            }}
        }}
        /* Default text and headings */
        .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2,
        .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"] {{
            color: #17212B !important;
        }}
        .main-title {{
            color: #123B66 !important;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }}
        .subtitle {{
            color: #40566B !important;
            margin-bottom: 1rem;
        }}
        .detail-card {{
            background-color: #FFFFFF !important;
            color: #17212B !important;
            color-scheme: light !important;
            border-radius: 12px;
            padding: 0 1.2rem 1rem 1.2rem;
            margin-top: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            border: 1px solid #D7E5F5;
        }}
        .detail-title {{
            color: #17324D !important;
            font-size: 1.35rem;
            font-weight: 700;
            margin: 0;
            padding: 0.3rem 0 0.55rem 0;
            border-top: 1px solid #D7E5F5;
        }}
        .field-label {{
            color: #3D556A !important;
            font-size: 1.02rem;
            font-weight: 700;
            margin-bottom: 0.15rem;
        }}
        .field-value {{
            color: #17212B !important;
            font-size: 0.96rem;
            margin-bottom: 0.9rem;
        }}
        /* Tighten the transition from the final Notes field to navigation. */
        .detail-card .field-value:last-child {{ margin-bottom: 0 !important; }}
        .navigation-title {{
            color: #17324D !important;
            font-size: 1.08rem;
            font-weight: 700;
            margin-top: 0 !important;
            margin-bottom: 0.7rem;
            padding-top: 0;
            border-top: none;
        }}
        /* Text inputs, password inputs, text areas and dropdowns */
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] > div,
        [data-baseweb="select"] > div,
        .stTextInput input, .stNumberInput input, .stTextArea textarea,
        input, textarea {{
            background-color: #FFFFFF !important;
            color: #17212B !important;
            -webkit-text-fill-color: #17212B !important;
            border-color: #8297AC !important;
            color-scheme: light !important;
            opacity: 1 !important;
        }}
        input::placeholder, textarea::placeholder,
        [data-baseweb="input"] input::placeholder,
        [data-baseweb="textarea"] textarea::placeholder {{
            color: #5B6875 !important;
            -webkit-text-fill-color: #5B6875 !important;
            opacity: 1 !important;
        }}
        [data-baseweb="select"] *, [data-baseweb="select"] input {{
            color: #17212B !important;
            -webkit-text-fill-color: #17212B !important;
        }}
        [data-baseweb="popover"], [data-baseweb="menu"],
        [role="listbox"], [role="option"] {{
            background-color: #FFFFFF !important;
            color: #17212B !important;
            color-scheme: light !important;
        }}
        [role="option"]:hover, [role="option"][aria-selected="true"] {{
            background-color: #DCEBFA !important;
            color: #123B66 !important;
        }}
        /* High-contrast buttons, including form submits and navigation links */
        .stButton > button, .stFormSubmitButton > button,
        .stLinkButton > a, [data-testid="stBaseButton-secondary"],
        [data-testid="stBaseButton-primary"] {{
            width: 100%;
            background-color: #1E5AA8 !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: 1px solid #17477F !important;
            border-radius: 0.5rem !important;
            font-weight: 600 !important;
            opacity: 1 !important;
        }}
        .stButton > button:hover, .stFormSubmitButton > button:hover,
        .stLinkButton > a:hover {{
            background-color: #17477F !important;
            border-color: #123B66 !important;
            color: #FFFFFF !important;
        }}
        .stButton > button:disabled, .stFormSubmitButton > button:disabled {{
            background-color: #D6DEE7 !important;
            color: #4B5968 !important;
            -webkit-text-fill-color: #4B5968 !important;
            border-color: #AAB6C2 !important;
            opacity: 1 !important;
        }}
        /* Radio buttons, checkboxes, alerts and sidebar */
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div {{
            background-color: #F5F8FC !important;
            color: #17212B !important;
        }}
        [data-testid="stAlert"] {{
            color: #17212B !important;
        }}
        [data-testid="stAlert"] p {{ color: #17212B !important; }}
        [data-testid="stCheckbox"] label, [data-testid="stRadio"] label {{
            color: #17212B !important;
        }}
        /* Keep focus visible for touch, keyboard and accessibility */
        button:focus-visible, input:focus-visible, textarea:focus-visible,
        [tabindex]:focus-visible {{
            outline: 3px solid #F2B705 !important;
            outline-offset: 2px !important;
        }}

        /* Follow the phone/browser appearance setting automatically. */
        @media (prefers-color-scheme: dark) {{
            :root {{ color-scheme: dark !important; }}
            html, body, .stApp,
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
            [data-testid="stMainBlockContainer"], .main, .block-container {{
                color-scheme: dark !important;
                background-color: #111820 !important;
                color: #F1F5F9 !important;
            }}
            .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2,
            .stApp h3, .stApp h4, .stApp h5, .stApp h6,
            [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
            [data-testid="stCheckbox"] label, [data-testid="stRadio"] label {{
                color: #F1F5F9 !important;
            }}
            .main-title, .detail-title, .navigation-title {{ color: #D8E9FF !important; }}
            .subtitle, .field-label {{ color: #C0CEDD !important; }}
            .detail-card {{
                background-color: #202B36 !important;
                color: #F1F5F9 !important;
                color-scheme: dark !important;
                border-color: #465768 !important;
            }}
            .field-value {{ color: #F1F5F9 !important; }}
            .detail-title, .navigation-title {{ border-color: #465768 !important; }}
            [data-baseweb="input"] > div,
            [data-baseweb="textarea"] > div,
            [data-baseweb="select"] > div,
            .stTextInput input, .stNumberInput input, .stTextArea textarea,
            input, textarea {{
                background-color: #263340 !important;
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
                border-color: #8093A6 !important;
                color-scheme: dark !important;
            }}
            input::placeholder, textarea::placeholder,
            [data-baseweb="input"] input::placeholder,
            [data-baseweb="textarea"] textarea::placeholder {{
                color: #C0CBD6 !important;
                -webkit-text-fill-color: #C0CBD6 !important;
                opacity: 1 !important;
            }}
            [data-baseweb="select"] *, [data-baseweb="select"] input {{
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
            }}
            [data-baseweb="popover"], [data-baseweb="menu"],
            [role="listbox"], [role="option"] {{
                background-color: #202B36 !important;
                color: #F1F5F9 !important;
                color-scheme: dark !important;
            }}
            [role="option"]:hover, [role="option"][aria-selected="true"] {{
                background-color: #34495D !important;
                color: #FFFFFF !important;
            }}
            .stButton > button, .stFormSubmitButton > button,
            .stLinkButton > a, [data-testid="stBaseButton-secondary"],
            [data-testid="stBaseButton-primary"] {{
                background-color: #2F74C0 !important;
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
                border-color: #78AEE8 !important;
            }}
            .stButton > button:hover, .stFormSubmitButton > button:hover,
            .stLinkButton > a:hover {{
                background-color: #3B86D8 !important;
                border-color: #B7D8FF !important;
                color: #FFFFFF !important;
            }}
            .stButton > button:disabled, .stFormSubmitButton > button:disabled {{
                background-color: #394653 !important;
                color: #D1D9E2 !important;
                -webkit-text-fill-color: #D1D9E2 !important;
                border-color: #657587 !important;
            }}
            [data-testid="stSidebar"], [data-testid="stSidebar"] > div {{
                background-color: #1A2530 !important;
                color: #F1F5F9 !important;
            }}
            [data-testid="stAlert"] {{
                background-color: #202B36 !important;
                color: #F1F5F9 !important;
            }}
            [data-testid="stAlert"] p {{ color: #F1F5F9 !important; }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Session state
# =========================
if "portal_unlocked" not in st.session_state:
    st.session_state.portal_unlocked = False
if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False
if "selected_hlz" not in st.session_state:
    st.session_state.selected_hlz = None
if "show_admin_portal" not in st.session_state:
    st.session_state.show_admin_portal = False
if "ignore_next_map_click" not in st.session_state:
    st.session_state.ignore_next_map_click = False
if "map_component_version" not in st.session_state:
    st.session_state.map_component_version = 0
if "user_latitude" not in st.session_state:
    st.session_state.user_latitude = None
if "user_longitude" not in st.session_state:
    st.session_state.user_longitude = None
if "user_location_accuracy" not in st.session_state:
    st.session_state.user_location_accuracy = None
if "location_permission_status" not in st.session_state:
    st.session_state.location_permission_status = "not_requested"
if "location_request_id" not in st.session_state:
    st.session_state.location_request_id = 1
if "show_user_location" not in st.session_state:
    st.session_state.show_user_location = False
if "map_center_mode" not in st.session_state:
    st.session_state.map_center_mode = "data"
if "selection_distance_km" not in st.session_state:
    st.session_state.selection_distance_km = None
if "selection_distance_mode" not in st.session_state:
    st.session_state.selection_distance_mode = None
if "selected_hlz_from_nearest" not in st.session_state:
    st.session_state.selected_hlz_from_nearest = False
if "nearest_results" not in st.session_state:
    st.session_state.nearest_results = None

# =========================
# Helper functions
# =========================
def clear_selected_hlz():
    # st_folium can return the previous marker click again on the rerun
    # triggered by this button. Ignore that one stale click.
    st.session_state.selected_hlz = None
    st.session_state.selection_distance_km = None
    st.session_state.selection_distance_mode = None
    st.session_state.ignore_next_map_click = True
    # Recreate the map component so any open popup/selected click state is cleared
    # in the browser, rather than only clearing the Python-side selection.
    st.session_state.map_component_version += 1


def exit_nearest_mode():
    st.session_state.nearest_results = None
    st.session_state.selected_hlz = None
    st.session_state.selected_hlz_from_nearest = False
    st.session_state.selection_distance_km = None
    st.session_state.selection_distance_mode = None
    st.session_state.map_center_mode = "data"


def reset_filters():
    # This callback runs before Streamlit reruns the page, so it is safe
    # to update the values of widgets that already have session-state keys.
    st.session_state.station_filter = "All"
    st.session_state.suburb_filter = "All"
    st.session_state.selected_hlz = None
    st.session_state.selection_distance_km = None
    exit_nearest_mode()

def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two latitude/longitude points."""
    radius_km = 6371.0088
    phi1, phi2 = math.radians(float(lat1)), math.radians(float(lat2))
    d_phi = math.radians(float(lat2) - float(lat1))
    d_lam = math.radians(float(lon2) - float(lon1))
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2
    return 2 * radius_km * math.asin(min(1.0, math.sqrt(a)))

def nearest_hlz(df, latitude, longitude, shortlist_size=12):
    """Find the closest HLZ by drivable road distance, falling back to straight-line.

    First shortlist nearby coordinate-valid HLZs by Haversine distance, then ask
    the public OSRM demo routing service for road distances in one table request.
    The public demo is best-effort and has no uptime guarantee.
    Returns (dataframe_index, distance_km, mode).
    """
    valid = df.dropna(subset=["Latitude", "Longitude"]).copy()
    if valid.empty:
        return None, None, None

    valid["_straight_km"] = valid.apply(
        lambda row: haversine_km(latitude, longitude, row["Latitude"], row["Longitude"]),
        axis=1,
    )
    candidates = valid.nsmallest(min(shortlist_size, len(valid)), "_straight_km")

    # OSRM expects coordinates as longitude,latitude. Index 0 is the user's
    # current position; all following indices are candidate HLZ destinations.
    coordinates = [f"{float(longitude):.6f},{float(latitude):.6f}"]
    coordinates += [
        f"{float(row['Longitude']):.6f},{float(row['Latitude']):.6f}"
        for _, row in candidates.iterrows()
    ]
    url = "https://router.project-osrm.org/table/v1/driving/" + ";".join(coordinates)
    url += "?sources=0&destinations=" + ";".join(str(i) for i in range(1, len(coordinates)))
    url += "&annotations=distance"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Shoalhaven-HLZ-Prototype/1.0"},
        )
        with urllib.request.urlopen(request, timeout=7) as response:
            result = json.loads(response.read().decode("utf-8"))
        distances = result.get("distances", [[]])[0]
        usable = [
            (candidates.index[i], float(distance) / 1000.0)
            for i, distance in enumerate(distances)
            if distance is not None and i < len(candidates)
        ]
        if usable:
            index, distance_km = min(usable, key=lambda item: item[1])
            return index, distance_km, "road"
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, IndexError, TypeError):
        pass

    # Clearly identified fallback: closest straight-line HLZ among all records.
    index = valid["_straight_km"].idxmin()
    return index, float(valid.loc[index, "_straight_km"]), "straight-line fallback"

def load_data():
    df = pd.read_csv(DATA_FILE)
    expected = [
        "HLZ Number", "Station Area", "Suburb", "Facility",
        "Street Address", "What3Words", "Latitude", "Longitude",
        "Landing Surface", "Gate", "Windsock", "Lighting", "Notes"
    ]
    for col in expected:
        if col not in df.columns:
            df[col] = ""
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    return df


def nav_urls(lat, lon, address, what3words):
    encoded_address = quote(str(address))
    urls = {
        "Google Maps": f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}",
        "Apple Maps": f"https://maps.apple.com/?daddr={lat},{lon}",
        "Waze": f"https://www.waze.com/ul?ll={lat}%2C{lon}&navigate=yes",
    }

    # What3Words links can open the exact three-word entry point.
    w3w = str(what3words).strip()
    if w3w:
        clean_w3w = w3w.replace("///", "").strip()
        if clean_w3w:
            urls["What3Words"] = (
                f"https://what3words.com/{quote(clean_w3w, safe='.')}"
            )

    return urls


def show_details(row, key_suffix=""):
    st.markdown('<div class="detail-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="detail-title">🚁 {row["HLZ Number"]} — {row["Facility"]}</div>',
        unsafe_allow_html=True,
    )

    fields = [
        ("Station Area", row["Station Area"]),
        ("Suburb", row["Suburb"]),
        ("Street Address", row["Street Address"]),
        ("Entry Point (What3Words)", row["What3Words"]),
        ("Location (Lat / Long)", f'{row["Latitude"]}, {row["Longitude"]}'),
        ("Landing Surface", row["Landing Surface"]),
        ("Gate", row["Gate"]),
        ("Windsock", row["Windsock"]),
        ("Lighting", row["Lighting"]),
        ("Notes", row["Notes"]),
    ]

    urls = nav_urls(
        row["Latitude"],
        row["Longitude"],
        row["Street Address"],
        row["What3Words"],
    )

    # Render row-by-row so mobile stacking follows desktop left-to-right reading order.
    for row_start in range(0, len(fields), 3):
        row_fields = fields[row_start:row_start + 3]
        cols = st.columns(3)
        for col, (label, value) in zip(cols, row_fields):
            with col:
                st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
                if label == "Entry Point (What3Words)" and str(value).strip():
                    clean_w3w = str(value).strip().replace("///", "")
                    w3w_url = urls.get("What3Words")
                    if w3w_url:
                        st.markdown(
                            f'<div class="field-value"><a href="{w3w_url}" target="_blank">///{clean_w3w}</a></div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(f'<div class="field-value">{value}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="field-value">{value if str(value).strip() else "—"}</div>',
                        unsafe_allow_html=True,
                    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Keep the always-visible navigation buttons at the bottom as well as the
    # clickable What3Words field above. Match the four navigation buttons used
    # in the nearest-HLZ dropdowns.
    st.markdown(
        f'<div class="navigation-title">Navigate to this HLZ</div>',
        unsafe_allow_html=True,
    )

    nav_order = ["Google Maps", "Apple Maps", "Waze", "What3Words"]
    nav_cols = st.columns(len(nav_order))
    for col, nav_name in zip(nav_cols, nav_order):
        with col:
            nav_url = urls.get(nav_name)
            if nav_url:
                st.link_button(nav_name, nav_url, use_container_width=True)

    # Clear selection sits underneath navigation and is styled red to make
    # the destructive/clearing action distinct from navigation controls.
    st.markdown(
        """
        <style>
        .st-key-clear_selected_hlz_button button {
            background: #DC2626 !important;
            color: #FFFFFF !important;
            border: 1px solid #B91C1C !important;
            font-weight: 700 !important;
        }
        .st-key-clear_selected_hlz_button button:hover {
            background: #B91C1C !important;
            color: #FFFFFF !important;
            border-color: #991B1B !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.button(
        "✕ Clear Selected",
        use_container_width=True,
        on_click=clear_selected_hlz,
        key="clear_selected_hlz_button",
    )


# =========================
# Portal login / 15-minute browser-tab grace period
# =========================
# Browser sessionStorage retains the original successful PIN time across page
# refreshes in the same tab. The expiry is fixed and is not extended by refresh.
auth_bridge_result = _location_component(
    mode="auth",
    authenticated=bool(st.session_state.portal_unlocked),
    request_id="auth",
    key="hlz_auth_grace_bridge",
    default={"valid": False},
)
if isinstance(auth_bridge_result, dict) and auth_bridge_result.get("valid"):
    st.session_state.portal_unlocked = True

# Keep the portal unlocked during normal Streamlit reruns (including GPS retry).
# This avoids forcing the user to sign in again just to refresh browser location.
if not st.session_state.portal_unlocked:
    st.image("shoalhaven_landing_zones_header.jpg", use_container_width=True)
    st.markdown('<div class="main-title">Shoalhaven Landing Zones</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Restricted access prototype</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Portal Access")
    with st.form("portal_login_form"):
        pin = st.text_input("Enter portal PIN", type="password")
        submitted = st.form_submit_button("Enter", use_container_width=True)
        if submitted:
            if pin == st.session_state.portal_pin:
                st.session_state.portal_unlocked = True
                st.rerun()
            else:
                st.error("Incorrect PIN.")

    st.stop()

# =========================
# Admin portal
# =========================
with st.sidebar:
    st.markdown("## 🔐 Administration")

    if not st.session_state.admin_unlocked:
        st.caption("Administrator access")
        with st.form("admin_login_form"):
            username = st.text_input("Username")
            admin_pin = st.text_input("Admin PIN", type="password")
            submitted = st.form_submit_button("Enter", use_container_width=True)

            if submitted:
                if (
                    username in st.session_state.admin_users
                    and admin_pin == st.session_state.admin_users[username]
                ):
                    st.session_state.admin_unlocked = True
                    st.rerun()
                else:
                    st.error("Incorrect admin credentials.")
    else:
        st.success("Admin unlocked")

        st.markdown("### HLZ Data")
        st.link_button(
            "📊 Open HLZ Excel Database",
            "https://onedrive.live.com/",
            use_container_width=True,
        )

        st.caption(
            "Prototype link only. The final version will point directly "
            "to your HLZ Excel workbook in OneDrive."
        )

        if st.button("🔄 Refresh HLZ Data", use_container_width=True):
            st.cache_data.clear()
            st.session_state.selected_hlz = None
            st.rerun()

        st.markdown("### Application Settings")

        st.markdown("**Change Portal PIN**")
        new_portal_pin = st.text_input(
            "New portal PIN",
            type="password",
            key="new_portal_pin",
            max_chars=12,
        )
        if st.button("Save Portal PIN", use_container_width=True):
            if new_portal_pin and new_portal_pin.isdigit():
                st.session_state.portal_pin = new_portal_pin
                st.success(
                    "Portal PIN changed. The new PIN will be required the next "
                    "time the portal is locked."
                )
            else:
                st.error("Use numbers only.")

        if st.button("Lock App / Test New Portal PIN", use_container_width=True):
            st.session_state.portal_unlocked = False
            st.session_state.admin_unlocked = False
            st.session_state.show_admin_portal = False
            st.rerun()

        st.divider()

        st.markdown("**Admin Users**")
        st.caption("Prototype only: changes are kept while the app session is running.")

        admin_rows = [
            {"Username": admin_name, "PIN": "••••"}
            for admin_name in sorted(st.session_state.admin_users)
        ]
        st.dataframe(
            pd.DataFrame(admin_rows),
            hide_index=True,
            use_container_width=True,
        )

        with st.expander("Add Admin User"):
            new_admin_username = st.text_input(
                "New admin username",
                key="new_admin_username",
            )
            new_admin_pin = st.text_input(
                "New admin PIN",
                type="password",
                key="new_admin_pin",
            )

            if st.button("Create Admin User", use_container_width=True):
                if not new_admin_username.strip():
                    st.error("Enter a username.")
                elif new_admin_username in st.session_state.admin_users:
                    st.error("That username already exists.")
                elif not new_admin_pin.isdigit():
                    st.error("Admin PIN must contain numbers only.")
                else:
                    st.session_state.admin_users[new_admin_username.strip()] = new_admin_pin
                    st.success(f"Admin user '{new_admin_username.strip()}' created.")
                    st.rerun()

        with st.expander("Change Admin PIN"):
            selected_admin = st.selectbox(
                "Admin account",
                sorted(st.session_state.admin_users),
                key="change_admin_user",
            )
            replacement_pin = st.text_input(
                "New admin PIN",
                type="password",
                key="replacement_admin_pin",
            )
            if st.button("Save Admin PIN", use_container_width=True):
                if replacement_pin.isdigit() and replacement_pin:
                    st.session_state.admin_users[selected_admin] = replacement_pin
                    st.success(f"PIN changed for '{selected_admin}'.")
                else:
                    st.error("Use numbers only.")

        st.divider()

        if st.button("Log out of Admin", use_container_width=True):
            st.session_state.admin_unlocked = False
            st.rerun()

# =========================
# Main app
# =========================
df = load_data()

# Branding-only update: preserve the existing map, filters, nearest-HLZ logic and details.
st.image("shoalhaven_landing_zones_header.jpg", use_container_width=True)
st.markdown(
    '<div class="main-title">Shoalhaven Landing Zones</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Search and select an HLZ to view operational details.</div>',
    unsafe_allow_html=True,
)

# Show the number of matching HLZs in the collapsed filter heading as well as inside it.
# Use the current session-state filters to calculate the count before rendering the expander.
_count_station = st.session_state.get("station_filter", "All")
_count_suburb = st.session_state.get("suburb_filter", "All")
_count_df = df.copy()
if _count_station != "All":
    _count_df = _count_df[_count_df["Station Area"].astype(str) == _count_station]
if _count_suburb != "All":
    _count_df = _count_df[_count_df["Suburb"].astype(str) == _count_suburb]
_filter_heading = f"🔎 Search by Station Area or Suburb · {len(_count_df)} HLZ{'s' if len(_count_df) != 1 else ''} found"

# Compact, collapsed search accordion to preserve map space on mobile.
with st.expander(
    _filter_heading,
    expanded=st.session_state.get("search_filters_expander", False),
    key="search_filters_expander",
    on_change="rerun",
):
    c1, c2 = st.columns(2)

    with c1:
        station_options = ["All"] + sorted(df["Station Area"].dropna().astype(str).unique().tolist())
        station = st.selectbox("Station Area", station_options, key="station_filter", on_change=exit_nearest_mode)

    with c2:
        suburb_options = ["All"] + sorted(df["Suburb"].dropna().astype(str).unique().tolist())
        suburb = st.selectbox("Suburb", suburb_options, key="suburb_filter", on_change=exit_nearest_mode)

    search_count_col, reset_col = st.columns([5, 1])
    with search_count_col:
        st.markdown(f"**Search results: {len(_count_df)} HLZ{'s' if len(_count_df) != 1 else ''}**")
        st.caption("Count updates when Station Area or Suburb filters change.")
    with reset_col:
        st.button("↩ Reset Filters", use_container_width=True, on_click=reset_filters)

# Read current filter values from session state even when the accordion is collapsed.
station = st.session_state.get("station_filter", "All")
suburb = st.session_state.get("suburb_filter", "All")
filtered = df.copy()
if station != "All":
    filtered = filtered[filtered["Station Area"].astype(str) == station]
if suburb != "All":
    filtered = filtered[filtered["Suburb"].astype(str) == suburb]

# =========================
# Current location permission and controls
# =========================
st.markdown("### 📍 Current Location")

# The component automatically requests a one-off location fix when it first
# appears after portal login. A visible explanation is rendered before it.
st.info(
    "This app can use your current location to show an ambulance marker and find the nearest recorded HLZ. "
    "Your location is used only in this session and is not saved to the HLZ database. "
    "Your browser will ask whether you want to allow access."
)

# A new component key forces Streamlit to mount a fresh browser iframe on each
# retry/refresh request, rather than relying only on an in-place component rerender.
location_result = _location_component(
    request_id=st.session_state.location_request_id,
    key=f"hlz_location_permission_component_{st.session_state.location_request_id}",
    default={"status": "pending"},
)

if isinstance(location_result, dict):
    # Ignore a cached component result from an earlier request. This matters
    # when the user changes browser permissions and taps Retry.
    result_request_id = location_result.get("request_id")
    is_current_request = result_request_id == st.session_state.location_request_id
    status = location_result.get("status") if is_current_request else None
    if status in {"granted", "denied", "error", "unavailable", "unsupported", "insecure", "desktop_disabled"}:
        st.session_state.location_permission_status = status
    if status == "granted":
        try:
            gps_lat = float(location_result.get("latitude"))
            gps_lon = float(location_result.get("longitude"))
            if math.isfinite(gps_lat) and math.isfinite(gps_lon) and -90 <= gps_lat <= 90 and -180 <= gps_lon <= 180:
                st.session_state.user_latitude = gps_lat
                st.session_state.user_longitude = gps_lon
                accuracy = location_result.get("accuracy")
                st.session_state.user_location_accuracy = float(accuracy) if accuracy is not None else None
                st.session_state.gps_request_error = None
                # Display the current-position marker as soon as a valid fix arrives.
                st.session_state.show_user_location = True
                if st.session_state.map_center_mode == "data":
                    st.session_state.map_center_mode = "user"
        except (TypeError, ValueError):
            st.session_state.location_permission_status = "error"
            st.session_state.gps_request_error = "The browser returned an invalid GPS position."
    elif status in {"denied", "error", "unavailable", "unsupported", "insecure", "desktop_disabled"}:
        st.session_state.user_latitude = None
        st.session_state.user_longitude = None
        st.session_state.user_location_accuracy = None
        st.session_state.show_user_location = False
        st.session_state.selected_hlz = None if st.session_state.get("selected_hlz_from_nearest", False) else st.session_state.selected_hlz
        st.session_state.selection_distance_km = None
        st.session_state.map_center_mode = "data"

permission_status = st.session_state.location_permission_status
has_gps = st.session_state.user_latitude is not None and st.session_state.user_longitude is not None

if permission_status == "desktop_disabled":
    st.markdown(
        """
        <div style="background:#FEE2E2; color:#991B1B; border:1px solid #DC2626; "
             "border-left:6px solid #DC2626; border-radius:8px; padding:12px 14px; "
             "margin:0 0 0 0; font-weight:600;">
          <div style="font-size:1rem; margin-bottom:4px;">💻 Desktop/laptop detected</div>
          <div style="font-weight:500;">Location access is disabled on this device. You can still browse HLZs, use the Station Area and Suburb filters, and open navigation links.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif permission_status == "denied":
    st.warning(
        "Location access was declined or blocked. The current-location marker and Find Nearest HLZ feature are disabled and hidden until access is enabled. "
        "You can still use the map and search HLZs manually."
    )
    st.markdown("**To enable location access:**")
    st.markdown(
        "- **iPhone/iPad (Safari):** open Settings → Privacy & Security → Location Services → Safari Websites, then choose the appropriate location permission. Also check Settings → Apps → Safari → Location if that option appears on your iOS version. Return to Safari and reload this site.\n"
        "- **Android (Chrome):** open Chrome → ⋮ → Settings → Site settings → Location, allow location, and ensure this site is not blocked. You may also need Android Settings → Location enabled."
    )
    retry_col, help_col = st.columns([1, 2])
    with retry_col:
        if st.button("I've enabled access — retry", use_container_width=True):
            st.session_state.location_request_id += 1
            st.session_state.location_permission_status = "pending"
            st.session_state.gps_request_error = None
            st.session_state.user_latitude = None
            st.session_state.user_longitude = None
            st.session_state.user_location_accuracy = None
            st.session_state.show_user_location = False
            st.rerun()
    with help_col:
        st.caption("For security reasons, a website cannot reliably open the exact iOS or Android system-settings screen directly. Follow the steps above, then retry.")
elif permission_status == "insecure":
    st.warning("Location requires a secure HTTPS connection (or localhost for local testing). Open the hosted app using its HTTPS address.")
elif permission_status == "unsupported":
    st.warning("This browser does not support location access. Try opening the app in Safari or Chrome.")
elif permission_status == "unavailable":
    st.warning("The device could not determine a location. Check that device Location Services are enabled, then retry.")
elif permission_status == "error":
    st.warning(st.session_state.get("gps_request_error", "Location could not be obtained. Check your device and browser settings, then retry."))

# Only show location/nearest-HLZ controls after permission is granted and a
# valid coordinate fix has been received. If denied, the whole feature is hidden.
if has_gps and permission_status == "granted":
    loc_col, refresh_col, nearest_col = st.columns([1.15, 1.35, 1.6])
    with loc_col:
        st.success("📍 Location enabled")
    with refresh_col:
        if st.button("🔄 Refresh Location", use_container_width=True):
            st.session_state.location_request_id += 1
            st.session_state.location_permission_status = "pending"
            st.session_state.gps_request_error = None
            st.rerun()
    with nearest_col:
        if st.button("🚁 Find Nearest HLZ", use_container_width=True):
            with st.spinner("Finding the closest HLZ by road distance…"):
                overall_result = nearest_hlz(
                    df, st.session_state.user_latitude, st.session_state.user_longitude
                )
                matching_result = None
                if station != "All" or suburb != "All":
                    matching_result = nearest_hlz(
                        filtered, st.session_state.user_latitude, st.session_state.user_longitude
                    )
            if overall_result[0] is None:
                st.warning("No HLZ records have valid latitude and longitude coordinates.")
            else:
                st.session_state.nearest_results = {
                    "overall": overall_result,
                    "matching": matching_result,
                    "filters_active": station != "All" or suburb != "All",
                    "filter_station": station,
                    "filter_suburb": suburb,
                }
                st.session_state.show_user_location = True
                st.session_state.map_center_mode = "nearest"
                st.session_state.selected_hlz = None
                st.session_state.selected_hlz_from_nearest = True
                st.session_state.selection_distance_km = None
                st.session_state.selection_distance_mode = None
                st.session_state.ignore_next_map_click = True
                st.rerun()
    if st.session_state.get("nearest_results"):
        if st.button("✖ Exit Nearest HLZ Results", use_container_width=False):
            exit_nearest_mode()
            st.session_state.ignore_next_map_click = True
            st.rerun()
    accuracy = st.session_state.user_location_accuracy
    accuracy_text = f"GPS accuracy reported by device: ±{accuracy:.0f} m." if accuracy is not None else "Location permission granted."
    st.caption(f"Your location is held only in this app session and is not written to the HLZ database. {accuracy_text}")
elif permission_status == "not_requested" or permission_status == "pending":
    st.caption("Checking device type and location availability…")

# Normal HLZs keep the original helicopter emoji. During Find Nearest HLZ mode,
# only the two recommended locations switch to coloured map pins.
def helicopter_icon(size=38):
    return folium.DivIcon(
        html=f'<div style="width:{size}px;height:{size}px;font-size:{size-4}px;line-height:{size}px;text-align:center;filter:drop-shadow(0 1px 1px rgba(255,255,255,.95));">🚁</div>',
        icon_size=(size, size),
        icon_anchor=(size // 2, size // 2),
        class_name="hlz-helicopter-marker",
    )

def location_pin_svg(colour, size=40):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 48 48" aria-label="Highlighted HLZ location pin">
      <path d="M24 3.5 C13.4 3.5 5.5 11.3 5.5 21.1 C5.5 33.2 24 45 24 45 S42.5 33.2 42.5 21.1 C42.5 11.3 34.6 3.5 24 3.5 Z" fill="{colour}" stroke="#111827" stroke-width="2.8" stroke-linejoin="round"/>
      <circle cx="24" cy="20.5" r="7.2" fill="#FFFFFF" stroke="#111827" stroke-width="2"/>
    </svg>'''

def location_pin_icon(colour, size=40):
    svg = location_pin_svg(colour, size)
    return folium.DivIcon(
        html=f'<div style="width:{size}px;height:{size}px;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35));">{svg}</div>',
        icon_size=(size, size),
        icon_anchor=(size // 2, size),
        class_name="hlz-nearest-location-pin",
    )

# =========================
# Map
# =========================
nearest_results = st.session_state.get("nearest_results")
overall_idx = None
matching_idx = None
same_nearest_result = False
if has_gps and nearest_results:
    overall = nearest_results.get("overall")
    matching = nearest_results.get("matching")
    overall_idx = overall[0] if overall else None
    matching_idx = matching[0] if matching else None
    same_nearest_result = bool(
        nearest_results.get("filters_active", False)
        and overall and matching
        and overall_idx is not None and overall_idx == matching_idx
    )


st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
st.markdown("#### Map key")
if st.session_state.get("nearest_results"):
    if same_nearest_result:
        map_key_html = (
            '<div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;padding:8px 12px;'
            'background:rgba(127,127,127,0.08);border:1px solid rgba(127,127,127,0.25);border-radius:8px;'
            f'<span style="display:flex;align-items:center;gap:6px;">{location_pin_svg("#DC2626", 28)} <b>Closest overall &amp; matching filters</b></span>'
            '<span style="display:flex;align-items:center;gap:6px;font-size:15px;">🚁 <b>Other HLZs</b></span>'
            '<span style="font-size:15px;">🚑 <b>Your current location</b></span></div>'
        )
    else:
        map_key_html = (
            '<div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;padding:8px 12px;'
            'background:rgba(127,127,127,0.08);border:1px solid rgba(127,127,127,0.25);border-radius:8px;'
            f'<span style="display:flex;align-items:center;gap:6px;">{location_pin_svg("#2563EB", 28)} <b>Closest overall</b></span>'
            f'<span style="display:flex;align-items:center;gap:6px;">{location_pin_svg("#16A34A", 28)} <b>Closest matching filters</b></span>'
            '<span style="display:flex;align-items:center;gap:6px;font-size:15px;">🚁 <b>Other HLZs</b></span>'
            '<span style="font-size:15px;">🚑 <b>Your current location</b></span></div>'
        )
else:
    map_key_html = (
        '<div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;padding:8px 12px;'
        'background:rgba(127,127,127,0.08);border:1px solid rgba(127,127,127,0.25);border-radius:8px;">'
        '<span style="display:flex;align-items:center;gap:6px;font-size:15px;">🚁 <b>Helicopter landing zone (HLZ)</b></span>'
        '<span style="font-size:15px;">🚑 <b>Your current location</b></span></div>'
    )
st.markdown(map_key_html, unsafe_allow_html=True)

valid_filtered = filtered.dropna(subset=["Latitude", "Longitude"])
nearest_for_center_results = st.session_state.get("nearest_results")
nearest_for_center = nearest_for_center_results.get("overall") if nearest_for_center_results else None
if has_gps and st.session_state.map_center_mode == "user":
    center_lat = st.session_state.user_latitude
    center_lon = st.session_state.user_longitude
    map_zoom = 13
elif has_gps and st.session_state.map_center_mode == "nearest" and nearest_for_center and nearest_for_center[0] in df.index:
    nearest_row_for_center = df.loc[nearest_for_center[0]]
    center_lat = (st.session_state.user_latitude + float(nearest_row_for_center["Latitude"])) / 2
    center_lon = (st.session_state.user_longitude + float(nearest_row_for_center["Longitude"])) / 2
    map_zoom = 11
elif len(valid_filtered):
    center_lat = valid_filtered["Latitude"].mean()
    center_lon = valid_filtered["Longitude"].mean()
    map_zoom = 9
else:
    center_lat = -35.0
    center_lon = 150.6
    map_zoom = 9

# Map base layers
# Hybrid is the original OpenStreetMap map used in the first prototypes.
# Satellite uses a single satellite+labels tile source so the place names are
# baked into the same tiles as the imagery. This avoids the separate transparent
# Esri reference-label overlay that was not rendering reliably in Streamlit/Folium.
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=map_zoom,
    control_scale=True,
    tiles=None,
)

hybrid = folium.TileLayer(
    tiles="OpenStreetMap",
    name="Hybrid",
    overlay=False,
    control=True,
    show=True,
)
hybrid.add_to(m)

satellite = folium.TileLayer(
    tiles="https://mt1.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}",
    attr="Google Satellite",
    name="Satellite",
    overlay=False,
    control=True,
    show=False,
    max_zoom=21,
)
satellite.add_to(m)

# During nearest-HLZ mode, keep the entire HLZ network visible. Filters determine
# the green matching recommendation, but must not hide the other orange HLZs.
map_marker_records = df if (has_gps and nearest_results) else filtered
for idx, row in map_marker_records.iterrows():
    if pd.isna(row["Latitude"]) or pd.isna(row["Longitude"]):
        continue
    popup_html = f"<b>{row['HLZ Number']}</b><br>{row['Facility']}"
    # Keep the original helicopter icon for normal HLZs and all non-highlighted
    # sites. Use blue/green location pins only for nearest-mode recommendations.
    if has_gps and nearest_results and idx == overall_idx and same_nearest_result:
        marker = location_pin_icon("#DC2626", 42)
    elif has_gps and nearest_results and idx == overall_idx:
        marker = location_pin_icon("#2563EB", 42)
    elif has_gps and nearest_results and idx == matching_idx:
        marker = location_pin_icon("#16A34A", 42)
    else:
        marker = helicopter_icon(38)
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_html, max_width=260),
        icon=marker,
    ).add_to(m)

# Keep the overall nearest HLZ visible even when it falls outside the active filters.
if has_gps and nearest_results and overall_idx is not None and overall_idx in df.index and overall_idx not in filtered.index:
    row = df.loc[overall_idx]
    if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
        popup_html = f"<b>{row['HLZ Number']}</b><br>{row['Facility']}"
        folium.Marker(
            location=[float(row["Latitude"]), float(row["Longitude"])],
            popup=folium.Popup(popup_html, max_width=260),
            icon=location_pin_icon("#DC2626" if same_nearest_result else "#2563EB", 42),
        ).add_to(m)

if st.session_state.selected_hlz is not None and st.session_state.selected_hlz in df.index:
    selected_for_map = df.loc[st.session_state.selected_hlz]
    if pd.notna(selected_for_map["Latitude"]) and pd.notna(selected_for_map["Longitude"]):
        already_in_filtered = st.session_state.selected_hlz in filtered.index
        if not already_in_filtered:
            folium.Marker(
                location=[float(selected_for_map["Latitude"]), float(selected_for_map["Longitude"])],
                popup=folium.Popup(f"<b>{selected_for_map['HLZ Number']}</b><br>{selected_for_map['Facility']}", max_width=260),
                icon=helicopter_icon(38),
            ).add_to(m)

# Current position is displayed automatically after permission is granted.
# Coordinates remain in session state only and are not written to the HLZ database.
if has_gps:
    folium.Marker(
        location=[st.session_state.user_latitude, st.session_state.user_longitude],
        tooltip="Your current location",
        popup=folium.Popup("<b>🚑 Your current location</b>", max_width=220),
        icon=folium.DivIcon(html='<div style="font-size:30px; text-align:center; text-shadow:0 0 3px white;">🚑</div>'),
        z_index_offset=1000,
    ).add_to(m)

# Automatically frame the relevant map extent:
# - # no filters: every valid HLZ plus current position (when available)
# - filters active: matching HLZs plus current location
# - nearest result: include the selected nearest HLZ as well
# fit_bounds gives a useful overview regardless of whether GPS is available.
map_extent_points = []
nearest_results_for_extent = st.session_state.get("nearest_results")
if has_gps and nearest_results_for_extent:
    # All HLZ markers remain visible in nearest mode, so fit the whole network
    # as well as the current location instead of framing only the recommendations.
    for _, extent_row in df.dropna(subset=["Latitude", "Longitude"]).iterrows():
        map_extent_points.append([float(extent_row["Latitude"]), float(extent_row["Longitude"])])
else:
    for _, extent_row in filtered.dropna(subset=["Latitude", "Longitude"]).iterrows():
        map_extent_points.append([float(extent_row["Latitude"]), float(extent_row["Longitude"])])

if has_gps:
    map_extent_points.append([
        float(st.session_state.user_latitude),
        float(st.session_state.user_longitude),
    ])

if len(map_extent_points) == 1:
    m.location = map_extent_points[0]
    m.options["zoom"] = 13
elif len(map_extent_points) > 1:
    m.fit_bounds(map_extent_points, padding=(24, 24), max_zoom=13)

# Map view selector: Hybrid (default) or Satellite.
folium.LayerControl(
    position="topright",
    collapsed=True,
).add_to(m)

map_data = st_folium(
    m,
    width=None,
    height=560,
    returned_objects=["last_object_clicked"],
    key=f"hlz_map_{st.session_state.map_component_version}",
)

# =========================
# Selected HLZ
# =========================
clicked = map_data.get("last_object_clicked") if map_data else None

# After Clear Selected, st_folium may still report the previous marker click
# once. Do not immediately re-select it.
if st.session_state.ignore_next_map_click:
    clicked = None
    st.session_state.ignore_next_map_click = False

if clicked:
    click_lat = clicked.get("lat")
    click_lng = clicked.get("lng")

    # Clicking the ambulance marker should not also select a nearby HLZ.
    clicked_user_marker = (
        st.session_state.show_user_location
        and has_gps
        and click_lat is not None
        and click_lng is not None
        and abs(float(click_lat) - st.session_state.user_latitude) < 0.00002
        and abs(float(click_lng) - st.session_state.user_longitude) < 0.00002
    )

    if click_lat is not None and click_lng is not None and len(df) and not clicked_user_marker:
        # Resolve clicks against the full HLZ database, not only filtered results.
        # This lets users select any visible HLZ while nearest mode is active.
        click_candidates = df.dropna(subset=["Latitude", "Longitude"]).copy()
        if not click_candidates.empty:
            click_candidates["_click_distance_km"] = click_candidates.apply(
                lambda row: haversine_km(click_lat, click_lng, row["Latitude"], row["Longitude"]),
                axis=1,
            )
            selected_index = click_candidates["_click_distance_km"].idxmin()
            st.session_state.selected_hlz = selected_index
            st.session_state.selection_distance_km = None
            st.session_state.map_center_mode = "data"

# Nearest results live directly below the single persistent map. Each result has
# its own expandable heading; there is no extra parent accordion.
nearest_results = st.session_state.get("nearest_results")
if has_gps and nearest_results:
    overall = nearest_results.get("overall")
    matching = nearest_results.get("matching")
    filters_active = nearest_results.get("filters_active", False)
    filter_station = nearest_results.get("filter_station", "All")
    filter_suburb = nearest_results.get("filter_suburb", "All")

    def _display_value(value):
        if pd.isna(value) or str(value).strip() == "":
            return "Not specified"
        return str(value).strip()

    applied = []
    if filter_station and filter_station != "All":
        applied.append(f"Station Area: {filter_station}")
    if filter_suburb and filter_suburb != "All":
        applied.append(f"Suburb: {filter_suburb}")
    applied_text = " · ".join(applied) if applied else "No filters selected"

    def nearest_result_card(result, heading, colour, distance_label, show_applied_filters=False):
        if not result or result[0] is None or result[0] not in df.index:
            return
        idx, distance_km, mode = result
        record = df.loc[idx]
        if mode == "road":
            distance_text = f"{distance_label}: {distance_km:.2f} km driving distance"
        else:
            distance_text = f"{distance_label}: {distance_km:.2f} km straight-line (road routing unavailable)"

        hlz_number = _display_value(record.get("HLZ Number", ""))
        suburb = _display_value(record.get("Suburb", ""))
        lat_value = record.get("Latitude", None)
        lon_value = record.get("Longitude", None)

        details = [
            ("Facility", "Facility"),
            ("Station Area", "Station Area"),
            ("Suburb", "Suburb"),
            ("Street Address", "Street Address"),
            ("Entry Point (What3Words)", "What3Words"),
            ("Location (Latitude, Longitude)", None),
            ("Landing Surface", "Landing Surface"),
            ("Gate", "Gate"),
            ("Windsock", "Windsock"),
            ("Lighting", "Lighting"),
            ("Notes", "Notes"),
        ]
        rows_html = []
        for label, column in details:
            if column is None:
                lat = _display_value(record.get("Latitude", ""))
                lon = _display_value(record.get("Longitude", ""))
                value = f"{lat}, {lon}" if lat != "Not specified" and lon != "Not specified" else "Not specified"
            else:
                value = _display_value(record.get(column, ""))
            if column == "What3Words" and value.startswith("///") and value != "Not specified":
                words = value[3:].replace("/", "").strip()
                value_html = f'<a href="https://what3words.com/{html.escape(words, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(value)}</a>'
            else:
                value_html = html.escape(value).replace("\n", "<br>")
            rows_html.append(
                '<div style="padding:7px 0;border-bottom:1px solid rgba(127,127,127,.22);">'
                f'<div style="font-size:.78rem;font-weight:700;opacity:.78;margin-bottom:2px;">{html.escape(label)}</div>'
                f'<div style="overflow-wrap:anywhere;">{value_html}</div></div>'
            )

        navigation_html = '<div style="margin-top:12px;color:#667085;">Navigation unavailable: this HLZ does not have valid coordinates.</div>'
        try:
            lat_num, lon_num = float(lat_value), float(lon_value)
            if math.isfinite(lat_num) and math.isfinite(lon_num):
                nav_items = [
                    ("Google Maps", f"https://www.google.com/maps/dir/?api=1&amp;destination={lat_num},{lon_num}"),
                    ("Apple Maps", f"https://maps.apple.com/?daddr={lat_num},{lon_num}"),
                    ("Waze", f"https://www.waze.com/ul?ll={lat_num}%2C{lon_num}&amp;navigate=yes"),
                ]
                w3w_value = _display_value(record.get("What3Words", ""))
                if w3w_value != "Not specified":
                    clean_words = w3w_value.replace("///", "").strip()
                    w3w_url = "https://what3words.com/" + quote(clean_words, safe=".")
                    nav_items.append(("What3Words", html.escape(w3w_url, quote=True)))
                else:
                    nav_items.append(("What3Words", None))

                buttons = []
                for nav_name, nav_url in nav_items:
                    if nav_url:
                        buttons.append(
                            f'<a href="{nav_url}" target="_blank" rel="noopener noreferrer" '
                            'style="display:block;text-align:center;padding:10px 8px;border-radius:8px;'
                            'background:#1E5AA8;color:#fff;text-decoration:none;font-weight:700;'
                            'font-size:.9rem;">' + html.escape(nav_name) + '</a>'
                        )
                    else:
                        buttons.append(
                            '<span title="No What3Words entry point is recorded for this HLZ" '
                            'style="display:block;text-align:center;padding:10px 8px;border-radius:8px;'
                            'background:#8A949E;color:#fff;font-weight:700;font-size:.9rem;opacity:.75;">'
                            'What3Words unavailable</span>'
                        )
                navigation_html = (
                    '<div style="margin-top:14px;font-weight:750;">Navigate to this HLZ</div>'
                    '<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:8px;">'
                    + ''.join(buttons) + '</div>'
                )
        except (TypeError, ValueError):
            pass

        applied_html = ""
        if show_applied_filters:
            applied_html = (
                '<div style="border-left:4px solid #16A34A;padding:8px 12px;margin:10px 0 4px;'
                'border-radius:5px;background:rgba(22,163,74,.08);">'
                '<div style="font-weight:750;color:#16A34A;margin-bottom:3px;">Filters applied to this result</div>'
                f'<div>{html.escape(applied_text)}</div></div>'
            )

        card_html = (
            f'<details style="border:2px solid {colour};border-left:8px solid {colour};'
            'border-radius:10px;margin:10px 0 14px 0;background:rgba(127,127,127,.06);overflow:hidden;">'
            '<summary style="cursor:pointer;list-style-position:inside;padding:13px 14px;font-weight:750;">'
            f'<span style="display:inline-flex;vertical-align:middle;margin-right:7px;">{location_pin_svg(colour, 30)}</span>'
            f'<span style="color:{colour};">{html.escape(heading)}</span>'
            f'<div style="font-size:1.06rem;font-weight:700;margin:7px 0 0 2px;">'
            f'{html.escape(hlz_number)} — {html.escape(suburb)}</div>'
            f'<div style="font-size:.9rem;font-weight:400;margin:5px 0 0 2px;">{html.escape(distance_text)}</div>'
            '</summary><div style="padding:4px 14px 14px 14px;">'
            + applied_html + ''.join(rows_html) + navigation_html + '</div></details>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

    same_result = bool(filters_active and overall and matching and overall[0] is not None and overall[0] == matching[0])
    overall_heading = "Closest Overall & Closest Matching Filters" if same_result else "Closest HLZ Overall"
    # When both recommendations are the same record, include filter context in
    # that one dropdown instead of duplicating the result.
    overall_colour = "#DC2626" if same_result else "#2563EB"
    nearest_result_card(
        overall, overall_heading, overall_colour, "Overall distance",
        show_applied_filters=bool(filters_active and same_result),
    )
    if filters_active:
        if matching and matching[0] is not None:
            if not same_result:
                nearest_result_card(
                    matching, "Closest HLZ Matching Filters", "#16A34A",
                    "Matching-filter distance", show_applied_filters=True,
                )
        else:
            st.info("No HLZs match the selected Station Area/Suburb filters. The closest overall HLZ is shown above.")
    if same_result:
        st.caption("Map highlights: red pin = closest overall and closest matching filters; 🚁 = other HLZs.")
    else:
        st.caption("Map highlights: blue pin = closest overall; green pin = closest matching filters; 🚁 = other HLZs.")

# Deliberate space between the map and the Selected HLZ heading.
st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
st.markdown('<div id="hlz-details"></div>', unsafe_allow_html=True)

if st.session_state.selected_hlz is not None and st.session_state.selected_hlz in df.index:
    selected_row = df.loc[st.session_state.selected_hlz]

    with st.container(border=True):
        st.markdown('<div style="font-size:1.2rem;font-weight:750;margin:0 0 6px 0;">Selected HLZ Details</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:0.88rem; color:#5A6772; margin:0 0 0.05rem 0; padding:0;">'
            'The information below relates to the HLZ selected on the map above.'
            '</div>',
            unsafe_allow_html=True,
        )
    
        if st.session_state.selection_distance_km is not None:
            distance_mode = st.session_state.get("selection_distance_mode") or "straight-line fallback"
            if distance_mode == "road":
                st.success(
                    f"🚁 Nearest HLZ by road distance: {selected_row['HLZ Number']} — "
                    f"{selected_row['Facility']} · {st.session_state.selection_distance_km:.2f} km driving distance."
                )
            else:
                st.warning(
                    f"🚁 Nearest HLZ by straight-line distance (routing service unavailable): "
                    f"{selected_row['HLZ Number']} — {selected_row['Facility']} · "
                    f"{st.session_state.selection_distance_km:.2f} km straight-line."
                )
        show_details(selected_row)

    # Attempt to scroll the main Streamlit page to the selected HLZ section
    # after the map selection causes a rerun.
    st.html(
        """
        <script>
        (function() {
            function scrollToHLZ() {
                const el = document.getElementById("hlz-details");
                if (el) {
                    el.scrollIntoView({behavior: "smooth", block: "start"});
                }
            }
            setTimeout(scrollToHLZ, 150);
            setTimeout(scrollToHLZ, 500);
            setTimeout(scrollToHLZ, 1000);
        })();
        </script>
        """,
        unsafe_allow_javascript=True,
    )
elif st.session_state.selected_hlz is None:
    st.info("Select an 🚁 on the map to view the HLZ details.")

st.markdown(
    '<div style="margin-top:1.2rem; padding-top:0.8rem; border-top:1px solid #CBD5E1;">'
    '<strong>Issues, faults, feedback or questions?</strong><br>'
    '<a href="mailto:xxx@email.com.au?subject=Shoalhaven%20HLZ%20application" '
    'style="color:#1E5AA8; font-weight:600; text-decoration:underline;">'
    '✉ Email the HLZ application team</a>'
    '</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Prototype: HLZ records are loaded from a local CSV. Current location uses browser/device GPS permission and is not saved to the database. "
    "The production version can connect to the approved master data source."
)
