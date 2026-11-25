"""Correct the guard's human-readable alias separator to the existing measured manuscript label."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_alias_label_tools_v6485c')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B209_editorial_manuscript_v4.json');row=next(r for r in doc['records'] if r['id']=='DK4_VOICE_B209_C8_T104');assert row['style_indices']==[2,7] and row['speaker']=='Source D0 role1 speaker,automatic original actor voice style 2,7'
    rows=[derive('dk4tool/patch/lil_B209_editorial_v2.py','dk4tool/patch/lil_B209_editorial_v3.py',{"'/'.join(map(str,row['style_indices']))":"','.join(map(str,row['style_indices']))",'lil_B209_editorial_release_v2.json':'lil_B209_editorial_release_v3.json','dk4-lil-B209-editorial-release-v2':'dk4-lil-B209-editorial-release-v3'})]
    rows.append(derive('scripts/validate_lil_B209_atomic_v6485b.py','scripts/validate_lil_B209_atomic_v6485c.py',{'lil_B209_editorial_v2':'lil_B209_editorial_v3','dk4-lil-B209-editorial-release-v2':'dk4-lil-B209-editorial-release-v3','lil_B209_atomic_v6485b':'lil_B209_atomic_v6485c'}));ROOT.mkdir(parents=True);save(ROOT/'separator_correction.json',dict(derivations=rows,earlier_v2_rejected_existing_comma_alias_label_before_any_ROM_mutation=True,source_tables_aliases_manuscript_names_prose_and_native_guards_unchanged=True,full_goal_complete=False));print('Guard separator now matches existing style2,7 label;source alias and all native constants unchanged. Earlier rejection preserved.')
