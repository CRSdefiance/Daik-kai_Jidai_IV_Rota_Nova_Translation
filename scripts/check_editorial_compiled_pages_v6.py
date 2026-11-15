"""Check native FE row membership as well as complete glyphs, bounds and consumption."""
import inspect
from types import FunctionType

from scripts import check_editorial_compiled_pages_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def validate_documented_layouts(doc, plans):
    if 'subset_of' not in doc:
        return previous.validate_documented_layouts(doc, plans)
    parent_path = previous.Path(doc['subset_of'])
    assert previous.sha(parent_path.read_bytes()) == doc['subset_of_sha256']
    parent = previous.load(parent_path)
    originals = {r['id']: r for r in parent['records']}
    assert len(doc['records']) == len({r['id'] for r in doc['records']})
    assert all(r == originals[r['id']] for r in doc['records'])
    source = checked_text(inspect.getsource(previous.validate_documented_layouts), {
        '    assert count == 13': "    assert count == sum('{LB}' in r['english'] for r in doc['records'])",
    })
    env = dict(previous.validate_documented_layouts.__globals__)
    exec(compile(source, __file__ + '::immutable-parent-subset-layouts', 'exec'), env)
    env['validate_documented_layouts'](doc, plans)


def check_FE_rows(expected, rendered):
    events = rendered['events']
    assert all(e['kind'] == 'ascii' and 0 <= e['code'] < 128 for e in events)
    target = [line.strip(b' ') for line in expected.split(b'\n')]
    actual = [bytes(e['code'] for e in events if e['y'] == 12 * i).strip(b' ') for i in range(len(target))]
    assert all(e['y'] in range(0, 12 * len(target), 12) for e in events)
    assert actual == target, (actual, target)
    return dict(planned_rows=[v.decode('ascii') for v in target],
                actual_rows=[v.decode('ascii') for v in actual],
                complete_glyph_row_membership_exact=True,
                guard_spaces_ignored_for_membership_only=True)


source = checked_text(previous.source, {
    '                rendered=painter(expected)':
    "                rendered=painter(expected)\n                rendered['planned_native_row_comparison']=check_FE_rows(expected,rendered)",
    'source_qualified_structural_or_dramatic_layouts=13,':
    "source_qualified_structural_or_dramatic_layouts=sum('{LB}' in r['english'] for r in doc['records']),FE_actual_glyph_row_membership_checked=True,",
})
exec(compile(source, __file__ + '::same-native-checks-plus-FE-row-membership', 'exec'), globals())
