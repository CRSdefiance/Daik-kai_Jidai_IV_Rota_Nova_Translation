"""One-paragraph compiler contract for source-proven duel-action voice tables."""
IDS=tuple(range(1957,1973))
PROFILE='duel-timed-reaction-postmacro24x3-v1'


def compiled(row):
    n,text=row['message_id'],row['english']
    if n not in IDS or row['native_argument_count']!=0 or row['source_native_macros']:
        raise ValueError('Original no-argument timed duel reaction required')
    if row['source_family']!=('positive_action_reaction' if n<1965 else 'negative_action_reaction'):
        raise ValueError('Source voice family differs')
    if not text or text!=' '.join(text.split()) or not text.isascii() or any(ord(c)<32 or ord(c)>126 for c in text):
        raise ValueError('Author one natural paragraph without alignment or manual breaks')
    if '%' in text or any(c in text for c in '{}') or len(text)>=100:
        raise ValueError('No new substitutions or controls permitted')
    return text.encode('ascii')
