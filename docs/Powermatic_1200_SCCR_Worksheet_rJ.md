# Powermatic 1200 Retrofit - SCCR Worksheet

**Revision:** J  
**Date:** 2026-08-05  
**Circuit:** nominal 208/240 V, 3-phase VFD input power circuit  
**Status:** **SELECTED POWER-CIRCUIT COMPONENT CHECK PASSED - personal-shop due-diligence worksheet**

## 1. Design target and source assumption

- Working panel target: **10 kA RMS symmetrical at 240 V maximum**.
- Shop feeder: Siemens three-pole Type QP branch breaker marked **10,000 A RMS symmetrical at 240 V**.
- The breaker's 10 kA interrupting rating is not a calculation or measurement of available fault current.
  Treat `available fault current <= 10 kA` as a provisional design assumption until confirmed from the
  serving transformer and conductor impedance or by a qualified field calculation.
- For a listed product panel, the marked SCCR would need to be at least the available fault current at the machine
  connection point. For this personal-shop retrofit, use this worksheet as a conservative design check and field
  record, not as a substitute for formal UL 508A certification.

## 2. Power-circuit path

`shop feeder -> ABB OT30F3 -> LFT300603C / 3 x TJN35 -> Contactor A -> GS23-22P0 VFD`

| Component | Selected device | Published/working SCCR basis | Worksheet result |
|---|---|---|---|
| Branch fuses | 3 x Mersen `TJN35`, Class T, 35 A | Class T current-limiting branch protection; interrupting rating to be retained with the fuse data sheet | Not the limiting component |
| Fuse block | Littelfuse `LFT300603C`, 300 V, 60 A, 3-pole Class T | Listed Class T block; fit one `LFT30060FBC` cover per pole | Not presently identified as limiting |
| Disconnect | ABB `OT30F3`, 30 A, 3-pole, UL 98 | ABB publishes **50 kA** with Class T fuses up to 60 A | Passes 10 kA target |
| Contactor A | Schneider `LC1D18BD`, 18 A AC-3 / 32 A AC-1, 24 VDC | Schneider high-fault table: **100 kA with fuse <=40 A**. Selected fuse is 35 A Class T. | **Passes 10 kA target** |
| VFD | AutomationDirect `GS23-22P0` | GS20 manual specifies 35 A fast-acting Class T `TJN35`; all GS20(X) drives are suitable for circuits up to 100 kA RMS symmetrical | **Passes 10 kA target** |
| Feeder breaker | Siemens Type QP, 3-pole | 10 kA interrupting rating at 240 V; this is not the panel SCCR and not proof of available fault current | Source assumption only |

## 3. Resolution and remaining release items

The former `LC1D09BD` was replaced by `LC1D18BD`. This clears the contactor/fuse mismatch: the selected
35 A Class T fuse is below Schneider's 40 A maximum for the contactor's 100 kA high-fault combination.

Before treating the power-circuit design as field-ready:

1. Retain the Schneider combination-table page in the panel file and record `LC1D18BD`, 35 A Class T,
   and 100 kA component/combination SCCR.
2. Retain the GS20 manual pages showing `GS23-22P0` with 35 A `TJN35` Class T protection and the
   100 kA short-circuit-withstand statement.
3. Confirm available fault current at the machine by qualified calculation. The branch breaker's 10 kA
   interrupting rating alone does not establish available fault current.
4. Complete the field-record entries below. If this design is ever sold as a product, have the final panel and
   documentation evaluated under the appropriate certification/listing process.

The contactor and VFD no longer present unresolved procurement holds. The available-fault-current entry remains
useful evidence for a conservative personal-shop installation and would become mandatory documentation for a
certified product build.

## 4. Field record fields

- Available fault current at machine: __________ kA RMS symmetrical at __________ V
- Calculation/source and date: _________________________________________________
- Final Contactor A catalog number: ____________________________________________
- Final fuse catalog/rating: ___________________________________________________
- VFD manufacturer SCCR condition verified: **Yes - GS20(X) manual, 1st Edition Rev E, pp. A-2/A-4 and 2-21**
- Lowest component/combination SCCR basis: __________ kA
- Personal-shop panel marking / note, if applied: __________ kA RMS symmetrical at __________ V
- Reviewed by / date: __________________________________________________________

## 5. Manufacturer references

- Schneider Electric, *Motor Control Solutions for the North American Market*, TeSys Deca 3-pole
  contactor SCCR table: `LC1D09` maximum 25 A fuse; `LC1D18` maximum 40 A fuse.
  <https://productinfo.se.com/8536db0901_motorcontrolsolutions_db/8536db0901-db-motor-control-solutions/English/8536DB0901R0119%20Motor%20Control%20Solutions%20for%20the%20North%20American%20MarketSchnei_0000295698.xml/$/CombinationStarterComponentsCPT_0000295590>
- Schneider Electric, LC1D mirror contacts: base-device 21-22 N.C. is the mirror contact.
  <https://www.se.com/uk/en/faqs/FA142116/>
- ABB, `OT30F3` product data and disconnect-switch short-circuit tables.
  <https://empower.abb.com/ecatalog/ec/EN_NA/p/1SCA105068R1001>
- Littelfuse, `LFT300603C` Class T block product data.
  <https://www.littelfuse.com/products/fuses-overcurrent-protection/fuse-holders-fuse-blocks-accessories/fuse-blocks/industrial-fuse-blocks/lft/lft300603c>
- AutomationDirect, *DURApulse GS20 & GS20X Drive User Manual*, 1st Edition Rev E: fuse specification
  table (`GS23-22P0` -> 35 A `TJN35`) and 100 kA short-circuit-withstand statement.
  <https://cdn.automationdirect.com/static/manuals/gs20m/gs20m.pdf>
