#!/usr/bin/env python3
"""Generate the controlled Rev M at-machine shop pack PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS = PROJECT_ROOT / "docs"
OUTPUT = DOCS / "Powermatic_1200_Shop_Pack_rM.pdf"

NAVY = colors.HexColor("#16324F")
BLUE = colors.HexColor("#245B8A")
PALE = colors.HexColor("#EAF1F7")
GRAY = colors.HexColor("#4B5563")
RED = colors.HexColor("#B42318")
PALE_RED = colors.HexColor("#FDECEC")
GREEN = colors.HexColor("#177245")


styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=17,
    leading=20,
    textColor=NAVY,
    alignment=TA_LEFT,
    spaceAfter=5,
)
SUBTITLE = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=11,
    textColor=GRAY,
    spaceAfter=10,
)
H1 = ParagraphStyle(
    "H1Custom",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=13,
    textColor=NAVY,
    spaceBefore=6,
    spaceAfter=4,
)
H2 = ParagraphStyle(
    "H2Custom",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=8.5,
    leading=10,
    textColor=BLUE,
    spaceBefore=4,
    spaceAfter=2,
)
BODY = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=7.4,
    leading=9.5,
    spaceAfter=3,
)
SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=6.6,
    leading=8.2,
)
BULLET = ParagraphStyle(
    "BulletCustom",
    parent=BODY,
    leftIndent=10,
    firstLineIndent=-6,
    bulletIndent=2,
    spaceAfter=2,
)
BOX = ParagraphStyle(
    "Box",
    parent=BODY,
    fontName="Helvetica-Bold",
    textColor=RED,
    leading=10,
)
CENTER = ParagraphStyle(
    "Center",
    parent=BODY,
    alignment=TA_CENTER,
)


def p(text, style=BODY):
    return Paragraph(text, style)


def bullets(items):
    return [Paragraph(item, BULLET, bulletText="-") for item in items]


def table(data, widths, header=True, font_size=6.8, row_bgs=None):
    cooked = []
    for row in data:
        cooked.append([cell if hasattr(cell, "wrap") else p(str(cell), SMALL) for cell in row])
    t = Table(cooked, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9AA6B2")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    if row_bgs:
        for row_index, color in row_bgs.items():
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), color))
    t.setStyle(TableStyle(commands))
    return t


def notice(title, text, danger=False):
    color = PALE_RED if danger else PALE
    title_color = RED if danger else NAVY
    content = Paragraph(
        f'<font color="{title_color.hexval()}"><b>{title}</b></font><br/>{text}',
        BODY,
    )
    t = Table([[content]], colWidths=[7.1 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("BOX", (0, 0), (-1, -1), 0.8, title_color),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(0.7)
    canvas.line(0.55 * inch, h - 0.42 * inch, w - 0.55 * inch, h - 0.42 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.55 * inch, h - 0.32 * inch, "POWERMATIC 1200 RETROFIT - SHOP PACK")
    canvas.drawRightString(w - 0.55 * inch, h - 0.32 * inch, "Rev M - 2026-08-07")
    canvas.line(0.55 * inch, 0.42 * inch, w - 0.55 * inch, 0.42 * inch)
    canvas.drawString(0.55 * inch, 0.28 * inch, "GoodBetterBestCo - E. Thayer")
    canvas.drawRightString(w - 0.55 * inch, 0.28 * inch, f"Sheet {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=letter,
    leftMargin=0.55 * inch,
    rightMargin=0.55 * inch,
    topMargin=0.58 * inch,
    bottomMargin=0.55 * inch,
    title="Powermatic 1200 Retrofit Shop Pack Rev M",
    author="GoodBetterBestCo - E. Thayer",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="shop", frames=[frame], onPage=header_footer)])

story = []


def page_title(title, subtitle):
    story.extend([p(title, TITLE), p(subtitle, SUBTITLE)])


# Sheet 1
page_title("Controlled Shop Pack", "At-machine working set - controlled braking followed by delayed STO and line isolation")
story.append(p("Implementation documents", H1))
story.extend(
    bullets(
        [
            "Wire Schedule Rev M is the point-to-point build authority. Ferrule number equals wire number.",
            "Ladder Logic Rev M is the CLICK PLUS programming authority.",
            "This Shop Pack supplies the one-line, safety loop, VFD card, and validation sequence.",
            "The owner-maintained BOM Rev M is the sourcing authority.",
            "The SCCR Worksheet Rev M records personal-shop SCCR due diligence and field verification. Revision L is intentionally skipped.",
        ]
    )
)
story.append(p("Rev M safety and hardware decisions", H1))
story.extend(
    bullets(
        [
            "Dold BH5928-92-61-24-1: 24 V, fixed screw terminals, 0.1-1.0 s adjustable release delay.",
            "Instantaneous safety contacts independently open Run-FWD and Run-REV. The GS20 performs a controlled ramp stop.",
            "Three Phoenix Contact 2966265 modules: CR-S1 asserts safety DI4, CR-S2 sources X013, and CR-DB asserts thermal DI4.",
            "Two C2-14D2 modules are installed. Slot 0 sources all six used outputs; Slot 1 outputs are reserved.",
            "Three BH5928 delayed contacts independently open the TD-DB/Contactor A path, STO1, and STO2. X011 proves KA status.",
            "TD-DB 2910140 delays thermal KA dropout after CR-DB immediately commands DI4. Hardware recovery is automatic; motion requires a fresh command.",
            "No BH5928 delayed output remains spare and Rev M includes no mechanical brake.",
            "Initial drive deceleration is 0.50 s; commission the relay at 1.00 s. Final delay is provisional until measured.",
        ]
    )
)
story.append(p("Fuse map", H1))
story.append(
    table(
        [
            ["Position", "Protects", "Holder", "Element", "Rating"],
            ["Branch (3x)", "VFD input branch", "LFT300603C, 3-pole", "TJN35 x3", "35 A Class T"],
            ["PSU-FU", "208 V PSU tap", "DN-F10MN x2", "GMC3 x2", "3 A time-delay"],
            ["KB-FU", "Contactor-B tap", "DN-F10MN x2", "GMC3 x2", "3 A time-delay"],
            ["24V-FU", "+24 V main bus", "DN-F10MN", "GMC5", "5 A time-delay"],
            ["SR-FU", "Safety-relay feed", "DN-F10MN", "GMC3", "3 A time-delay"],
            ["DB-FU", "DB thermal control", "DN-F10MN", "GMC1", "1 A time-delay"],
        ],
        [0.95 * inch, 1.65 * inch, 1.6 * inch, 1.2 * inch, 1.2 * inch],
    )
)
story.append(Spacer(1, 8))
story.append(
    notice(
        "POWER-CIRCUIT PROCUREMENT CHECK PASSED",
        "The LC1D18BD is rated 100 kA with fuses through 40 A. The GS20 manual specifies TJN35 Class T protection for GS23-22P0 and rates GS20 drives for circuits up to 100 kA. For this personal-shop retrofit, the worksheet is due diligence and a field record, not a product-certification gate.",
    )
)
story.append(Spacer(1, 7))
story.append(
    notice(
        "STOP-TIME LIMITATION",
        "At 2,000 RPM a linear 0.50 s stop represents about 8.3 spindle revolutions; 0.25 s represents about 4.2. This design materially improves coast-down but is not contact-triggered SawStop behavior.",
    )
)
story.append(PageBreak())


# Sheet 2
page_title("DWG 01 - Power One-Line", "208/240 V 3PH - permanent high-speed motor connection - VFD braking resistor")
story.append(p("Main power path", H1))
story.append(
    table(
        [
            ["Stage", "Device", "Build requirement"],
            ["1. Supply", "Rear line-entry j-box", "3PH plus PE; remove the front AH7810 switch and line-voltage operator loop."],
            ["2. Disconnect", "ABB OT30F3", "UL 98, 3-pole, 30 A, non-fused. External handle and shaft selected with enclosure. Padlockable OFF."],
            ["3. Branch protection", "LFT300603C + 3 x TJN35", "35 A Class T. Install one LFT30060FBC cover per pole."],
            ["4. Contactor A", "Schneider LC1D18BD", "3 poles, 18 A AC-3 / 32 A AC-1, 24 VDC coil. Coil path is BH5928 47-48 in series with TD-DB 11-14. 21-22 mirror N.C. is EDM; 13-14 N.O. is X011."],
            ["5. VFD", "GS23-22P0", "2 HP, 230 V class, 3PH input. DB resistor on + / BR. Separate delayed STO1 and STO2."],
            ["6. Motor", "Existing 1.5 HP motor", "Permanent high-speed lead connection. Shielded U/V/W plus dedicated PE."],
        ],
        [1.15 * inch, 1.75 * inch, 4.2 * inch],
    )
)
story.append(p("Auxiliary power and braking", H1))
story.append(
    table(
        [
            ["Function", "Device / wiring", "Notes"],
            ["24 VDC control", "Owner NDR-240-24", "PSU-FU: 2 x GMC3; 24V-FU GMC5; SR-FU GMC3; DB-FU GMC1. Bond -V/0 V to PE once at PSU."],
            ["Contactor B theater", "Vintage Furnas through CR-B 52102", "Both line tap legs fused at origin. Main contacts switch no load. Y004 supplies 300 ms chunk."],
            ["Dynamic braking", "BR-N1-280W50, 50 ohm / 280 W", "Thermal N.C. drives X012, CR-DB, and TD-DB B1. CR-DB asserts DI4 immediately; TD-DB later drops KA. Mount high; internal stirring fan."],
            ["PE and shield", "Dedicated PE and 360-degree motor-cable clamp", "Bond enclosure, panel, door, disconnect, KA, KB, rails, VFD, motor, and machine frame. Target PE continuity below 0.1 ohm."],
        ],
        [1.35 * inch, 2.15 * inch, 3.6 * inch],
    )
)
story.append(Spacer(1, 7))
story.append(notice("ORDER OF DEVICES", "Line -> OT30F3 -> LFT300603C/TJN35 -> LC1D18BD -> GS23-22P0 -> motor. Disconnect line-side terminals remain live with the switch OFF."))
story.append(Spacer(1, 7))
story.append(notice("SCCR FIELD RECORD", "The selected contactor, fuse, disconnect, and VFD conditions pass the 10 kA target. Confirm available fault current for the personal-shop record; formal certification/listing would be a separate future product step."))
story.append(PageBreak())


# Sheet 3
page_title("DWG 02 - Stop Category 1 Safety Loop", "Dual-channel E-stop - monitored reset/EDM - controlled braking - delayed independent safe state")
story.append(p("Dold BH5928-92-61-24-1", H1))
story.append(
    table(
        [
            ["Circuit", "Terminals", "Function"],
            ["E-stop channel 1", "S11 -> NC1 -> S12", "Positive-opening N.C. contact"],
            ["E-stop channel 2", "S31 -> NC2 -> S32", "Positive-opening N.C. contact; cross-fault monitoring configured"],
            ["Configuration", "S21-S22; Y39-Y40", "Cross-fault/timing jumpers per exact relay instructions; seal delay after validation"],
            ["Manual reset / EDM", "S34 -> SAFETY RESET -> KA 21-22 -> S33", "KA base-device mirror N.C.; welded KA blocks reset"],
        ],
        [1.45 * inch, 2.35 * inch, 3.3 * inch],
    )
)
story.append(p("Output allocation", H1))
story.append(
    table(
        [
            ["Timing", "Contact", "Destination", "Role"],
            ["Instant", "13-14 N.O.", "Y001 to DI1", "Open Run-FWD"],
            ["Instant", "23-24 N.O.", "Y002 to DI2", "Open Run-REV"],
            ["Instant monitor", "31-32 N.C.", "CR-S1 A1+ and CR-S2 A1+", "Close on trip; two 9 mA polarized coils"],
            ["Delayed", "47-48 N.O.", "TD-DB 11-14 -> LC1D18BD A1+", "Open Contactor A after safety or thermal delay"],
            ["Delayed", "57-58 N.O.", "VFD STO1", "Independent torque-removal channel"],
            ["Delayed", "67-68 N.O.", "VFD STO2", "Independent torque-removal channel"],
        ],
        [1.05 * inch, 1.25 * inch, 2.25 * inch, 2.55 * inch],
    )
)
story.append(p("Signal relays and thermal timer", H1))
story.append(
    table(
        [
            ["Relay", "Coil", "Contact path", "Result"],
            ["CR-S1 - Phoenix 2966265", "A1+ from SR32; A2- to 0 V", "+24 V -> 11-14 -> DI4", "GS20 function 18 Force to Stop"],
            ["CR-S2 - Phoenix 2966265", "A1+ from SR32; A2- to 0 V", "+24 V -> 11-14 -> PLC X013", "Immediate advisory trip indication"],
            ["CR-DB - Phoenix 2966265", "A1+ from DB thermal OK; A2- to 0 V", "+24 V -> 11-12 N.C. -> DI4", "Immediate thermal Force to Stop"],
            ["TD-DB - Phoenix 2910140", "A1/A2 continuous; B1 from DB thermal OK", "SR48 -> 11-14 N.O. -> KA A1+", "Release-delayed KA dropout"],
        ],
        [1.7 * inch, 1.75 * inch, 2.1 * inch, 1.55 * inch],
    )
)
story.append(Spacer(1, 6))
story.append(notice("POLARITY AND TIMER", "All three 2966265 modules contain input protection and flywheel diodes; observe A1+/A2-. CR-S contacts 12 are unused. Set TD-DB to Rs, 0.1-10 s range, nominal 1.00 s, then measure actual dropout."))
story.append(p("Sequence on E-stop", H1))
story.extend(
    bullets(
        [
            "Instant contacts open DI1 and DI2. Contact 31-32 energizes CR-S1/CR-S2, sourcing +24 V to DI4 and X013.",
            "GS20 ramps according to P07.20=2 and P01.15 while KA and both STO channels remain enabled.",
            "At the validated delay, KA, STO1, and STO2 open independently; KA 13-14 drops X011.",
            "Reset is blocked until delay completion and healthy EDM. Reset cannot restart the spindle.",
            "DB thermal trip is equipment protection: CR-DB asserts DI4 immediately; TD-DB opens KA after its measured delay. Recovery is automatic without restart.",
        ]
    )
)
story.append(PageBreak())


# Sheet 4
page_title("VFD Parameter Card - GS23-22P0", "Enter with motor uncoupled if practical - parameter numbers per current GS20 manual")
story.append(
    table(
        [
            ["Function", "Setting", "Why"],
            ["Motor current", "6.42 A", "Electronic thermal overload"],
            ["Motor base", "60 Hz / measured supply voltage", "Use the verified machine supply and motor base point"],
            ["Command source", "External terminals", "PLC brokers operational commands"],
            ["Main / preset 1", "60 Hz / 30 Hz", "High and low ranges"],
            ["DI1 / DI2 / DI3", "FWD / REV / preset 1", "DI1 and DI2 pass through separate instant safety contacts"],
            ["DI4", "Function 18 - Force to Stop", "Asserted by CR-S1 on safety trip or CR-DB on thermal trip"],
            ["P00.22", "0 - ramp to stop", "Never coast on loss of run command"],
            ["P01.13", "0.50 s initial", "Normal/fallback deceleration"],
            ["P01.15", "0.50 s initial", "Emergency deceleration time 2"],
            ["P01.26 / P01.27", "0.00 s / 0.00 s", "Remove deceleration S-curve timing addition"],
            ["P07.20", "2", "Force-to-stop uses deceleration time 2"],
            ["P02.35", "0 - line-start lockout", "Maintained RUN cannot start after reset/reboot"],
            ["DI function 28", "UNUSED", "It disables output and free-runs/coasts"],
            ["DB chopper", "Enabled; resistor on + / BR", "Absorbs stop and reversal energy"],
            ["STO1 / STO2", "Separate delayed contacts", "Independent torque-removal paths"],
            ["DI mode", "PNP - external +24 V", "Drive DIs sink current; DCM is grounded 0 V reference"],
        ],
        [1.5 * inch, 2.05 * inch, 3.55 * inch],
    )
)
story.append(p("Control-wiring checks", H1))
story.extend(
    bullets(
        [
            "Set the GS20 input selector to PNP. CLICK Y001/Y002/Y003 and the DI4 relay contacts source external +24 V to the drive's sinking inputs.",
            "Wire 81 connects grounded 0 V to DCM. The drive's internal +24 V terminal is unused for DI1-DI4.",
            "Y001 -> 13-14 -> DI1; Y002 -> 23-24 -> DI2. CR-S1 11-14 and de-energized CR-DB 11-12 independently source +24 V to DI4; CR-S2 sources +24 V to X013.",
            "Set P02.35=0. A RUN command present during reset or reboot must be removed before a fresh command can start the spindle.",
            "Set P01.26=P01.27=0.00 s. Factory 0.20 s S-curve values add about 0.20 s to nominal 0.50 s deceleration.",
            "Initial relay delay is 1.00 s. Reduce only after worst-case measured stop time is <=0.50 s and margin remains.",
            "A 0.25 s target is aspirational and may be rejected by overvoltage, overcurrent, belt/CVT dynamics, chuck retention, or resistor temperature.",
        ]
    )
)
story.append(PageBreak())


# Sheet 5
page_title("Commissioning - Before Power and VFD Setup", "Check in order - LOTO before wiring work - begin motor uncoupled where practical")
story.append(notice("SCCR FIELD RECORD", "LC1D18BD and GS23-22P0 are verified with the selected 35 A TJN35 Class T protection. Confirm available fault current for the personal-shop field record; formal product certification would be separate."))
story.append(p("Before first power-up", H1))
story.extend(
    bullets(
        [
            "Continuity and insulation check complete; no line voltage reaches operator controls or machine-front lamps.",
            "Power order verified: line -> OT30F3 -> LFT300603C/TJN35 -> KA -> VFD. Disconnect line terminals front-protected; three fuse pole covers installed.",
            "PE continuity below 0.1 ohm including dedicated machine-frame bond, door braid, rails, contactors, VFD, and motor.",
            "One and only one 0V-to-PE bond installed adjacent to the PSU. All grounded 0 V conductors are white with blue identification at both ends.",
            "CLICK modules are C2-14D2. Slot 0 is X001-X008/Y001-Y006; Slot 1 is X009-X016 with outputs reserved. Startup I/O configuration check enabled.",
            "Slot 0 V1/V2 -> protected +24 V and CO -> grounded 0 V. Slot 1 output power terminals remain unconnected.",
            "BH5928 inputs wired S11-S12 and S31-S32; S21-S22 and Y39-Y40 jumpers fitted; manual reset/EDM proven by continuity.",
            "Instant paths: Y001 through 13-14 to DI1 and Y002 through 23-24 to DI2. No bypass around either contact.",
            "Delayed paths: 47-48 through TD-DB 11-14 to KA, 57-58 to STO1, 67-68 to STO2. STO factory jumper removed.",
            "+24 V -> SR31-32 -> CR-S1/CR-S2 A1+; each A2- -> 0 V. CR-S1 11-14 sources +24 V to DI4; CR-S2 11-14 sources +24 V to X013.",
            "LC1D18BD 21-22 N.C. is in EDM; 13-14 N.O. supplies X011; built-in coil suppressor used with correct polarity.",
            "DB-FU is GMC1 1 A. TD-DB A1/A2 is continuously powered; DB thermal OK feeds X012, CR-DB A1, and TD-DB B1.",
            "Machine and panel red pilots are in parallel on Y006 and labeled FAULT / NOT READY; black button is SAFETY RESET; white pilot is CONTROL POWER.",
        ]
    )
)
story.append(p("Mechanical checks", H1))
story.extend(
    bullets(
        [
            "Depth-rod metal stop takes bottom load; neither limit-switch lever is used as a mechanical stop.",
            "Bottom and top limit tags set slightly before the physical stops.",
            "Carlo Gavazzi ICF12 target is clean and ferrous; SIO mode selected; X010=1 only with lever confirmed OFF.",
            "Chuck, arbor, belts, CVT sheaves, guards, and tool retention inspected before any rapid-stop test.",
        ]
    )
)
story.append(p("VFD setup - staged", H1))
story.extend(
    bullets(
        [
            "Measure supply voltage; enter 6.42 A, 60 Hz, and the verified motor base voltage; enable electronic thermal protection.",
            "Set P00.22=0, P01.13=0.50 s, P01.15=0.50 s, P01.26=P01.27=0.00 s, P02.35=0, P07.20=2, and DI4 function 18. Confirm function 28 is unused.",
            "Enable braking chopper. Force the DB thermostat path open: DI4 must assert immediately and KA must drop only after the measured TD-DB delay.",
            "At low speed with light tooling, verify FWD/REV directions and that E-stop commands a ramp rather than coast.",
            "Increase speed and inertia in stages; stop immediately if the drive trips, belt/CVT shifts, chuck loosens, or resistor overheats.",
        ]
    )
)
story.append(PageBreak())


# Sheet 6
page_title("Commissioning - Safety and Sequences", "Do not release for use until every required test passes and results are recorded")
story.append(p("Safety sequence and timing", H1))
story.extend(
    bullets(
        [
            "Set BH5928 delay to 1.00 s. With spindle running, E-stop picks CR-S1/CR-S2 and X013, opens DI1/DI2, and starts a controlled ramp.",
            "During braking, KA and both STO inputs remain enabled. At delay expiry KA, STO1, and STO2 open independently; X011 falls with KA.",
            "Measure stop time at minimum and maximum CVT settings, FWD and REV, and maximum expected chuck/tool inertia. Record each result.",
            "Reduce delay to about 0.75 s only after worst-case stop time is <=0.50 s and at least 0.20-0.25 s margin remains.",
            "EDM test: prevent KA 21-22 from proving open and confirm reset is refused. Remove the test condition before proceeding.",
            "After reset, spindle remains stopped and a fresh FWD command is required. E-stop during TAP returns state to IDLE.",
            "Hold a RUN command through drive reset and power-up: P02.35=0 must block motion until the command is removed and a fresh command is made.",
            "Thermal test: open the DB thermostat path while running; verify immediate DI4 ramp, delayed KA dropout, X012=0, and blinking red on both pilots.",
            "Restore the thermostat; verify automatic hardware recovery, 10 s healthy cooldown, and no spindle restart without a fresh command.",
        ]
    )
)
story.append(p("PLC indication and sequence", H1))
story.extend(
    bullets(
        [
            "Immediate trip: X013=1, C20/C60 clear, green turns off, red turns solid even while X011 remains high during braking.",
            "Safety final state: X011=0 after KA opens and red remains solid. Thermal KA dropout keeps red blinking because C11 explains X011=0.",
            "DRILL: FWD and REV latch separately; opposite button stops first; second press starts opposite direction; no plug reversal.",
            "TAP: lever-OFF proof required; bottom reverses; top stops; lever engagement mid-cycle faults and stops.",
            "JOG: the 5 s FWD timer runs only at full permissive and standstill; the held entry press never moves the spindle. Holding FWD during any DRILL/TAP motion state must not time, arm jog, or force 30 Hz. Drum OFF inhibits motion; any STOP exits jog.",
        ]
    )
)
story.append(p("Acceptance boundary", H1))
story.extend(
    bullets(
        [
            "SCCR worksheet completed as a personal-shop field record; certification/listing deferred unless this becomes a product.",
            "No nuisance drive faults, DC-bus overvoltage, or contactor opening before the spindle reaches zero.",
            "No belt/CVT upset, chuck/arbor release, abnormal motor noise, or repeated DB-resistor thermal trip over the planned stop frequency.",
            "If <=0.50 s cannot be demonstrated with margin, do not release the machine. Correct the braking hardware/drive configuration and repeat validation; a longer BH5928 delay requires a formal safety-timing redesign.",
            "This is not contact detection and cannot guarantee stopping within one revolution at 2,000 RPM.",
        ]
    )
)
story.append(Spacer(1, 8))
story.append(
    table(
        [
            ["Recorded item", "Result"],
            ["Available fault current / SCCR field note", "____________________________________________"],
            ["Worst-case measured stop time", "____________________________________________"],
            ["Final BH5928 delay setting", "____________________________________________"],
            ["Final TD-DB measured dropout", "____________________________________________"],
            ["Maximum validated chuck/tool inertia", "____________________________________________"],
            ["Reviewed by / date", "____________________________________________"],
        ],
        [3.05 * inch, 4.05 * inch],
    )
)

doc.build(story)
print(OUTPUT)
