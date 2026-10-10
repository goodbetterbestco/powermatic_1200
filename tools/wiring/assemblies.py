"""Resolve explicitly mated supplier contacts and native KiCad jumper groups."""
import json
from collections import Counter

from source import one, prop


def supplied_assemblies(board, footprints, pin_nets):
    pads = {(p['footprint_id'], p['pin']): p for p in board['pads']}
    aliases, connections, assemblies = {}, [], []
    for footprint in footprints:
        if prop(footprint, 'Wire.SuppliedAssembly') != 'busbar':
            continue
        fid = one(footprint, 'uuid')[1]
        ref = prop(footprint, 'Reference')
        quantity = prop(footprint, 'Wire.PurchaseQuantity')
        if quantity is not None and quantity not in ('0', '1'):
            raise ValueError(ref + ': supplier purchase quantity must be 0 or 1.')
        payload = json.loads(prop(footprint, 'Wire.MatingPads') or '{}')
        mapping = payload.get('pads', {})
        actual = {pin for owner, pin in pads if owner == fid}
        if payload.get('schema') != 1 or set(mapping) != actual or not actual:
            raise ValueError(ref + ': supplier mating map must cover every contact pad.')
        targets = {}
        for pin, target in mapping.items():
            if not isinstance(target, list) or len(target) != 2:
                raise ValueError(ref + ': invalid supplier mating target for ' + pin)
            host = prop(footprint, 'Wire.Host.' + target[0])
            source = pads[fid, pin]
            destination = pads.get((host, target[1]))
            if destination is None or destination['fields'].get('Wire.SuppliedAssembly'):
                raise ValueError(ref + '.' + pin + ': missing or invalid host terminal.')
            if any(abs(a-b) > 0.000002 for a, b in zip(source['at'], destination['at'])):
                raise ValueError(ref + '.' + pin + ': supplier contact does not overlap its host terminal.')
            endpoint = destination['ref'], destination['pin']
            net = pin_nets.get(endpoint)
            if not net or net.startswith('unconnected-') or net != source['net'] or net != destination['net']:
                raise ValueError(ref + '.' + pin + ': supplier contact and host schematic net disagree.')
            aliases[source['id']] = destination['id']
            targets[pin] = destination
        if len({p['id'] for p in targets.values()}) != len(targets):
            raise ValueError(ref + ': multiple supplier contacts claim the same host terminal.')
        groups = one(footprint, 'jumper_pad_groups')
        groups = groups[1:] if groups else []
        if Counter(pin for group in groups for pin in group) != Counter(actual):
            raise ValueError(ref + ': native jumper groups must cover each supplier contact exactly once.')
        bridges = []
        for group in groups:
            if len(group) != 2:
                raise ValueError(ref + ': each busbar bridge needs two contacts.')
            pair = [targets[pin] for pin in group]
            if len({p['net'] for p in pair}) != 1:
                raise ValueError(ref + ': native busbar jumper group joins different electrical nets.')
            endpoints = [[p['ref'], p['pin']] for p in pair]
            bridge = {'assembly': ref, 'part': prop(footprint, 'MPN'),
                      'pad_ids': [p['id'] for p in pair], 'endpoints': endpoints, 'net': pair[0]['net']}
            connections.append(bridge)
            bridges.append(bridge)
            board['internal_groups'].append(endpoints)
        assemblies.append({'reference': ref, 'part': prop(footprint, 'MPN'),
                           'quantity': int(quantity) if quantity is not None else 1,
                           'kit_id': prop(footprint, 'Wire.KitID'),
                           'piece': prop(footprint, 'PartID'), 'connections': bridges})
    board['pad_aliases'] = aliases
    board['supplied_connections'] = connections
    return assemblies
