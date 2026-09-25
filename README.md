# Powermatic 1200 Controls Retrofit

Design and shop documentation for the safety and controls retrofit of a 1967 Powermatic 1200 variable-speed tapping/drilling press.

> **Current baseline — Rev O, updated 2026-09-24:** Retain the existing motor, OFF/LOW/HIGH drum switch and FWD/REV/STOP pendant. All operator controls carry only 24 VDC; all motor-power switching moves into the panel. The basic BOM uses five three-pole contactors, two mechanical interlocks, the existing 24 VDC supply, and a three-pole disconnect followed by a separate Class R motor fuse block. See the [current scope decision](docs/Scope_Reset_2026-09-23.md#rev-o-basic-contactor-bom-current).

## Current working BOM

[Rev P CSV](Powermatic_BOM_revP.csv) is the active BOM for live changes. Its **20 unique-part rows** include five `HMC-9B30-11-DS` contactors ($31 each), two `HMX1-MI` interlocks ($16.50 each), one Dold `HC3096N-52-900-24` coil-enable relay ($46.50), the existing supply and controls, four selected Socomec disconnect components, the selected fuses/block/covers, an Eaton PSU input breaker, two motor overloads, five coil suppressors, one white indicator, one M12 E-stop panel socket, one reversing busbar kit, and one conditional auxiliary-block row with quantity zero. Each contactor includes 1 NO + 1 NC auxiliary contacts; each interlock includes two NC electrical-interlock contacts.

The earlier five-pole KH specification is replaced by separate three-pole KH (high-speed supply) and KS (high-speed shorting) contactors. The **current component total is $735.24**: $205.00 contactors/interlocks/reversing busbars, $119.22 motor fuses/block/covers, $122.50 Socomec disconnect assembly, $55.00 PSU input breaker, $63.00 overloads, $60.00 suppressors, $52.92 indicator, $46.50 coil-enable relay and $11.10 M12 panel socket. See the [fuse and breaker selection record](docs/Fuse_Selection_2026-09-24.md), [disconnect selection](Disconnect_Distributor_Comparison_2026-09-24.md) and [overload, indicator and suppression selection](docs/Overload_Indicator_Suppression_2026-09-24.md). This excludes tax, shipping and Allfuses' $5 small-order fee. One `HMX1-BBREV` reversing busbar kit is included at $17.00 for KF/KR; it includes line-side and load-side bars. The `HMX1-AUX11-F` extra auxiliary block remains $8.50 each with quantity pending the final control schematic. Only the conditional auxiliary-block row has quantity zero and is excluded. All included rows are priced; enclosure and installation materials remain separate work.

OL-L and OL-H are matching IronHorse `HTOR32-6-S` 4–6 A relays, directly mounted on KL and KH, with manual reset and nameplate settings of 4.0 A LOW / 4.4 A HIGH. Both trips must inhibit both speeds. Five `HMX1-SSVRC-DC` suppressors cover all five 24 VDC coils. PL1 is a white `XB4BVB1` 22 mm indicator connected across the control supply. PL1 is sourced as DigiKey 4008-XB4BVB1-ND at $52.92; the US listing showed two available when checked September 24. The overloads and suppressors remain sourced from AD.

CB-PS1 is Eaton `FAZ-D4-2-NA-L`, 4 A, two-pole, D curve, UL 489, 35 mm DIN mounted. It feeds the NDR-240-24 from two phases downstream of DS1 at 208 V line-to-line; both L and N input conductors pass through the breaker, while FG connects directly to PE. Separate 24 VDC branch fuses/breakers are omitted per the owner's September 24 decision; final wiring and device ratings must suit the supply's available output current.

DS1 uses Socomec `22013003` ($75), red/yellow S0 handle `148E1111` ($27.50), shaft `14070532` ($9, includes alignment guide), and one two-cover pack `22943016` ($11). The handle operates through the fixed right enclosure wall. The owner will order the eBay handle; purchase/receipt is not yet confirmed. The other three components are sourced from AutomationDirect. Its switch page showed a backorder with earliest October 14, 2026 availability when checked September 24; the shaft and covers showed stock. The shaft cut length awaits enclosure layout.

The CSV columns are `cat`, `part name`, `qua`, `unit`, `line`, `supplier`, `part no`, in that order. Each part number has one row with quantities combined. `unit` is unit cost and `line` is line cost; calculate `line` as `qua` × `unit`, rounded to cents. Values are numeric snapshots, not spreadsheet formulas. Quantity zero means an accessory is not included. Leave unknown costs blank and keep TOTAL blank until all included items are priced. PRICED SUBTOTAL counts item rows only; never add it again into TOTAL. The new control schematic remains pending.

## Rev M reference package

- `docs/Powermatic_1200_Retrofit_Documentation_rM.md` — design intent, power topology, sequence of operations, I/O assignments, VFD configuration, and safety architecture
- `docs/05_ladder_logic_rM.md` — CLICK PLUS ladder-logic source
- `docs/Powermatic_1200_Retrofit_Wire_Schedule_rM.md` — point-to-point build authority
- `docs/Powermatic_1200_SCCR_Worksheet_rM.md` — personal-shop SCCR due-diligence worksheet and field record
- `docs/05_ladder_logic_rM.pdf` — CLICK PLUS programming reference generated from the ladder source
- `docs/Powermatic_1200_Shop_Pack_rM.pdf` — power one-line, safety loop, VFD card, and commissioning checklists
- `Powermatic_1200_Retrofit_BOM_rM.numbers` — prior BOM; live changes now use Rev O CSV
- `docs/Powermatic_1200_Retrofit_BOM_rM.pdf` — frozen Rev M procurement snapshot
- [Datasheet collection and source index](docs/Powermatic_1200_Datasheet_Index_rM.md) — local PDFs in shared `_parts`, coverage and remaining identity gaps
- `TODO.md` — open build and validation items

Local helper scripts for regenerating the PDFs live in `scripts/`.

Rev M is the prior design package; Rev N is the earlier reduced BOM, and Rev O is the current basic component baseline. Revision L was intentionally skipped. The sections below describe the historical Rev M design and do not reinstate items omitted from Rev O.

## Rev M safety and thermal basis

The E-stop implements a controlled stop followed by delayed torque and input-power removal. A Dold `BH5928-92-61-24-1` immediately interrupts both VFD run directions. After the validated delay, independent contacts open Contactor A, STO1, and STO2. The final delay must be established by measured worst-case spindle stop-time testing; commissioning begins at 1.00 s.

Rev M does not include contact detection or a mechanical brake. All three delayed safety outputs are allocated. Two supplementary Phoenix Contact `2966265` hard-gold SPDT relay modules source external +24 V: `CR-S1` commands GS20 DI4 and `CR-S2` commands CLICK input `X013`. Their polarized 24 VDC coils are energized together by BH5928 monitoring contact 31-32.

DB-resistor thermal protection is also hardwired. A third `2966265` module,
`CR-DB`, immediately asserts DI4 when the resistor thermostat opens. Phoenix
Contact timer `2910140` (`277-2910140-ND`) then opens the Contactor A coil path
after a commissioned release delay nominally near 1.00 s. A dedicated
`DN-F10MN` holder with a Bussmann `GMC1` 1 A fuse protects that branch.
Thermal hardware recovers automatically, while the PLC requires 10 seconds of
healthy feedback and a fresh motion command.

Both CLICK option modules are `C2-14D2`. Slot 0 provides the six used sourcing
outputs; Slot 1 outputs are reserved. The GS20 input selector is set to PNP,
`DCM` is the external grounded-0 V reference, and the drive's internal +24 V
terminal is unused for DI1-DI4. The NDR-240-24 `-V` is bonded to PE at exactly
one point adjacent to the supply. Grounded 0 V conductors are white with blue
identification at both ends. GS20 `P02.35=0` prevents a maintained run command
from starting the drive after reset or reboot.

## Procurement status and commissioning constraints

- Use three Phoenix Contact `PLC-RSC-24DC/21AU` (`2966265`) modules, Mouser `651-2966265`: `CR-S1` serves safety DI4, `CR-S2` serves PLC `X013`, and `CR-DB` serves DB-thermal DI4. Observe A1+/A2- polarity; the modules include input protection and flywheel diodes. Do not substitute the existing Murrelektronik `52102` (`CR-B`): its power contacts are not specified for these low-current signals.
- Use Phoenix Contact `PLC-TR-1T-MUL-300M` (`2910140`), DigiKey `277-2910140-ND`, as `TD-DB`. Configure `Rs` release delay on the 0.1-10 s range, start near 1.00 s, and commission by measured Contactor A dropout time.
- Use AutomationDirect `GMC1`, 1 A medium time-delay 5 x 20 mm fuses, in the existing `DN-F10MN` holder type for `DB-FU`.
- Use two Schneider Harmony red pilots, DigiKey `4008-XB4BVB4-ND`, in parallel on `Y006`: one machine-front and one enclosure-panel `FAULT / NOT READY` indication. Label the black button `SAFETY RESET` and the white pilot `CONTROL POWER`.
- Use two AutomationDirect `C2-14D2` option modules. Configure Slot 0 as `X001-X008` / `Y001-Y006` and Slot 1 as `X009-X016` with outputs unused; enable the CLICK startup I/O configuration check before downloading ladder logic.
- **Power-circuit procurement check resolved:** `LC1D18BD` has a Schneider high-fault rating of 100 kA with fuses through 40 A. The GS20 manual specifies `TJN35` Class T protection for `GS23-22P0` and rates GS20 drives for circuits up to 100 kA RMS symmetrical. For this personal-shop retrofit, the SCCR worksheet is due diligence and a field record, not a product-certification gate.
- Order only the exact `BH5928-92-61-24-1`: fixed screw terminals, 24 VAC/DC, 0.1–1.0 s release delay.
- The OT30F3 handle, shaft, enclosure, fan, DIN rail, and wire duct remain intentionally deferred until enclosure layout.
- Do not set a final safety-relay delay until the complete drive train is running and worst-case stopping has been measured at every CVT setting, both directions, and maximum intended chuck/tool inertia.
- Set GS20 `P01.26` and `P01.27` to `0.00 s` before stop-time testing; their factory S-curve values otherwise add about 0.20 s to a nominal 0.50 s deceleration.
- Set GS20 `P02.35=0` and prove that a run command present during drive reset or power-up cannot start the spindle; require command removal and a fresh FWD/REV action.
- Treat the braking resistor as operationally essential to the stop-time objective. Its thermostat is equipment protection, not a safety-rated input; verify immediate DI4 assertion, delayed Contactor A dropout, automatic recovery, and no automatic spindle restart.

Installation and validation must be performed by qualified personnel under the applicable machine-safety and electrical requirements. This repository is a personal-shop design package, not a UL listing or certification of the finished machine. If the control setup is ever sold as a product, pursue the appropriate certification/listing at that time.
