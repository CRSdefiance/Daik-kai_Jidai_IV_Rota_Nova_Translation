"""Attach already approved typed-object metadata and prepare exact B201 relocation checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_relocation_tools_v5930')

if __name__=='__main__':
    assert not ROOT.exists()
    prior=read('work/analysis/editorial_handoff_verification_v5927/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    registry=read('translations/release_stack.json');assert registry['profiles'][prior['profile']]['status']=='experimental' and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    approval=read('work/analysis/lil_B201_native_approval_v5925/all26_source_prose_current_native_approval.json');assert approval['all26_five_gates_approved']
    oldd=Path('translations/lil_B201_editorial_manuscript_v5.json');oldm=Path('translations/lil_B201_choice_manuscript_v2.json')
    newd=Path('translations/lil_B201_editorial_manuscript_v6.json');newm=Path('translations/lil_B201_choice_manuscript_v3.json')
    assert not newd.exists() and not newm.exists();doc,menu=map(read,[oldd,oldm]);d,m=deepcopy(doc),deepcopy(menu)
    summary=Path('work/analysis/lil_B201_choices_v5924/all1_typed_menu_native_proof.json');mp=read(summary);assert len(mp['menus'])==1
    proof=read(mp['menus'][0]['proof']);assert proof['six_original_VM_selection_and_cancel_cases_pass'] and proof['eight_complete_native_style_label_planes_pass']
    for row in m['records']:
        row['typed_target_object_hex']=proof['typed_target_object_hex'];row['typed_choice_proof']=mp['menus'][0]['proof']
        row['typed_choice_proof_sha256']=sha(Path(row['typed_choice_proof']).read_bytes())
    m.update(typed_choice_proof=str(summary),typed_choice_proof_sha256=sha(summary.read_bytes()),previous_manuscript=str(oldm),previous_manuscript_sha256=sha(oldm.read_bytes()),
        metadata_only_typed_target_object_attached_no_words_or_native_gates_changed=True)
    save(newm,m);d.update(typed_choice_manuscript=str(newm),typed_choice_manuscript_sha256=sha(newm.read_bytes()),previous_manuscript=str(oldd),previous_manuscript_sha256=sha(oldd.read_bytes()),
        metadata_only_choice_reference_update_no_words_or_native_gates_changed=True)
    assert d['records']==doc['records'] and all(a['english']==b['english'] and a['review']==b['review'] for a,b in zip(m['records'],menu['records'],strict=True))
    save(newd,d)
    tools=[derive('scripts/research_lil_B196_relocation_v5615.py','scripts/research_lil_B201_relocation_v5931.py',{
        'B196':'B201','relocation_v5615':'relocation_v5931','editorial_manuscript_v3.json':'editorial_manuscript_v6.json',
        'choice_manuscript_v2.json':'choice_manuscript_v3.json','combined_v5580':'combined_v5891',
        'number==196 and len(end_maps)==7':'number==201 and len(end_maps)==1',
        "        assert all(a['target_offset']+4<b['target_offset'] for a,b in zip(end_maps,end_maps[1:])) # six purchases and final refusal have distinct ends":
        "        assert end_maps[0]['source_offset']==1448 # original shared end after both choice branches",
        'assert source[old_end:]==bytes(2)':'assert source[old_end:]==bytes(0)',
        'inverse_plus_original_two_tailzeros':'inverse_plus_original_zero_tailzeros',
        "choice_commands']) for r in results)==6":"choice_commands']) for r in results)==1",
        "relative_skip_fixups']) for r in results)==52":"relative_skip_fixups']) for r in results)==4",
        "target_native_skip_cases']) for r in results)==260":"target_native_skip_cases']) for r in results)==20",
        "command_map']) for r in results)==119":"command_map']) for r in results)==44",'in [196]':'in [201]',
        'six_original2100_objects_twelve_source_ordered_buy_refusal_labels':'one_original2100_object_two_source_ordered_buy_refusal_labels',
        'all24speech_six_menus_and52_relative_operands':'all24speech_one_menu_and4_relative_operands','all260_relocated':'all20_relocated',
        'source_FE_system_objects=1':'source_FE_system_objects=3','seven_separated_declared_purchase_refusal_end_words_exact':'single_original_shared_declared_end_word_exact',
        '119commands/24speech/six2100/52spans/260targetskipcases,seven separated ends,all1816 source bytes inverse and335otherblocks exact.':
        '44commands/24speech/one2100/fourspans/20targetskipcases,one shared end,all1452 predecessor bytes inverse and335otherblocks exact.'})]
    tools.append(derive('scripts/prove_lil_B200_stored_v5852.py','scripts/prove_lil_B201_stored_v5932.py',{
        'B200':'B201','all19':'all24','stored_v5852':'stored_v5932','editorial_manuscript_v4.json':'editorial_manuscript_v6.json',
        'relocation_v5851':'relocation_v5931','voices_v5827':'voices_v5903','lil_current_font_oracles_v4792':'lil_current_font_oracles_v5918',
        '[19,172,254]':'[2,19,105,254]','len(cases)==19':'len(cases)==24','fresh+reused==76':'fresh+reused==96',
        'targets76_macro':'targets96_macro','current_final_stored_macro_alignment_cases=76':'current_final_stored_macro_alignment_cases=96',
        'stored_targets=19,progressive=17,FE=2,macro_cases=76':'stored_targets=24,progressive=21,FE=3,macro_cases=96'}))
    tools.append(derive('scripts/prove_lil_B196_stored_choices_v5617.py','scripts/prove_lil_B201_stored_choices_v5933.py',{
        'B196':'B201','stored_choices_v5617':'stored_choices_v5933','relocation_v5615':'relocation_v5931','choice_manuscript_v2.json':'choice_manuscript_v3.json',
        "block['block']==196":"block['block']==201","len(block['choice_commands'])==6 and len(doc['records'])==12":"len(block['choice_commands'])==1 and len(doc['records'])==2",
        'geometry_and48_style_planes':'geometry_and8_style_planes','six_final_typed_objects_twelve_references':'one_final_typed_object_two_references',
        'fresh_count_calls=12,fresh_label_pointer_calls=24,reused_native_selection_cancel_cases=36,reused_complete_current_reviewed_style_planes=48':
        'fresh_count_calls=2,fresh_label_pointer_calls=4,reused_native_selection_cancel_cases=6,reused_complete_current_reviewed_style_planes=8',
        'all_six_stored_objects_and_twelve_actual_offsets':'one_stored_object_and_two_actual_offsets',
        'All six stored menus/twelve label references':'One stored menu/two label references','36 selection/cancel cases and48 style planes':'six selection/cancel cases andeight style planes'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_metadata_and_frozen_relocation_tools.json',dict(tools=tools,manuscript=str(newd),choices=str(newm),
        prior_verified_checkpoint='work/analysis/editorial_handoff_verification_v5927/verified_handoff.json',previous_goal_turn_classification='progress',
        unchanged24_speech_words_two_choice_words_source_context_and_five_native_gates=True,
        exact_source44_commands_24_speeches_one2100_four_relative_sites_one_end_no_tailzeros=True,
        no_ROM_registry_ledger_or_completion_credit_change=True,full_goal_complete=False))
    print('B201 metadata-only successors and exact44-command relocation/stored-speech/menu checks prepared;prior progress verified.')
