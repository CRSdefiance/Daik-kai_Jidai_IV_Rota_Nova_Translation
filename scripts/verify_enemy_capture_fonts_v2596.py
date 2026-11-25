"""Current direct pipelines and208 complete literal-name/CP932 font cases."""
from pathlib import Path
if __name__=='__main__':
 needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})"
 city=Path('scripts/verify_aftermath_city_fonts_v2566.py').read_text();assert city.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(city.replace(needle,'\n captured=source'),__file__,'exec'),env);bridge=env['captured'];a=bridge.index(' rom,oldrom=');b=bridge.index(' ROOT.mkdir(parents=True);',a);bridge=bridge[a:b]
 bridge=bridge.replace('out/all_routes_combined_v1224_candidate.nds','out/all_routes_combined_v1430_candidate.nds').replace('range(2038,2046)','range(2082,2090)')
 outer=Path('scripts/probe_enemy_capture_fonts_v1424.py').read_text();last="    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})";assert outer.count(last)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(last,'    captured=source'),__file__,'exec'),env);source=env['captured']
 source=source.replace('from types import FunctionType','from types import FunctionType,SimpleNamespace\nimport struct\nfrom ndspy.code import MainCodeFile\nfrom unicorn import UC_HOOK_CODE\nfrom dk4tool.patch.refit_contextual_spritsail_v1 import current_entries\nfrom dk4tool.patch.main_pool_cache_visibility import POOL\nfrom dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET\nfrom scripts.probe_escape_direct_source_v1186 import machine\nfrom scripts.probe_reinforcement_sniping_layout_v1030 import native_layout\nfrom scripts.verify_arrival_native_v792 import prepared\nfrom scripts.probe_common_single_cache_v862 import Loader\nfrom scripts.probe_button_prompt_native import BASE')
 source=source.replace('from scripts.probe_battle_aftermath_fonts_v1256 import consumer','from scripts.probe_battle_aftermath_fonts_v1256 import consumer')
 source=source.replace("ROOT = Path('work/analysis/enemy_capture_fonts_v1424')","ROOT = Path('work/analysis/enemy_capture_fonts_v2596')\nROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1430_candidate.nds')")
 source=source.replace("PLAN = Path('work/analysis/enemy_capture_payload_v1423/native_payload_plan.json')","PLAN = ROOT/'current_native_pipeline_plan.json'")
 source=source.replace("DOC = Path('translations/enemy_capture_editorial_manuscript_v2.json')","DOC = Path('translations/enemy_capture_contextual_editorial_manuscript_v1.json')")
 a=source.index('    plan,doc = ');b=source.index('    bound_path = ',a)
 setup=bridge+""" current=rom
 observed=dict(snapshot=context['actual_snapshot'],snapshot_sha256=context['actual_snapshot_sha256'])
 representatives={}
 for choice in context['all208_original_voice_selections']:
  representatives.setdefault(choice['voice_class'],dict(source_voice=choice['voice_class'],actor_object=choice['actor_object'],existing_actor_ID=choice['actor_ID']))
  if choice['actor_ID']==18:representatives[choice['voice_class']]=dict(source_voice=choice['voice_class'],actor_object=choice['actor_object'],existing_actor_ID=choice['actor_ID'])
 assert set(representatives)==set(range(8)) and representatives[0]['existing_actor_ID']==18
 prior=read('work/analysis/enemy_capture_fonts_v1424/native_font_research.json');priorcases={(c['message_ID'],c['variant']):c for c in prior['cases']}
"""
 setup='\n'.join('   '+line if line else ''for line in setup.splitlines())+'\n';source=source[:a]+setup+source[b:]
 source=source.replace('    ROOT.mkdir(parents=True)','    ROOT.mkdir(parents=True)\n    save(PLAN,dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),historical_ROM=str(OLDROM),historical_ROM_sha256=sha(OLDROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_snapshot=context["actual_snapshot"],historical_snapshot_sha256=sha(raw),patches=patches,current_audited_table_gate_entry_exit_extents=audited,current_deployed_payload_delta=delta,no_whole_initialized_RAM_overlay=True,full_goal_complete=False))')
 source=source.replace("native = consumer(arm,common,raw,plan,0x53F0C,source['actor_object'],context['source_table'],name)","native = run(arm,common,raw,plan,0x53F0C,source['actor_object'],context['original_table'],name)\n            assert bytes(last_model['cpu'].mem_read(root,0x1A04))==last_model['before']\n            assert native['parent']==0x02053F40 and native['selector_offset']==0x274 and native['selector']==0x02117B00")
 needle2="            issues = []";extra="""            previous=priorcases[(row['message_id'],index)]
            assert native['formatted_hex']==previous['native_pipeline']['formatted_hex'] and lines==previous['lines'] and sha(bytes(pixels))==previous['whole_native_font_plane_sha256'] and events==previous['complete_native_glyph_events']
""";assert source.count(needle2)==1;source=source.replace(needle2,extra+needle2)
 source=source.replace("'CPU_only_not_original_GPU_or_individual_gameplay_activation':True}","'all_executed_pipeline_instructions_current_ROM_including_deployed_pool':True,'all_actor_models_unchanged_after_complete_pipeline':True,'current_historical_formatted_bytes_lines_full_font_and_glyph_events_equal':True,'CPU_only_not_original_GPU_or_individual_gameplay_activation':True}")
 source=source.replace("save(ROOT/'native_font_research.json'","save(ROOT/'native_font_proof.json'")
 source=source.replace("'manuscript':str(DOC),","'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'manuscript':str(DOC),")
 source=source.replace("'all206_source_existing_actor_choices':context['all206_existing_actor_choices'],","'all208_source_existing_actor_choices':context['all208_original_voice_selections'],")
 source=source.replace("'sheets_for_visual_review':sheets,","'review_sheets':sheets,'all8_complete_native_cases':[c for c in cases if c['variant']==0],'all16_native_cold_warm_copies':[Loader(arm,common).copy(n,entries[n].text,mode)for mode in('cold','warm')for n in range(2082,2090)],'all8_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,'current_parent_projection_controls':0,'current_portrait_consumer_no_Deck_or_duel_projection_claim':True,'complete_native_font_cases':208,'all208_original_direct_named_capture_pipelines':len(cases),'all_executed_pipeline_instructions_current_ROM_byte_exact':True,'no_actor_or_roster_fixture':True,'all_original_actor_models_unchanged':True,'scope':'Current CPU direct53F0C attacker-officer speech with literal one-name printf/macro protection,scoped wrapping,ABI and independent228x64 fonts.26 declared original/length/command-like/CP932 name cases per voice;these are formatting tests,not26 earned game names or208 individual gameplay visits. Existing actors passed directly;no roster changes. Historical RAM receives bounded verified immutable overlays only. UI construction/file success are explicit CPU boundaries;native painter executes separately.',")
 source=source.replace("'visual_review_registered_release_and_original_gameplay_still_pending':True","'visual_review_pending':True")
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
