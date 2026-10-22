"""Six unwrapped fire alerts; native formatting/integration approval is separate."""
IDS = tuple(range(2052,2058))
PROFILE = 'powder-fire-portrait-postmacro-v1'


def paragraph(row):
    text = row['english']
    if row['message_id'] not in IDS or not text.isascii() or text != ' '.join(text.split()):
        raise ValueError('One faithful ASCII paragraph without authored alignment is required')
    if not text or any(ord(c) < 32 or ord(c) > 126 for c in text) or any(c in text for c in '{}%'):
        raise ValueError('These clean sources have no formatting commands or substitutions')
    if row['native_argument_count'] != 0 or row['source_native_macros'] or len(text.encode('ascii')) >= 160:
        raise ValueError('Preserve the source argument contract and prospective native input bound')
    return text.encode('ascii')
