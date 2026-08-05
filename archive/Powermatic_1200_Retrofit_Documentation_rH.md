# Powermatic 1200 Drill Press — Controls Retrofit

**Machine:** 1967 Powermatic 1200, 3PH tapping/drilling drill press
**Owner / designer:** Evan Thayer — GoodBetterBestCo
**Document rev:** H · **Date:** 2026-07-19
**Design references:** NFPA 79 (Electrical Standard for Industrial Machinery), UL 508A (panel construction)

> **Rev H changes (operator model + logic hardening; prox PNP; pricing).**
> - **Latched bidirectional DRILL run (§3.2, §7).** Reverse now behaves exactly like forward: **one press of REV
>   latches a reverse run** (`C31`) that continues until STOP — symmetric with FWD's `C30`. **Stop-first, opposite-
>   as-stop:** while running one direction, a press of STOP *or* of the opposite button **stops** the run; it takes
>   a **second** press to start the other direction (no plug-reversal under power). The old momentary REV jog on
>   `X005` is removed from normal operation and folded into jog mode below.
> - **JOG MODE (§3.5, §7).** **Hold FWD ≥ 5 s** to enter jog (FWD only). In jog mode **FWD and REV become momentary
>   hold-to-run jogs at 30 Hz** (preset-LOW forced), gated safe/no-fault. **Exit** on a **short (< 5 s) STOP press**,
>   or **60 s idle**, or **any fault**, or **E-stop**. STOP always stops motion first; the < 5 s qualifier only adds
>   the mode-exit. Annunciated as **blinking green = JOG ARMED** (see indicators).
> - **TAP abort hardened (§7 RUNG 13).** A loss of run-permit — which includes an **E-stop / safety trip** (`X011`),
>   drum-OFF, or STOP — now forces the TAP state machine to **IDLE**. Previously `C2`/`C3` survived an E-stop, so a
>   safety reset could **resume a tap with no fresh FWD press**; that auto-restart path is closed. DRILL already
>   self-cleared via `¬C20`; TAP now matches.
> - **DB-resistor over-temp is self-clearing + distinctly annunciated (§4/§7).** Over-temp now drives a dedicated
>   **`C11` (THERMAL)** bit that follows `X012` with a short cool-down delay — it inhibits run and **self-clears**
>   when the resistor cools (no manual reset, and no more fighting the fault-reset rung). Shown as **blinking red**,
>   distinct from a solid-red hard fault, so the operator reads "let it cool" vs "investigate."
> - **Indicators (§4/§7 RUNG 28/29).** Four states on the two machine-front lamps, exactly one active: **green solid**
>   = all-good; **green blink** = jog armed; **red blink** = DB over-temp (self-clearing); **red solid** = safety
>   trip or latched hard fault (top priority). White bus lamp unchanged.
> - **Feed-lever prox NPN → PNP (§4, §12).** Swapped to a **P&F NBN8-12GM50-E2-V1 (PNP-NO)** so it lands on the
>   **standard sinking input common** with every other +24-fed contact. The Rev G split-common (dedicated sourcing
>   group for the NPN unit) is deleted — `X010` stays put, logic sense and fail-safe behavior unchanged.
> - **STO wiring rationale recorded (§6).** STO1/STO2 are fed from the **single** safety output 23-24 by design;
>   **Contactor A (13-14) is the diverse, independent stop channel** and the CWBS12 mirror contact catches a weld
>   via EDM. Redundancy lives in the contactor path, not in STO's own two channels — documented, not changed.
> - **Selector detail (§4).** `X001`/`X002` come from the owner's **XB4BD21** with **both N.O. blocks installed**
>   (supersedes the "ZBE-101" placeholder).
> - **Pricing reconciled (BOM).** DB resistor $55 → **$156** and Contactor A ~$60 → **~$150** were materially low;
>   most other itemized parts verified in-range. See `..._BOM.md`.

> **Rev G changes (procurement + inventory pass; pilot scheme finalized).**
> - **Disconnect re-architected** to a **non-fused rotary switch + separate Class J fuse block** instead of an
>   integrated fusible unit: **Socomec SIRCO M Compact** (UL 98, 3-pole, 60 A, 100 kA SCCR — AD 22013006) feeding a
>   **Mersen US6J3** finger-safe Class J block (3× **JHL35**, Class J 35 A). Operated by an **external S00 rotary
>   handle (Socomec 14741111, NEMA 3R/12)** mounted on a **fixed enclosure wall — not the door** — with **no
>   through-door coupling rod**. Padlockable in OFF; sole disconnecting means.
> - **Contactor A fixed as a WEG CWBS12-33-30C03** IEC **safety contactor** (3-pole, 12 A, 24 VDC coil) with
>   **mechanically-linked mirror contacts integral** (IEC 60947-4-1 / -5-1) — the EDM contact is built in, no add-on aux.
> - **E-stop is now the owner's AvidCNC station** (Schneider mushroom operator + **2× ZB2-BE102 positive-opening N.C.**,
>   M12 4-pin, yellow CM12 enclosure), verified direct-opening and sound — replaces the Eaton E22 assembly.
> - **Feed-lever prox is the owner's P&F NBN8-12GM50-E0-V1** — an **NPN-NO** unit (10–30 V, M12, 8 mm non-flush).
>   Because it's NPN it lands on a **sourcing input common** (see §4); the C2-14D1's two isolated 4-point commons make
>   this clean without disturbing the +24-fed contacts.
> - **24 V control supply is the owner's Mean Well NDR-240-24** (10 A / 240 W). Because it can source ~10 A into a
>   fault, a **24 V bus overcurrent device** is added (§9/§10).
> - **Line reactor deleted** — optional for a single small drive on an ordinary branch; add back only on a stiff
>   supply or if overvoltage nuisance trips appear.
> - **Safety relay pinned to 440R-N23135S** (24 VDC MSR127RP, spring-clamp terminals).
> - **Pilot scheme revised (§4/§6/§7):** two lamps on the **machine front** between the travel limits — **green = "all
>   good," red = "not good"** — driven as **firmware complements** (`Y005`/`Y006`), so exactly one is lit whenever the
>   panel is powered. A **white "power on" lamp (XB4BVB1)** sits at the disconnect, fed straight off the 24 V bus.
>   The old cycle-active / amber "safety-tripped" indications are removed; the safety-relay **41-42 N.C. aux is now spare.**
> - **Wiring detailing (from the wire schedule):** the **PSU primary gets its own 2-pole ~3 A fuse** (the 35 A branch
>   can't protect the 16 AWG PSU tap; both L-N conductors are live at 208 V — 1-pole/120 V only if a neutral is run).
>   The **DB-resistor over-temp thermal switch is wired to spare input `X012`** with a fault rung (§4/§7). A **dedicated
>   PE bond to the machine frame/column** is added (do not rely on the motor mounting bolts), plus DIN-rail and
>   Contactor B frame bonds. All accessories are **home-run** to the panel — no field j-boxes. See `..._Wire_Schedule.md`.

> **Rev F changes (safety parts finalized):** safety relay confirmed as **440R-N23135** (MSR127RP,
> **24 V DC** supply — not the 115/230 VAC N23134/N23133). Output allocation set: 13-14 → Contactor A
> coil, 23-24 → STO, 33-34 → `X011` (fail-safe N.O., no ladder change), 41-42 aux → "SAFETY TRIPPED"
> lamp. Operator devices (DRILL/TAP selector, reset, pilot lamps) now come **from the owner's 22 mm
> stock** — parts to be identified in the shop; E-stop may also be from stock if direct-opening and
> dual-N.C.-capable. *(Rev G supersedes the 41-42 → amber lamp allocation; see above.)*

> **Rev E changes (safety confirmed):** safety relay is an **AB Guardmaster MSR127RP** (monitored
> reset + EDM, ≥3 N.O. outputs → Contactor A coil + VFD STO1 + STO2). E-stop is an **Eaton E22LTA2QB**
> (EN 418, DEMKO, direct-opening) + **E22B1** second N.C. for dual channel + **E22VA8** yellow legend.
> Contactor A confirmed as a **mirror-contact (mechanically-linked) contactor** — required for valid
> EDM. STO wired dual-channel (remove the GS20 STO jumper). Clarified that the IDEC **RF1V** is a
> force-guided relay component, not an MSR127 alternative (optional fan-out / discrete-build only).
> *(Rev G supersedes the Eaton E-stop with the owner's AvidCNC/Schneider station, and names Contactor A
> as the WEG CWBS12 safety contactor.)*

> **Rev D changes (control & logic confirmed):** PLC is a **CLICK PLUS C2-01CPU-2** (no built-in I/O)
> with **two C2-14D1** option modules (16 in / 12 out) — inputs sink/source-selectable, C2-14D1 outputs
> sinking (NPN) so GS20 DIs set to source mode. Interposing relay **CR-B = Murrelektronik 52102** (24 VDC
> coil, DPDT, 6 A/250 VAC); land the Furnas theater coil on its 240 V tap. Added CPU battery (D0-MC-BAT)
> and USB programming cable; CLICK software is a free v3.00+ download.

> **Rev C changes (drive selection + disconnect):** VFD confirmed as **GS23-22P0** against the
> GS20(X) selection tables (CT 7.5 A ≥ 6.42 A FLA); matched accessories named — braking resistor
> **BR-N1-280W50** (50 Ω), branch fuses **3× JHL35 (Class J, 35 A)** per the drive's fuse chart.
> *(Rev G removes the optional line reactor and replaces the integrated fusible disconnect with a
> non-fused SIRCO M + separate US6J3 Class J block.)*

> **Scope of this package.** Complete control retrofit replacing the original all-line-level
> control wiring with a modern low-voltage architecture: safety relay + VFD power section +
> CLICK PLUS logic controller, in a UL 508A–style DIN-rail enclosure. The original drum switch,
> button pendant, and travel limit switches are retained and converted to 24 VDC signaling.
>
> **This is a design package, not a substitute for on-machine verification.** Field-verify every
> mechanical assumption (noted in §12), size branch protection to the *actual* VFD manual, and have
> the finished installation LOTO-validated by a qualified person before production use.

---

## 1. Design intent

The original machine ran every control conductor — drum switch, pendant, limits, contactor
coils — at 208 V line level. That is a large surface area of live wiring for a machine an operator
leans over. This retrofit accomplishes four goals stated at the outset:

1. **Kill the all-line-level hazard.** Everything a human touches (drum, pendant, limits, e-stop,
   selector) *and everything a human reads* (the machine-front pilot lamps) now runs at **24 VDC**.
   The only line-level conductors remaining are inside the enclosure between the disconnect and the motor.
2. **Add single-tap capability.** Reverse-at-bottom, stop-at-top, as a selectable software mode.
   Continuous tapping remains available as a one-rung change (§7, note C).
3. **Keep the original controls and the "chunk."** Drum switch, pendant, and limits are reused as
   24 V inputs. Both original contactors are reused — one doing real safety work, one for sound.
4. **Put the logic in software, not fixed wiring.** A CLICK PLUS PLC brokers every command; the
   sequence lives in ladder, not in relay hardwiring.

### The one rule that governs the whole design
**The PLC is not the safety system.** A standard PLC's outputs can weld and its firmware can hang.
The **E-stop and the over-travel backstop remove motor power through a hardwired safety relay that
does not depend on the controller executing code.** The PLC *sees* the safety state but is never the
thing that makes the machine safe. (This is also why the operator status lamps — which *are* firmware —
are advisory only: see §6/§7.)

### Three layers
| Layer | Trust model | What lives here |
|---|---|---|
| **Safety** | Hardwired, firmware-independent | E-stop → safety relay → drops Contactor A + opens VFD STO |
| **Logic** | CLICK PLUS PLC | DRILL/TAP modes, single-tap state machine, VFD command, preset select, status lamps |
| **Telemetry** *(optional, future)* | Read-only ESP32 | Cycle counting → Cloudflare stack. Never touches control or safety path |

---

## 2. Power topology (see DWG 01)

- Motor is wired **permanently in its 4-pole Δ (high-speed) configuration** — treat it as a plain
  3-lead 1750 RPM motor. The YY (8-pole) leads are capped but left accessible in the peckerhead.
- The **VFD synthesizes both nameplate speed ranges** through the *existing* mechanicals: 60 Hz
  reproduces the high ranges, **30 Hz reproduces the low range exactly** (the drive is doing the
  same 2:1 the pole-change used to do). At 30 Hz the drive holds V/Hz so low-range torque is full.
- The operator still moves the 2-groove belt and spins the Reeves v/s dial exactly as before; only
  "low/high" changes from a winding-swap clunk to a soft VFD preset.

> **Demolition — remove the existing front-of-machine switch.** The machine as found routes line
> from a rear entry j-box, up through an **Allen-Bradley AH7810 3-pole manual switch** on the front
> of the machine, then down to the contactor box. Confirmed on inspection to be a plain 3-pole
> switch (no overload heaters). **Delete it entirely**, along with its front-of-machine cable loop:
> it is line-level wiring in the operator's space — exactly the hazard this retrofit exists to
> remove. Feed the new enclosure **directly from the rear line-entry j-box**; the enclosure's
> disconnect becomes the **sole disconnecting means** (mount its external handle where it is readily
> reachable for LOTO). Before cutting: LOTO and meter to confirm which rear cable is the true
> incoming supply, size the run into the enclosure for VFD input + branch protection, and patch or
> repurpose the vacated front j-box location (candidate spot for the operator pendant/station).

```
208V 3PH 60Hz  ──►  MAIN DISCONNECT — non-fused rotary (Socomec SIRCO M, UL 98, 3-pole 60 A,
                    external S00 handle on a fixed enclosure wall, padlockable OFF, NO door interlock)
                    ──►  BRANCH FUSES (3× JHL35 — Class J, 35 A — in a Mersen US6J3 finger-safe block)
                    ──►  CONTACTOR A (WEG CWBS12 safety contactor, 24 VDC coil, dropped by SAFETY RELAY)
                    ──►  VFD (GS23-22P0, 2 HP / 230 V class / 3PH input)  +DB resistor, STO
                    ──►  MOTOR (permanent 4-pole Δ, 1.5 HP, 143TC, 6.42 A FLA)
```

> **Disconnect + branch protection — split, wall-mounted, no door rod (Rev G).** The integrated
> fusible disconnect of earlier revisions is replaced by two devices in series inside the enclosure:
> a **non-fused rotary switch** (Socomec SIRCO M Compact, **UL 98**, 3-pole, 60 A, 100 kA SCCR,
> load-break) followed by a **separate Class J fuse block** (Mersen **US6J3**, IP20 finger-safe,
> 60 A frame, holding the 3× **JHL35**). Order matters: **line → disconnect → fuse block → Contactor A
> → VFD**, so throwing/locking the disconnect de-energizes the fuse block for safe fuse changes.
>
> The switch is operated by an **external S00 rotary handle (Socomec 14741111, NEMA 3R/12)** mounted
> on a **fixed wall of the enclosure**, handle outside, **padlockable in OFF** for LOTO. There is
> **no through-door coupling rod** — the door interlock is intentionally omitted (the box runs
> door-open for commissioning/tuning by choice), so a door coupling would serve no purpose and only
> add alignment fuss. A fixed-wall penetration is a one-time alignment; a large switch-to-wall offset
> would need a separate extension shaft, which a compact mount avoids.
>
> **Class J frame:** the JHL35 is a 35–60 A (60 A-frame) Class J fuse, so both the block and the
> switch sit on the 60 A tier. **Live-access mitigations:** the fuse block is finger-safe (protects
> against contact during door-open tuning, when it is live); the always-critical shrouding is on the
> **disconnect's incoming line lugs**, which stay live with the disconnect OFF — confirm those are
> IP20 or fit terminal covers. No door interlock is wired to the safety relay.

> **Contactor assignment (the two units in the box).**
> - **Contactor A = WEG CWBS12-33-30C03** (line/safety), a purpose-built **IEC safety contactor**:
>   3-pole, 12 A (ample for the ~9.6 A VFD input), **24 VDC coil switched directly by the safety
>   relay**, with **mechanically-linked mirror contacts integral** (IEC 60947-4-1 / -5-1). The mirror
>   N.C. contact used for EDM is built in — no add-on aux block, and no risk of pairing a
>   non-mirror aux (e.g. a plain Fuji SC-E aux) that would invalidate the EDM.
> - **Contactor B = the vintage right-hand Furnas contactor** (theater). It switches **no load**, so
>   its only duty is mechanical armature cycling — the gentlest possible use of vintage iron, and it's
>   the unit you actually *hear*. Keep its original D2936-32 coil (the dual-voltage rating is moot
>   since it switches nothing); drive it via interposing relay CR-B on `Y004`.
> - **Remove both heaters / the overload block.** Motor overload is now the VFD's electronic thermal
>   (§5); a fixed overload downstream of a drive mis-reads PWM current and nuisance-trips. The EDM
>   contact comes from Contactor A's own mirror aux, so nothing is lost by removing the overload block.

---

## 3. Sequence of operations

### 3.1 Mode selection
A door-mounted **DRILL / TAP** selector (2-position maintained) sets `X001`/`X002`. The drum switch
(OFF / LOW / HIGH) remains the operator's speed selector and a run permissive: **OFF = no run.**

### 3.2 DRILL mode (latched, bidirectional)
Power feed is engaged by the operator (mechanical lever). The controller's job is spindle run +
direction + speed. **Forward and reverse are symmetric latched runs** (`C30` / `C31`):

1. Operator sets drum to LOW or HIGH and engages the mechanical power-feed lever.
2. Press **FWD** → spindle **latches** forward at the selected preset and runs until stopped.
   Mechanical trip + return spring perform the down-trip-retract cycle unaided.
3. Press **REV** → spindle **latches** reverse and runs until stopped. Same one-press-and-go model
   as FWD.
4. **Stop-first, opposite-as-stop.** While running one direction, pressing **STOP _or_ the opposite
   direction button stops** the run. It takes a **second press** of the opposite button to actually
   run the other way — the spindle is never plug-reversed under power. (Reversal energy, when the
   drive does ramp through zero, is bled by the DB resistor; §5.)
5. **Fault:** if the lower travel limit is reached while running **forward** in DRILL, the mechanical
   trip has failed and the quill is running to the hard end — the controller **fault-stops** and
   goes red. (In DRILL the bottom limit is a fault, not a sequence step; reverse is not a feed-down
   runaway, so the bottom-limit fault is FWD-only. A reverse over-travel into the top stop is caught
   by the VFD over-torque backstop, §5.)

### 3.3 TAP mode (single-tap, self-lead)
Power feed lever **OFF** — the tap threads itself in and self-leads; feed-per-rev auto-synchronizes
to any pitch. The controller runs the state machine; the limits sequence it.

```
IDLE ──FWD pressed──► TAP_DOWN ──bottom limit──► BACK_OUT ──top limit──► (STOP) ──► IDLE
```

- **Entry gate:** TAP mode cannot leave IDLE unless the **feed-lever-OFF proximity** proves the
  lever is disengaged. Starting a tap with power feed engaged is the tap-snapping condition.
- **Runtime trip:** the feed-lever-OFF signal is also watched *during* TAP_DOWN and BACK_OUT. If the
  lever is bumped engaged mid-cycle, the controller **fault-stops immediately** — entry-only checking
  would let a mid-cycle bump break the tap.
- Direction reversal is done **electronically by the VFD** (ramped decel-through-zero-reaccel with
  the DB resistor bleeding the reversal energy) — gentle on the tap, no contactor shoot-through.
- **Continuous mode** (future): at the top limit, re-enter TAP_DOWN instead of IDLE (§7 note C).

### 3.4 STOP vs E-STOP — two physically distinct controls
| Control | Path | Behavior |
|---|---|---|
| **STOP** (pendant) | Soft — PLC input `X004`, VFD ramp | Normal cycle stop. Gentle. Depends on firmware — *and that's fine, because it is not the safety stop.* |
| **E-STOP** (panel, mushroom) | Hard — hardwired to safety relay, **bypasses the PLC** | Drops Contactor A (power removal + chunk) and opens VFD STO (fast torque-off). Firmware-independent. |

**No auto-restart.** After E-stop or a power interruption, the safety relay requires a deliberate
monitored **RESET**, and the PLC requires a fresh FWD press. Nothing restarts on its own. In TAP,
a safety trip also drops the state machine to IDLE (§7 RUNG 13), so a reset alone never resumes a tap.

### 3.5 JOG mode (setup inching)
A **long hold of FWD (≥ 5 s)** arms jog mode. The 5 s hold is deliberately un-fakeable and the button's
duration is what selects "enter jog" vs. the normal short-press run — so FWD's short-press latch acts on
**release** (a quick tap latches a run; a 5 s hold enters jog and does *not* start a run on release).

- **In jog mode**, the pendant **FWD and REV buttons are momentary hold-to-run jogs** — the spindle turns
  only while a button is held — at a forced **30 Hz** (preset-LOW) for controllable inching, in either
  direction, gated **safe (`X011`) · no fault · no over-temp**. Normal latched runs and TAP starts are
  inhibited while armed.
- **Exit** on any of: a **short (< 5 s) STOP press**, **60 s of jog inactivity**, **any latched fault**,
  or an **E-stop / safety trip**. STOP always stops motion on press; the < 5 s qualifier only adds the
  mode-exit so a long STOP hold is a plain stop.
- **Annunciation: blinking green = JOG ARMED** (§4). Because jog is a "safe + armed" state, it lives in the
  green family; the lamp blink makes the hidden mode visible so it can't be silently forgotten.

> Jog mode is firmware, and — like the status lamps — advisory to the operator, not a safety function. The
> hardwired safety path (Contactor A drop + VFD STO) is unaffected by what mode the PLC believes it is in; an
> E-stop always wins and also force-exits jog.

---

## 4. I/O assignment (CLICK PLUS)

CLICK addressing: `X` = discrete input, `Y` = discrete output, `C` = control relay (internal bit),
`T` = timer. CLICK PLUS **CPUs have no built-in I/O**; this build uses a **C2-01CPU-2** (2 option
slots) with **two C2-14D1** option modules (each 8 DC sink/source in + 6 DC sink out) → 16 in / 12 out
for the 12 in / 6 out needed.

> **Sink/source (Rev H — simplified by the PNP prox).** The C2-14D1's **8 inputs are split into two
> isolated 4-point commons** (`X1–X4` on C1, `X5–X8` on C2 per module), each independently wire-able as
> sinking or sourcing. In Rev G the NPN prox forced one bank sourcing — but with two modules, `X009`–`X012`
> land in the *same* 4-point bank, so the NPN prox (`X010`) could not be isolated from the +24-fed contacts
> `X009`/`X011`/`X012` that shared its common. **Rev H swaps the prox to a PNP-NO unit** (P&F
> NBN8-12GM50-E2-V1), which **sources +24** on target — so it lands on the **same sinking common** (to 0 V)
> as every other dry contact. **All input commons now go to 0 V; there is no sourcing bank.** Logic sense is
> unchanged and still fail-safe: target present (lever OFF) → `X010` = 1; any break/dead sensor → `X010` = 0
> → TAP entry blocked. The **C2-14D1 outputs are sinking (NPN)**, so set the GS20 DIs to **source mode** with
> commons bonded (see §5/§10).

### Inputs
| Addr | Signal | Field device | Wiring / polarity | Used in |
|---|---|---|---|---|
| `X001` | Mode: DRILL | Door selector pos 1 (XB4BD21, N.O. block) | N.O., 1 = DRILL selected | Logic |
| `X002` | Mode: TAP | Door selector pos 2 (XB4BD21, 2nd N.O. block) | N.O., 1 = TAP selected | Logic |
| `X003` | START / FWD (+ jog-enter on long hold) | Pendant FWD button | N.O. momentary; short-press latches on **release**, ≥5 s hold arms jog | Both |
| `X004` | STOP | Pendant STOP button | **Wired N.C.**, 1 = *not* pressed (fail-safe); <5 s press also exits jog | Both |
| `X005` | REV (latched run; momentary jog in jog mode) | Pendant REV button | N.O. momentary; press latches DRILL_REV, or jogs while armed | Both |
| `X006` | Bottom travel limit | Existing Honeywell 1LS1-J (SPDT) | Wire the **N.C. side**: 1 = not at bottom; 0 = at bottom *or wire break* (fail-safe) | TAP=reverse; DRILL=fault |
| `X007` | Top travel limit | Existing Honeywell 1LS1-J (SPDT) | Wire the **N.C. side**: 1 = not at top; 0 = at top *or wire break* | TAP=stop |
| `X008` | Drum LOW | Drum switch LOW pos | N.O., 1 = LOW selected | Speed preset |
| `X009` | Drum HIGH | Drum switch HIGH pos | N.O., 1 = HIGH selected | Speed preset / permit |
| `X010` | Feed-lever-OFF proof | P&F NBN8-12GM50-E2-V1 (**PNP-NO**) on the **sinking** common | 1 = lever confirmed OFF (safe) | TAP interlock |
| `X011` | Safety-relay OK | MSR127 33-34 N.O. safety output | 1 = safety healthy (fail-safe) | Run permissive + green lamp |
| `X012` | DB-resistor over-temp | BR-N1-280W50 thermal switch | Wire the **N.C. side**: 1 = normal; 0 = over-temp *or wire break* (fail-safe) | Fault |

> Drum OFF = `X008`=0 **and** `X009`=0 → no run permissive. That reproduces the original OFF detent.
> The **1LS1-J** limits are SPDT rated 10 A line duty but only 0.8 A/115 Vdc pilot-duty; switched at
> 24 VDC into PLC inputs the load is a few mA. The **N.C.-side wiring is fail-safe** (a filming/failing
> contact drifts open = "at limit / stop" = safe direction). The spare N.O. on each switch is free —
> use it for a local indicator or a cross-check sense line.

### Outputs
| Addr | Signal | Drives | Notes |
|---|---|---|---|
| `Y001` | VFD Run-FWD | VFD DI1 | Mutually exclusive with `Y002` |
| `Y002` | VFD Run-REV | VFD DI2 | Mutually exclusive with `Y001` |
| `Y003` | VFD Preset-LOW (30 Hz) | VFD DI3 (multi-speed) | ON = low range; OFF = 60 Hz |
| `Y004` | Contactor B coil | Interposing relay CR-B → Contactor B (vintage Furnas, no load) | **Theater chunk** — pulsed on each FWD/REV transition |
| `Y005` | **GREEN lamp** | Machine-front green pilot (24 V ZBVB3) | **Solid** = all-good (`X011`∧¬`C10`∧¬`C11`∧¬`C60`); **blink** = JOG ARMED (same ∧ `C60`) |
| `Y006` | **RED lamp** | Machine-front red pilot (24 V ZBVB4) | **Solid** = safety trip or latched fault (`¬X011`∨`C10`); **blink** = DB over-temp (`C11`, when no solid-red) |

> **Pilot scheme (Rev H — four states, exactly one active).** The two machine-front lamps encode four
> operator states, in priority order (§7, RUNG 28/29). A ~1 Hz free-running blink bit (`C99`) modulates
> whichever lamp is active:
>
> | Priority | Lamp | Meaning | Condition |
> |---|---|---|---|
> | 1 | **Red — solid** | Safety tripped or latched hard fault → **investigate** | `¬X011 ∨ C10` |
> | 2 | **Red — blink** | DB resistor over-temp → **let it cool** (self-clears) | `C11 ∧ X011 ∧ ¬C10` |
> | 3 | **Green — blink** | **JOG ARMED** | `X011 ∧ ¬C10 ∧ ¬C11 ∧ C60` |
> | 4 | **Green — solid** | All-good | `X011 ∧ ¬C10 ∧ ¬C11 ∧ ¬C60` |
>
> The states are mutually exclusive and exhaustive, so **exactly one lamp is doing something** (solid or
> blinking) whenever the PLC scans. Both lamps live on the **machine front, between the travel limits**,
> run on a 24 V pair out to the machine (keeping line voltage out of the operator space). The distinct
> *blink-red vs solid-red* split matters because the operator's response differs: a thermal event is
> "wait," a hard fault is "look."
>
> The **white "power on" lamp (XB4BVB1)** is **not a PLC output** — it is wired straight across the
> protected 24 V bus by the disconnect, so it is a true "panel energized" tell independent of the
> controller.
>
> **Firmware-honesty caveat:** because green/red are firmware, a total CPU hang freezes both in their
> last state. This is acceptable **only** because the lamps (and jog mode) are advisory — the real safety
> (Contactor A drop + VFD STO) is hardwired through the safety relay and does not depend on the PLC.

> **Contactor A is NOT a PLC output.** It is owned by the safety relay only, so firmware can never
> hold the line contactor closed against a safety event.
>
> **CR-B is a power stage, not a logic stage.** All chunk *timing* is decided in the PLC on `Y004`
> (Rungs 14–15) — CR-B (24 VDC coil ← `Y004`; 6 A/250 VAC contact → Furnas coil) only amplifies that
> decision to drive the vintage AC coil. Drive CR-B's coil with a free-wheeling diode (or a suppressed
> relay variant) to protect the CLICK output; the DPDT part leaves a spare pole for a telemetry tap.

### Internal bits / timers
| Addr | Meaning |
|---|---|
| `C1` | State IDLE (derived: TAP mode ∧ ¬C2 ∧ ¬C3 ∧ ¬fault) |
| `C2` | State TAP_DOWN (latched) |
| `C3` | State BACK_OUT (latched) |
| `C10` | FAULT — latched hard fault (manual clear via RUNG 11) |
| `C11` | THERMAL — DB over-temp, **self-clearing** (follows `X012` with cool-down delay); inhibits run, drives blink-red |
| `C20` | RUN_PERMIT (`X011 ∧ (X008∨X009) ∧ X004 ∧ ¬C10 ∧ ¬C11`) |
| `C30` | DRILL_RUN — forward latch |
| `C31` | DRILL_REV — reverse latch (**new**) |
| `C40` | Chunk-pulse request |
| `C50` | FWD-press consumed flag (long-hold-entered-jog **or** press-that-stopped-REV → suppress release-latch) |
| `C60` | JOG_MODE armed (**new**) |
| `C99` | ~1 Hz free-running blink bit (indicator modulation) |
| `T1` | Chunk pulse timer (300 ms) |
| `T5FWD` | FWD hold timer (5 s → arm jog) |
| `T5STP` | STOP hold timer (5 s → distinguishes short-exit from long-stop, jog mode) |
| `T60` | Jog inactivity timer (60 s → auto-exit) |
| `Tcool` | DB-resistor cool-down delay (self-clear `C11` after `X012` recovers) |
| `Tb1`/`Tb2` | Blink astable (500 ms / 500 ms → `C99`) |

---

## 5. VFD configuration

**Selected drive: AutomationDirect GS23-22P0** (2 HP, 230 V class, 3-phase input; frame B). Confirmed
against the GS20(X) selection tables: 200–240 VAC 3-phase input covers 208 V; **CT rated output
7.5 A ≥ 6.42 A motor FLA**. Catalog data used elsewhere in this package: input current 9.6 A, fuse
**JHL35 (Class J, 35 A)** or **TJN35 (Class T, 35 A)** per the drive's fuse chart — **this build uses
JHL35 (Class J)** to match the US6J3 block, braking resistor min 47.5 Ω → **BR-N1-280W50**, heat
**74.3 W total**, clearances 50 mm top/bottom · 30 mm sides. (The optional input **line reactor is
deleted in Rev G**.) Built-in features this design relies on: **STO (TÜV/SIL2)**, **over-torque
detection**, **16-step speed**, **7 DI (24 V, NPN/PNP-selectable)**. Set the following (parameter
numbers per the GS20(X) manual):

| Function | Setting | Why |
|---|---|---|
| Motor rated current | **6.42 A** (nameplate FLA) | Enables the drive's electronic thermal overload — replaces the original heaters |
| Motor rated freq / voltage | 60 Hz / 208 V | Base point for V/Hz |
| Command source | External terminals (DI) | PLC brokers all commands |
| Frequency source | Preset / multi-speed via DI | `Y003` selects 30 Hz preset vs 60 Hz main |
| Main frequency | 60 Hz (HIGH range) | Reproduces the high ranges through the belts |
| Preset 1 frequency | **30 Hz** (LOW range) | Exactly reproduces the low range |
| DI1 / DI2 / DI3 | Run-FWD / Run-REV / preset-1 | ← `Y001` / `Y002` / `Y003` |
| Accel / decel + S-curve | Tuned, S-curve ON | Soft start; gentle self-lead reversal |
| Braking (DB) | Enable chopper; DB resistor on `+`/`BR` | Bleed reversal energy so REV doesn't overvolt-trip |
| STO | Wired to safety relay 23-24 (jumper removed) | Fast torque-off; belt-and-suspenders with Contactor A |
| **Over-torque / stall detection** | **Enable; level just above real tapping torque; short trip delay; action = trip/fault; active 30–60 Hz** | **The functional backstop for a jam** — catches a "failed to reverse/stop" stall independent of the PLC |
| DI sink/source | **Source mode** (match sinking CLICK outputs) | Electrical compatibility |

> **Sink/source:** C2-14D1 outputs are sinking (NPN) → set the GS20 DIs to **source mode** and bond
> CLICK 0 V to the GS20 DCM. Align before power-up.

---

## 6. Safety system (see DWG 02)

**Device:** **AB Guardmaster MSR127RP — cat # 440R-N23135S** (24 V DC supply, spring-clamp terminals,
monitored manual reset + EDM, **3 N.O. safety + 1 N.C. aux**, Cat 4 / PLe / SIL CL3). *(The base
-N23135 is the screw-terminal variant; the `S` denotes spring-clamp — identical relay and ratings.)*

**E-stop:** the **owner's AvidCNC station** — a Schneider mushroom **operator** with **2× ZB2-BE102**
N.C. blocks (verified **direct/positive-opening** per IEC 60947-5-1, genuine branding, sound
mechanism), an **M12 4-pin** lead, in a **yellow CM12** polycarbonate enclosure. This replaces the
Eaton E22 assembly of earlier revisions; it is the **sole safety input**.

### Safety inputs (series, both channels)
- **E-stop** — 4-wire dual-channel mushroom, maintained, twist-release. **Sole safety input.**

> **No door interlock in the safety loop — intentional.** The disconnect handle is on a fixed wall,
> not the door, and the door interlock is omitted so the machine can run door-open (§2). No
> disconnect/door interlock is wired to the safety relay; the E-stop is the only safety input.

> **No over-travel safety switch — the correct answer, not a compromise.** In TAP mode the bottom
> limit `X006` is struck on **every** cycle as the reversal trigger, so a hardwired trip there would
> drop the machine on every tap. The depth rod has a **chunky metal end stop** at the bottom of
> travel and the bottom tag is already at the end of usable rod travel, so there is physically no
> over-travel region for such a switch. Travel is **positively bounded by the mechanical stop**
> (metal-on-metal, load on the rod — *not* on a limit-switch lever). The residual "controller failed
> to reverse/stop" fault manifests as a **stall** (a *torque* event), covered by **VFD over-torque
> detection** (§5) independent of the PLC, plus the E-stop. Set the mechanical stop to engage before
> the switch levers reach their internal over-travel limit, both directions.

### Safety outputs (3 N.O. safety + 1 N.C. aux)
1. **13-14 → Contactor A coil (24 VDC).** Switches the CWBS12's 24 VDC coil directly on the DC
   control bus. Category-0 mechanical power removal, and the *session* chunk (once at start-up, once
   at shutdown/E-stop — **not** per-operation; that's Contactor B's job).
2. **23-24 → VFD STO** (STO1 + STO2). Remove the GS20's factory STO-to-+24 V jumper and route STO
   through this contact — torque removed in milliseconds without waiting for the contactor.
   **STO single-sourced by design (Rev H note):** both STO1 and STO2 are fed from the *single* output
   pair 23-24, so a welded 23-24 contact would defeat both STO channels at once — this is accepted
   because **Contactor A (13-14) is the diverse, independent stop channel** (mechanical Cat-0 power
   removal) and the CWBS12 **mirror contact catches a welded A via EDM**, blocking reset. The system's
   redundancy therefore lives in the contactor + EDM path, not in STO's own two channels. (The MSR127
   has only three N.O. outputs — A-coil, STO, `X011` — so splitting STO across two outputs isn't
   available without giving up the contactor drive or the PLC's safety-state sense.)
3. **33-34 → PLC `X011`** ("safety OK"). N.O., closed when the relay is running → `X011` = 1 when
   safe. Keeps the ladder's fail-safe sense unchanged (a broken wire reads "not safe"). `X011` is
   also what makes the **green** operator lamp honest — green drops the instant safety trips.
4. **41-42 (N.C. aux) → spare (Rev G).** Previously drove an amber "SAFETY TRIPPED" lamp; with safety
   state now shown through the firmware green/red lamps, this aux is **unused**. Leave landed on a
   labeled terminal for future use (e.g. telemetry "safety tripped" flag).

> Confirm the safety relay's output rating covers the CWBS12 coil inrush (it does). Going 24 VDC on
> the coil keeps line-adjacent voltage off the coil run entirely.

### Monitoring
- **Monitored manual reset** (`S33`-`S34`): a deliberate RESET press (XB4BA21, N.O. momentary) is
  required after any safety event or power restore → **no auto-restart**.
- **EDM / external device monitoring:** the CWBS12's **integral mirror / mechanically-linked N.C.
  contact** goes into the reset loop so a *welded* Contactor A prevents reset — the safety system
  detects its own output failure. (The CWBS12 is a safety contactor precisely so this mirror contact
  is a certified, trustworthy part with no add-on aux.)
- **Safety state to PLC (`X011`) ← 33-34 N.O.:** the PLC knows the safety state (permissive) but has
  no authority over it. N.O. output = fail-safe sense (1 when running).

> The sequencing travel limits `X006`/`X007` do **not** go to the safety relay — in TAP mode,
> hitting them is normal operation. The safety string is **E-stop only**; over-travel/stall is handled
> mechanically + by the VFD.

---

## 7. Ladder logic — CLICK PLUS (see DWG 05)

Transcribe into the free **CLICK Programming Software**. Symbols:
`─] [─` N.O. · `─]/[─` N.C. · `─]↑[─` leading-edge (press) · `─]↓[─` trailing-edge (release) ·
`─( )─` OUT · `─(S)─` SET · `─(R)─` RST · `[TMR …]` timer.

> **Scan order is load-bearing in Rev H.** The bidirectional stop-first behavior and the jog-mode
> short-press logic depend on rungs executing in the order listed. Two rules to preserve: (a) the DRILL
> **latch-SET** rungs (4, 5) run **before** the **opposite-stop** rung (7); (b) the jog/consume flag `C50`
> is set before the FWD **release-latch** is evaluated. Transcribe in the numbered order and don't reorder.

```
RUNG 1 · RUN PERMISSIVE → C20      (safe · drum-not-OFF · STOP-not-pressed · no fault · no over-temp)
   X011      X004       C10       C11
 ──] [───┬──] [───────]/[───────]/[──────────────( )── C20  RUN_PERMIT
   X008  │  STOP(nc=1) noFault   noTherm
 ──] [───┤ (drum LOW ─ OR)
   X009  │
 ──] [───┘ (drum HIGH)

RUNG 2 · SPEED PRESET → Y003       (drum LOW → 30 Hz; jog forces LOW)
   X008
 ──] [───┬───────────────────────────────────────( )── Y003  PRESET_LOW
   C60   │ (jog armed → force 30 Hz)
 ──] [───┘

RUNG 3 · BLINK ASTABLE → C99       (~1 Hz; or substitute a CLICK built-in clock relay)
   C99
 ──]/[──────────────────────────────[TMR  Tb1  K500ms]
   Tb1
 ──] [─────────────────────────────────────────────(S)── C99
   C99
 ──] [──────────────────────────────[TMR  Tb2  K500ms]
   Tb2
 ──] [─────────────────────────────────────────────(R)── C99

────────────────────────────────  DRILL — latched, bidirectional  ────────────────────────────────

RUNG 4 · DRILL FWD — LATCH SET on RELEASE   (short tap latches; ¬C50 = not consumed by a long-hold/opposite-stop; ¬C60 = not in jog)
   X001      X003      C50       C60       C20       C10       C31
 ──] [─────]↓[──────]/[───────]/[───────] [───────]/[───────]/[──(S)── C30  DRILL_RUN
          release  ¬consumed  ¬jog     permit   noFault   ¬REV

RUNG 5 · DRILL REV — LATCH SET on PRESS      (mirror of FWD; no long-hold role, so acts on press)
   X001      X005      C60       C20       C10       C30
 ──] [─────]↑[──────]/[───────] [───────]/[───────]/[──────────(S)── C31  DRILL_REV
          press    ¬jog      permit   noFault   ¬FWD

RUNG 6 · DRILL — LATCH RESET   (stop / not DRILL / lost permit / fault → drop both)
   X004
 ──]/[───┬───────────────────────────────┬───────(R)── C30
   X001  │                                └───────(R)── C31
 ──]/[───┤ (¬DRILL)
   C20   │ (¬permit — incl. X011 safety, drum-OFF, over-temp)
 ──]/[───┤
   C10   │ (fault)
 ──] [───┘

RUNG 7 · OPPOSITE-AS-STOP   (opposite button = stop only; runs AFTER the SET rungs)
   X005      C30
 ──]↑[──────] [────────────────────────┬─(R)── C30      REV press stops a FWD run
                                        └─(S)── C50      …and consume, so its release can't latch REV path
   X003      C31
 ──]↑[──────] [────────────────────────┬─(R)── C31      FWD press stops a REV run
                                        └─(S)── C50      …and consume, so its RELEASE can't latch FWD
   (Why it works: RUNG 5's ¬C30 / RUNG 4's ¬C31 interlocks block the opposite latch on the *same* press
    because the running latch is still set when SET evaluates; RUNG 7 then drops it. Second press latches.)

RUNG 8 · CLEAR FWD-CONSUMED ON RELEASE
   X003
 ──]/[─────────────────────────────────────────────(R)── C50

RUNG 9 · DRILL BOTTOM-LIMIT FAULT   (FWD only; reverse is not a feed-down runaway)
   X001       C30        X006
 ──] [──────] [───────]/[─────────────────────────(S)── C10  FAULT

────────────────────────────────  TAP — single-tap state machine  ────────────────────────────────

RUNG 10 · TAP START (IDLE → TAP_DOWN)   entry gate: lever OFF (X010=1), not in jog
   X002     X003     X010     C60      C20      C10      C2       C3
 ──] [────]↑[─────] [─────]/[─────] [─────]/[─────]/[─────]/[──(S)── C2  TAP_DOWN
                          ¬jog     permit  noFault

RUNG 11 · TAP DOWN → BACK_OUT   (bottom limit)
   C2         X006
 ──] [──────]/[─────────────────────────┬────────(R)── C2
                                         └────────(S)── C3  BACK_OUT

RUNG 12 · TAP BACK_OUT → IDLE   (top limit)      [note C: SET C2 here for continuous]
   C3         X007
 ──] [──────]/[───────────────────────────────────(R)── C3

RUNG 13 · TAP ABORT   (stop / not TAP / fault / lost-permit-or-safety)   ← Rev H: adds ¬C20 leg
   X004
 ──]/[───┬───────────────────────────────┬───────(R)── C2
   X002  │                                └───────(R)── C3
 ──]/[───┤ (¬TAP)
   C10   │ (fault)
 ──] [───┤
   C20   │ (lost permit — incl. E-stop/safety via X011, drum-OFF, STOP)
 ──]/[───┘

RUNG 14 · TAP FEED-LEVER RUNTIME TRIP   (lever ON during a cycle = tap-snap)
   C2         X010
 ──] [───┬──]/[───────────────────────────────────(S)── C10  FAULT
   C3    │ LeverON
 ──] [───┘

────────────────────────────────  DB over-temp — self-clearing  ────────────────────────────────

RUNG 15 · DB OVER-TEMP SET   (X012=0 = over-temp OR wire break → assert immediately)
   X012
 ──]/[─────────────────────────────────────────────(S)── C11  THERMAL

RUNG 16 · DB COOL-DOWN → SELF-CLEAR   (clears only after X012 stays normal for the cool-down delay)
   X012
 ──] [──────────────────────────────[TMR  Tcool  K10000ms]
   Tcool
 ──] [─────────────────────────────────────────────(R)── C11
   (Self-clearing: no manual reset, and C11 is NOT the operator-clearable C10 — so it can't fight RUNG 17.)

RUNG 17 · FAULT RESET   (STOP while fully stopped clears the hard-fault latch)
   X004      C2        C3        C30       C31
 ──]/[─────]/[──────]/[──────]/[──────]/[──────────(R)── C10  FAULT

────────────────────────────────  JOG mode  ────────────────────────────────

RUNG 18 · FWD HOLD TIMER   (times how long FWD is held)
   X003
 ──] [──────────────────────────────[TMR  T5FWD  K5000ms]

RUNG 19 · ENTER JOG   (FWD held ≥5 s, safe, not already armed; consume the press so release won't latch a run)
   T5FWD     C50       C60       X011      C10
 ──] [─────]/[───────]/[───────] [───────]/[──────┬─(S)── C60  JOG_MODE
                                                  └─(S)── C50  (consumed)

RUNG 20 · JOG IDLE TIMEOUT   (60 s with no jog button → auto-exit)
   C60      X003      X005
 ──] [────]/[──────]/[──────────────[TMR  T60  K60000ms]
   T60
 ──] [─────────────────────────────────────────────(R)── C60

RUNG 21 · JOG FORCE-EXIT   (any latched fault or safety trip)
   C10
 ──] [───┬─────────────────────────────────────────(R)── C60
   X011  │
 ──]/[───┘ (¬safe → E-stop / safety trip)

RUNG 22 · STOP HOLD TIMER (jog)
   C60       X004
 ──] [─────]/[──────────────────────[TMR  T5STP  K5000ms]

RUNG 23 · SHORT-STOP EXIT (jog)   (STOP released before 5 s → exit; long hold = plain stop)
   C60       X004      T5STP
 ──] [─────]↑[───────]/[───────────────────────────(R)── C60
          STOP released  ¬(was long hold)

────────────────────────────────  VFD run outputs  ────────────────────────────────

RUNG 24 · VFD RUN-FWD → Y001
   C30        C20       Y002
 ──] [───┬──] [──────]/[──────────────────────────( )── Y001  VFD_FWD
   C2    │  (normal: DRILL_RUN or TAP_DOWN)
 ──] [───┤
   C60   │  X003      X004     X011     C10      C11      Y002
 ──] [───┴─] [──────] [──────] [──────]/[─────]/[─────]/[──   (jog-FWD: armed · held · STOP-clear · safe · no fault/therm)

RUNG 25 · VFD RUN-REV → Y002
   C31        C20       Y001
 ──] [───┬──] [──────]/[──────────────────────────( )── Y002  VFD_REV
   C3    │  (normal: DRILL_REV or TAP back-out)
 ──] [───┤
   C60   │  X005      X004     X011     C10      C11      Y001
 ──] [───┴─] [──────] [──────] [──────]/[─────]/[─────]/[──   (jog-REV)

────────────────────────────────  Chunk (Contactor B, theater)  ────────────────────────────────

RUNG 26 · CHUNK REQUEST   (edge of entering any run / direction — TAP or DRILL)
   C2
 ──]↑[───┬────────────────────────────────────────(S)── C40  CHUNK_REQ
   C3    │
 ──]↑[───┤
   C30   │
 ──]↑[───┤
   C31   │
 ──]↑[───┘

RUNG 27 · CHUNK TIMER + OUTPUT
   C40
 ──] [──────────────────────────────[TMR  T1   K300ms]
   C40        T1
 ──] [──────]/[────────────────────────────────────( )── Y004  CONTACTOR_B
   T1
 ──] [─────────────────────────────────────────────(R)── C40

────────────────────────────────  Indicators (4 states, exactly one active)  ────────────────────────────────

RUNG 28 · GREEN → Y005      (solid = all-good; blink = jog armed)
   X011       C10       C11       C60
 ──] [──────]/[──────]/[──────]/[─────────────────( )── Y005  GREEN
   X011  │   C10       C11       C60       C99
 ──] [───┴─]/[──────]/[──────] [──────] [──   (jog: blink via C99)

RUNG 29 · RED → Y006        (solid = safety/hard fault; blink = over-temp)
   X011
 ──]/[───┬─────────────────────────────────────────( )── Y006  RED
   C10   │ (¬safe OR fault → solid)
 ──] [───┤
   C11   │ X011      C10       C99
 ──] [───┴─] [──────]/[──────] [──   (over-temp: blink via C99, only when no solid-red)
```

### Ladder notes
- **Note A — force LOW in TAP (optional).** Rung 2 already `Y003 = X008 ∨ C60` for jog. To also force LOW in
  every TAP cycle, add `∨ C2 ∨ C3`. Left off so the drum is honored in TAP.
- **Note B — FWD/REV interlock.** Rungs 24/25 each carry the other output's N.C.; the drive ramps through zero
  on reversal, so no PLC dead-time is required. Direction *changes* in DRILL are stop-first (RUNGs 5/6/7), so
  the interlock only ever guards simultaneous-edge corner cases.
- **Note C — continuous tapping.** In Rung 12 also `SET C2` when it `RST C3` (top → back down). One rung.
- **Note D — first scan.** IDLE is derived and every latch (`C2 C3 C10 C11 C30 C31 C60`) comes up cleared, so
  the machine powers up stopped, out of jog, and valid — no init rung.
- **Note E — max-dwell watchdog (optional).** Time `C2`/`C3`; if a state overruns its limit, `SET C10`.
  Backstops the VFD over-torque trip and E-stop; does not replace them.
- **Note F — `C50` is a shared "this FWD press is spent" flag.** It is set either when a 5 s hold enters jog
  (RUNG 19) or when a FWD press is used to stop a running REV (RUNG 7). Either way the FWD **release** in RUNG 4
  sees `C50=1` and does not latch a forward run. It clears on release (RUNG 8). This is what makes "hold-to-jog"
  and "opposite-as-stop" coexist on the one FWD button without a stray run.
- **Note G — blink source.** RUNG 3 is a portable 1 Hz astable. If you prefer, CLICK PLUS exposes a built-in
  clock-pulse relay you can use for `C99` instead and delete RUNG 3.
- **Note H — jog is advisory.** Nothing in the jog rungs touches the safety path. An E-stop opens STO and drops
  Contactor A regardless of mode, and RUNG 21 force-exits jog on the resulting `¬X011`.

---

## 8. Bill of materials

Maintained as a separate, orderable document: **`Powermatic_1200_Retrofit_BOM.md`** (grouped by
subsystem; VENDOR / PART NO / UNIT + LINE cost; owner-supplied items tagged **GBB** at $0). Keep it in
sync with this document's revision. Rev G highlights: SIRCO M 22013006 + 14741111 handle + US6J3
block, CWBS12-33-30C03 contactor, NDR-240-24, 24 V bus protection, XB4BVB1 white pilot, line reactor
removed, E-stop/prox/operator devices from inventory. **Rev H: prox → PNP NBN8-12GM50-E2-V1; DB-resistor
and Contactor-A prices corrected (+~$190 total); no new hardware from the logic changes.**

---

## 9. Wire numbering & color scheme (NFPA 79)

| Color | Circuit |
|---|---|
| **Black** | Line power (208 V, ungrounded, disconnect-controlled) |
| **Red** | AC control ≤120 V (largely N/A here) |
| **Blue** | DC control (24 VDC) — including the machine-front green/red pilots and the white power-on lamp |
| **Orange** | **Live with the main disconnect OFF** — design goal is that nothing is orange. Contactor A's coil is 24 VDC (blue); the only line-voltage coil is Contactor B's Furnas coil (theater), fed **downstream of the disconnect** so it de-energizes on LOTO. The disconnect's own incoming line lugs are inherently live with the switch OFF — shroud them (IP20), do not run them as general orange wiring |
| **White** | Grounded (neutral) conductor, if present |
| **Green / green-yellow** | Equipment grounding (PE) |

**Wire numbering:** number every conductor uniquely (both ends); land power on one duct run and 24 V
control on another; keep VFD output (U/V/W, motor cable) segregated and shielded, shield landed at the
drive end only. Run the **machine-front green/red pilots** as a 24 V pair out to the machine on the
control scheme (blue). **24 V bus overcurrent** (§10) sits at the supply output; the **PSU primary** gets
its own 2-pole ~3 A fuse (16 AWG tap can't be protected by the 35 A branch). All field accessories are
**home-run** to the panel — no machine j-boxes. **PE bond** the enclosure, back panel, door (bonding
strap), disconnect, both contactor frames, DIN rail, VFD PE, and — with a **dedicated bonding conductor,
not the motor mounting bolts** — the **machine frame/column**, all to a common ground bus.

---

## 10. Commissioning & validation checklist

**Before first power-up**
- [ ] Continuity/insulation check all power conductors; verify no line-level wire reaches any operator control or the machine-front lamps.
- [ ] Confirm branch fuses are **3× JHL35 (Class J, 35 A)** in the US6J3 block; upstream wall branch intact.
- [ ] Confirm disconnect wiring order: **line → SIRCO → US6J3 → Contactor A → VFD**; disconnect line-side lugs are shrouded/finger-safe (live with disconnect OFF).
- [ ] **24 V bus protection** landed at the NDR-240-24 output (≈5 A main + a dedicated feed for the safety relay).
- [ ] **PSU primary protection** landed — 2-pole ~3 A on the 208 V L-N feed (or 1-pole/120 V if a neutral is run).
- [ ] Confirm 24 V field polarity per §4; **prox is PNP-NO on the sinking input common** (BN→+24, BU→0V, BK→`X010`), sharing the single sinking common with all +24-fed contacts.
- [ ] PE bonding verified end-to-end (< 0.1 Ω to ground bus), including a **dedicated bond to the machine frame/column** (not via motor bolts), plus DIN-rail, disconnect, VFD, both contactors, door braid, panel, and enclosure.
- [ ] Live-access review: no door interlock (handle is wall-mounted, not on the door); door-open live work is for qualified persons only.

**Mechanical**
- [ ] Depth-rod **metal end stop** takes the bottom load — rod lands on the stop, **not** a limit lever.
- [ ] Set the stop first, then bottom/top tags **slightly shy** of it (both directions).

**VFD setup (motor uncoupled if practical)**
- [ ] Enter motor FLA 6.42 A; enable electronic thermal overload.
- [ ] 60 Hz main, 30 Hz preset-1; verify `Y003` selects 30 Hz.
- [ ] Accel/decel + S-curve; enable DB chopper; confirm DB resistor wired, including its **over-temp thermal switch to `X012`** (N.C.; open = fault). Verify a forced-open reads a fault.
- [ ] **Enable over-torque/stall detection**; level just above real tapping torque, short trip delay, active 30–60 Hz; verify a deliberate jam trips to fault.
- [ ] **Sink/source:** GS20 DIs set to **source mode**; bond CLICK 0 V to GS20 DCM.
- [ ] Jog FWD — verify spindle direction (swap two VFD *output* leads if reversed, never input).

**Contactor wiring**
- [ ] Both overload heaters removed; motor phases run straight through.
- [ ] **Contactor A = CWBS12**, 24 VDC coil switched by the safety-relay output; verify clean pull-in/drop-out.
- [ ] CWBS12 **integral mirror N.C.** landed in the EDM/reset loop.
- [ ] Contactor B = vintage Furnas, coil via CR-B, **contacts switching no load**.

**Safety validation (the part that keeps you alive)**
- [ ] E-stop pressed → Contactor A drops (audible chunk) **and** VFD STO opens; motor stops.
- [ ] Reset required to restart (no auto-restart); cycle power → machine comes up stopped.
- [ ] **EDM test:** jumper Contactor A closed (simulate weld) → safety relay refuses to reset.
- [ ] Confirm `X011` reflects safety state at the PLC.

**Indicator validation (Rev H — four states, exactly one active)**
- [ ] Powered + safe + no fault + not jogging → **green solid** (red off).
- [ ] Arm jog (hold FWD ≥5 s) → **green blink**; exit jog → back to green solid.
- [ ] Force DB over-temp (open `X012`) → **red blink**; restore + wait cool-down → self-clears to green.
- [ ] E-stop / drop `X011`, or latch a hard fault (`C10`) → **red solid** (outranks all).
- [ ] With over-temp AND a hard fault both active → **red solid** wins (priority order holds).
- [ ] Confirm **never two lamps at once, never neither** while powered.
- [ ] **White lamp** on whenever the disconnect is closed and 24 V is up, independent of the PLC.

**Sequence validation — DRILL (bidirectional)**
- [ ] FWD press → latched forward run at drum speed; STOP → ramps down.
- [ ] REV press → latched reverse run; STOP → ramps down. (Same one-press-and-go as FWD.)
- [ ] **Stop-first:** while running FWD, a REV press **stops** (does not reverse); a **second** REV press
      then runs reverse. Mirror-check FWD-stops-REV.
- [ ] Rapid opposite tap never plug-reverses under power; no stray run from the FWD release after an
      opposite-stop (verifies the `C50` consume path, RUNG 7/8).
- [ ] Bottom limit while running **forward** → fault + red solid. Running **reverse** into the top stop →
      VFD over-torque trips (not a ladder fault).

**Sequence validation — TAP**
- [ ] Entry gate: lever engaged (prox = lever ON) → FWD does **not** start a cycle.
- [ ] Cycle: lever OFF, FWD → down → bottom limit → ramped reverse → top limit → stop.
- [ ] Runtime trip: bump lever engaged mid-cycle → immediate fault-stop.
- [ ] **No auto-restart:** E-stop mid-cycle, then reset → machine stays stopped in IDLE; a **fresh FWD press**
      is required to start a new cycle (verifies RUNG 13 `¬C20` abort).

**Sequence validation — JOG mode**
- [ ] Hold FWD ≥5 s → **green blink** (armed); a normal FWD tap does **not** enter jog.
- [ ] In jog: FWD and REV are momentary hold-to-run at ~30 Hz, both directions; release → stops.
- [ ] Exit on: short (<5 s) STOP press; 60 s idle; any fault; E-stop. Long STOP hold = plain stop, stays armed.
- [ ] While armed, normal latched runs and TAP starts are inhibited.

**Chunk**
- [ ] Contactor B fires ~300 ms on each run start / direction change (DRILL and TAP); Contactor A does **not**
      cycle per-operation.

---

## 11. File index

| File | Contents |
|---|---|
| `Powermatic_1200_Retrofit_Documentation.md` | This document — design intent, architecture, sequence, I/O, VFD config, safety, ladder (§7), wiring, commissioning |
| `Powermatic_1200_Retrofit_BOM.md` | Bill of materials (VENDOR / PART NO / UNIT + LINE cost; GBB = owner-supplied) |
| `Powermatic_1200_Retrofit_Wire_Schedule.md` | Wire schedule — 96 conductors, from/to, color, gauge, stranded; ferrule = wire no.; all home-run |
| `01_power_one_line.svg` | Power one-line (Rev H) — SIRCO M non-fused rotary + US6J3 Class J block; wall-mount handle; CWBS12 24 VDC Contactor A; line reactor removed; PSU primary 2-pole fuse |
| `02_safety_loop.svg` | Dual-channel safety loop (Rev H) — E-stop = AvidCNC/ZB2-BE102 station; Contactor A = CWBS12, **24 VDC coil**, integral mirror aux in EDM; 41-42 spare; STO single-sourced note |
| `03_plc_io_wiring.svg` | CLICK terminal wiring (Rev H) — `X010` prox **PNP on the sinking common**; `X011`←**33-34**; `X012` DB over-temp; sinking outputs; green/red machine-front with blink legend; white lamp on 24 V bus; 24 V bus fuse |
| `04_panel_layout.svg` | Back-panel layout (Rev H) — SIRCO + US6J3 + wall-mount handle; **NDR-240-24**; CWBS12; 24 V + PSU-primary fuse holders; green/red **on the machine**; E-stop station off-panel; white pilot by the disconnect |
| `05_ladder_logic.svg` | Ladder render (Rev H) — bidirectional latched DRILL (stop-first), jog mode, self-clearing thermal, four-state indicators; authoritative listing in §7 |

---

## 12. Assumptions to field-verify (from remote inspection)

1. **Feed-lever prox mounting (`X010`).** Sense the **power-feed engagement lever** in its **OFF
   detent** with the M12 prox on an L-bracket off the head casting; target a ferrous flat/tab on the
   engagement shaft. Rev H uses the **PNP-NO** NBN8-12GM50-E2-V1 on the **sinking input common** (§4):
   `X010` = 1 = target present = lever OFF = safe. If the natural target is non-ferrous or dirty, add a
   steel flag or fall back to a sealed roller-lever switch (same `X010` point).
2. **Mechanical end stop set correctly.** The depth rod's metal bottom stop takes the over-travel
   load — set it to engage *before* the 1LS1-J levers reach their internal limit, both directions;
   tags slightly shy of the stop (§6, §10).
3. **AH7810 removed.** Front-of-machine 3-pole switch and its cable loop deleted; enclosure fed
   directly from the rear line-entry j-box; enclosure disconnect (SIRCO M) is the sole disconnecting
   means. Prove incoming-supply direction before re-landing.
4. **Only two feed-per-rev values** exist (the 2-groove belt positions). If more exist, self-lead
   tapping is unaffected (tap sets its own feed/rev).
5. **Power feed direction follows motor direction** (feed worm on the v/s drive shaft, upstream of
   the spindle reduction) — basis for "controller commands motor only; feed follows."
6. **Contactor B coil is 220 V** and pulls in reliably on 208 phase-to-phase (≈5% low, within pickup).
7. **Return-spring dial (4–12)** is counterbalance/retract preload; tune empirically for self-lead
   tapping — light enough not to oppose the tap pulling in, enough to assist back-out.
8. **Disconnect handle mounting (Rev G).** Confirm the S00 handle (14741111) mates the 22013006 frame
   and that the switch-to-wall offset is short enough for a direct external handle (no extension shaft).
9. **Machine-front lamp mounting (Rev G).** Confirm a spot between the travel limits for the green/red
   22 mm pilots (small bracket or two holes), reachable in the operator's line of sight, with a 24 V
   pair routed from the enclosure.

---

*End of document — GoodBetterBestCo, rev G, 2026-07-18.*
