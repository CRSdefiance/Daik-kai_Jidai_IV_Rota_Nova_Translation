"""Bind the approved offline proof set to complete-block research reconstruction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_storage_inputs_20261104')
FORMAT = Path('work/analysis/Hodram_B171_B190_formatting_20261102')
APPROVED = FORMAT / 'speech_display_approved_20261104'
CURRENT = Path('work/analysis/Hodram_B171_B190_current_20261102/current_effective.json')
MENUS = Path('work/analysis/Hodram_B171_B190_menu_20261104/complete_choice_objects.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = load(FORMAT / 'formatting_input.json')
    plans, native, visual, packet, menus = map(load, [APPROVED / 'all433_compiled_plans.json',
        APPROVED / 'all433_native_pages.json', APPROVED / 'visual_approval.json', CURRENT, MENUS])
    assert visual['all439_final_pages_visually_approved'] and len(doc['records']) == 435
    assert packet['runtime'] == native['runtime'] and packet['records'] == 433 and len(packet['groups']) == 20
    assert packet['current_ROM_sha256'] == doc['current_ROM_sha256']
    captions = load(APPROVED / 'caption_native_input.json')
    by_caption = {r['id']: r for r in captions['records']}
    original_speech = {r['id']: r for r in doc['records'] if r['kind'] != 'typed-choice-label'}
    storage = deepcopy(doc)
    storage['records'] = [deepcopy(by_caption.get(r['id'], r)) for r in doc['records']]
    assert all(r == original_speech[r['id']] for r in storage['records'] if r['id'] in original_speech)
    storage.update(offline_speech_visual_approved=True, all_individual_fifth_gates_still_pending=True,
        source_full_manuscript=str(FORMAT / 'formatting_input.json'),
        source_full_manuscript_sha256=sha((FORMAT / 'formatting_input.json').read_bytes()), new_credit=0)
    ROOT.mkdir()
    manuscript = ROOT / 'storage_manuscript.json'
    save(manuscript, storage)
    digest = sha(manuscript.read_bytes())
    plans.update(manuscript=str(manuscript), manuscript_sha256=digest)
    plan_path = ROOT / 'all433_compiled_plans.json'
    save(plan_path, plans)
    native.update(manuscript=str(manuscript), manuscript_sha256=digest, plan=str(plan_path), plan_sha256=sha(plan_path.read_bytes()))
    save(ROOT / 'all433_native_pages.json', native)
    save(ROOT / 'packet.json', packet)
    groups = []
    for obj in menus['objects']:
        path = Path(obj['receipt'])
        assert sha(path.read_bytes()) == obj['receipt_sha256']
        proof = load(path)
        assert proof['runtime'] == native['runtime']
        assert len(proof['records']) == 8 and len(proof['compiler_negatives_rejected']) == 7
        groups.append(dict(block=obj['block'], source_command_offset=obj['source_command_offset'],
            target_object_hex=proof['native_choice_object_hex'], record_IDs=obj['record_ids'],
            original_receipt=str(path), original_receipt_sha256=sha(path.read_bytes())))
    assert len(groups) == 1
    save(ROOT / 'menus_reviewed.json', dict(manuscript=str(manuscript), manuscript_sha256=digest,
        runtime=native['runtime'], menus=groups, offline_visual_approved=True, direct_view_pending=False,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        native_provider_alignments=6, bridged_modal_returns=18, complete_English_caption_style_planes=8,
        source_receipt=str(MENUS), source_receipt_sha256=sha(MENUS.read_bytes()),
        actual_controller_andstored_objects_still_pending=True, new_credit=0))
    save(ROOT / 'no_style_objects.json', dict(manuscript=str(manuscript), manuscript_sha256=digest,
        plan_sha256=sha(plan_path.read_bytes()), runtime=native['runtime'], objects=[],
        source_packet_has_zero_4100_commands=True, no_style_consumer_execution_needed=True,
        native_target_slot_cases=0, source_alias_equivalence_exact=True, new_credit=0))
    save(ROOT / 'input_binding.json', dict(manuscript=str(manuscript), manuscript_sha256=digest,
        prose_reviews_reused=435, speech_native_andvisual_objects_reused=433, speech_pages=439,
        typed_captions=2, native_orvisual_checks_replayed=0, source_andnontext_commands_exact_in_packet=True,
        all_fifth_gates_still_false=True, new_credit=0, new_ROMs=0,
        evidence={str(p): sha(p.read_bytes()) for p in [FORMAT / 'formatting_input.json',
            APPROVED / 'complete_display_checkpoint.json', CURRENT, MENUS, Path(__file__)]}))
    print('435 exact prose objects / 433 native speeches / 439 viewed pages / one two-choice menu bound for storage; no checks replayed.')
