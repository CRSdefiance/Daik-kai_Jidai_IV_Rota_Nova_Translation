"""Approve native layouts; revised gameplay and registered release remain separate."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lesson_layout_approval_v1742')
OUT = Path('translations/lil_lessons_editorial_manuscript_v3.json')
CHOICES = Path('translations/lil_lesson_choices_editorial_draft_v2.json')
FONT = Path('work/analysis/lil_lesson_layout_v1725/all60_native_font_reconciliation.json')
DISPLAY = Path('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')
CHOICE_PROOF = Path('work/analysis/lil_lesson_choice_ui_v1735/original_choice_VM_geometry_and_native_pixels.json')
VISUAL = ROOT / 'visual_native_formatting_review.json'

if __name__ == '__main__':
    assert not ROOT.exists() and not OUT.exists() and not CHOICES.exists()
    fonts, display, choice = map(read, (FONT, DISPLAY, CHOICE_PROOF))
    doc = deepcopy(read('translations/lil_lessons_editorial_manuscript_v2.json'))
    menu = deepcopy(read('translations/lil_lesson_choices_editorial_draft_v1.json'))
    assert sha(Path(fonts['manuscript']).read_bytes()) == fonts['manuscript_sha256']
    assert display['all6_current_FE_native_actual_complete_ink_and_blank_cells_match']
    assert display['all9_reviewed_FE_full_actual_context_native_planes_pass']
    assert display['all9_complete_targets_fit_one_native_page_inside228x48']
    assert choice['four_complete_reviewed_labels_two_styles_each']
    assert choice['all12_original_selection_cancel_VM_cases_and_source_extents_verified']
    assert len(fonts['cases']) == len(doc['records']) == 60
    for sheet in fonts['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    assert sha(Path(choice['visual_review_sheet']).read_bytes()) == choice['visual_review_sheet_sha256']
    sheet = read('work/analysis/lil_FE_visual_v1738/sheet_receipt.json')
    assert sha(Path(sheet['sheet']).read_bytes()) == sheet['sheet_sha256']
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    # This scoped instance is deliberately not registered as a generic story profile.
    panel = replace(base, name='lil-lessons-FE-runtime-bound-v1',
                    leading_speaker_bytes=base.leading_speaker_bytes | frozenset({254}))
    by_id = {r['id']: r for r in fonts['cases']}
    warnings = []
    doc.update(encoder='dialogue-relocatable-v1', formatting_review_pending=False,
        status='60-source-prose-and-native-layout-approved;actual-revised-paths-map-and-release-pending',
        native_font_proof=str(FONT), native_font_proof_sha256=sha(FONT.read_bytes()),
        actual_context_FE_proof=str(DISPLAY), actual_context_FE_proof_sha256=sha(DISPLAY.read_bytes()),
        visual_review=str(VISUAL), no_playable_release_without_scoped_runtime_binding=True,
        required_runtime_ARM9_sha256=fonts['ARM9_sha256'],
        scoped_FE_profile_contract={'name': panel.name, 'base': base.name,
            'added_source_mapped_selector': 254, 'generic_story_profile_registry_unchanged': True})
    doc.pop('release_validation_rejects_unapproved_formatting', None)
    for row in doc['records']:
        case = by_id[row['id']]
        assert case['whole_native_and_independent_font_plane_exact']
        assert case['complete_printable_glyph_order_unique_cells_and_bounds_verified']
        row['english'] = row['english'].replace('{PAD}', '')
        profile = panel if row['source_presentation_prefix_hex'] == 'fe' else base
        compiled = encode_relocatable_dialogue(bytes.fromhex(row['source_hex']), row['english'], profile)
        assert compiled.encoded.hex() == case['encoded_hex']
        assert [d.as_dict() for d in compiled.diagnostics] == case['diagnostics']
        row['compiled_hex'] = case['encoded_hex']
        row['formatted_markup'] = case['formatted_markup']
        row['review']['formatting'] = True
        row['formatting_evidence'] = str(VISUAL)
        row['actual_revised_gameplay_and_registered_release_pending'] = True
        for diagnostic in case['diagnostics']:
            assert diagnostic['severity'] == 'warning' and diagnostic['code'] == 'line-break-count'
            lines = case['formatted_markup'].split('{LB}')
            assert 1 <= len(lines) <= 4
            reason = (diagnostic['message'] + '. Automatic English word wrapping replaces Japanese line divisions; '
                f'this exact {len(lines)}-line native panel was reviewed. Complete first/last letters, all glyph cells '
                'and bounds pass; no authored line breaks, omitted source facts or extra page. '
                + ('FE native228x48 geometry uses the independently established12-to16 display-row contract.'
                   if profile is panel else 'Progressive native216x64 complete font plane matches the independent mask.'))
            row['qa_waivers'] = ['line-break-count']
            row['qa_waiver_reason'] = reason
            warnings.append({'id': row['id'], 'code': 'line-break-count', 'reason': reason,
                             'formatted_markup': case['formatted_markup']})
    assert len(warnings) == 25
    validate_natural_dialogue_batch(doc)
    assert len(menu['records']) == 4
    for row in menu['records']:
        row['review']['formatting'] = True
        row['formatting_evidence'] = str(CHOICE_PROOF)
        row['actual_revised_choice_selection_and_release_pending'] = True
    menu.update(status='four-source-prose-native-choice-layout-approved;actual-branches-map-and-release-pending',
                visual_review=str(VISUAL), original_choice_UI_proof=str(CHOICE_PROOF),
                original_choice_UI_proof_sha256=sha(CHOICE_PROOF.read_bytes()))
    ROOT.mkdir(parents=True)
    save(VISUAL, {'all8_original60_panel_sheets_and_refined_sheet05_previously_viewed': True,
        'all9_actual_context_FE_display_previews_actually_viewed': True,
        'all4_current_and_reviewed_choice_pairs_actually_viewed': True,
        'no_visible_leading_trailing_letter_loss_clipping_or_orphaned_final_lines': True,
        'FE_actual_current_panels6_pixel_exact_under_prior_independent_screen_contract': True,
        'all9_reviewed_FE_native_planes_fit_one_page': True,
        'not_an_independent_whole_GPU_trace': True,
        'all25_warning_decisions_are_specific_automatic_language_line_count_differences': warnings,
        'proofs': {str(p): sha(p.read_bytes()) for p in (FONT, DISPLAY, CHOICE_PROOF)},
        'revised_gameplay_external_reference_approval_registered_integration_and_exact_patch_pending': True,
        'no_completed_editorial_entries_added': True, 'producer_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    doc['visual_review_sha256'] = menu['visual_review_sha256'] = sha(VISUAL.read_bytes())
    save(OUT, doc)
    save(CHOICES, menu)
    save(ROOT / 'approval_receipt.json', {'manuscript': str(OUT), 'manuscript_sha256': sha(OUT.read_bytes()),
        'choices': str(CHOICES), 'choices_sha256': sha(CHOICES.read_bytes()),
        'speech_panels': 60, 'choice_labels': 4, 'specific_warning_decisions': len(warnings),
        'all64_native_formatting_approved_actual_revised_gameplay_still_pending': True,
        'no_global_profile_ROM_registry_or_completion_change': True, 'full_goal_complete': False})
    print('60 native speech/system layouts and4 choice labels approved;25 specific line-count decisions. Actual revised branches/map/release still pending.')
