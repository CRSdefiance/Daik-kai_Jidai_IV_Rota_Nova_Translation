"""Keep the original source/current qualifier andvalidate exact FE child ownership separately."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from scripts import plan_maria328_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B73_B95_clean_20261109')
OWNER = 'DK4_MES_B87_R0139'
env = {'__name__':'qualified_maria328_original_planner','__file__':previous.__file__}
exec(compile(previous.source,previous.__file__+'::unchanged-original328-source-qualifier','exec'),env)
original_qualifier = env['qualify_source']
original_main = env['main']


def qualify_source(doc):
    path = ROOT/'formatting_v1/formatting_input.json'
    assert doc['source_owner_manuscript'] == str(path) and doc['source_owner_manuscript_sha256'] == digest(path)
    source = load(path)
    rejected, bindings = original_qualifier(source)
    assert not rejected and len(bindings) == 313
    assert doc['runtime'] == source['runtime'] and doc['source_full_manuscript'] == source['source_full_manuscript']
    assert doc['source_editorial_objects'] == len(source['records']) == 328
    assert doc['physical_speech_objects'] == 314 and len(doc['records']) == 329
    pagination = doc['pagination_owners']
    assert len(pagination) == 1 and pagination[0]['source_ID'] == OWNER
    pagination = pagination[0]
    originals = {r['id']:r for r in source['records']}
    owner = originals[OWNER]
    assert pagination['unchanged_logical_English'] == owner['english']
    assert pagination['complete_source_preamble_hex'] == owner['source_complete_preamble_hex'] == '0040ffff00fe'
    children = [r for r in doc['records'] if r.get('source_editorial_ID')==OWNER]
    assert len(children) == 2 and [r['native_child_page'] for r in children] == [1,2]
    assert [r['id'] for r in children] == pagination['child_IDs']
    assert [r['english'] for r in children] == pagination['page_segments']
    assert ' '.join(r['english'] for r in children) == owner['english']
    assert all(not any(r['source_macros'].values()) for r in children)
    seen, result = set(), []
    byid = {r['id']:r for r in bindings}
    for row in doc['records']:
        ident = row.get('source_editorial_ID',row['id'])
        original = originals[ident]
        seen.add(ident)
        if ident == OWNER:
            expected = deepcopy(original)
            expected.update(id=row['id'],english=row['english'],planned_English_markup='{SPEAKER:FE}'+row['english'],
                source_editorial_ID=OWNER,native_child_page=row['native_child_page'],native_child_page_count=2,
                source_complete_paragraph=owner['english'],virtual_formatting_child_not_another_source_editorial_record=True,
                prior_macro_normalized_comparison=None)
            assert expected == row and row['source_selector'] == 254 and row['kind'] == 'system-FE'
            assert row['source_complete_paragraph'] == original['english']
            bound = deepcopy(byid[ident])
            bound.update(id=row['id'],source_editorial_ID=ident,virtual_pagination_child_not_new_source_coverage=True)
            result.append(bound)
        else:
            assert row == original
            if ident in byid:
                result.append(deepcopy(byid[ident]))
    assert seen == set(originals) and len(result) == 314
    return set(), result


main = FunctionType(original_main.__code__,{**original_main.__globals__,'qualify_source':qualify_source},
    argdefs=original_main.__defaults__)
if __name__ == '__main__':
    main()
