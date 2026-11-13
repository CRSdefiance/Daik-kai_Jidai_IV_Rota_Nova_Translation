"""Compile reviewed sighting paragraphs before original native macro expansion."""
IDS=tuple(range(614,629))
PROFILE='sighting-native-post-expansion-35x4-v1'


def compiled(row):
    n=row['message_id'];english=row['english']
    if n not in IDS:raise ValueError('Original sighting source ID required')
    if (not english or not english.isascii() or english!=' '.join(english.split())
        or any(ord(c)<32 or ord(c)>126 for c in english) or any(c in english for c in '{}')):
        raise ValueError('One natural ASCII paragraph required;no authored alignment or line breaks')
    if english.count('%s')!=2 or '%' in english.replace('%s','') or row['native_argument_count']!=2:
        raise ValueError('Original two source substitutions required in bearing/faction order')
    family='fleet-sighting-battle-preparation' if n<622 else 'fleet-sighting-under-attack'
    if row['source_family']!=family:raise ValueError('Original source family mismatch')
    if any(token in english for token in ('FA','FI','FO','FU','IC')) or len(english)>=220:
        raise ValueError('Unsupported native macro or excessive speech scratch input')
    return b' '+english.encode('ascii')
