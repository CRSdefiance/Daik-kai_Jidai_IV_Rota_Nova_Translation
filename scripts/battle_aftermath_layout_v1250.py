"""Unwrapped prose contract; native formatting approval is deliberately separate."""
IDS=(*range(1994,2052),*range(2114,2122),*range(2138,2146),2192)
PROFILE='battle-aftermath-portrait-postmacro-v1'


def paragraph(row):
    n=row['message_id'];text=row['english']
    if n not in IDS or not text.isascii() or text!=' '.join(text.split()):
        raise ValueError('One reviewed ASCII paragraph without authored alignment is required')
    if not text or any(ord(c)<32 or ord(c)>126 for c in text) or any(c in text for c in '{}'):
        raise ValueError('Authored controls and layout markup are forbidden')
    count=1 if 1994<=n<=1999 else 0
    if row['native_argument_count']!=count or text.count('%s')!=count or '%' in text.replace('%s',''):
        raise ValueError('Preserve the exact original town-name substitution only')
    if len(text.encode('ascii'))>=160:
        raise ValueError('Prose exceeds the reviewed prospective input bound')
    return text.encode('ascii')
