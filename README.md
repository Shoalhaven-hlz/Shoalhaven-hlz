# Shoalhaven HLZ Map — Prototype 89 (Full project package)

## Prototype 89 updates
- Removed the embedded browser component's “Location access granted.” status text on mobile after a successful GPS fix.
- Collapsed the permission component iframe to zero height after success, removing the gap beneath Search HLZs.
- Preserved the green “Location enabled” banner, GPS coordinates, refresh control, and nearest-HLZ functionality.
- No other location status messages or permission handling changed.


## Prototype 87 updates
- Increased the main **Map** heading from 1.15rem to 1.5rem.
- Tightened the map key vertical spacing: legend rows now use a 6px row gap and the **Map key** heading has no extra bottom margin. Horizontal spacing remains unchanged.
- Kept `app.py` as the sole Python app entry point; removed the redundant `hlz_streamlit_app_fixed.py`.
- Full project package retains the database, branding assets, HTML, requirements and configuration files.

# Shoalhaven HLZ Map — Prototype 86 (Full project package)

## Prototype 86 updates
- Updated both `app.py` and `hlz_streamlit_app_fixed.py` to the same current Shoalhaven HLZ application code, preventing an older alternate Python entrypoint from being deployed.
- The map section is plain **Map** text, without a Markdown heading anchor.
- **Map key** appears inside the map legend banner above the marker labels.
- Removed the redundant “Location permission granted” caption. The current-location privacy note and GPS accuracy remain.
- Full project package includes database, images, HTML, requirements and configuration files.

# Shoalhaven HLZ Map — Prototype 85 (Full project package)

## Prototype 85 updates
- Corrected the actual root `app.py` Streamlit entry point, not just the prototype folder file.
- Map section heading is plain **Map** with no Markdown anchor link.
- Added **Map key** as a heading inside the legend banner above its marker labels.
- This package includes the complete project so all deployment files can be replaced together.

# Shoalhaven HLZ Map — Prototype 67

Fix: When Find Nearest HLZ is active, show the entire HLZ network on the map. The closest overall and closest matching results retain their highlighted pins, while all other HLZs remain visible as orange helicopter markers. Filters still determine which HLZ qualifies as the closest matching result.

Deploy by replacing `app.py` in the existing repository. Keep your current `hlz_database.csv` if it contains newer records.


## Shoalhaven Landing Zones branding update

This update is based on the supplied `app.py`, `index.html`, and the matching project ZIP. It is intended as a branding-only change:
- Keeps the existing Streamlit map, filters, nearest-HLZ behaviour, navigation and admin prototype code.
- Adds a navy/orange Shoalhaven Landing Zones banner.
- Sets the Streamlit page icon to the supplied branded icon image.

### Important iPhone Home Screen icon limitation
The banner and Streamlit page icon do not, by themselves, guarantee that Safari's **Add to Home Screen** shortcut will use the custom icon. The iOS Home Screen icon is normally read from an `apple-touch-icon` link in the actual top-level page HTML. `index.html` in this project is a Streamlit custom component used for location/auth messaging; it is not the top-level Streamlit page HTML, so changing it will not set Safari's Home Screen icon. Streamlit Community Cloud does not provide a normal setting for editing that top-level HTML head. A separate hosting/proxy/PWA approach may be required to guarantee a custom iPhone icon. Do not replace this component's `index.html` with a generic HTML page, as that would break the existing location/auth bridge.


## Prototype 88 changes
- Mobile: hide the green “Location enabled” status banner beneath the search controls. GPS, refresh, and nearest-HLZ controls remain available.
- Selected HLZ details: replace the white rounded/shadow spacer with a thin horizontal divider and modest spacing.


## Prototype 90
- Updated the Selected HLZ Details explanatory text to use Streamlit `var(--text-color)`, adapting automatically to light and dark themes.
- Kept the horizontal divider and its spacing unchanged.


## Prototype 91
- Updated Map key styling: orange heading text and a prominent 3px orange border around the key container.
- Preserved map key entries, pins, and responsive layout.


## Prototype 92
- Map key retains a subtle light blue/grey background.
- Map key border changed to 2px orange; heading remains orange.
- Legend entries and spacing preserved.
