"""One prose paragraph before native name expansion and automatic speech wrapping."""
IDS=tuple(range(1911,1931))
PROFILE='reinforcement-sniping-native-post-expansion-35x4-v1'


def compiled(row):
    n=row['message_id'];english=row['english']
    if n not in IDS:raise ValueError('Original reinforcement/covering-fire/shot source ID required')
    if (not english or not english.isascii() or english!=' '.join(english.split())
        or any(ord(c)<32 or ord(c)>126 for c in english) or any(c in english for c in '{}')):
        raise ValueError('One natural ASCII paragraph required;no authored alignment or line breaks')
    arguments=int(n<1924)
    if english.count('%s')!=arguments or '%' in english.replace('%s','') or row['native_argument_count']!=arguments:
        raise ValueError('Original source substitutions must be preserved exactly')
    family='reinforcement' if n<1917 else 'covering_fire' if n<1924 else 'admiral_shot'
    if row['source_family']!=family:raise ValueError('Original source family mismatch')
    if any(token in english for token in ('FA','FI','FO','FU','IC')) or len(english)>=220:
        raise ValueError('Unsupported native macro or excessive speech scratch input')
    return b' '+english.encode('ascii')
