# Powermatic 1200 Retrofit - CLICK PLUS Ladder Logic

Transcribe into the free **CLICK Programming Software**. Symbols:
`─] [─` N.O. · `─]/[─` N.C. · `─]↑[─` leading-edge (press) · `─]↓[─` trailing-edge (release) ·
`─( )─` OUT · `─(S)─` SET · `─(R)─` RST · `[TMR …]` timer.

> **Scan order is load-bearing in Rev M.** The bidirectional stop-first behavior and the jog-mode
> short-press logic depend on rungs executing in the order listed. Two rules to preserve: (a) the DRILL
> **latch-SET** rungs (4, 5) run **before** the **opposite-stop** rung (7); (b) the jog/consume flag `C50`
> is set by the 5 s entry hold before the jog output rung can act on that held FWD input. Transcribe in
> the numbered order and don't reorder.

```
RUNG 1 · RUN PERMISSIVE → C20      (KA proved · no immediate trip · drum ON · STOP clear · healthy)
   X011      X013       X008        X004       C10       C11
 ──] [─────]/[───────┬──] [─────┬──] [───────]/[───────]/[──────( )── C20
                     │   X009   │
                     └──] [─────┘

   C20 = X011 AND NOT X013 AND (X008 OR X009) AND X004 AND NOT C10 AND NOT C11

RUNG 2 · SPEED PRESET → Y003       (drum LOW → 30 Hz; jog forces LOW)
   X008
 ──] [───┬───────────────────────────────────────( )── Y003  PRESET_LOW
   C60   │ (jog armed → force 30 Hz)
 ──] [───┘

RUNG 3 · BLINK ASTABLE → C99       (~1 Hz)
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

RUNG 12 · TAP BACK_OUT → IDLE   (top limit)
   C3         X007
 ──] [──────]/[───────────────────────────────────(R)── C3

RUNG 13 · TAP ABORT   (stop / not TAP / fault / lost-permit-or-safety)
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

RUNG 18 · FWD HOLD TIMER   (times FWD only while fully permissive and stopped)
   X003      C20       C30       C31       C2        C3
 ──] [─────] [───────]/[───────]/[───────]/[───────]/[──[TMR  T5FWD  K5000ms]

RUNG 19 · ENTER JOG   (FWD held ≥5 s at standstill; repeat all motion-state interlocks and consume the press)
   T5FWD     C50       C60       C20       C30       C31       C2        C3
 ──] [─────]/[───────]/[───────] [───────]/[───────]/[───────]/[───────]/[──┬─(S)── C60  JOG_MODE
                                                                      └─(S)── C50  (consumed)

RUNG 20 · JOG IDLE TIMEOUT   (60 s with no jog button → auto-exit)
   C60      X003      X005
 ──] [────]/[──────]/[──────────────[TMR  T60  K60000ms]
   T60
 ──] [─────────────────────────────────────────────(R)── C60

RUNG 21 · JOG FORCE-EXIT   (any latched fault, thermal trip, or safety trip)
   C10
 ──] [───┬─────────────────────────────────────────(R)── C60
   C11   │
 ──] [───┤ (DB thermal trip/cooldown)
   X011  │
 ──]/[───┤ (final safe state lost)
   X013  │
 ──] [───┘ (immediate safety trip)

RUNG 22 · STOP EXIT (jog)   (any STOP press exits jog mode)
   C60       X004
 ──] [─────]/[─────────────────────────────────────(R)── C60

RUNG 23 · RESERVED   (the former STOP-hold distinction remains deleted)

RUNG 23A · JOG RUN PERMISSIVE → C61
   C60       X011      X013       X008        X004       C10       C11
 ──] [─────] [───────]/[───────┬──] [─────┬──] [───────]/[───────]/[──────( )── C61
                               │   X009   │
                               └──] [─────┘

────────────────────────────────  VFD run outputs  ────────────────────────────────

RUNG 24 · VFD RUN-FWD → Y001
   C30        C20       Y002
 ──] [───┬──] [──────]/[──────────────────────────( )── Y001  VFD_FWD
   C2    │  (normal: DRILL_RUN or TAP_DOWN)
 ──] [───┤
   C61   │  X003      C50       Y002
 ──] [───┴─] [──────]/[───────]/[──   (jog-FWD: NOT C50 means the 5 s entry hold can NOT jog)

  Y001 = [ (C30 OR C2) AND C20 AND NOT Y002 ] OR [ C61 AND X003 AND NOT C50 AND NOT Y002 ]

RUNG 25 · VFD RUN-REV → Y002
   C31        C20       Y001
 ──] [───┬──] [──────]/[──────────────────────────( )── Y002  VFD_REV
   C3    │  (normal: DRILL_REV or TAP back-out)
 ──] [───┤
   C61   │  X005      Y001
 ──] [───┴─] [──────]/[──   (jog-REV)

  Y002 = [ (C31 OR C3) AND C20 AND NOT Y001 ] OR [ C61 AND X005 AND NOT Y001 ]

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
   X011      X013       C10       C11       C60
 ──] [─────]/[───────]/[──────]/[──────]/[──────────────( )── Y005  GREEN
   X011  │  X013       C10       C11       C60       C99
 ──] [───┴─]/[───────]/[──────]/[──────] [──────] [──   (jog: blink via C99)

RUNG 29 · RED → Y006        (solid = safety/hard fault; blink = thermal trip/cooldown)
   X013
 ──] [───┬─────────────────────────────────────────( )── Y006  RED
   C10   │
 ──] [───┤ (immediate safety trip OR hard fault → solid)
   X011     C11
 ──]/[────]/[───┤ (KA not proved, except while thermal state explains its intentional dropout)
   C11      X013       C10       C99
 ──] [────]/[────────]/[───────] [────────────────┘ (thermal blink when no solid-red cause)

  RED_SOLID = X013 OR C10 OR (NOT X011 AND NOT C11)
  RED_BLINK = C11 AND NOT X013 AND NOT C10 AND C99
```
