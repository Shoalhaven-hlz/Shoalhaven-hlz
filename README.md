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
