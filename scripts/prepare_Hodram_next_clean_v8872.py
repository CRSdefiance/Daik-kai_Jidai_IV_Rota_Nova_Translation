"""Queue complete Japanese candidate exchanges while release checks run; no current English or credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_next_clean_tools_v8872');assert not root.exists()
    prior="work/analysis/Hodram_B54_B60_clean_context_v8795/complete_clean_linked_15_37_65_128_142_context_before_B54_B60_English.json"
    inserted="""    previous_context=read('PRIOR_CONTEXT')
    old65=next(g for g in previous_context['groups'] if g['block']==65)
    new65=next(g for g in groups if g['block']==65)
    assert old65['clean_block_hex']==new65['clean_block_hex'] and old65['commands']==new65['commands']
    new65['earlier_clean_linked_context_inventory_reused_by_exact_complete_block']=dict(path='PRIOR_CONTEXT',sha256=sha(Path('PRIOR_CONTEXT').read_bytes()),new_credit=0)
    assert len(groups)==10 and sum(len(g['records']) for g in groups)==224 and not failures
    assert sum(g['completed_coverage_overlap'] for g in groups)==0
    assert not any(c['word']==0x2100 for g in groups for c in g['commands'])
    ROOT.mkdir(parents=True);output=""".replace('PRIOR_CONTEXT',prior)
    result=derive('scripts/inventory_Hodram_next_clean_v8785.py','scripts/inventory_Hodram_next_clean_v8872.py',{
        'Inventory complete clean Hodram B53 andoriginal EV1 context':'Inventory complete clean Hodram B61-B70 andoriginal EV1 context',
        'Hodram_next_clean_v8785':'Hodram_next_clean_v8872',
        'work/analysis/editorial_handoff_verification_v8775/verified_handoff.json':'work/analysis/Hodram_B54_B60_checkpoint_v8861/verified_handoff_v8862.json',
        "ledger['records_editorially_completed']==7234":"ledger['records_editorially_completed']==7237",
        "verified['profile']=='all-routes-unified-v8704'":"ledger['current_integrated_candidate']['profile']=='all-routes-unified-v8778' and verified['candidate_sha256']==ledger['current_integrated_candidate']['sha256']",
        'len(keys)==7234':'len(keys)==7237',
        '[54,55,56,57,58,59,60]':'[61,62,63,64,65,66,67,68,69,70]',
        "    ROOT.mkdir(parents=True);output=":inserted,
        'complete_clean_SC1_B54_B60_EV1_andcoverage_before_current_English.json':'complete_clean_SC1_B61_B70_EV1_andcoverage_before_current_English.json',
    })
    root.mkdir(parents=True);save(root/'source_locked_next_inventory.json',dict(derivation=result,complete_clean_source_only_candidates_not_chronological_scene_selection_ornewreview_credit=True,B65_existing_clean_context_inventory_reused_by_exact_block_andcommand_identity=True,all_speaker_preambles_branches_names_default_macros_native_glyphs_full_context_andactual_activation_still_unapproved=True,no_current_English_body_orROM_opened=True,new_credit=0,full_goal_complete=False))
