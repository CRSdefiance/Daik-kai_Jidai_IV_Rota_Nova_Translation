"""Preserve the rejected assumption; bind Hodram's actual approved Joakim middle field and distinct full getter."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_name_binding_tools_v8386b');assert not root.exists()
    d=derive('scripts/prove_Hodram_B49_source_display_v8386.py','scripts/prove_Hodram_B49_source_display_v8386b.py',{
        'Hodram_B49_source_display_v8386':'Hodram_B49_source_display_v8386b',
        "[['Hodram','Bergstrom',None],['Lil','Argot',None]]":"[['Hodram','Bergstrom','Joakim'],['Lil','Argot',None]]",
        "assert len(getters)==4 and all(r['text']=={1:'Hodram Bergstrom',2:'Lil Argot'}[r['actor_ID']] for r in getters)":"assert len(getters)==4 and [[r['text'] for r in getters if r['actor_ID']==actor] for actor in [1,2]]==[['Hodram Bergstrom','Hodram Joakim Bergstrom'],['Lil Argot','Lil Argot']]",
    })
    root.mkdir(parents=True);save(root/'approved_middle_field_anddistinct_full_getter.json',dict(derivation=d,source_Hodram_fields=['ホドラム','ベルグストロン','ヨアキム'],current_approved_fields=['Hodram','Bergstrom','Joakim'],progressive_name='Hodram Bergstrom',full_catalogue_name='Hodram Joakim Bergstrom',no_new_name_asset_renaming_orbiography=True,old_failed_assertion_andall_previous_name_proofs_preserved=True,new_credit=0,full_goal_complete=False))
