"""Derive the source-locked35-speech compiler without inactive menu/FE gates."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('dk4tool/patch/lil_B131_B133_editorial_v1.py');new=Path('dk4tool/patch/lil_B135_B136_editorial_v1.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'Source/runtime-locked61 speeches including18 actor00 andone two-option menu.':'Source/runtime-locked35 progressive speeches;one predicate andfour relative spans.',
      'lil_B131_B133':'lil_B135_B136','B131-B133':'B135-B136','B131/B133':'B135/B136','[131,133]':'[135,136]',
      "doc,menu=[load(config[k]) for k in ['manuscript','choices']]":"doc=load(config['manuscript']);menu={'records':[]}",
      'for d in [doc,menu]:':'for d in [doc]:',
      "representative.get('individual_selected_B131_B133_visits_not_required_for_reusable_rules')":"representative.get('individual_selected_B135_B136_visits_not_required_for_reusable_rules')",
      "and representative.get('one2100_menu_source_order_indices_geometry_complete_planes_and_selection_cancel_bound') is True\n        and representative.get('source00_full_typed_body_and_static_Rafael_Lil_context_macros_bound') is True":"and representative.get('all35_final_planes140_macros_static_dispatches_and_one_predicate_bound') is True\n        and representative.get('no_FE_choice_pause_source00_dynamic_or4100_scope') is True",
      'actual_selected_B131_B133_IDs':'actual_selected_B135_B136_IDs',
      "len(doc['records'])==len(refs)==61":"len(doc['records'])==len(refs)==35",'61speech coverage':'35speech coverage','len(fonts)==61':'len(fonts)==35','61complete native':'35complete native',
      "len(menu['records'])==len({r['id'] for r in menu['records']})==2":"len(menu['records'])==len({r['id'] for r in menu['records']})==0",
      'sum(expected_commands.values())==112':'sum(expected_commands.values())==61',
      "profile=profile_for(arm,block);fe_profile=profile_for(arm,block,'FE-paper')":"profile=profile_for(arm,block);fe_profile=profile",
      '{0,2,5,9,20,254}':'{2,9,14,36,47,96}',
      "len({r['id'] for r in changes})==63":"len({r['id'] for r in changes})==35",
      'all61_speeches_two_choice_labels24_relative_operands_verified':'all35_speeches4_relative_operands_verified',
      'all18_source00_prefixes_nonempty_bodies_and_no_source2000_verified=True':'no_FE_source00_2100_2000_dynamic_or4100_objects=True',
      'one2100_menu_count_indices01_cancel_and_native_planes_verified=True':'all35_progressive_consumers_and_native_planes_verified=True',
    }
    # Specific replacements precede generic namespace substitutions.
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    a=t.index("    for key in ['all112_");z=t.index("    _require(mapping['original_event_queries']",a)
    t=t[:a]+"""    for key in ['all61_physical_nested_command_boundaries_and4_relative_sites_verified',
        'all20_relocated_relative_skip_cases_preserve_original_targets',
        'all1_relocated_predicate_pair_preserves_source_operands_results_and_unowned_RAM',
        'all35_active_speech_targets_preserved','no_FE_source00_2100_2000_dynamic_or4100_objects',
        'representative_shared_rules_approved']:
        _require(mapping.get(key) is True,'missing reference approval:'+key)
"""+t[z:]
    a=t.index("    FE=load(doc['native_FE_font_proof'])");z=t.index('    refs=',a)
    t=t[:a]+"""    controls=load(doc['relocated_control_proof']);native=load(doc['native_font_proof'])
    _require(controls['all35_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text']
        and controls['all1_predicate_current_relocated_result_and_source_operands_equal']
        and len(controls['relocated_predicate_pairs'])==1 and controls['original_event_queries']==[],
        'relocated static dispatch andpredicate proof required')
    _require(len(native['source_consumer_negative_controls'])==21 and len(native['source_bound_formatter_negatives'])==14
        and all(c['rejected'] for c in native['source_consumer_negative_controls']+native['source_bound_formatter_negatives']),
        'native source andformatter negatives required')
    _require(all(r['source_selector'] in {2,9,14,36,47,96} and r['kind']=='progressive' for r in doc['records']),
        'exact progressive static actor scope required')
    menu_targets={}
"""+t[z:]
    # Prohibit inactive typed object data even when a forged mapping hashes it.
    a="        _require(spec['actor_style_commands']==[],'unexpected actor-style object')"
    assert a in t;t=t.replace(a,a+"\n        _require(spec['choice_commands']==[],'unexpected choice object')")
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B135_B136_compiler_tools_v3370');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),only_exact_35_progressive_static_sources_allowed=True,global_encoder_and_all_previous_profiles_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
