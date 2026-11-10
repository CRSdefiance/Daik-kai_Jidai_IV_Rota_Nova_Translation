"""Correct a handoff address transcription from the original saved numeric trace."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_control_correction_v5681b')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/prove_lil_B197_relocated_controls_v5681.py')
    new=Path('scripts/prove_lil_B197_relocated_controls_v5681b.py')
    text=old.read_text(encoding='utf-8')
    changes={
        "ROOT=Path('work/analysis/lil_B197_relocated_controls_v5681')":"ROOT=Path('work/analysis/lil_B197_relocated_controls_v5681b')",
        'BASE+(0x29FEC if word==0x4700 else 0x2A1EC)':'BASE+0x29FEC',
        'assert not before-after and after-before==Counter({0x2A1EC:1})':'assert before==after',
        "bridge[0]['LR']==picture_base.BASE+0x2A1EC":"bridge[0]['LR']==picture_base.BASE+0x29FEC",
        'original_high_instruction_constants_preserved_and_only_original_47xx_return_address_added':'all_original_high_instruction_constants_and_multiplicity_preserved',
        '    # Preserve all old instruction-address constants and add only its separately\n    # source-observed return address. No executable ROM byte is changed.':
        '    # The saved original decimal LR33726444 is0x02029FEC,also used by4700.\n    # All instruction constants and their multiplicity stay exact;no ROM edit.'}
    # Changing the failed TEST's incorrect literal is deliberate. The derived
    # native picture adapter separately requires exact unchanged constants.
    tool=derive(old,new,changes)
    a,b=map(native_numbers,[text,new.read_text(encoding='utf-8')])
    assert a-b==Counter({0x2A1EC:2}) and b-a==Counter({0x29FEC:1})
    proof=Path('work/analysis/lil_B197_controls_v5654/eleven_exact_leaves_five_effect_two47xx_pairs_picture_resource_6003_and_end_cases.json')
    source=read(proof);pairs=[r for r in source['source_A000_and47xx_structural_pairs'] if r['word'] in [0x4720,0x4735]]
    assert len(pairs)==2
    for r in pairs:
        for v in r['versions']:
            b=v['opaque_effect_bridges'];assert len(b)==1 and b[0]['LR']==33726444==0x02029FEC and b[0]['PC']==0x02028A8C
            assert b[0]['args'][1]==r['word']
    ROOT.mkdir(parents=True);save(ROOT/'source_numeric_trace_corrects_handoff_hex_transcription.json',dict(tool=tool,
        source_proof=str(proof),source_return_decimal=33726444,correct_source_return_hex='0x02029FEC',
        superseded_handoff_hex='0x0202A1EC',source_callee_hex='0x02028A8C',entire_word_argument_preserved=True,
        failed5681_stopped_before_output_or_ROM_change=True,failed_producer_and_historical_handoff_preserved=True,
        old_test_removed_high_literals=dict(a-b),new_test_added_high_literals=dict(b-a),
        native_picture_adapter_itself_must_keep_all_original_instruction_constants_exact=True,
        new_credit=0,full_goal_complete=False))
