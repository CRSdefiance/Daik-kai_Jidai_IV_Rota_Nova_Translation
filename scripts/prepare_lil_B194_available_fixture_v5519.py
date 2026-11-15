"""Use the independently bound original join command, then every B194 source command."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B194_available_tools_v5519')
if __name__ == '__main__':
    assert not ROOT.exists()
    rows = [derive('scripts/research_lil_B194_display_fixture_v5514.py', 'scripts/research_lil_B194_available_fixture_v5519.py', {
        'display_fixture_v5514': 'available_fixture_v5519', 'display_v5514': 'available_v5519',
        "plan,doc=read(PLAN),read(DOC);packet=read(doc['source_context'])":
        "plan,doc=read(PLAN),read(DOC);packet=read(doc['source_context'])\n    binding_path=Path('work/analysis/lil_B194_recruitment_binding_v5518/source_B165_Julio6_recruitment_initializer_disclosed_for_conditional_test.json');binding=read(binding_path)\n    assert binding['candidate_sha256']==doc['current_ROM_sha256'] and binding['decoded_actor']==6 and binding['decoded_join_bit']==1\n    setup=bytes.fromhex(binding['original_command_hex']);assert setup==bytes.fromhex('00a0ffff06100120')",
        'b22[:8]+prelude+bank[194][8:end]': 'b22[:8]+prelude+setup+bank[194][8:end]',
        'len(walk)==30': 'len(walk)==31', "sum(c['word']==0xA000 for c in walk)==5": "sum(c['word']==0xA000 for c in walk)==6",
        "at=command['offset']+first-8": "at=command['offset']+first",
        'all30_stored_fixture_commands': 'all31_stored_fixture_commands',
        'original_B22_prelude_commands=init[:9],selected_original_objects=objects':
        "original_B22_prelude_commands=init[:9],additional_original_setup_commands=[dict(source_block=165,source_offset=1532,fixture_offset=56,word=0xA000,native_extent=8,whole_command_hex=setup.hex())],selected_original_objects=objects",
        "fixtures=fixtures,closing_notice_names_Hangzhou":
        "fixtures=fixtures,original_recruitment_setup_binding=str(binding_path),original_recruitment_setup_binding_sha256=sha(binding_path.read_bytes()),original_setup_effect_body_resource48_and_modal_execute_without_bridge=True,original_B165_earned_recruitment_and_eligibility_not_claimed=True,closing_notice_names_Hangzhou",
        'original_B22_nine_init_commands_including_four_A000s_preserved=True':
        'original_B22_nine_init_commands_including_four_A000s_preserved=True,one_disclosed_source_B165_actor6_join_A000_prepended_after_original_init=True',
        'Paired B194 fixtures retain21 source commands,one unforced actor6 availability predicate,four relative sites,11 stored speeches,one FI,resource42 and two C200 sites.':
        'Paired B194 fixtures retain21 source commands after nine original B22 initializers and one independently bound original Julio recruitment command. Availability and all source effects remain unforced.',
    })]
    rows.append(derive('scripts/run_lil_B194_display_fixture_v5515.py', 'scripts/run_lil_B194_available_fixture_v5520.py', {
        'display_fixture_v5514': 'available_fixture_v5519', 'display_run_v5515': 'available_run_v5520',
        'display_v5515': 'available_v5520',
        "'explicit_B22_entry_ROM_fixture':True": "'explicit_B22_entry_ROM_fixture':True,'disclosed_original_B165_actor6_recruitment_setup':True,'earned_recruitment_and_natural_B165_eligibility_not_claimed':True",
    }))
    rows.append(derive('scripts/pin_lil_B194_display_v5516.py', 'scripts/pin_lil_B194_available_v5521.py', {
        'display_tools_v5516': 'available_tools_v5521', 'display_fixture_v5514': 'available_fixture_v5519',
        'source_commands=21,stored_fixture_commands=30': 'source_commands=21,stored_fixture_commands=31',
        'source_A000=1,prelude_A000=4': 'source_A000=1,prelude_A000=4,disclosed_original_recruitment_setup_A000=1',
        'B194 complete-content paired fixture': 'B194 complete-content paired fixture with disclosed original B165 recruitment setup',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'prepared_tools.json', dict(tools=rows, source_commands=21, stored_fixture_commands=31,
        original_B22_initializers=9, independently_bound_original_B165_join_initializer=1,
        all21_B194_commands_and_original_unforced_predicate_retained=True,
        no_earned_recruitment_natural_scene_eligibility_or_full_route_claim=True,
        new_emulator_runs=0, new_review_credit=0, full_goal_complete=False))
