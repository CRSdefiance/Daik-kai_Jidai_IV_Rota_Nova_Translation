"""Keep all native checks and qualify a batch explicitly containing no authored layout breaks."""
from scripts import check_editorial_compiled_pages_v6 as previous


def validate_documented_layouts(doc, plans):
    assert all('{LB}' not in r['english'] and '{ALIGN' not in r['english'] for r in doc['records'])
    assert all(not r.get('manual_break_reason') for r in doc['records'])


exec(compile(previous.source, __file__ + '::same-native-checks-zero-authored-layouts', 'exec'), globals())
