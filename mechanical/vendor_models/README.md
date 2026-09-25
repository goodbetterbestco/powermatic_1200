# Powermatic vendor STEP models

Sourced 2026-09-25 from the current `Powermatic_BOM_revP.csv`.

**20 of 24 active BOM lines have STEP files.** An additional model covers the quantity-zero HMX1-AUX11-F row: 21 vendor models total.

## DIN rail reference

**35 mm wide × 7.5 mm high top-hat DIN rail**. Height is measured from the rail mounting base to the top of the profile. Reference: [AutomationDirect DN-R35S1](https://www.automationdirect.com/adc/shopping/catalog/wire_-a-_cable_management/din_rail/din_rail/dn-r35s1). Rail and duct models are being made separately by the user.

## Import and validation

- Open the files in `step/` in Fusion 360 or use them as source models for later KiCad footprint work.
- Geometry and native orientations are unchanged. Front-up orientation and mounting origins still need to be established.
- Honor the STEP files’ embedded units. Several AD files declare inches; others declare millimeters. Do not apply a blanket 25.4 scale conversion.
- All downloaded STEP files pass header/footer, unique entity, referenced entity and declared-unit checks. See `validation.json`.
- Selected vendor models have been imported and measured; see `../layout_models/step_measurements.json`. The M12 socket also imported successfully and passed BRep validity; see `geometry_checks.json`. Full dimension, mounting datum, terminal-location and assembly-clearance review remains pending.
- `manifest.json` records source URLs, exact/family status and SHA-256 hashes. Original AD drawing ZIPs and extracted PDFs are in `drawings/`.

## Downloaded models

| BOM part | Part name | STEP | Match / notes |
|---|---|---|---|
| HMC-9B30-11-DS | Power Contactor | [HMC-9B30-11-DS.step](step/HMC-9B30-11-DS.step) | Exact SKU source |
| HMX1-MI | Contactor Interlock | [HMX1-MI.step](step/HMX1-MI.step) | Exact SKU source |
| HC3096N-52-900-24 | Coil Enable Relay | [HC3096N-52-900-24.step](step/HC3096N-52-900-24.step) | Exact SKU source |
| HMX1-BBREV | Reversing Busbars | [HMX1-BBREV.step](step/HMX1-BBREV.step) | Exact SKU source |
| HMX1-AUX11-F | Auxiliary Contact Block | [HMX1-AUX11-F.step](step/HMX1-AUX11-F.step) | Exact SKU source; optional, qty 0 |
| NDR-240-24 | DC Power Supply | [NDR-240.stp](step/NDR-240.stp) | Family model |
| FAZ-D4-2-NA-L | Circuit Breaker | [FAZ-D4-2-NA-L.step](step/FAZ-D4-2-NA-L.step) | Exact SKU source |
| 22013003 | Motor Disconnect | [22013003.step](step/22013003.step) | Exact SKU source |
| 148E1111 | Disconnect Handle | [148E1111.step](step/148E1111.step) | Exact SKU source |
| 14070532 | Disconnect Shaft | [14070532.step](step/14070532.step) | Exact SKU source |
| 22943016 | Terminal Cover Pack | [22943016.step](step/22943016.step) | Exact SKU source |
| RM25030-3SR | Class R Fuse Holder | [RM25030-3SR.step](step/RM25030-3SR.step) | Exact SKU source |
| CVR-RH-25030 | Fuse Cover | [CVR-RH-25030.step](step/CVR-RH-25030.step) | Exact SKU source |
| HTOR32-6-S | Thermal Overload | [HTOR32-6-S.step](step/HTOR32-6-S.step) | Exact SKU source |
| HMX1-SSVRC-DC | Coil Surge Suppressor | [HMX1-SSVRC-DC.step](step/HMX1-SSVRC-DC.step) | Exact SKU source |
| 4008-XB4BVB1-ND | White Indicator | [XB4BVB1.stp](step/XB4BVB1.stp) | Exact SKU source |
| A125513-ND | M12 Panel Socket | [T4171310004-001.stp](step/T4171310004-001.stp) | TE revision B; manufacturer download supplied by user |
| KN-T12GRY-25 | Feedthrough Terminal | [KN-T12GRY-25.step](step/KN-T12GRY-25.step) | Exact SKU source |
| KN-ECT6GRY-25 | Terminal End Cover | [KN-ECT6GRY-25.step](step/KN-ECT6GRY-25.step) | Exact SKU source |
| KN-EB7-10 | DIN End Stop | [KN-EB7-10.step](step/KN-EB7-10.step) | Exact SKU source |
| KN-10J12 | Terminal Jumper | [KN-10J12.step](step/KN-10J12.step) | Exact SKU source |

The NDR-240 file is the manufacturer’s family model for the NDR-240 series. The Schneider lamp file is the current XB4BVB1_NEW_2024 model. Packaged accessories are not necessarily represented as the full package quantity. The shaft remains at its supplied CAD length.

## Remaining model work

| Part | Status | Evidence / next step |
|---|---|---|
| FRN-R-10 | model not required | User excluded the fuse itself from STEP sourcing. The fuse holder and its cover are already downloaded. |
| L15-20 plug | deferred | Outside the panel enclosure; user deferred modeling. |
| 365-TAV2111 | deferred | Outside the panel enclosure; user deferred modeling the retained drum switch. Saved catalog PDF: drawings/365-TAV2111_saved_reference.pdf. |
| 800S-3SA catalog mapping | deferred | Outside the panel enclosure; user deferred modeling the fixed FOR/REV/STOP station. Actual marking: Allen-Bradley Bulletin 800, Type 3SA; see identification note below. |
| KN-L5X-BLNK-220 | not found | No STEP or drawing ZIP link found on the checked AutomationDirect product page. |

“Not found” means no usable manufacturer STEP file was located in the checked sources; it does not establish that none exists. Current layout work focuses on the panel enclosure. The fuse model is excluded, and modeling of the external L15-20 plug, drum switch and button station is deferred by the user. These external models do not block the panel layout. The terminal marker is the remaining vendor-model gap. BOM quantities are unchanged.

[Pushbutton station identification](800_3SA_identification.md) distinguishes the vintage marking from the later 800S-3SA designation and documents the supporting manufacturer references. The station is surface mounted; earlier acquisition/BOM records called it a pendant.

## Files

- `step/`: importable vendor STEP/STP files.
- `drawings/`: supporting dimensional drawings and original AD archives.
- `manifest.json`: BOM-to-model mapping and sources.
- `validation.json`: structural checks and declared units.
- `geometry_checks.json`: M12 socket CAD import, solid validity and native coordinate bounds.
- `archives/`: original manufacturer ZIPs, including the user-supplied TE download.
- `ad_sources.json`, `other_sources.json`, `fallback_sources.json`: acquisition records, including failed attempts.
- `source_pages/`: retrieved source pages.
