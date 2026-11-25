"""Prepare first existing-English comparison only after the complete clean-source review."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_current_tools_v8799');assert not root.exists()
    source=Path('scripts/map_Hodram_B31_B53_current_v8722.py').read_text('utf-8')
    a=source.index("    assert view['all3_complete");z=source.index('    image=NdsImage.open',a)
    review="""    assert view['all82_source_native_pages_and11_sheets_directly_viewed'] and view['existing_B54_B60_English_dialogue_bodies_still_unconsulted']
    assert view['source_ready_for_current_English_comparison_not_final_localization_orformatting_approval']
    assert gloss['all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English'] and control['source_gloss_sha256']==display['evidence'][str(GLOSS)]==sha(GLOSS.read_bytes())
    assert view['evidence'][DISPLAY.as_posix()]==sha(DISPLAY.read_bytes())
    for sheet in view['viewed_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
"""
    receipt=derive('scripts/map_Hodram_B31_B53_current_v8722.py','scripts/map_Hodram_B54_B60_current_v8799.py',{
        source[a:z]:review,
        'scripts.Hodram_B52_registered_route_context_v8707':'scripts.Hodram_B31_B53_registered_route_context_v8781',
        'Hodram_B31_B53_current_v8722':'Hodram_B54_B60_current_v8799',
        'work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json':'work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json',
        'work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json':'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json',
        'work/analysis/Hodram_B31_B53_source_view_v8721/direct_source_view_andscoped_name_findings.json':'work/analysis/Hodram_B54_B60_source_review_v8798b/source_context_names_display_review_before_current_English.json',
        'work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json',
        'work/analysis/Hodram_B31_actor34_names_v8719/source_names_native_getters_andplanes.json':'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json',
        'current_V8704_Hodram_native_v8707':'current_V8778_Hodram_native_v8781',
        'editorial_handoff_verification_v8716':'editorial_handoff_verification_v8790',
        "verified['completed']==7234":"verified['completed']==7237",
        "names['fresh_actor34_source_voice']['rows']+names['scoped_reused_actor113']['source_voice']":"names['ten_source_selector_voices']['rows']",
        "len(commands)==len(source['commands'])==9":"len(commands)==len(source['commands'])",
        "result=ctx.execute(ns['dispatch'],prefix,raw[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==prefix and result['source_voice_class']==voices[prefix] and not result['FE_original_null_actor_calls']":"result=ctx.execute(ns['dispatch'],prefix,raw[1:]);ctx.machines.pop();is_FE=prefix==254\n            assert result['resolved_actor_ID']==(None if is_FE else prefix) and result['source_voice_class']==(None if is_FE else voices[prefix])\n            assert bool(result['FE_original_null_actor_calls'])==is_FE",
        "if q['kind']=='unexecuted-progressive-body'":"if q['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body')",
        "row.update(kind='progressive',source_kind='progressive'":"row.update(kind='system-FE' if is_FE else 'progressive',source_kind='system-FE' if is_FE else 'progressive'",
        'len(rows)==len(keys)==3 and len(completed)==7234':'len(rows)==len(keys)==82 and len(completed)==7237',
        'len(relative_cases)==4 and len(query_cases)==1':'len(relative_cases)==24 and len(query_cases)==6',
        'all3_source_units_uncredited_in_current_ledger':'all82_source_units_uncredited_in_current_ledger',
        'complete18commands3preambles4relative_targets_query8opaque_controls_andboth_full_ends_bound':'complete152commands82preambles24relative_targets6queries33nonprose_controls_and7normal_ends_bound',
        'source_native_calls_reused_exact_same_own8704_context_not_replayed':'source_native_calls_reused_exact_same_own8778_context_not_replayed',
        'source_names_fullmiddle_finding_remains_open':'Geronimo_Alonso_shared_de_middle_field_finding_remains_open',
        'First current comparison:3fresh dispatches/20relative cases/1unforcedquery;18commands fully mapped':'First current comparison:82fresh dispatches/120relative cases/6unforcedqueries;152commands fully mapped',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_original_complete_source_current_command_mapping_prefix_fields_branch_targets_queries_dispatches_catalogue_effective_templates_anddisjoint_coverage_guards_preserved=True,
        all82_clean_meanings_names_native_pages_FE_andbranch_context_precede_this_first_current_English_read=True,
        FE_null_actor_consumer_bound_without_fallback_actor_orinvented_name=True,
        source_native_calls_reused_byexact_own_current_context_not_replayed=True,no_ROM_orledger_credit_by_preparer=True,full_goal_complete=False))
