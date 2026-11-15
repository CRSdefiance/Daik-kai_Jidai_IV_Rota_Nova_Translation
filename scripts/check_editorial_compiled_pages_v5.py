"""Normalize only source-qualified structural/dramatic LB markers for native comparison."""
from scripts import check_editorial_compiled_pages_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def validate_documented_layouts(doc, plans):
    by_id = {r['id']: r for r in plans['records']}
    count = 0
    for row in doc['records']:
        if '{LB}' not in row['english']:
            continue
        count += 1
        assert row['manual_break_reason'] and row['qa_waiver_reason']
        plan = by_id[row['id']]
        if row['kind'] == 'system-FE':
            assert row['block'] == 142 and row['source_selector'] == 254
            assert row['source_Japanese'].startswith('＜異国の少女＞\n')
            assert row['english'].startswith('<Foreign Girl>{LB}')
            assert row['english'].count('{LB}') == 1
        else:
            assert row['id'] == 'DK4_MES_B143_R0033'
            assert row['english'] == '...{LB}...{LB}...'
            assert row['source_Japanese'].count('\n') == 2
        encoded = bytes.fromhex(plan['encoded_hex'])
        assert encoded[0] == row['source_selector'] and b'{LB}' not in encoded
        assert encoded.count(b'\n') == row['english'].count('{LB}')
        assert plan['expected_native_pages'] == 1
        warnings = {i['code'] for i in plan['unmodified_base_QA']['issues'] if i['severity'] == 'warning'}
        assert warnings == set(row['qa_waivers']) <= {'manual-break', 'orphan-final-line'}
        assert not any(i['severity'] == 'error' for i in plan['unmodified_base_QA']['issues'])
    assert count == 13


source = checked_text(previous.source, {
    '    doc,plans,source,macros=map(load,[args.manuscript,args.plan,SOURCE,MACROS])':
    '    doc,plans,source,macros=map(load,[args.manuscript,args.plan,SOURCE,MACROS])\n    validate_documented_layouts(doc,plans)',
    "logical=row['english'].replace('{MACRO:FI}','Hodram')":
    "logical=row['english'].replace('{LB}',' ').replace('{MACRO:FI}','Hodram')",
    '        FE_factory_calibration=calibration,':
    '        source_qualified_structural_or_dramatic_layouts=13,ordinary_wraps_remain_formatter_owned=True,FE_factory_calibration=calibration,',
})
exec(compile(source, __file__ + '::same-native-checks-source-qualified-break-semantics', 'exec'), globals())
