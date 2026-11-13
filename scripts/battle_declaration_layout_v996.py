"""One logical paragraph before the original speech macro/word-wrap consumer."""
IDS = tuple(range(1889, 1911))
PROFILE = 'battle-declaration-native-post-expansion-35x4-v1'


def compiled(row):
    n = row['message_id']
    if n not in IDS:
        raise ValueError('Original battle/declaration source ID required')
    english = row['english']
    arguments = int(1897 <= n <= 1903)
    if (not english or not english.isascii() or english != ' '.join(english.split())
            or any(ord(c) < 32 or ord(c) > 126 for c in english)
            or any(c in english for c in '{}')):
        raise ValueError('One natural ASCII paragraph required;no authored or pregenerated breaks/alignment')
    if english.count('%s') != arguments or '%' in english.replace('%s', ''):
        raise ValueError('The original complete faction-label substitution must be preserved exactly')
    if row['native_argument_count'] != arguments:
        raise ValueError('Declared arguments differ from the source caller')
    if any(token in english for token in ('FA', 'FI', 'FO', 'FU', 'IC')):
        raise ValueError('No native name/pronoun macro appears in these22 clean source entries')
    if len(english) >= 220:
        raise ValueError('Paragraph exceeds the established speech scratch contract')
    # This is compiler-owned presentation state,never translator alignment.
    # Do not prewrap a paragraph before53914:literal I followed byLF is an
    # original control-suffixed pronoun command. The actual native speech path
    # performs expansion first and then generates the protected display breaks.
    return b' '+english.encode('ascii')
