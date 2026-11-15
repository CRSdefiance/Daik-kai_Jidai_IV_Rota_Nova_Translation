"""Seal the one-record amendment after direct native and actual Help page review."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.reviewed_help_fleet66_amendment_v1 import plan_articles
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/HELP66_Command_amendment_20261104')
OUT = Path('translations/help_fleet66_Command_contextual_amendment_v1.json')

if __name__ == '__main__':
    assert not OUT.exists() and not (ROOT/'production_plan_v1.json').exists()
    plan_path = ROOT/'automatic_plans_v1.json'
    plan = load(plan_path)
    native_path = ROOT/'native_pages_v1/native_help_pages.json'
    native = load(native_path)
    actual_path = ROOT/'focused_navigation_checked_v1/ordinary_gameplay_verification.json'
    actual = load(actual_path)
    assert native['native_pages'] == 2 and len(native['records']) == 2
    assert native['plan_sha256'] == sha(plan_path.read_bytes())
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    assert actual['actual_pages'] == 2 and actual['actual_articles'] == 1 and actual['offline_only_pages'] == 0
    assert actual['all_selected_complete_actual_pages_andnative_child_targets_pass']
    assert actual['cold_boot_frames'] == 23481 and len(actual['original_forward_back_andL_R_history_returns']) == 2
    assert len(actual['readable_actual_sheets']) == 1
    for sheet in actual['readable_actual_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    visual_path = ROOT/'focused_navigation_checked_v1/direct_actual_visual_approval.json'
    assert not visual_path.exists()
    save(visual_path, dict(actual_verification=str(actual_path), actual_verification_sha256=sha(actual_path.read_bytes()),
        all_two_observed_complete_pages_andone_actual_sheet_directly_viewed=True, sheets=actual['readable_actual_sheets'],
        finding='Complete Command/threshold line, natural full prose, continuous funding/return paragraph and all policy/navigation labels. Both original history returns verified.',
        no_hardware_orfull_story_playthrough_claim=True, guide_photos=False, new_credit=0))
    doc = deepcopy(load(plan['manuscript']))
    parent, clean, base = [NdsImage.open(p) for p in [doc['current_ROM'], 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds']]
    raw = parent.read_file(doc['file_path'])
    row = doc['records'][0]
    row['review']['formatting'] = True
    row['fresh_display_allocation_widgets_andintegration_pending'] = False
    row['native_terms_andcontrols_binding_pending'] = False
    row['offline_only'] = False
    row['planned_stored_pages'] = []
    for page in plan['pages']:
        t = page['topic_id']
        nr = next(r for r in native['records'] if r['topic_id'] == t)
        ar = next(r for r in actual['actual_HELP_cases'] if r['topic_id'] == t)
        assert nr['encoded_hex'] == page['encoded_hex']
        row['planned_stored_pages'].append(dict(file_path=doc['file_path'], block=t, exact_stored_hex=page['encoded_hex'],
            native_preview=nr['preview'], native_preview_sha256=nr['preview_sha256'], actual_frame=ar['frame'],
            actual_capture=ar['capture'], actual_capture_sha256=ar['capture_sha256']))
    doc.update(format='dk4-help66-command-contextual-amendment-final-v1', all_fifth_gates_pending=False, all_individual_five_gates_pass=True,
        proposed_revisions=1, justified_retentions=0, registered_integration_pending=True, integration_credit_pending=True,
        once_only_credit_belongs_to_original37_record_not_anadditional_review=True,
        native_andvisually_approved_pages=2, actual_pages=2, actual_articles=1, offline_only_pages=0,
        actual_ordinary_coldboot_frames=23481, native_proof=str(native_path), actual_proof=str(actual_path),
        actual_visual_approval=str(visual_path), native_visual_approval=str(ROOT/'preview_qualification_v1/direct_visual_approval.json'))
    for key in ['native_proof','actual_proof','actual_visual_approval','native_visual_approval']:
        doc[key+'_sha256'] = sha(Path(doc[key]).read_bytes())
    encoded, compiled = plan_articles(doc, clean.read_file(doc['file_path']), base.read_file(doc['file_path']), raw)
    assert encoded == Path(plan['research_resource']).read_bytes()
    assert all(row['review'].values()) and compiled['owned_topic_ids'] == [66,216]
    save(OUT, doc)
    save(ROOT/'production_plan_v1.json', dict(**compiled, manuscript=str(OUT), manuscript_sha256=sha(OUT.read_bytes()),
        research_resource=plan['research_resource'], current_ROM=doc['current_ROM'], current_ROM_sha256=doc['current_ROM_sha256'],
        all_source_current_term_native_actual_andindividual_five_gates_bound=True, registered_integration_pending=True, new_credit=0))
    print('Fleet66 Command amendment passes all five research gates; two observed pages and two returns, no duplicate credit.')
