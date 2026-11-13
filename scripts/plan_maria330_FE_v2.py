"""Qualify both complete FE source owners with the unchanged calibrated planner and native width."""
from copy import deepcopy
import inspect
import linecache
from pathlib import Path
from types import FunctionType
from scripts import plan_maria330_v1 as previous
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

env={'__name__':'qualified_maria330_original_planner','__file__':__file__}
exec(compile(previous.source,__file__+'::unchanged-original330-source-qualifier','exec'),env)
original_qualifier=env['qualify_source'];original_main=env['main']

def qualify_source(doc):
    path=ROOT/'formatting_v1/formatting_input.json';assert doc['source_owner_manuscript']==str(path) and doc['source_owner_manuscript_sha256']==digest(path)
    source=load(path);rejected,bindings=original_qualifier(source)
    assert not rejected and len(bindings)==328 and doc['runtime']==source['runtime']
    assert doc['source_editorial_objects']==len(source['records'])==330 and doc['physical_speech_objects']==330 and len(doc['records'])==332
    originals={r['id']:r for r in source['records']};byid={r['id']:r for r in bindings}
    owners={p['source_ID']:p for p in doc['pagination_owners']}
    assert set(owners)=={'DK4_MES_B116_R0041','DK4_MES_B116_R0051'}
    for ident,p in owners.items():
        owner=originals[ident];children=[r for r in doc['records'] if r.get('source_editorial_ID')==ident]
        assert owner['kind']=='system-FE' and owner['source_complete_preamble_hex']==p['complete_source_preamble_hex']=='0040ffff00fe'
        assert not any(owner['source_macros'].values()) and len(children)==2
        assert [r['native_child_page'] for r in children]==[1,2] and [r['id'] for r in children]==p['child_IDs']
        assert [r['english'] for r in children]==p['page_segments'] and ' '.join(p['page_segments'])==p['unchanged_logical_English']==owner['english']
        assert all(p[k]==owner[k] for k in ['source_reference','current_reference','source_hex','current_hex'])
    seen=set();result=[]
    for row in doc['records']:
        ident=row.get('source_editorial_ID',row['id']);original=originals[ident];seen.add(ident)
        if ident in owners:
            expected=deepcopy(original);expected.update(id=row['id'],english=row['english'],planned_English_markup='{SPEAKER:FE}'+row['english'],
                source_editorial_ID=ident,native_child_page=row['native_child_page'],native_child_page_count=2,
                source_complete_paragraph=original['english'],virtual_formatting_child_not_another_source_editorial_record=True,prior_macro_normalized_comparison=None)
            assert row==expected
            bound=deepcopy(byid[ident]);bound.update(id=row['id'],source_editorial_ID=ident,virtual_pagination_child_not_new_source_coverage=True);result.append(bound)
        else:
            assert row==original
            if ident in byid:result.append(deepcopy(byid[ident]))
    assert seen==set(originals) and len(result)==330
    return set(),result

body=checked_text(inspect.getsource(original_main),{
    "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":"assert row['id']=='DK4_MES_B115_R0035'",
})
filename=__file__+'::same-full-width-planner-two-source-owned-FE-continuations'
linecache.cache[filename]=(len(body),None,body.splitlines(keepends=True),filename)
scope={**original_main.__globals__,'qualify_source':qualify_source,'__file__':__file__}
exec(compile(body,filename,'exec'),scope);main=scope['main']
if __name__=='__main__':main()
