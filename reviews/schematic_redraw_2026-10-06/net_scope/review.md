# Label scope and terminal-block review

Saved schematic SHA-256: `bb05958a39119846300fce05969b7905a73c1c09c221175002b918e74857a105`.

The assertion "every global net requires a terminal block; every local net requires none" does not hold for the present drawing. Label scope specifies schematic connectivity, not a physical termination requirement. It could be adopted as a project convention after correcting the classification and defining assembly boundaries.

| Current label(s) | Saved endpoints | Physical interpretation |
|---|---|---|
| Global HS_SHORT | K5.1, K5.3, K5.5 | Local shorting bridge on K5; no separate terminal block is necessary. |
| Global L1/L2/L3_LOW | K4.2/4/6 to OL4.IN1/IN2/IN3 | Direct-mount contactor/overload connections; classify local under the proposed convention. |
| Global L1/L2/L3_HIGH | K6.2/4/6 to OL6.IN1/IN2/IN3 | Direct-mount contactor/overload connections; classify local under the proposed convention. |
| Global FWD_COIL and REV_COIL | K1/K2 coil, opposite NC auxiliary, suppressor | Direct wiring within the reversing assembly if K1/K2 are treated as one serviceable assembly. |
| Global LOW_COIL and HS_COIL | K4/K5 coils, opposite NC auxiliary, suppressor; HS_COIL also K5.43 | Direct wiring within the low/shorting assembly if K4/K5 are one assembly. |
| Global HIGH_COIL, LOW_K6_OK | K5 to K6 plus associated suppressor | Crosses the K4/K5 versus K6 assembly boundary under the preceding grouping; use the selected terminal interface. |
| Global OL4_OK | OL4.96 to OL6.95 | Crosses the two starter assemblies under that grouping. |
| Global L1/L2/L3_IN and M1_T1 through M1_T6 | External plug/motor to panel devices | Cable-boundary terminal interfaces fit the agreed policy. |
| Global FWD_CMD, REV_CMD, LOW_CMD, HIGH_CMD, STOP_RELEASED, SPEED_SET | External controls to panel components, often multiple branches | Cable-boundary interfaces fit the agreed policy; each net can also contain direct internal branches. |
| Global +24V, 0V, PE | Distributed supply/return/earth endpoints | Distribution or PE terminals are appropriate where needed; device-local branches need not each return independently to a block. PE uses the selected PE termination, not an ordinary gray block by assumption. |
| Global +24V_EN and L1/L2/L3_SW, L1/L2/L3_DIR | Panel power/control distribution among groups | Allocation follows actual assembly boundaries and branch/landing requirements; label type alone cannot set block count. |
| Local K3_JUMPER | K3.14 to K3.23 | Direct jumper within K3. |
| Local L1/L2/L3_FUSED | FH1 to SW1 | Direct panel wiring is reasonable; local scope alone does not mandate the physical routing. |
| Local L1/L2_PSU | Q1 to PS1 | Direct panel wiring is reasonable; local scope alone does not mandate the physical routing. |
| Local ESTOP_JUMPER | J1.2/3, J6.2/3, S1.2/3 | The net crosses the M12 interface into the external E-stop. The common jumper can be local at the panel connector, but the whole net is not confined to one assembly. Additional terminal blocks behind the connector are a physical layout choice. |

Unlabelled named-by-KiCad nets in S2 and S3 are internal retained switch links; no additional terminal blocks are indicated by their electrical topology.

A terminal interface belongs to a connection crossing an assembly boundary. A net may have both interface connections and direct branches. A global net therefore does not imply one block, one block per device, or a home run from every pin.

Recommended drafting convention: local labels for assembly-internal nets; global labels for nets crossing assembly boundaries or used for distribution, with explicit interface assignments. That convention still needs a connector exception and defined assembly membership. A visible label field or a separate terminal-allocation record would be a more exact indication of PCB-only terminal usage than label scope alone.

References: KiCad 10.0 Schematic Editor manual, Labels; AutomationDirect HTOR32-6-S cut sheet, direct-mount power connections. No source schematic, board, or library edits were made.
