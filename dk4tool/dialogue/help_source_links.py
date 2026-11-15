"""Read binary HELP links without treating Shift-JIS trail bytes as delimiters."""


def sjis_lead(value):
    return 0x81 <= value <= 0x9F or 0xE0 <= value <= 0xFC


def source_links(raw):
    result, cursor = [], 0
    while cursor < len(raw):
        byte = raw[cursor]
        if sjis_lead(byte):
            if cursor + 1 >= len(raw):
                raise ValueError('Truncated source Shift-JIS character')
            raw[cursor:cursor + 2].decode('cp932')
            cursor += 2
        elif byte == 0x7B:
            start, end = cursor, cursor + 1
            while end < len(raw) and raw[end] != 0x3A:
                if sjis_lead(raw[end]):
                    if end + 1 >= len(raw):
                        raise ValueError('Truncated Shift-JIS link label')
                    raw[end:end + 2].decode('cp932')
                    end += 2
                else:
                    if raw[end] in (0, 0x7B, 0x7D):
                        raise ValueError('Malformed source HELP link label')
                    end += 1
            if end + 2 >= len(raw) or raw[end + 2] != 0x7D:
                raise ValueError('Malformed source HELP link destination')
            result.append({'start': start, 'end': end + 3,
                           'label': raw[start + 1:end].decode('cp932'),
                           'topic_id': raw[end + 1],
                           'label_hex': raw[start + 1:end].hex()})
            cursor = end + 3
        else:
            cursor += 1
    return result


def readable_source(raw):
    parts, cursor = [], 0
    for link in source_links(raw):
        parts.append(raw[cursor:link['start']].decode('cp932'))
        parts.append(f"[[{link['topic_id']}|{link['label']}]]")
        cursor = link['end']
    parts.append(raw[cursor:].rstrip(b'\0').decode('cp932'))
    return ''.join(parts)
