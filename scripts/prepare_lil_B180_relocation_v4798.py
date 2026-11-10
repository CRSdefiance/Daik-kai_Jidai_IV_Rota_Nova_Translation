"""Prepare complete conditional B180 relocation and44 stored alignment cases."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_relocation_tools_v4798')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B173_relocation_v4428.py','scripts/research_lil_B180_relocation_v4798.py',{
        'Relocate all11 B173 speeches;preserve four relative sites,predicate,two A000s,eight leaves and one tail end.':
            'Relocate all11 B180 speeches;preserve ten relative sites,two500 RNG predicates,three alternative A000s,C200 and one tail end.',
        'lil_B173_relocation_v4428':'lil_B180_relocation_v4798','lil_B173_editorial_manuscript_v3':'lil_B180_editorial_manuscript_v3',
        'all_routes_combined_v4404':'all_routes_combined_v4766','number==173':'number==180','in [173]':'in [180]',
        '[762] # one complete source tail end preserved':'[572] # one complete source tail end preserved',
        "assert sha(source)==spec['current_block_sha256']":"assert sha(source)==spec['current_block_sha256']\n        assert len(source)==old_end==576\n        assert len(spec['all_current_native_commands'])==28\n        assert sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==11\n        assert sum(c['word']==0x8000 for c in spec['all_current_native_commands'])==2\n        assert sum(c['word']==0xA000 for c in spec['all_current_native_commands'])==3\n        assert sum(c['word']==0xC200 for c in spec['all_current_native_commands'])==1",
        "sum(len(r['relative_skip_fixups']) for r in results)==4":"sum(len(r['relative_skip_fixups']) for r in results)==10",
        "sum(len(r['target_native_skip_cases']) for r in results)==20":"sum(len(r['target_native_skip_cases']) for r in results)==50",
        "sum(len(r['command_map']) for r in results)==23":"sum(len(r['command_map']) for r in results)==28",
        'all11speech_and8_nonrelative_leaves_preserved':'all11speech_and7_nonrelative_leaves_preserved',
        'all4_source_relative_sites_and20_native_skip_cases_preserved':'all10_source_relative_sites_and50_native_skip_cases_preserved',
        'source_FE_system_objects=0':'source_FE_system_objects=1',
        '23structural commands/11speech/noFE/four relative sites/20 target cases,no pause,two A000s/one predicate/one tail end,inversebytes and335otherblocks exact. Researchonly.':
            '28structural commands/11speech/1FE/ten relative sites/50 target cases,no pause,three alternative A000s/two500 RNG predicates/C200/end,inversebytes and335otherblocks exact. Researchonly.'}),
        derive('scripts/prove_lil_B179_stored_v4730.py','scripts/prove_lil_B180_stored_v4799.py',{
            'Verify all14':'Verify all11','lil_B179_stored_v4730':'lil_B180_stored_v4799',
            'lil_B179_editorial_manuscript_v3':'lil_B180_editorial_manuscript_v3',
            'lil_B179_relocation_v4729':'lil_B180_relocation_v4798',
            'from scripts.current_common_native_context_v2677 import CurrentContext':'from scripts.current_build_native_context_v4774 import CurrentContext',
            'from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter':'from scripts.lil_current_font_oracles_v4792 import make_painter,expected_pixels',
            'from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels':'from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster',
            'work/analysis/lil_B179_fonts_v4724/current_native_input.json':'work/analysis/lil_B180_voices_v4775/current_native_input.json',
            'in [92,96,152,254]':'in [166,167,254]','len(cases)==14':'len(cases)==11','fresh+reused==56':'fresh+reused==44',
            'all14_final_stored_targets56_macro_cases':'all11_final_stored_targets44_macro_cases',
            'current_final_stored_macro_alignment_cases=56':'current_final_stored_macro_alignment_cases=44',
            'all14_final_targets':'all11_final_targets',
            'actual_selected_B179_scene_A000_body_and_single_end_reachability_unexecuted':
                'actual_selected_B180_scene_predicates_three_effects_C200_and_end_reachability_unexecuted',
            'stored_targets=14,progressive=13':'stored_targets=11,progressive=10','macro_cases=56':'macro_cases=44'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,block=180,source_logical_stored_bytes=576,
        speeches=11,progressive=10,FE=1,commands=28,relative_sites=10,new_skip_cases=50,
        predicates=2,alternative_A000=3,C200=1,single_end=572,all_stored_alignment_cases=44,
        all_reviewed_prose_preserved=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B180 conditional relocation/inverse and44 stored native alignment cases;no ROM or credit.')
