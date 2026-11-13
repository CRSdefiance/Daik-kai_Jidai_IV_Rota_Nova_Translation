"""One paragraph for15 source-mapped numeric special-move calls."""
IDS=(*range(1980,1994),2146)
PROFILE='duel-special-numeric-postmacro24x3-v1'


def compiled(row):
    if row['message_id'] not in IDS or row['native_argument_count']!=0 or row['source_native_macros']:
        raise ValueError('Original no-argument special call required')
    text=row['english']
    if not text or not text.isascii() or text!=' '.join(text.split()) or any(ord(c)<32 or ord(c)>126 for c in text):
        raise ValueError('One natural paragraph without authored line breaks or alignment required')
    if '%' in text or any(c in text for c in '{}') or len(text)>=100:
        raise ValueError('No new substitutions or controls; preserve the proven input bound')
    return text.encode('ascii')
