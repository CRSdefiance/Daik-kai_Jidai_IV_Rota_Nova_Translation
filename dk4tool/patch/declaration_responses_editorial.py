"""Eight source-locked NPC war responses after the full V1520 combined stack."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.declaration_responses_native_plan_v1535b import plan, compiled, IDS, SOURCE_COMMON, SOURCE_ARM
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/declaration_responses_editorial_release_v1.json'


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return owned_entries(common, arm, config['directory_sha256'])


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-NPC-declaration-responses-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    doc = read(config['manuscript'])
    validate_natural_dialogue_batch(doc)
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    assert not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records'])
    c, a, proof = plan(common, arm, doc)
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    assert proof['actual_changed_message_IDs'] == list(IDS)
    assert proof['all3660_unselected_or_retained_texts_and_native_copy_spans_preserved']
    assert proof['all40_other_blocks_and_opaque_duel_prefix_exact']
    assert proof['shared_balance_literal_status_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    rp = proof['runtime_plan']
    assert rp['encoded_table_bytes'] == 186 and rp['owned_table_bytes'] == 188 and rp['original172_byte_gate_exact']
    assert rp['new_memberships'] == [{'parent': 0x02053F40, 'stack_selector_offset': 0x274, 'table': 0x021184E0}]
    assert read('work/analysis/declaration_responses_runtime_v1536/runtime_plan.json')['patches'] == rp['patches']
    assert read('work/analysis/declaration_responses_runtime_v1536/scope_proof.json')['total_cases'] == 529442
    fonts, copies, escape, runtime, visual = [read(doc[k]) for k in
        ['native_font_proof', 'native_copy_proof', 'escape_regression_proof', 'native_runtime_proof', 'visual_review']]
    assert len(fonts['cases']) == 8 and not fonts['findings']
    assert len(fonts['all207_existing_actor_choices']) == 207 and len(fonts['invalid_compiler_inputs_rejected']) == 14
    assert fonts['manuscript_sha256'] == doc['reviewed_research_manuscript_sha256']
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert len(escape['all13_original_direct_pipeline_cases']) == 13
    assert all(p['ARM9_sha256'] == sha(a) and p['COMMON_sha256'] == sha(c) for p in [fonts, copies, escape])
    assert runtime['source_ARM9_sha256'] == SOURCE_ARM and runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    authored = {r['message_id']: compiled(r).hex() for r in doc['records']}
    assert all(case['compiled_hex'] == authored[case['message_ID']] for case in fonts['cases'])
    assert visual['all1_sheet_and8_native_panels_actually_visually_reviewed']
    assert visual['all8_full_glyph_planes_ordered_complete_letters_uniform6px_margins_bounds_and_blank_paper_pass']
    assert visual['remaining_layout_findings'] == 0
    return c, a, proof
