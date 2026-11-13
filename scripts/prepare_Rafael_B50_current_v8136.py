"""Prepare first B50 English comparison after complete clean source, callback, title and macro review."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_current_tools_v8136')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/map_Rafael_B49_current_v8086.py').read_text('utf8')
    guard=source[source.index("    assert read(gloss['source_gloss'])"):source.index('    current=NdsImage',source.index("    assert read(gloss['source_gloss'])"))]
    newguard="""    assert read(gloss['first_source_gloss'])['source_packet_sha256']==sha(SOURCE.read_bytes()) and names['source_gloss_sha256']==gloss['first_source_gloss_sha256']
    assert gloss['all28_current_B50_English_bodies_still_unread'] and names['current_English_B50_bodies_still_unread']
    controls=read('work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json')
    assert controls['source_packet_sha256']==sha(SOURCE.read_bytes()) and controls['all37_original_commands28_complete_preambles_andseparate_terminal_tail_bound']
"""
    names='Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json'
    a=derive('scripts/map_Rafael_B49_current_v8086.py','scripts/map_Rafael_B50_current_v8136.py',{
        guard:newguard,
        'Rafael_B49_current_v8086':'Rafael_B50_current_v8136',
        'Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json':'Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json',
        'Rafael_B49_branch_gloss_v8085/61_refined_glosses256_paths_B39_B41_context_before_current_English.json':'Rafael_B50_context_v8135/28_refined_glosses_dye_identity_FA_FI_title_context_before_current_B50_English.json',
        'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json':names,
        'B49':'B50','len(rows)==61':'len(rows)==28','all61_complete_source_current_refs':'all28_complete_source_current_refs','all61_clean_whole_context_glosses':'all28_clean_whole_context_glosses',
        'source_explicit_completion_dependencies=[39],source_explicit_exclusions=[151],source_completion_queries=[41]':'source_explicit_completion_dependencies=[],source_explicit_exclusions=[],source_completion_queries=[]',
        'current_English_dialogue_body_now_exposed=True,current_effective_body_dispatch_andcatalogue_pending=True':'current_English_dialogue_body_now_exposed=True,current_B50_English_body_still_unread=False,current_effective_body_dispatch_andcatalogue_pending=True',
        'after61clean glosses,B39/B41context,names and256native source paths':'after28clean glosses,complete13-speech dye callback,title context,names/macros andnative source entry/end checks',
    })
    b=derive('scripts/prove_Rafael_B49_effective_v8087.py','scripts/prove_Rafael_B50_effective_v8137.py',{
        'Rafael_B49_effective_v8087':'Rafael_B50_effective_v8137',
        'Rafael_B49_current_v8086/all61_complete_source_current_refs':'Rafael_B50_current_v8136/all28_complete_source_current_refs',
        'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json':names,
        'B49':'B50','all61_clean_whole_context_glosses':'all28_clean_whole_context_glosses',
        'len(cases)==122 and len(rows)==61':'len(cases)==56 and len(rows)==28',
        'all61_effective_English_templates122_original_dispatches_no_FE':'all28_effective_English_templates56_original_dispatches_no_FE',
        'all61_progressive_speakers_andvoices_match':'all28_progressive_speakers_andvoices_match',
        'all_seven_static_source_speakers_not_invented_from_incidental_r1':'all_three_static_source_speakers_not_invented_from_incidental_r1',
        'all61_actual_body_name_bounds':'all28_actual_body_name_bounds','122 original dispatches/61 effective templates':'56 original dispatches/28 effective templates',
        'Bind61clean/current B49speeches':'Bind28clean/current B50speeches',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b])
    print('Prepared first B50 current/effective comparison; complete clean source/context preceded this exposure.')
