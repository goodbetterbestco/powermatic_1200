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
