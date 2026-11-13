"""Reuse the full-width planner with286 exact bindings, including source-owned Rafael zero prefixes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B37_B50_clean_20261109',
    "doc['physical_speech_objects']==299":"doc['physical_speech_objects']==282",
    "doc['blocks']==list(range(15))+list(range(16,33))":"doc['blocks']==list(range(37,51))",
    '==len(doc[\'records\'])==301':"==len(doc['records'])==286",
    '    bindings=[]':'    bindings=[];zeros=set()',
    '        bindings.append(dict(id=row[\'id\']':"        if raw[0]==0:zeros.add(raw)\n        if raw[0]==254:assert row['kind']=='system-FE' and row['FE_is_not_an_ordinary_actor_nameplate']\n        bindings.append(dict(id=row['id']",
    '    assert len(bindings)==299':'    assert len(bindings)==282',
    '    return set(),bindings':'    assert len(zeros)==sum(r[\'kind\']==\'progressive\' and r[\'source_selector\']==0 for r in doc[\'records\'])\n    return zeros,bindings',
})
exec(compile(source,__file__+'::same-full-width-source-bound-planner-Maria286-withzero-prefix-andFE-membership','exec'),globals())
