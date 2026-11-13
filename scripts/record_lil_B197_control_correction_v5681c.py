"""Finish the address-correction receipt after a stopped variable-shadowing serialization."""
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_control_correction_v5681c')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/prove_lil_B197_relocated_controls_v5681.py');new=Path('scripts/prove_lil_B197_relocated_controls_v5681b.py')
    before,after=[native_numbers(p.read_text(encoding='utf-8')) for p in [old,new]]
    assert before-after==Counter({0x2A1EC:2}) and after-before==Counter({0x29FEC:1})
    proof=Path('work/analysis/lil_B197_controls_v5654/eleven_exact_leaves_five_effect_two47xx_pairs_picture_resource_6003_and_end_cases.json')
    pairs=[r for r in read(proof)['source_A000_and47xx_structural_pairs'] if r['word'] in [0x4720,0x4735]]
    assert len(pairs)==2
    for row in pairs:
        for version in row['versions']:
            calls=version['opaque_effect_bridges'];assert len(calls)==1 and calls[0]['LR']==33726444==0x02029FEC and calls[0]['PC']==0x02028A8C
            assert calls[0]['args'][1]==row['word']
    ROOT.mkdir(parents=True);save(ROOT/'source_trace_address_correction_and_stopped_receipt_preserved.json',dict(
        old_test=str(old),old_test_sha256=sha(old.read_bytes()),corrected_test=str(new),corrected_test_sha256=sha(new.read_bytes()),
        source_proof=str(proof),source_proof_sha256=sha(proof.read_bytes()),
        source_return_decimal=33726444,correct_source_return_hex='0x02029FEC',superseded_handoff_hex='0x0202A1EC',source_callee_hex='0x02028A8C',
        old_test_removed_high_literals=dict(before-after),new_test_added_high_literals=dict(after-before),
        native_picture_adapter_itself_must_keep_all_original_instruction_constants_exact=True,
        original5681_stopped_before_output_or_ROM_change=True,
        corrector5681b_derived_test_and_passed_source_assertions_then_stopped_serializing_shadowed_Counter=True,
        all_stopped_producers_and_partial_directory_preserved=True,new_credit=0,full_goal_complete=False))
