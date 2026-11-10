"""Reuse the native guarded full-width Maria planner for310 exact body bindings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B51_B57_clean_20261109',
    "objects=load(ROOT/'current_objects_v1/current_objects.json')":
        "objects=dict(runtime=current['runtime'],style_records=[],choice_records=[])",
    "doc['physical_speech_objects']==299":"doc['physical_speech_objects']==310",
    "doc['blocks']==list(range(15))+list(range(16,33))":"doc['blocks']==list(range(51,58))",
    "len(bound)==len(original)==len(doc['records'])==301":"len(bound)==len(original)==len(doc['records'])==310",
    "        bindings.append(dict(id=row['id']":
        "        if raw[0]==254:assert row['kind']=='system-FE' and row['FE_is_not_an_ordinary_actor_nameplate']\n        bindings.append(dict(id=row['id']",
    'assert len(bindings)==299':'assert len(bindings)==310',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-width-parity-pagination-andall-source-current-guards310','exec'),globals())
