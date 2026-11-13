"""Correct the actual-audit zero-value assumption using the preserved seeded normal-end contract."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_actual_tools_v7752b');assert not root.exists()
    proof=Path('work/analysis/maria_B207_controls_v7686b/Maria_CS0101_50_fresh_seeded_ends_two_exact_isolated_effect_reuses.json');old=read(proof)
    assert NdsImage.open(old['candidate']).read_file('/__arm9__.bin')==NdsImage.open('out/all_routes_combined_v7717_candidate.nds').read_file('/__arm9__.bin')
    assert any(r['native_result']==[0,1,0,0,0,0] and not r['flagged_terminal'] for r in old['normal_terminal_seed_cases'])
    result=derive('scripts/audit_Maria_story_scenes_v7752.py','scripts/audit_Maria_story_scenes_v7752b.py',{
        'maria_story_actual_v7752':'maria_story_actual_v7752b',
        "assert row['result_words']==[0,0];finished=True":
        "assert row['result_words'][0]==0 and len(pairs)>1 and row['result_words'][1]==pairs[-2]['native_result'][1];finished=True",
        "pairs[-1]['native_result']==[0,0]":
        "pairs[-1]['native_result'][0]==0 and pairs[-1]['native_result'][1]==pairs[-2]['native_result'][1]",
        'actual_normal_return_results_all_zero=True':
        'actual_normal_return_type_words_zero_value_words_preserve_previous_decoded_result=True',
    })
    root.mkdir(parents=True);save(root/'source_locked_audit_correction_original_value_carry.json',dict(
        derivation=result,prior_seeded_original_decoder_proof=str(proof),prior_seeded_original_decoder_proof_sha256=sha(proof.read_bytes()),
        identical_whole_ARM9_binds_proof_to_current=True,
        actual_B34_source_andEnglish_normal_terminal_results=[0,1],type0_normal_stop_preserves_preexisting_value_word=True,
        normal_value_word_not_assumed_equal_previous_R3_argument_oran_RNG_seed=True,
        all_other_actual_body_name_gray_branch_extent_andROM_guard_assertions_preserved=True,
        original_failed_audit_script='scripts/audit_Maria_story_scenes_v7752.py',original_partial_audit_directory_preserved=True,
        no_ROM_capture_orcredit_change=True,full_goal_complete=False))
    print('Preserved failed actual7752;successor7752b checks normal type0 plus exact observed preceding value carry.No ROM orcapture rerun.')
