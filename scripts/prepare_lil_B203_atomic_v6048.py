"""Prepare whole-image positive reconstruction and semantic mutation rejection checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    proof=derive('scripts/validate_lil_B202_atomic_v5996d.py','scripts/validate_lil_B203_atomic_v6048.py',{
        'B202':'B203','lil_B202_editorial_v4':'lil_B203_editorial_v1',
        'seal_lil_B202_references_v5994b':'seal_lil_B203_references_v6046','prepare_lil_B202_references_v5982':'prepare_lil_B203_references_v6034',
        'atomic_v5996d':'atomic_v6048','reference_approval_v5994b':'reference_approval_v6046','verification_v5981':'verification_v6033',
        "len(proof['changed_records'])==19":"len(proof['changed_records'])==22",'Positive19-object':'Positive22-object','positive_records=19':'positive_records=22','Atomic19-object':'Atomic22-object',
        'english=\'{SPEAKER:9D}{MACRO:FI}\'':'english=\'{SPEAKER:4C}{MACRO:FI}\'',
        'research_logical_end=580':'research_logical_end=770','source_bytes=586':'source_bytes=814',
        'actual_unique_speech_panels=18':'actual_unique_speech_panels=21','all7_source_current_target_control_leaves':'all9_source_current_target_control_leaves',
        "{'157':'Retainer'}":"{'170':'Doctor'}","{'18':'Charles Jean Rochefort'}":"{'76':'Mikhail Volk Letzel'}",
        'wrong-spoken-title':'wrong-existing-item-title','source_item14':'source_item18','fresh4_actor_names':'fresh3_actor_names',
        'all19_five_gates_approved':'all22_five_gates_approved',
        "('lost-RNG-witness',doc['postscene_native_state_proof'],lambda v:v['within_scene_RNG_differences'].pop())":"('invented-RNG-witness',doc['postscene_native_state_proof'],lambda v:v['within_scene_RNG_differences'].append({'source_offset':8}))",
        "('claimed-equal-PRNG',doc['postscene_native_state_proof'],lambda v:v.update(final_PRNG_equal=True))":"('lost-measured-PRNG-equality',doc['postscene_native_state_proof'],lambda v:v.update(final_PRNG_equal=False))",
        "    for gate in doc['records'][0]['review']:":'''    mutations += [
      ('lost-original-FI',DOC,lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english=next(r for r in v['records'] if r['kind']=='system-FE')['english'].replace('{MACRO:FI}','Lil'))),
      ('duplicated-original-FI',DOC,lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english=next(r for r in v['records'] if r['kind']=='system-FE')['english']+'{MACRO:FI}')),
      ('FE-as-progressive',DOC,lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(kind='progressive')),
      ('wrong-FE-native-consumer',DOC,lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(native_display_consumer='original_progressive_54020')),
      ('wrong-source-alignment-tail',MAP,lambda v:v['blocks'][0].update(source_alignment_tail_bytes=0)),
      ('invented-target-alignment-tail',MAP,lambda v:v['blocks'][0].update(target_alignment_tail_bytes=2)),
      ('lost-generated-acquisition-observation',PROOFS['representative_proof'],lambda v:v.update(generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350=False))]
    for gate in doc['records'][0]['review']:''',
    })
    root=Path('work/analysis/lil_B203_atomic_tools_v6048');root.mkdir(parents=True);save(root/'derivation.json',proof)
