"""Prepare exact B204 dispatch,entry,branch and complete Japanese scene checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_contract_tools_v6066')
if __name__=='__main__':
    assert not ROOT.exists()
    proofs=[derive('scripts/prove_lil_B203_dispatches_v6014.py','scripts/prove_lil_B204_dispatches_v6066.py',{
        'B203':'B204','dispatches_v6014':'dispatches_v6066','source_v6010':'source_v6062','voices_v6011':'voices_v6063',
        'all22_clean_current_complete_context':'all20_clean_current_complete_context',
        'len(cases)==44 and len(leaves)==9':'len(cases)==40 and len(leaves)==6',
        "sum(c['source_selector']==254 for c in cases)==2":"sum(c['source_selector']==254 for c in cases)==8",
        'all22_source_current_dispatches_FI_and9_control_leaves':'all20_source_current_dispatches_four_FE_letters_no_macros_and6_control_leaves',
        'all9_nonrelative':'all6_nonrelative','all3_static_actors':'all5_static_actors',
        'one_FE_system_object_uses_original_null_actor_path':'four_FE_letter_objects_use_original_null_actor_path',
        'Bind44 source/current speech calls and9 exact nonrelative control leaves.':'Bind40 source/current speech calls and6 exact nonrelative control leaves.',
        '44 source/current dispatches pass:three static actors,one FE FI notice. All9 nonrelative leaves exact. No native display/gameplay/reviewcredit claim.':'40 source/current dispatches pass:five static actors,four FE letters,no macros. All6 nonrelative leaves exact. No native display/gameplay/reviewcredit claim.',
    })]
    proofs.append(derive('scripts/prove_lil_B203_entry_v6015.py','scripts/prove_lil_B204_entry_v6067.py',{
        'B203':'B204','entry_v6015':'entry_v6067','source_v6010':'source_v6062','voices_v6011':'voices_v6063',
        'all22_clean_current_complete_context':'all20_clean_current_complete_context','[203]':'[204]',
    }))
    proofs.append(derive('scripts/prove_lil_B203_branches_v6016.py','scripts/prove_lil_B204_branches_v6068.py',{
        'B203':'B204','branches_v6016':'branches_v6068','source_v6010':'source_v6062',
        'all22_clean_current_complete_context':'all20_clean_current_complete_context',
    }))
    proofs.append(derive('scripts/research_lil_B203_source_fixture_v6018.py','scripts/research_lil_B204_source_fixture_v6070.py',{
        'B203':'B204','fixture_v6018':'fixture_v6070','source_v6018':'source_v6070','source_v6010':'source_v6062',
        'all22_clean_current_complete_context':'all20_clean_current_complete_context',
        '.blocks[203]':'.blocks[204]','source_block=203':'source_block=204',
        'len(jp)==816 and end==814 and jp[end:]==bytes(2)':'len(jp)==end==1312 and jp[end:]==b\'\'',
        'len(commands)==40 and len(speeches)==22':'len(commands)==35 and len(speeches)==20',
        "sum(c['word']==0xA000 for c in commands)==8":"sum(c['word']==0xA000 for c in commands)==5",
        'all40_stored_fixture_commands':'all35_stored_fixture_commands',
        'all31_source_commands_plus9_original_initializers_stored':'all26_source_commands_plus9_original_initializers_stored',
        'source_event203_not_naturally_activated':'source_event204_not_naturally_activated',
        'cordyceps/medicinal-material-book-offer/1000-to100-negotiation':'castle/shachihoko/gift-claim/theft-accusation/four-part-letter',
        '31 original+9 initializer commands,22 objects,no predicates':'26 original+9 initializer commands,20 objects,no predicates',
    }))
    proofs.append(derive('scripts/run_lil_B203_source_fixture_v6019.py','scripts/run_lil_B204_source_fixture_v6071.py',{
        'B203':'B204','fixture_v6018':'fixture_v6070','run_v6019':'run_v6071','source_v6019':'source_v6071',
        "selected['source_block']==203":"selected['source_block']==204",'source_event203_not_naturally_selected':'source_event204_not_naturally_selected',
        "'displayed_original_source_block':203":"'displayed_original_source_block':204",'all31_source_commands_retained':'all26_source_commands_retained',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tools.json',dict(tools=proofs,no_new_prose_or_controls_inherited=True,no_ROM_registry_ledger_orcompletion_credit_change=True,full_goal_complete=False))
    print('B20440 dispatches/six leaves,entry,no-relative-site and full35-command clean fixture tools prepared.')
