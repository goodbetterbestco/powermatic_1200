"""Minimal KiCad S-expression reader and byte-preserving direct-child patches."""
import json
import re

TOKEN = re.compile(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+')


def parse(text):
    stack, root = [], None
    for token in TOKEN.findall(text):
        if token == '(':
            if not stack and root is not None:
                raise ValueError('Multiple schematic roots')
            stack.append([])
        elif token == ')':
            if not stack:
                raise ValueError('Unbalanced closing parenthesis')
            value = stack.pop()
            if stack:
                stack[-1].append(value)
            else:
                root = value
        else:
            if not stack:
                raise ValueError('Unexpected data outside an S-expression')
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    if stack or root is None:
        raise ValueError('Incomplete S-expression')
    return root



# KiCad's native board serializer puts root footprints and their children at
# one and two tabs respectively. Read only their metadata, never dense artwork.
FOOTPRINT_BLOCK = re.compile(r'^\t\(footprint\b.*?^\t\)', re.M | re.S)
FOOTPRINT_FIELD = re.compile(r'^\t\t\((?:uuid|property|jumper_pad_groups)\b.*?(?=^\t\t\(|^\t\)|\Z)', re.M | re.S)


def footprint_metadata(text):
    """Fast native-serialized metadata, with full parsing for other formatting."""
    blocks = FOOTPRINT_BLOCK.findall(text)
    if blocks and len(blocks) == len(re.findall(r'^\s*\(footprint\b', text, re.M)):
        result = []
        for raw in blocks:
            fields = FOOTPRINT_FIELD.findall(raw)
            parsed = [parse(f) for f in fields]
            if sum(n[0] == 'uuid' for n in parsed) != 1 or sum(n[0] != 'uuid' for n in parsed) != len(re.findall(r'^\s*\((?:property|jumper_pad_groups)\b', raw, re.M)):
                break
            result.append(['footprint', *parsed])
        else:
            return result
    return nodes(parse(text), 'footprint')


def nodes(node, name):
    return [n for n in node if isinstance(n, list) and n and n[0] == name]


def one(node, name):
    return next(iter(nodes(node, name)), None)


def prop(node, name):
    return next((n[2] for n in nodes(node, 'property') if n[1] == name), None)


def children(text):
    depth, start = 0, None
    for match in TOKEN.finditer(text):
        if match[0] == '(':
            if depth == 1:
                start = match.start()
            depth += 1
        elif match[0] == ')':
            depth -= 1
            if depth == 1:
                yield start, match.end(), text[start:match.end()]
    if depth != 0:
        raise ValueError('Unbalanced source text')


def key(node):
    return next(TOKEN.finditer(node[1:]))[0]


def replace(text, edits):
    for a, b, new in sorted(edits, reverse=True):
        text = text[:a] + new + text[b:]
    return text
