"""Expose B52 English only after complete clean source/context/native binding; reuse exact source CPU proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_current_tools_v8631');assert not root.exists()
    source=Path('scripts/map_Hodram_B49_current_v8387.py').read_text(encoding='utf-8')
    a=source.index("    for a,b in zip(source['commands'],commands,strict=True):",source.index('    rows=[];dispatches=[]'))
    b=source.index('    assert len(rows)==14',a)
    branches="""    for a,b in zip(source['commands'],commands,strict=True):
        if a['word'] in [0x100,0x200,0x300,0x400]:
            relative_cases.append(dict(version='source-reused-exact-code',**next(c for c in controls['source_relative_cases'] if c['offset']==a['offset'])))
            relative_cases.append(dict(version='current',**ctx.execute(native_skip,block,b)));ctx.machines.pop()
    for original in source['records']:
        previous=next(r for r in display['records'] if r['id']==original['id'])
        assert previous['source_hex']==original['source_hex'] and previous['complete_source_preamble_hex']==original['source_complete_preamble_hex']
        dispatches.append(dict(id=original['id'],version='source-Japanese-reused-exact-own8609-context',**deepcopy(previous['original_dispatch'])))
    for row in menu['records']:
        sr,cr=row['source_reference'],row['current_reference'];si=clean[:sr['offset']].count(bytes([0]));ci=block[:cr['offset']].count(bytes([0]))
        row.update(previous_inventory_alias=row['id'],id=f'DK4_MES_B52_R{si:04d}',source_record_index=si,current_record_index=ci,kind='typed-choice',source_kind='typed-choice',source_typed_command_hex=menu['source_command']['whole_command_hex'],current_typed_command_hex=menu['current_command']['whole_command_hex'],source_choice_command_offset=sr['command_offset'],current_choice_command_offset=cr['command_offset'],current_raw_storage_English=row['current_English'],current_effective_paragraph=' '.join(row['current_English'].split()),current_storage_trailing_ASCII_spaces=len(row['current_English'])-len(row['current_English'].rstrip(' ')),source_prose_orcompletion_credit_added=False)
        sr.update(file_path='/data/SC1.DK4',record_index=si,header_offset=sr['command_offset'],option_index=row['option_index']);cr.update(file_path='/data/SC1.DK4',record_index=ci,header_offset=cr['command_offset'],option_index=row['option_index'])
    from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
    allrows=rows+menu['records'];old=read(ledger);keys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    assert len(allrows)==len({historical_key(r) for r in allrows})==5 and len(keys)==7229 and not keys&{historical_key(r) for r in allrows}
"""
    result=derive('scripts/map_Hodram_B49_current_v8387.py','scripts/map_Hodram_B52_current_v8631.py',{
        source[a:b]:branches,
        'scripts.Hodram_outcomes_registered_route_context_v8380':'scripts.Hodram_B51_registered_route_context_v8612',
        'Hodram_B49_current_v8387':'Hodram_B52_current_v8631',
        'work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json':'work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json',
        'Hodram_B49_source_display_v8386b':'Hodram_B52_source_display_v8626',
        'work/analysis/Hodram_B49_source_view_v8386c/source_view.json':'work/analysis/Hodram_B52_source_names_v8630/three_source_pages_role_andHayreddin_component_review.json',
        'Hodram_B49_source_controls_v8384':'Hodram_B52_source_controls_v8620',
        'current_V8377_Hodram_native_v8380':'current_V8609_Hodram_native_v8612','editorial_handoff_verification_v8383':'editorial_handoff_verification_v8624',
        "verified['completed']==7205":"verified['completed']==7229",
        'all14_clean_utterances_andtwo_choices_glossed_before_current_English':'all3_clean_utterances_andtwo_choices_glossed_before_current_English',
        "display['current_English_dialogue_bodies_unconsulted']":"display['current_B52_English_dialogue_bodies_unconsulted']",
        'current_B49_English_dialogue_bodies_still_unconsulted':'current_B52_English_dialogue_bodies_still_unconsulted',
        "view['all14_source_pages_directly_viewed']":"view['all_three_complete_Japanese_speech_pages_andone_reused_role_plane_directly_viewed']",
        "view['source_native_proof_sha256']":"view['display_sha256']",
        'assert number==49':'assert number==52',
        "len(commands)==len(source['commands'])==36 and len(speeches)==len(source['records'])==14":"len(commands)==len(source['commands'])==14 and len(speeches)==len(source['records'])==3",
        'DK4_MES_B49_CHOICE_':'DK4_MES_B52_CHOICE_','block=49':'block=52',
        'len(relative_maps)==8':'len(relative_maps)==4',
        "for version,value in [('source-Japanese',bytes.fromhex(original['source_hex'])),('current-English',raw)]:":"for version,value in [('current-English',raw)]:",
        '{1:1,2:3}[value[0]]':'{113:0}[value[0]]',
        'template,expanded,result=bodies[1]':'template,expanded,result=bodies[0]',
        'source_native_display_in_prior8300_context_preserved':'source_native_display_in_exact_own8609_context_reused',
        'source_andcurrent_dispatches_fresh_own8377_context':'current_dispatches_fresh_source_dispatches_exact_reuse_own8609_context',
        'len(rows)==14 and len(dispatches)==28 and len(relative_cases)==16 and len(query_cases)==2':'len(rows)==3 and len(dispatches)==6 and len(relative_cases)==8 and len(query_cases)==0',
        'source_native_context_historical8300_not_overlaid_orcalled_current':'source_native_context_exact_own8609_not_overlaid',
        'all28_source_current_dispatches_in_new_own8377_context':'all6_source_current_dispatches_3reused3fresh_own8609_context',
        'all36_commands14_preambles8_relative_targets_two_typed_labels_opaque_effects_andcomplete_end_bound':'all14_commands3_preambles4_relative_targets_two_typed_labels_opaque_effects_andboth_distinct_ends_bound',
        'current_comparison_not_English_editorial_orUI_approval=True':'current_comparison_not_English_editorial_orUI_approval=True,physical_speeches=3,typed_choice_labels=2,total_editorial_objects=5,typed_choices_canonical_clean_record_IDs_bound=True,all5_source_units_uncredited_in_current_ledger=True,source_dispatches_and20_native_relative_cases_reused_not_replayed=True',
        'First complete B49':'First complete B52','fresh own-V8377 dispatches':'fresh own-V8609 current dispatches; exact source proofs reused',
        'Fresh8377:28dispatches/80relative cases/2rawqueries;all36commands/source-current references bound.No editorial approval orcredit.':'Own8609:3fresh current/3reused source dispatches,20fresh current/20reused source relative cases,zeroqueries;all14commands/3speeches/2canonical choices/bothends bound.No editorial approval orcredit.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,first_B52_English_exposure_after_clean_source_gloss_native_pages_names_choice_getters_andVM_paths=True,source_native_calls_reused_by_exact_source_bytes_code_FONT_COMMON_andown8609_context_not_replayed=True,all_source_current_command_maps_preambles_relative_targets_typed_labels_opaque_controls_andboth_end_words_preserved=True,five_disjoint_source_IDs_require_no_prior_coverage_overlap=True,no_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
