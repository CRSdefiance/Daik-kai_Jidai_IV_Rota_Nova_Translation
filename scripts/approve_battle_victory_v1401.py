"""Approve eight native victory panels;integration/gameplay stay unfinished."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_victory_native_plan_v1396 import compiled
from scripts.ship_sinking_runtime_v1328 import CONTRACTS,TABLE_BYTES,GATE,GATE_BYTES
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_native_review_v1401')
OLD = Path('translations/battle_victory_editorial_manuscript_v1.json')
NEW = Path('translations/battle_victory_editorial_manuscript_v2.json')


if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc = read(OLD)
    fonts_path = Path('work/analysis/battle_victory_fonts_v1397b/native_font_proof.json')
    copies_path = Path('work/analysis/battle_victory_copies_v1399/all_native_copies_and_prefix_cache_sequence.json')
    escape_path = Path('work/analysis/battle_victory_escape_v1400/original_direct_escape_regression.json')
    plan = read('work/analysis/battle_victory_payload_v1396/native_payload_plan.json')
    fonts,copies,escape = [read(p) for p in [fonts_path,copies_path,escape_path]]
    assert fonts['manuscript_sha256']==sha(OLD.read_bytes()) and len(fonts['cases'])==8 and not fonts['findings']
    assert len(fonts['all206_existing_actor_choices'])==206 and len(fonts['invalid_compiler_inputs_rejected'])==14
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(r['ARM9_sha256']==fonts['ARM9_sha256'] and r['COMMON_sha256']==fonts['COMMON_sha256'] for r in [copies,escape])
    assert plan['actual_changed_message_IDs']==[2136,2137]
    target = Path(plan['target_ARM9']).read_bytes()
    source = NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin')
    for address,size in [(CONTRACTS,TABLE_BYTES),(GATE,GATE_BYTES)]:
        at = address-0x02000000
        assert target[at:at+size]==source[at:at+size]
    for case in fonts['cases']:
        assert case['whole228x64_native_and_independent_font_exact'] and len(case['lines'])==1
        assert case['complete_first_final_glyphs_uniform_single_line_margin_bounds_and_blank_paper_pass']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    assert sha(Path(fonts['review_sheet']).read_bytes())==fonts['review_sheet_sha256']
    ROOT.mkdir(parents=True)
    visual = ROOT/'visual_and_native_review.json'
    save(visual,{'all8_native_victory_panels_actually_visually_reviewed':True,
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all_native_fonts_margins_bounds_first_final_letters_and_blank_paper_pass':True,
        'original_one_leading_cell_and_odd_pair_trailing_blank_verified':True,
        'native_font_probe_V1397_assumed_no_pair_padding_V1397b_requires_exact_original_blank':True,
        'no_new_formatter_membership_or_runtime_code_allocation_change':True,
        'entire188_byte_selector_and172_byte_gate_explicitly_exact':True,
        'new_ROM_loading_GPU_and_original_reward_return_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    native = deepcopy(doc)
    native.update(formatting_review_pending=False,status='victory-source-native-approved;registered-integration-gameplay-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(fonts_path),native_font_proof_sha256=sha(fonts_path.read_bytes()),
        native_copy_proof=str(copies_path),native_copy_proof_sha256=sha(copies_path.read_bytes()),
        escape_regression_proof=str(escape_path),escape_regression_proof_sha256=sha(escape_path.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    for row in native['records']:
        row['review']['formatting'] = True
        row['compiled_hex'] = compiled(row).hex()
        row['status'] = 'native-approved;registered-integration-and-original-gameplay-pending'
    validate_natural_dialogue_batch(native)
    save(NEW,native)
    print('Eight victory panels native-approved;runtime/selector unchanged;registered integration and original replay still pending.',flush=True)
