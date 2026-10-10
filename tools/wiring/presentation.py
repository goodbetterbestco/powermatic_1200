"""Compact wire-schedule labels, retaining full source terminal metadata."""
import re


def pin_label(pad):
    label = pad['fields'].get('Wire.PinLabel.' + pad['pin'], pad['pin'])
    label = label.replace('+', '_PLUS').replace('-', '_MINUS')
    label = re.sub(r'[^A-Za-z0-9_]+', '_', label).strip('_')
    return pad['ref'] + '_' + label


def termination_code(text, awg):
    """F = ferrule, R = ring, B = bare; retain explicit unknowns."""
    gauge = re.search(r'\b(\d+)\s*AWG\b', text)
    gauge = gauge.group(1) if gauge else str(awg or 'TBD')
    if text.startswith(('Ferrule', 'Single ferrule', 'Twin ferrule')):
        twin = text.startswith('Twin ferrule')
        length = re.search(r'\bL\s*=\s*(\d+(?:\.\d+)?|TBD)\s*mm', text)
        suffix = '_' + length.group(1) + 'mm' if length else '_TBDmm'
        return 'F' + ('2x' if twin else '') + gauge + suffix
    if text.startswith('Ring'):
        stud = re.search(r'stud\s*=\s*#?(\d+)-(\d+)', text)
        diameter = re.search(r'\bOD\s*(?:<=|=)\s*(\d+(?:\.\d+)?|TBD)\s*mm', text)
        size = ''.join(stud.groups()) if stud else 'TBD'
        return 'R' + gauge + '_' + size + '_' + (diameter.group(1) if diameter else 'TBD') + 'mm'
    if text.startswith(('Bare stranded copper', 'Plug clamp')):
        strip = re.search(r'\bstrip\s*=\s*(\d+(?:\.\d+)?)\s*mm', text)
        return 'B' + gauge + ('_' + strip.group(1) + 'mm' if strip else '')
    # Non-assembly endpoints are kept explicit rather than assigned a false type.
    if text.startswith(('Factory pigtail', 'M12 mating contact',
                        'Supplied assembly connection', 'Supplied fork-ended', 'Retained jumper')):
        return 'supplier'
    if text.startswith(('N/A', 'Required jumper', 'Conductive DIN-rail')):
        return ''
    raise ValueError('Assign an F/R/B termination before scheduling this endpoint: '+text)
