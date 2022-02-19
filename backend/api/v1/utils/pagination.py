#!/usr/bin/python3
import re


def range_slicer(span: str, items: list):
    '''Retrieves a section of a list of items with a given span.'''
    if span is None:
        return items
    span_match = re.fullmatch(
        r'(?P<size>\d+)(?:,(?P<index>\d+))?',
        span
    )
    size = int(span_match.group('size'))
    index = 0
    if span_match.group('index') is not None:
        index = int(span_match.group('index'))
    start = size * index
    end = start + size
    return items[start: end]


def extract_page(
    data=[],
    span=12,
    after=None,
    before=None,
    pop_top=False,
    key_fxn=lambda x: x['id']):
    '''Extracts a section of a data list.
    '''
    sub_data = []
    if after and before:
        return sub_data
    elif after:
        add_item = False
        n = 0
        for item in data:
            if add_item:
                sub_data.append(item)
                n += 1
                if n == span:
                    break
            elif key_fxn(item):
                add_item = True
    elif before:
        n = 0
        for item in data:
            if key_fxn(item):
                break
            else:
                n += 1
        a = n - (span + 1) if n > (span + 1) else 0
        b = n - 1 if n > 1 else 0
        sub_data = data[a:b]
    else:
        sub_data = data[0:span] if pop_top else data[-span:]
    return sub_data
