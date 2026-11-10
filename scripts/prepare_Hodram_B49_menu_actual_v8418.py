"""Bind original menu backing/view/glyph checks to four B49 bounded-tail captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_menu_tools_v8418');assert not root.exists()
    source=Path('scripts/audit_Rafael_B46_menu_v7950c.py').read_text('utf8')
    old="""        flow=read('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
        native_rect=(flow['source_menu_versions'][0]['native_VM'] if version=='clean_Japanese' else choices['native_target_VM'])['native_menu_rectangle']"""
    new="""        menu_version='clean-Japanese' if version=='clean_Japanese' else 'reviewed-stored-English'
        native_rect=next(v for v in choices['versions'] if v['version']==menu_version)['cases'][0]['native_VM']['native_menu_rectangle']"""
    result=derive('scripts/audit_Rafael_B46_menu_v7950c.py','scripts/audit_Hodram_B49_menu_v8418.py',{
        'Hodram_B49_not_present':'unused',
    } if False else {
        'Rafael_B46_menu_actual_v7950c':'Hodram_B49_menu_actual_v8418',
        'work/analysis/Rafael_B46_actual_v7948/four_runs24_unique_speeches58_occurrences_two_choices_actual_body_name_FE_return_audit.json':'work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json',
        'work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json':'work/analysis/Hodram_B49_menu_v8400/menu_provider_and_planes.json',
        'work/analysis/Rafael_B46_scene_runs_v7945':'work/analysis/Hodram_B49_tail_runs_v8416',
        "f'route0_{version}_{choice}'":"f'route1_{version}_{choice}'",
        '2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a':'12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b',
        "width=84 if version=='clean_Japanese' else 66":"width=60",
        old:new,
        "        pointers={r['backing_pointer'] for r in owner['rows']};assert len(pointers)==1;pointer=next(iter(pointers))":"        active_owner_rows=[r for r in owner['rows'] if g['actual_menu_pair']['start']<=r['frame']<=g['actual_menu_pair']['returned']]\n        excluded_owner_rows=[r for r in owner['rows'] if r not in active_owner_rows]\n        assert active_owner_rows and all(r['context_words'][3]==84 and r['text']=='All right.' and r['frame']>g['normal_return']['frame'] for r in excluded_owner_rows)\n        pointers={r['backing_pointer'] for r in active_owner_rows};assert len(pointers)==1;pointer=next(iter(pointers))",
        "        for r in owner['rows']:":"        for r in active_owner_rows:",
        '[4810,4870,4930]':'[4310,4370,4430]',
        'frame>4905':'frame>4355',
        "    assert off==[dict(version='clean_Japanese',choice='accept',frame=4930,logical_selected_option=0)]":"    assert off==[]",
        'original_source84_target66_constructor_widths_and256x36_backing_confirmed':'original_source60_target60_constructor_widths_and256x36_backing_confirmed',
        'owner_observation=str(op),owner_observation_sha256=sha(op.read_bytes()),caption_owner_bindings=style_rows,':'owner_observation=str(op),owner_observation_sha256=sha(op.read_bytes()),caption_owner_bindings=style_rows,all_owner_rows=owner[\'rows\'],excluded_later_nonB49_Allright_caption_rows=excluded_owner_rows,original_B49_menu_interval_filters_identical_word_in_later_sailing_menu=True,',
        'One source4930 highlight-off sample retained,not phase equality.':'All12 sampled selected highlights visible;later sailing-menu All right. owner rows retained separately.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_native_high_integer_constants_andmultiplicity_preserved=True,owned_caption_views_exact_not_unowned_bitmap_blank_claim=True,actual_B49_interval_disambiguates_same_Allright_word_in_later_original_sailing_menu=True,all_owner_rows_retained_with_later_rows_explicit=True,no_emulator_replay_orstate_font_glyph_guard_orinput_change=True,new_credit=0,full_goal_complete=False))
