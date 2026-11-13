"""Prepare exact B203 speech,entry,branch and complete-scene source checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B203_contract_tools_v6014')
if __name__=='__main__':
    assert not ROOT.exists()
    proofs=[derive('scripts/prove_lil_B202_dispatches_v5963.py','scripts/prove_lil_B203_dispatches_v6014.py',{
        'B202':'B203','dispatches_v5963':'dispatches_v6014','source_v5959':'source_v6010','voices_v5960':'voices_v6011',
        'all19_clean_current_complete_context':'all22_clean_current_complete_context',
        'len(cases)==38 and len(leaves)==7':'len(cases)==44 and len(leaves)==9',
        "sum(c['source_selector']==254 for c in cases)==0":"sum(c['source_selector']==254 for c in cases)==2",
        'all19_source_current_dispatches_no_macros_and7_control_leaves':'all22_source_current_dispatches_FI_and9_control_leaves',
        'all7_nonrelative':'all9_nonrelative','all4_static_actors':'all3_static_actors',
        'no_FE_system_objects_or_null_actor_paths_in_source':'one_FE_system_object_uses_original_null_actor_path',
        'Bind38 source/current speech calls and12 exact nonrelative control leaves.':'Bind44 source/current speech calls and9 exact nonrelative control leaves.',
        '38 source/current dispatches pass:four static actors,no FE or FI/FA/FO. All7 nonrelative leaves exact. No native display/gameplay/reviewcredit claim.':'44 source/current dispatches pass:three static actors,one FE FI notice. All9 nonrelative leaves exact. No native display/gameplay/reviewcredit claim.',
    })]
    proofs.append(derive('scripts/prove_lil_B202_entry_v5964.py','scripts/prove_lil_B203_entry_v6015.py',{
        'B202':'B203','entry_v5964':'entry_v6015','source_v5959':'source_v6010','voices_v5960':'voices_v6011',
        'all19_clean_current_complete_context':'all22_clean_current_complete_context','[202]':'[203]',
    }))
    proofs.append(derive('scripts/prove_lil_B202_branches_v5965.py','scripts/prove_lil_B203_branches_v6016.py',{
        'B202':'B203','branches_v5965':'branches_v6016','source_v5959':'source_v6010',
        'all19_clean_current_complete_context':'all22_clean_current_complete_context',
    }))
    proofs.append(derive('scripts/research_lil_B202_source_fixture_v5967.py','scripts/research_lil_B203_source_fixture_v6018.py',{
        'B202':'B203','fixture_v5967':'fixture_v6018','source_v5967':'source_v6018','source_v5959':'source_v6010',
        'all19_clean_current_complete_context':'all22_clean_current_complete_context',
        '.blocks[202]':'.blocks[203]','source_block=202':'source_block=203',
        'len(jp)==588 and end==586':'len(jp)==816 and end==814',
        'len(commands)==35 and len(speeches)==19':'len(commands)==40 and len(speeches)==22',
        "sum(c['word']==0xA000 for c in commands)==6":"sum(c['word']==0xA000 for c in commands)==8",
        'all35_stored_fixture_commands':'all40_stored_fixture_commands',
        'all26_source_commands_plus9_original_initializers_stored':'all31_source_commands_plus9_original_initializers_stored',
        'source_event202_not_naturally_activated':'source_event203_not_naturally_activated',
        'unsolicited-book-handoff/pursuit/glassmaking-title':'cordyceps/medicinal-material-book-offer/1000-to100-negotiation',
        '26 original+9 initializer commands,19 speeches,no predicates':'31 original+9 initializer commands,22 objects,no predicates',
    }))
    proofs.append(derive('scripts/run_lil_B202_source_fixture_v5968.py','scripts/run_lil_B203_source_fixture_v6019.py',{
        'B202':'B203','fixture_v5967':'fixture_v6018','run_v5968':'run_v6019','source_v5968':'source_v6019',
        "selected['source_block']==202":"selected['source_block']==203",'source_event202_not_naturally_selected':'source_event203_not_naturally_selected',
        "'displayed_original_source_block':202":"'displayed_original_source_block':203",'all26_source_commands_retained':'all31_source_commands_retained',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tools.json',dict(tools=proofs,no_new_prose_or_controls_inherited=True,no_ROM_registry_ledger_orcompletion_credit_change=True,full_goal_complete=False))
    print('B20344 dispatches/nine leaves,entry,no-relative-site and full40-command clean fixture tools prepared.')
