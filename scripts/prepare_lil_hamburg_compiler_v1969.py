"""Generate the guarded B74 compiler with exact separate FE/progressive scope."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

SOURCE = Path('dk4tool/patch/lil_speyer_editorial.py')
SOURCE_SHA = '10cbb86b51c0828b42f58e50b399dc91d65bcacaa0dd5993121c54da0922a344'
OUT = Path('dk4tool/patch/lil_hamburg_editorial.py')
ROOT = Path('work/analysis/lil_Hamburg_compiler_v1969')

if __name__ == '__main__':
    assert not OUT.exists() and not ROOT.exists() and sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'Source/runtime-bound B25/B128 Speyer prose and typed-choice relocation layer.':'Source/runtime-bound B74 Hamburg progressive/FE prose and typed-choice layer.',
        'from pathlib import Path':'from itertools import pairwise\nfrom pathlib import Path',
        'from dk4tool.dialogue.lil_speyer_profile import profile_for':'from dk4tool.dialogue.lil_hamburg_profile import profile_for',
        'translations/lil_speyer_editorial_release_v1.json':'translations/lil_hamburg_editorial_release_v1.json',
        'Lil Speyer ':'Lil Hamburg ',
        'dk4-lil-speyer-editorial-release-v1':'dk4-lil-hamburg-editorial-release-v1',
        'dk4-lil-speyer-source-relocation-map-v1':'dk4-lil-hamburg-source-relocation-map-v1',
        'all137_nested_command_boundaries_and48_relative_sites_verified':'all123_nested_command_boundaries_and20_relative_sites_verified',
        'all240_relocated_relative_skip_cases_preserve_original_targets':'all100_relocated_relative_skip_cases_preserve_original_targets',
        'all51_activated_revised_speeches102_holds_complete_native_independent_actual_glyphs':'all79_activated_revised_speeches158_holds_complete_native_independent_actual_glyphs',
        'same107_original_B128_commands_results_and_event_transitions':'same116_original_B74_commands_results_and_event_transitions',
        'normal_docking_Port_action_B128_entry_and_Hamburg_return_not_overridden':'normal_docking_B74_entry_and_Hamburg_return_not_overridden',
        'representative51_speech102_holds_and_two_choice_labels_approved':'representative79_speech158_holds_and_two_choice_labels_approved',
        'len(refs)==57':'len(refs)==79',
        'exhaustive57 speech coverage differs':'exhaustive79 speech coverage differs',
        '[25,128]':'[74]',
        'exact two-block reference map required':'exact B74 reference map required',
        'profile=profile_for(arm,block)':'profile=profile_for(arm,block)\n        fe_profile=profile_for(arm,block,\'FE-paper\')',
        "row.get('native_display_consumer')=='original_progressive_54020'":
            "row.get('native_display_consumer')==('original_FE_modal_5473C_mode1' if raw[:1]==b'\\xfe' else 'original_progressive_54020')",
        'complete original progressive preamble differs:':'complete original display preamble differs:',
        "compiled=encode_relocatable_dialogue(raw,row['english'],profile)":
            "compiled=encode_relocatable_dialogue(raw,row['english'],fe_profile if raw[:1]==b'\\xfe' else profile)",
        'zip(patches,patches[1:])':'pairwise(patches)',
        '(15 if number==25 else 122)':'123',
        '(8 if number==25 else 40)':'20',
        'len(changes)==59':'len(changes)==81',
        'only_SC2_blocks25_and128_changed':'only_SC2_block74_changed',
        'all334_other_SC2_blocks_unchanged':'all335_other_SC2_blocks_unchanged',
        'all57_speeches_two_choices_and48_relative_operands_verified':'all79_speeches_two_choices_and20_relative_operands_verified',
    }
    for old,new in changes.items():
        count = 2 if old == '[25,128]' else 1
        assert text.count(old) == count,(old,text.count(old))
        text = text.replace(old,new)
    anchor = "        and actual.get('all_readonly_observer_boundaries_and_host_restoration_pass') is True,"
    addition = """        and actual.get('all3_FE_panels_six_actual_holds_match_separate_paper_planes') is True
        and actual.get('original_join_command_and_complete_bottom_screen_ink_preserved') is True
"""
    assert text.count(anchor) == 1
    text = text.replace(anchor,addition+anchor)
    compile(text,str(OUT),'exec')
    ROOT.mkdir(parents=True)
    OUT.write_text(text,encoding='utf-8')
    save(ROOT/'compiler_provenance.json',dict(source=str(SOURCE),source_sha256=SOURCE_SHA,
        compiler=str(OUT),compiler_sha256=sha(OUT.read_bytes()),
        exact_scope='SC2 B74;79 speeches,two labels,123 commands,20 relative spans;separate FE consumer',
        all_guards_before_sole_image_mutation=True,registered_config_not_yet_created=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(compiler=str(OUT),sha256=sha(OUT.read_bytes()),registered_config_pending=True))
