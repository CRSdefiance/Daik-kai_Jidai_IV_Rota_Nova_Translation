"""Bind every retained name field and manuscript speaker to the measured consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_atomic_name_tools_v6485b')
if __name__=='__main__':
    assert not ROOT.exists()
    extra="""    fields=load(names['source_name_fields'])['source_name_fields']
    require(names['proper_name_retentions']==[r for r in fields if r['actor_ID'] in [2,11,12]] and names['fallback151_consumer_specific_open_lead']==next(r for r in fields if r['actor_ID']==151),'exact proper/full/additional/fallback name fields')
    require([(r['actor_ID'],r['progressive'],r['catalogue']) for r in names['proper_name_retentions']]==[(2,'Lil Argot','Lil Argot'),(11,'Jam Ludwyan','Jam Jack Ludwyan'),(12,'Yukihisa Shiraki','Yukihisa Genjo Shiraki')],'existing source-bound spellings')
"""
    rows=[derive('dk4tool/patch/lil_B209_editorial_v1.py','dk4tool/patch/lil_B209_editorial_v2.py',{
        'lil_B209_editorial_release_v1.json':'lil_B209_editorial_release_v2.json','dk4-lil-B209-editorial-release-v1':'dk4-lil-B209-editorial-release-v2',
        '    exact(actual,dict(actual_unique_objects=6,':extra+'    exact(actual,dict(actual_unique_objects=6,',
        "        if typed:\n            require(selector==208":"        require(row['speaker']==('Source D0 role1 speaker,automatic original actor voice style '+('/'.join(map(str,row['style_indices']))) if typed else {2:'Lil Argot',11:'Jam Jack Ludwyan',12:'Yukihisa Genjo Shiraki'}.get(selector)),'source-mapped speaker label:'+ident)\n        if typed:\n            require(selector==208",
    })]
    rows.append(derive('scripts/validate_lil_B209_atomic_v6485.py','scripts/validate_lil_B209_atomic_v6485b.py',{'lil_B209_editorial_v1':'lil_B209_editorial_v2','dk4-lil-B209-editorial-release-v1':'dk4-lil-B209-editorial-release-v2','lil_B209_atomic_v6485':'lil_B209_atomic_v6485b'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derived=rows,all_native_instruction_constants_preserved=True,full_goal_complete=False));print('Source-locked B209 name/speaker guards prepared;v1 positive proof retained.')
