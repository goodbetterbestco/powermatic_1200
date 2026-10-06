# Terminal routing review

All 29 gray feedthrough schematic symbols are vertical with pin 1 above pin 2. Physical pin 1 is TOP and pin 2 is BOT on all 29 gray feedthrough footprints and all three PE footprints. No PCB placement was changed.

Your final vertical M12 drawing and wire paths were preserved. All four panel pigtails use BOT; the distribution feed, coil-enable return and midpoint bridge use TOP. The incoming phase block identities follow the existing backplate: TB40/L1, TB41/L2 and TB42/L3. Replaced M12/terminal schematic UUIDs were matched to the existing hardware footprint links, preventing duplicate additions on the next PCB update.

## PS1 and mains labels

PS1 uses 1_BOT (PE), 2_BOT (N), 3_BOT (L), 1_TOP/2_TOP (-V), and 3_TOP/4_TOP (+V), consistent with its manufacturer terminal drawing. Its three old schematic landing captions are replaced with PS1.1_BOT, PS1.1_TOP and PS1.3_TOP. Five CSV pin fields follow that numbering. The three mains CSV pin labels are L1/L2/L3. Other user-edited CSV data is preserved.

## Routing method

The saved board has three 40 mm horizontal ducts centered at Y=52, 207 and 412 mm and an unsplit right trunk at X=430 mm. Horizontal half-ducts 1–6 have centerlines Y=42/62, 197/217 and 402/422 mm. The saved board does not contain a fourth horizontal duct for halves 7/8.

Top device connections use the duct above the device; bottom connections use the duct below. Sidewall connections enter through the closest open duct end. External motor, control and mains conductors use their respective glands. Different whole ducts transition to their whole-duct centerlines and route through the right trunk; connections in the same whole duct use the target half-duct centerline. Listed differences exclude cut/slack allowance and are estimates from the modeled terminal positions.

## Assignments using the longer side

| Terminal pin | Endpoint | Assigned side | Closer side | Extra route estimate, mm | Closer clamp assignment |
|---|---|---|---|---:|---|
| TB2.1 | K3.13 | TOP | BOT | 573.0 | SPARE |
| TB12.1 | K3.A2 | TOP | BOT | 529.0 | K4.A2_BOT |
| TB14.1 | PS1.1_TOP | TOP | BOT | 509.0 | K6.A2_BOT |
| TB20.1 | K4.43 | TOP | BOT | 365.8 | K6.43 |
| TB30.1 | K3.A1+ | TOP | BOT | 675.0 | S1.4, J6.4, J1.4 |
| TB50.1 | J3.G | TOP | BOT | 158.0 | MOTOR |
| TB51.1 | PS1.1_BOT | TOP | BOT | 158.0 | BACKPLATE |
| TB60.1 | K5.2 | TOP | BOT | 381.3 | SPARE |
| TB61.1 | OL1.2 | TOP | BOT | 488.9 | M1.T1 |
| TB62.1 | K5.4 | TOP | BOT | 357.3 | SPARE |
| TB63.1 | OL1.4 | TOP | BOT | 460.3 | M1.T2 |
| TB64.1 | K5.6 | TOP | BOT | 333.3 | SPARE |
| TB65.1 | OL1.6 | TOP | BOT | 431.7 | M1.T3 |
| TB66.1 | OL2.4 | TOP | BOT | 570.3 | M1.T4 |
| TB67.1 | OL2.6 | TOP | BOT | 541.7 | M1.T5 |
| TB68.1 | OL2.2 | TOP | BOT | 598.9 | M1.T6 |

TB2.2 and TB60.2/TB62.2/TB64.2 are marked SPARE for wire landings. These are the simplest candidate changes, provided the existing bridge hardware is accounted for.

The other closer clamps are occupied. TB30 is an intentional exception to keep all four M12 pigtails on one side and route the coil feed from the other side. Each paired motor group has three conductors but only two BOT clamps, so at least one conductor requires another side if each clamp accepts one conductor. No wire was silently moved or doubled into an occupied clamp.

## All terminal assignments

| Terminal | PCB pin 1 TOP / pin 2 BOT | Pin 1 assignment | Pin 2 assignment | Routing finding |
|---|---|---|---|---|
| TB1 | Yes | H1.X1 | PS1.3_TOP | No identified side detour |
| TB2 | Yes | K3.13 | SPARE | longer side |
| TB3 | Yes | J1.1 | SPARE | stale caption: J1.1 already lands on TB31.2; distribution feed to TB31 is not documented as a physical wire |
| TB10 | Yes | SPARE | K1.A2_BOT | No identified side detour |
| TB11 | Yes | SPARE | K2.A2_BOT | No identified side detour |
| TB12 | Yes | K3.A2 | K4.A2_BOT | longer side |
| TB13 | Yes | H1.X2 | K5.A2_BOT | No identified side detour |
| TB14 | Yes | PS1.1_TOP | K6.A2_BOT | longer side |
| TB20 | Yes | K4.43 | K6.43 | longer side |
| TB21 | Yes | SPARE | J5.1 | No identified side detour |
| TB22 | Yes | K1.43 | K4.44 | No identified side detour |
| TB23 | Yes | K2.43 | K6.44 | No identified side detour |
| TB24 | Yes | SPARE | J5.2 | No identified side detour |
| TB30 | Yes | K3.A1+ | S1.4, J6.4, J1.4 | longer side |
| TB31 | Yes | +24V | S1.1, J6.1, J1.1 | endpoint not located / no documented physical wire |
| TB32 | Yes | TB33.1 | S1.3, J6.2, J1.2 | No identified side detour |
| TB33 | Yes | TB32.1 | S1.2, J6.3, J1.3 | No identified side detour |
| TB40 | Yes | FH1.P1.A | J2.X | No identified side detour |
| TB41 | Yes | FH1.P2.A | J2.Y | No identified side detour |
| TB42 | Yes | FH1.P3.A | J2.Z | No identified side detour |
| TB50 | Yes | J2.G | MOTOR | longer side; endpoint not located / no documented physical wire |
| TB51 | Yes | PS1.1_BOT | BACKPLATE | longer side; endpoint not located / no documented physical wire |
| TB52 | Yes | ENCLOSURE | DOOR | endpoint not located / no documented physical wire; endpoint not located / no documented physical wire |
| TB60 | Yes | K5.2 | SPARE | longer side |
| TB61 | Yes | OL1A.2 | M1.T1 | longer side |
| TB62 | Yes | K5.4 | SPARE | longer side |
| TB63 | Yes | OL1A.4 | M1.T2 | longer side |
| TB64 | Yes | K5.6 | SPARE | longer side |
| TB65 | Yes | OL1A.6 | M1.T3 | longer side |
| TB66 | Yes | OL2A.4 | M1.T4 | longer side |
| TB67 | Yes | OL2A.6 | M1.T5 | longer side |
| TB68 | Yes | OL2A.2 | M1.T6 | longer side |

## Remaining consistency items

- PS1's library footprint and placed PCB footprint still use the old TB1.x/TB2.x pad numbers. Rename those pads to the updated symbol numbers before relying on Update PCB from Schematic. The pad coordinates and model placement were preserved.
- TB3 TOP still has a J1.1 caption, but that pigtail now lands on TB31.2. The actual distribution-to-TB31 feed needs a documented physical endpoint and wire-schedule row.
- Several CSV landings differ from the schematic notes. In particular, the CSV still assigns TB32 TOP to K3.A1+, while the schematic uses TB30 TOP. There are also 0V, CTRL and paired-motor assignment differences. Those other CSV cells were preserved.
- Motor captions still use OL1A/OL2A even though the device designators are OL1/OL2.
- Chassis, door and backplate stud coordinates are not modeled electrical endpoints, so their shortest terminal side cannot be established from the PCB alone.

## PS1 footprint pad-number mapping

| Existing pad | Updated symbol pin |
|---|---|
| TB1.1 | 1_BOT |
| TB1.2 | 2_BOT |
| TB1.3 | 3_BOT |
| TB2.1 | 1_TOP |
| TB2.2 | 2_TOP |
| TB2.3 | 3_TOP |
| TB2.4 | 4_TOP |

## Saved-file verification

- Native ERC: 0 errors, 0 warnings.
- All terminal pins 1/2 share their intended native net.
- J2.X/Y/Z and TB40/TB41/TB42 match L1_IN/L2_IN/L3_IN.
- Every terminal schematic UUID matches its PCB footprint link.
- The PCB file hash is unchanged.
- Changed schematic areas and CSV fields were rendered and inspected.

