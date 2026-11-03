# Shoalhaven HLZ Map — Prototype 78

## Changes in Prototype 68

## Changes in Prototype 78

- Added a bold blue left border to the “Select an 🚁 on the map to view the HLZ details” banner.
- Made the Search HLZs accordion more prominent with a blue border, light-blue header, bold heading, and subtle shadow.

## Changes in Prototype 77

- Restored the original laptop icon (💻) in the desktop/laptop detected banner.
- Changed the Location enabled banner spacing from a right margin to a 16px bottom margin so the gap appears vertically on mobile before the Refresh Location button.



This prototype carries forward the existing Shoalhaven Landing Zones app and includes the following updates:

- Added free-text keyword search across **Station Area**, **Suburb**, **Notes**, and **Street Address**.
- Keyword search supports case-insensitive partial matches and literal text (not regular expressions).
- Fixed abbreviation normalisation so searches such as `rd` correctly match `road` (and vice versa).
- Keyword search recognises common address abbreviations and their full forms, including `rd`/`road`, `st`/`street`, `ave`/`avenue`, `dr`/`drive`, `ct`/`court`, `cres`/`crescent`, `hwy`/`highway`, `ln`/`lane`, `pl`/`place`, `pde`/`parade`, `tce`/`terrace`, and `cl`/`close`. For example, searching `Princes Hwy` can match `Princes Highway`, and `Main St` can match `Main Street`.
- Keyword search works alongside the existing Station Area and Suburb dropdown filters.
- Filter result counts update to reflect the active filters.
- Reset Filters clears the keyword search as well as the dropdown filters.
- Updated the contact email link to **shoalhavenhlz@gmail.com**.
- Removed the current-location ambulance icon from the map legend.
- Kept current-location functionality for supported mobile devices.
- Removed the non-working current-location display/information from desktop and laptop layouts.
- Restored the previous desktop/laptop warning information, with a laptop icon (💻) at the start.
- Added coloured left borders to the mobile current-location information banners: blue for the location information banner and green for the Location enabled banner.
- Added a 16px bottom margin to the green Location enabled banner to create a vertical gap before the Refresh Location button on mobile.
- Updated the desktop/laptop warning icon to a laptop (💻).
- Changed the location access declined/blocked message to a red warning banner with a red left border and warning icon.
- Added a small 8px gap below the blue location information banner before the green Location enabled or red declined/blocked banner.
- Changed the desktop/laptop warning banner to a red style with a red left border. The warning explains that location access is disabled on the device, while users can still browse and select HLZs on the map, use the search function, and open navigation links.

## Deployment

Replace `app.py` in the existing prototype/repository with the version in this ZIP. The ZIP contains only the updated prototype application and this README; unchanged files, including `hlz_database.csv`, are intentionally excluded.

Keep your existing `hlz_database.csv` and other project assets unless a future update specifically identifies them as changed.

## Version numbering

This release is **Prototype 78**. The next update will be **Prototype 79**, followed by 80, 81, and so on.
