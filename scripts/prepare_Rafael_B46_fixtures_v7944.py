"""Derive complete source/English fixtures retaining every original B46 command and both choices."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_fixture_tools_v7944');assert not root.exists()
    menus="""        mc=next(c for c in source_commands if c['word']==0x2100);menu_refs=[]
        for r in current['typed_choice_records']:
            i=r['option_index'];base=mc['offset']+6;at=base+struct.unpack_from('<H',selected,mc['offset']+2+2*i)[0]
            label=r['source_Japanese'] if version=='clean_Japanese' else g['choice_commands'][0]['labels'][i]
            value=label.encode('cp932');assert target[at+delta:at+delta+len(value)+1]==value+b'\\0'
            menu_refs.append(dict(id=r['id'],option_index=i,fixture_command_offset=mc['offset']+delta,fixture_label_offset=at+delta,
                source_menu_command_offset=mc['offset'],label=label,label_hex=value.hex(),source_reference=r['source_reference']))
        assert len(menu_refs)==2
"""
    row=derive('scripts/create_Rafael_B45_fixtures_v7892b.py','scripts/create_Rafael_B46_fixtures_v7944.py',{
        'Two complete B45 exchanges behind the source-bound original ten-command Rafael opening prelude.':'Two complete B46 exchanges/all24 speeches/two choices behindthe original ten-command Rafael prelude.',
        'scripts.create_Rafael_B45_reference_v7887':'scripts.create_Rafael_B46_reference_v7941',
        'Rafael_B45_scene_fixtures_v7892':'Rafael_B46_scene_fixtures_v7944',
        'Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B45_reference_census_v7889/all24_commands_five_relative_sites_EV0_entry_shipped_callers.json':'Rafael_B46_reference_census_v7943/all37_commands_four_relative_sites_two_choices_EV0_entry_shipped_callers.json',
        'Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json':'Rafael_B46_relocated_controls_v7940/24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json',
        'Rafael_B45_context_runs_v7867':'Rafael_B45_context_runs_v7913',
        "len(controls['final_dispatches'])==12 and len(refs['all_command_maps'])==24":"len(controls['final_dispatches'])==24 and len(refs['all_command_maps'])==37",
        "out/Rafael_B45_{v}_v7892_RESEARCH_ONLY.nds":"out/Rafael_B46_{v}_v7944_RESEARCH_ONLY.nds",
        "g['block']==cg['block']==45":"g['block']==cg['block']==46",
        'blocks[45]':'blocks[46]',
        '==34 and len(speeches)==len(g[\'text_records\'])==12':'==47 and len(speeches)==len(g[\'text_records\'])==24',
        'original_block=45':'original_block=46',
        'len(texts)==12 and len(objects)==24':'len(texts)==24 and len(objects)==37',
        '        image=NdsImage.open(PARENT)':menus+'        image=NdsImage.open(PARENT)',
        'version=version,source_block=45':'version=version,source_block=46',
        'original_text_records=texts,all_fixture_commands=commands':'original_text_records=texts,original_menu_records=menu_refs,all_fixture_commands=commands',
        'all_five_relative_spans_unchanged_under_constant32_byte_shift':'all_four_relative_spans_unchanged_under_constant32_byte_shift',
        'initialized_Lisbon_background_not_original_Ceuta_event_location':'initialized_opening_entry_not_original_event_location',
        'Rafael B45 complete':'Rafael B46 complete',
        'twelve-speech/24-command exchange with all five original branches':'24-speech/37-command exchange/two choices with all four original relative sites',
        'natural B45/Ceuta activation':'natural B46 activation',
        'all12_source_speeches24_commands_andfive_relative_sites_preserved_in_both_languages':'all24_source_speeches37_commands_two_choices_four_relative_sites_preserved_in_both_languages',
        'only_disclosed_opening_ROM_entry_fixture_not_natural_B45_activation_ororiginal_location':'only_disclosed_opening_ROM_entry_fixture_not_natural_B46_activation_ororiginal_location',
        'original_FE_condition_andunconditional_skips_unchanged':'original_two_choice_control_paths_andunconditional_skips_unchanged',
        'Two pinned B45 source/English fixtures:12 speeches/24 commands/five original relative sites plus the exact ten-command B44 prelude. No condition/state forcing ornatural activation claim.':'Two pinned B46 source/English fixtures:24 speeches/37 commands/two choices/four relative sites plusthe exact ten-command B44 prelude. No condition/state forcing ornatural activation claim.',
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
