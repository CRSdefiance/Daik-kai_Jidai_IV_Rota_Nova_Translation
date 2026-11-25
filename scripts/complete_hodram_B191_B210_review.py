"""Credit the checked batch only after registered reconstruction andown startup pass."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/complete_hodram_B171_B190_review.py').read_text(encoding='utf-8'),{
    'Hodram_B171_B190_clean_next_20261102':'Hodram_B191_B210_clean_next_20261104',
    'Hodram_B171_B190_actual_pixels_v2_20261104':'Hodram_B191_B210_actual_pixels_20261104',
    'Hodram_B171_B190':'Hodram_B191_B210','hodram_B171_B190':'hodram_B191_B210',
    'Hodram_SC1B171_B190':'Hodram_SC1B191_B210',
    'B171–B190':'B191–B210',
    'pending_B171_B190_completion':'pending_B191_B210_completion',
    '435':'373','433':'352','195':'154','240':'219','9498':'9933','9933':'10306','9936':'10309','6004':'6158','3929':'4148','2853':'3226','663':'664',
    "    assert pixels['full_pirate30_andtown130_native_body_sequence_matches_copied_source_commands']":
        "    assert {k:v['calls'] for k,v in pixels['ordered_linear_scene_sequences'].items()} == dict(town_exchanges=128,castle_letter=20,parrot=17)",
    '    intervals = dict(sail=(2816, 10247), pirate=(2817, 11208), town=(2816, 35209), refusal=(2816, 5686))':
        "    intervals = {k:(v['first_target_frame'],v['first_following_nonfixture_modal_frame']) for k,v in pixels['target_capture_intervals'].items()}",
    "len(pixels['body_pages']) == 413":"len(pixels['body_pages']) == 468",
    "            assert row['source_count'] == 2 and int.from_bytes(block[command:command + 2], 'little') == 0x2100\n            offset = int.from_bytes(block[command + 2 + 2 * index:command + 4 + 2 * index], 'little')\n            assert command + 6 + offset == at and row['block'] == 171\n            samples = [dict(**s, source_index=index) for s in pixels['menu_samples']]":
    """            count = row['source_count']
            assert count in [2,3] and int.from_bytes(block[command:command+2],'little') == reference['native_command_word'] == (0x2100 if count==2 else 0x2200)
            offset = int.from_bytes(block[command+2+2*index:command+4+2*index],'little')
            assert command+2+2*count+offset == at
            samples = [dict(**s,source_index=index) for s in pixels['menu_samples'] if s['block']==row['block'] and s['source_command_offset']==row['source_command_offset']]""",
    "                ordered = sample['ordered_fixture_record_id']":
        "                ordered = sample['ordered_fixture_record_id']\n                ordered = ordered[0] if isinstance(ordered,list) else ordered",
    'initialized_fixture_runs=5, fixture_frames=85005':'initialized_fixture_runs=6, fixture_frames=98006',
    'captured_body_planes_matched=413, native_record_page_observations=188, actual_name_headers=27':
        'captured_body_planes_matched=468, native_record_page_observations=204, actual_name_headers=36',
    'complete_menu_highlights=2, reviewed_actual_sheets=8':'complete_menu_highlights=4, reviewed_actual_sheets=9',
    'ordered_town130_andpirate30_source_calls=True':'ordered_town128_letter20_parrot17_source_calls=True',
    'typed_choices=2, typed_choice_commands=1':'typed_choices=21, typed_choice_commands=10',
    'typed_choices=2, final_review':'typed_choices=21, final_review',
    'layout_findings_resolved=15, scoped_name_term_decisions=49, native_name_strings=31':
        'layout_findings_resolved=4, scoped_name_term_decisions=70, native_name_strings=36',
    'session=42463':'session=93360',
    "    ledger['latest_checkpoint'] = 'Registered B171–B190 verified and credited once: 435 reviews, 195 revisions and 240 retentions; 9933 complete. All 439 pages and 15 layout fixes pass. Exact clean patch and own startup pass. Full scope/main/ROMs preserved; next clean B191–B210 meanings saved; no guide photos.'":
        "    ledger['latest_checkpoint'] = 'Registered B191–B210 verified andcredited once:373 reviews,154 revisions/219 retentions;10306 complete.355 pages/four layout fixes,exact clean patch andown startup pass. User priority now Rafael early game/all tutorials;40 clean B42/B43 meanings saved. Later277-meaning/114-draft batch preserved. Full scope/main/allROMs/evidence preserved;no guide photos.'",
})
exec(compile(source,__file__+'::same-once-only-completion-exact-mixed-menu-references','exec'),globals())
