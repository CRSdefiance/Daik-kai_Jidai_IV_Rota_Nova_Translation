"""Compiler-owned presentation for the two proven original duel consumers."""
DUEL_IDS = tuple(range(1931, 1951))
ESCAPE_IDS = (*range(1951, 1957), *range(1973, 1980))
IDS = (*DUEL_IDS, *ESCAPE_IDS)
PROFILE = 'duel-distinct-postmacro24x3-and-escape-speech35x4-v1'


def compiled(row):
    number, english = row['message_id'], row['english']
    if number not in IDS:
        raise ValueError('Original duel or post-duel escape source ID required')
    if (not english or not english.isascii() or english != ' '.join(english.split())
            or any(ord(c) < 32 or ord(c) > 126 for c in english)
            or any(c in english for c in '{}')):
        raise ValueError('One natural ASCII paragraph required; no authored breaks or alignment')
    arguments = int(number <= 1938 or 1951 <= number <= 1956)
    if english.count('%s') != arguments or '%' in english.replace('%s', ''):
        raise ValueError('Preserve the original name substitution exactly')
    if row['native_argument_count'] != arguments:
        raise ValueError('Declared name arguments differ from native source')
    family = ('challenge' if number <= 1938 else 'acceptance' if number <= 1944 else
              'defeated_opponent_threat' if number <= 1950 else
              'cover_for_defeated_captain' if number <= 1956 else 'cover_for_main_captain')
    if row['source_family'] != family:
        raise ValueError('Source voice-table family mismatch')
    if any(token in english for token in ('FA', 'FI', 'FO', 'FU', 'IC')):
        raise ValueError('No original name/pronoun commands occur in these source templates')
    if len(english) >= (100 if number in DUEL_IDS else 220):
        raise ValueError('One paragraph exceeds this proven consumer input contract')
    # Shared portrait speech owns one presentation-state byte. Distinct static
    # duel widgets consume the whole template and require no such state prefix.
    return (b' ' if number in ESCAPE_IDS else b'')+english.encode('ascii')
