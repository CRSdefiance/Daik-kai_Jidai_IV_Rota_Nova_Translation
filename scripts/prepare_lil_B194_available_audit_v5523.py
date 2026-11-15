"""Audit observed availability1,all11 panels,FI,resource42,two UI paths and disclosed setup."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/audit_lil_B194_actual_v5517.py', 'scripts/audit_lil_B194_available_v5523.py', {
        'actual_v5517': 'available_actual_v5523', 'display_fixture_v5514': 'available_fixture_v5519',
        'display_run_v5515': 'available_run_v5520', 'display_v5515': 'available_v5520',
        'all30_stored_fixture_commands': 'all31_stored_fixture_commands',
        "len(fixture['all30_stored_fixture_commands'])==30": "len(fixture['all31_stored_fixture_commands'])==31",
        "result=pair['result_words'][1];assert result==0": "result=pair['result_words'][1];assert result==1",
        '==9': '==11', '=9,': '=11,',
        "[r['id'] for r in fixture['original_text_records'] if r['source_selector']!=6]": "[r['id'] for r in fixture['original_text_records']]",
        "predicates[0]['result']==0": "predicates[0]['result']==1",
        "len(ui)==1 and ui[0]['original_source_offset']==534 and ui[0]['result_words']==[3,predicates[-1]['result']]":
        "len(ui)==2 and [r['original_source_offset'] for r in ui]==[494,534] and all(r['result_words']==[3,1] for r in ui)",
        "assert ui[0]['UI_request_after']==[1,2,13,0,2,0,1]  # Source actual resource bodies have advanced request fields4/5.":
        "assert all(r['UI_request_after'][:3]==[1,2,13] and r['UI_request_after'][5:]==[0,1] for r in ui)\n        assert ui[0]['UI_request_after']==ui[1]['UI_request_after']  # Preserve observed fields3/4;no opaque UI meaning or baseline zero-state assumption.",
        "intervals[-1]['returned']<=ui[0]['start']<=ui[0]['returned']<=selected[-1]['start']":
        "intervals[-1]['returned']<=ui[1]['start']<=ui[1]['returned']<=selected[-1]['start'] and ui[0]['returned']<=intervals[-1]['start']",
        'actual_selected9_progressive_FE_availability0_A000_C200_and_single_end':
        'actual_all11_progressive_FE_FI_availability1_resource42_two_C200_and_single_end',
        'all9_selected_speeches8_progressive1_impersonal_FE_observed': 'all11_speeches10_progressive1_impersonal_FE_observed',
        'original_selected_A000_common_C200_and_single_end_executed_without_source_omission':
        'original_selected_A000_resource42_both_C200_and_single_end_executed_without_source_omission',
        "assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event194_not_selected']":
        "assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event194_not_selected']\n        assert rp['disclosed_original_B165_actor6_recruitment_setup'] and rp['earned_recruitment_and_natural_B165_eligibility_not_claimed']",
        "by_at={r['fixture_command_offset']:r for r in fixture['original_text_records']}":
        "by_at={r['fixture_command_offset']:r for r in fixture['original_text_records']}\n        setup=fixture['additional_original_setup_commands'];assert len(setup)==1 and setup[0]['fixture_offset']==56 and setup[0]['whole_command_hex']=='00a0ffff06100120'",
        "if word==0x4000:\n                record=by_at[at]":
        "if at==56:\n                assert word==0xA000 and pair['extent']==8 and block[at:at+8].hex()==setup[0]['whole_command_hex']\n                pair.update(original_setup_source_block=165,original_setup_source_offset=1532,disclosed_original_recruitment_initializer=True)\n            if word==0x4000:\n                record=by_at[at]",
        "elif word==0xA000 and pair.get('original_source_block')==194:effect_offsets.append(pair['original_source_offset'])":
        "elif word==0xA000 and pair.get('original_source_block')==194:effect_offsets.append(pair['original_source_offset'])\n            elif word==0x632A:assert pair['original_source_offset']==406 and pair['result_words']==[3,last] and pair['extent']==2",
        "assert selected[-1]['word']==0":
        "assert len(selected)==30 and sum(r.get('disclosed_original_recruitment_initializer',False) for r in selected)==1\n        assert sum(r['word']==0x632A for r in selected)==1\n        assert selected[-1]['word']==0",
        "assert versions[0]['source_C200'][0]['UI_request_after']==versions[1]['source_C200'][0]['UI_request_after']":
        "assert [r['UI_request_after'] for r in versions[0]['source_C200']]==[r['UI_request_after'] for r in versions[1]['source_C200']]",
    }))
