# Powermatic 1200 Controls Retrofit

Design and shop documentation for the safety and controls retrofit of a 1967 Powermatic 1200 variable-speed tapping/drilling press.

## Current controlled revision

- `docs/Powermatic_1200_Retrofit_Documentation_rJ.md` — design intent, power topology, sequence of operations, I/O assignments, VFD configuration, and safety architecture
- `docs/05_ladder_logic_rJ.md` — CLICK PLUS ladder-logic source
- `docs/Powermatic_1200_Retrofit_Wire_Schedule_rJ.md` — point-to-point build authority
- `docs/Powermatic_1200_SCCR_Worksheet_rJ.md` — personal-shop SCCR due-diligence worksheet and field record
- `docs/05_ladder_logic_rJ.pdf` — CLICK PLUS programming reference generated from the ladder source
- `docs/Powermatic_1200_Shop_Pack_rJ.pdf` — power one-line, safety loop, VFD card, and commissioning checklists
- `docs/Powermatic_1200_Retrofit_BOM_rJ.numbers` — owner-maintained procurement authority
- `docs/Powermatic_1200_Retrofit_BOM_rJ.pdf` — frozen Rev J procurement snapshot
- `TODO.md` — open build and validation items

Local helper scripts for regenerating the PDFs live in `scripts/`.

Rev J is the controlled revision in this repository.

## Rev J safety basis

The E-stop implements a controlled stop followed by delayed torque and input-power removal. A Dold `BH5928-92-61-24-1` immediately interrupts both VFD run directions. After the validated delay, independent contacts open Contactor A, STO1, and STO2. The final delay must be established by measured worst-case spindle stop-time testing; commissioning begins at 1.00 s.

Rev J does not include contact detection or a mechanical brake. All three delayed safety outputs are allocated. Two supplementary Phoenix Contact `2966265` hard-gold SPDT relay modules isolate the GS20 sink-mode DI4 stop request from the sourcing PLC indication: `CR-S1` switches DCM to DI4 and `CR-S2` switches +24 V to `X013`. Their polarized 24 VDC coils are energized together by BH5928 monitoring contact 31-32.

The Ladder Logic PDF's generic `CR-S` wording refers to the immediate `X013` indication path, now implemented specifically by `CR-S2`; the PLC addresses and rung behavior are unchanged.

## Procurement status and commissioning constraints

- Use two `CR-S` modules: Phoenix Contact `PLC-RSC-24DC/21AU` (`2966265`), 24 VDC, SPDT hard-gold signal contacts, screw terminals, complete DIN-rail modules. `CR-S1` serves VFD DI4 and `CR-S2` serves PLC `X013`. Observe A1+/A2- polarity; the modules include input protection and flywheel diodes. Do not substitute the existing Murrelektronik `52102` (`CR-B`): its power contacts are not specified for these low-current signals.
- **Power-circuit procurement check resolved:** `LC1D18BD` has a Schneider high-fault rating of 100 kA with fuses through 40 A. The GS20 manual specifies `TJN35` Class T protection for `GS23-22P0` and rates GS20 drives for circuits up to 100 kA RMS symmetrical. For this personal-shop retrofit, the SCCR worksheet is due diligence and a field record, not a product-certification gate.
- Order only the exact `BH5928-92-61-24-1`: fixed screw terminals, 24 VAC/DC, 0.1–1.0 s release delay.
- The OT30F3 handle, shaft, enclosure, fan, DIN rail, and wire duct remain intentionally deferred until enclosure layout.
- Do not set a final safety-relay delay until the complete drive train is running and worst-case stopping has been measured at every CVT setting, both directions, and maximum intended chuck/tool inertia.
- Set GS20 `P01.26` and `P01.27` to `0.00 s` before stop-time testing; their factory S-curve values otherwise add about 0.20 s to a nominal 0.50 s deceleration.
- Treat the braking resistor as operationally essential to the stop-time objective; its thermal switch is monitored, but it is not a safety-rated input.

Installation and validation must be performed by qualified personnel under the applicable machine-safety and electrical requirements. This repository is a personal-shop design package, not a UL listing or certification of the finished machine. If the control setup is ever sold as a product, pursue the appropriate certification/listing at that time.
