# Shoalhaven HLZ Map — Prototype 69

## Changes in Prototype 68

This prototype carries forward the existing Shoalhaven Landing Zones app and includes the following updates:

- Added free-text keyword search across **Station Area**, **Suburb**, **Notes**, and **Street Address**.
- Keyword search supports case-insensitive partial matches and literal text (not regular expressions).
- Keyword search works alongside the existing Station Area and Suburb dropdown filters.
- Filter result counts update to reflect the active filters.
- Reset Filters clears the keyword search as well as the dropdown filters.
- Updated the contact email link to **shoalhavenhlz@gmail.com**.
- Removed the current-location ambulance icon from the map legend.
- Kept current-location functionality for supported mobile devices.
- Removed the non-working current-location display/information from desktop and laptop layouts.
- Restored the previous desktop/laptop warning information, with a computer icon (💻) at the start.
- Changed the desktop/laptop warning banner to a red style with a red left border. The warning explains that location access is disabled on the device, while HLZ browsing, Station Area/Suburb filters, and navigation links remain available.

## Deployment

Replace `app.py` in the existing prototype/repository with the version in this ZIP. The ZIP contains only the updated prototype application and this README; unchanged files, including `hlz_database.csv`, are intentionally excluded.

Keep your existing `hlz_database.csv` and other project assets unless a future update specifically identifies them as changed.

## Version numbering

This release is **Prototype 69**. The next update will be **Prototype 70**, followed by 71, 72, and so on.
