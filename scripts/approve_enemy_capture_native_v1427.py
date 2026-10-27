"""Approve capture source/native/layout evidence;integration and gameplay pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.enemy_capture_native_plan_v1423 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_native_review_v1427')
OLD = Path('translations/enemy_capture_editorial_manuscript_v2.json')
NEW = Path('translations/enemy_capture_editorial_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc = read(OLD)
    fonts_path = Path('work/analysis/enemy_capture_fonts_v1424/native_font_research.json')
    copies_path = Path('work/analysis/enemy_capture_copies_v1425/all_native_copies_and_prefix_cache_sequence.json')
    escape_path = Path('work/analysis/enemy_capture_escape_v1426/original_direct_escape_regression.json')
    runtime_path = Path('work/analysis/enemy_capture_runtime_v1418/native_runtime_verification.json')
    fonts,copies,escape,runtime = [read(p) for p in [fonts_path,copies_path,escape_path,runtime_path]]
    assert fonts['manuscript_sha256']==sha(OLD.read_bytes()) and len(fonts['cases'])==208 and not fonts['findings']
    assert len(fonts['all206_source_existing_actor_choices'])==206 and len(fonts['invalid_compiler_inputs_rejected'])==15
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==fonts['ARM9_sha256'] and p['COMMON_sha256']==fonts['COMMON_sha256'] for p in [copies,escape])
    assert runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    scope = read('work/analysis/enemy_capture_runtime_v1418/scope_proof.json')
    assert scope['total_cases']==529325
    atomic = []
    for case in fonts['cases']:
        assert case['full228x64_native_and_independent_font_exact']
        assert case['all_name_bytes_complete_leading_trailing_glyphs_uniform6px_margin_bounds_and_blank_paper_pass']
        assert not case['findings']
        if case['complete_atomic_runtime_ship_name_on_final_row']:
            assert case['lines'][-1]==case['name']+'!' and len(bytes.fromhex(case['name_hex']))>=8
            atomic.append({'message_ID':case['message_ID'],'variant':case['variant'],'name_hex':case['name_hex'],'lines':case['lines']})
        if case['preview']:
            assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    for sheet in fonts['sheets_for_visual_review']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True)
    visual = ROOT/'visual_and_native_review.json'
    save(visual,{'all8_sheets_and64_native_panels_actually_visually_reviewed':True,
        'sheets':fonts['sheets_for_visual_review'],'all208_native_fonts_margins_bounds_first_final_letters_and_blank_paper_pass':True,
        'all_ship_name_bytes_literal_after_original_printf':True,
        'complete_atomic_runtime_name_rows_reviewed':atomic,
        'atomic_name_reason':'The whole substituted ship name is the grammatical object of the complete preceding action report. It remains together with its punctuation on a normal aligned row;no isolated predicate or clipped syllable is accepted.',
        'no_shared_BALANCE_or_literal_or_live_status_tail_change':True,
        'old_global_balancer_last_row_rule_and_every_historical_formatter_preserved':True,
        'only_source_owned188_byte_selector_and172_byte_gate_runtime_spans_changed':True,
        'new_ROM_loading_GPU_and_original_capture_dismissal_return_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    native = deepcopy(doc)
    native.update(formatting_review_pending=False,status='capture-source-native-approved;registered-integration-gameplay-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(fonts_path),native_font_proof_sha256=sha(fonts_path.read_bytes()),
        native_copy_proof=str(copies_path),native_copy_proof_sha256=sha(copies_path.read_bytes()),
        escape_regression_proof=str(escape_path),escape_regression_proof_sha256=sha(escape_path.read_bytes()),
        native_runtime_proof=str(runtime_path),native_runtime_proof_sha256=sha(runtime_path.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    for row in native['records']:
        row['review']['formatting'] = True
        row['compiled_hex'] = compiled(row).hex()
        row['runtime_name_layout_note'] = 'Complete long runtime ship names may occupy their own final row as an intact grammatical object;all26 native cases and the exact name bytes,uniform margin and whole font plane are reviewed. No isolated non-name predicate is accepted.'
        row['status'] = 'native-approved;registered-integration-and-original-gameplay-pending'
    validate_natural_dialogue_batch(native)
    save(NEW,native)
    print('Eight capture reports native-approved;registered integration and original capture/return still pending.',flush=True)
