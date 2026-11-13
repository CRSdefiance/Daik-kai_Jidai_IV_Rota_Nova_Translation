"""Record the complete offline Rafael review and its remaining release gates."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.finish_rafael_B261_B280_native_pages_v1 import MANUSCRIPT, ROOT, SHEETS, digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.save_rafael3514_registered_checkpoint_v1 import NEXT
from scripts.verify_rafael3514_registered_release_v1 import RELEASE


REVIEW = Path('translations/rafael_B261_B280_contextual_review_v4.json')
PLAN = ROOT / 'visual_plan_v4/automatic_plans.json'
NATIVE = ROOT / 'final_native_pages_v1.json'
DELTA = ROOT / 'visual_delta_sheets_v2/sheet_index.json'
STYLES = ROOT / 'compiled_style_v1/compiled_style_objects.json'
MENU_PATHS = [ROOT / f'B261_C{offset}_native_v1/menu_provider_and_planes.json' for offset in (270, 1664)]
OWNERSHIP = ROOT / 'surname_ownership_v1/ownership_verification.json'
JACOB = OWNERSHIP.parent / 'jacob_native_v1/native_name_fields_verification.json'


def main():
    body_sheets = SHEETS / 'sheet_index.json'
    paths = (REVIEW, PLAN, NATIVE, body_sheets, DELTA, STYLES, *MENU_PATHS, OWNERSHIP, JACOB)
    review, plan, native, sheets, delta, styles, ternary, binary, ownership, jacob = map(load, paths)
    ledger, release, package = map(load, (LEDGER, RELEASE, PACKAGE))
    assert review['runtime'] == native['runtime'] == styles['runtime'] == ternary['runtime'] == binary['runtime'] == ownership['runtime']
    assert review['current_ROM_sha256'] == ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert (review['proposed_revisions'], review['justified_retentions']) == (118, 17)
    assert native['plan_sha256'] == digest(PLAN) and native['manuscript_sha256'] == digest(MANUSCRIPT)
    assert native['pages'] == sheets['pages'] == 131 and len(native['records']) == 130
    assert native['fresh_visual_delta_records'] == 15 and delta['pages'] == 16
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and native['FE_actual_glyph_row_membership_checked']
    assert not plan['failures'] and not any(
        issue['severity'] in ('error', 'warning') for record in plan['records'] for issue in record['base_QA']['issues']
    )
    assert (len(styles['objects']), styles['physical_alternatives'], styles['native_target_slot_cases']) == (2, 16, 16)
    assert all(menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] for menu in (ternary, binary))
    assert (ternary['bridged_modal_returns'], binary['bridged_modal_returns']) == (24, 18)
    assert (ternary['complete_English_caption_style_planes'], binary['complete_English_caption_style_planes']) == (12, 8)
    captions = {record['id']: record for record in review['records'] if record['kind'] == 'typed-choice-label'}
    for menu in (ternary, binary):
        manuscript = Path(menu['manuscript'])
        assert digest(manuscript) == menu['manuscript_sha256']
        for row in load(manuscript)['records']:
            assert all(row[key] == captions[row['id']][key] for key in ('english', 'source_hex', 'current_hex'))
    viewed = [*sheets['sheets'], *delta['sheets'], *ternary['review_sheets'], binary['review_sheet'], jacob['review_sheet']]
    assert len(viewed) == 10 and all(digest(row['path']) == row['sha256'] for row in viewed)
    assert jacob['original_progressive_andfull_name_getters_pass']
    assert {row['text'] for row in jacob['versions'][1]['names']['rows']} == {'Jacob Portunto'}
    assert ownership['plett']['relocation_required'] and ownership['plett']['adjacent_protected_text'] == 'Sakura'
    assert not native['actual_gameplay'] and review['new_credit'] == 0
    summary = (
        'Rafael B261–B280 passed offline checks for 131 pages, five puzzle captions and both cave-in voice tables. '
        'Visual review led to 15 fresh wrap checks. Both original getters and native glyph planes passed for Jacob Portunto. '
        'Plett Perrault needs surname relocation. Stored script checks, focused gameplay and registration remain pending. '
        'Integrated coverage is 15,359.'
    )
    doc = f"""# Rafael B261–B280 offline display checkpoint

{summary}

The 135 contextual decisions remain 118 revisions and 17 justified retentions. The ice puzzle preserves the full premise and uses the menu’s own labels in its directions. Native rendering caught two FE width problems. The instruction page needed room for invisible wrap controls, and the Sao Jorge share notice wrapped past its planned first row. Both pass after source-specific layout adjustments. The revised bounty briefing begins its second page with the reported lead. All 131 final pages were visually reviewed across the initial sheets and 16 changed previews. Three town greetings retain FI and expand to Rafael in the verified default runtime. {link('Revised contextual ledger', REVIEW)}. {link('Final native page evidence', NATIVE)}. {link('Visual wrap checks', DELTA)}.

Both original menu providers, all five captions, 20 current and revised caption style planes, and 42 bridged selection or cancel results passed. Both cave-in tables passed the original slot getters for all 16 physical voice alternatives. The native checks used Rafael3514 and did not execute controller scenes. {link('Stone choices', MENU_PATHS[0])}. {link('Figurehead choices', MENU_PATHS[1])}. {link('Voice tables', STYLES)}.

Jacob Portunto fits in an exclusive surname field, reverses to the exact registered ARM9 and passed both original getters and the viewed name planes. Plett’s source slot is eight bytes including the terminator. Perrault needs nine bytes, and Sakura starts at the next byte. Use a proven allocation and verify both consumers before integrating the surname. {link('Jacob getter and display checks', JACOB)}. {link('Surname ownership evidence', OWNERSHIP)}.

Next verify reversible relocation and stored scripts, then use focused initialized emulator sequences for the three-way and binary selections, both cave-in branches, the B277 page transition and representative reward or town behavior. Include Jacob’s nameplate where his encounter is sampled. Carry all nine Rafael3514 final stages into the registered cumulative release and verify the exact clean-input patch. The current registered ROM and weekend package remain available. No gameplay or release credit is assigned at this checkpoint.
"""
    evidence = {**ledger[NEXT]['evidence'], **{str(path): digest(path) for path in (*paths, MANUSCRIPT, Path(__file__))}}
    checkpoint(
        mutation=ROOT/'B261_B280_display_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(
            new_credit=0, contextual_review=str(REVIEW), contextual_review_sha256=digest(REVIEW),
            native_page_receipt=str(NATIVE), native_page_receipt_sha256=digest(NATIVE),
            native_offline_pages=131, native_offline_typed_captions=5, native_offline_style_slots=16,
            all_final_dialogue_pages_directly_viewed=True, fresh_wrap_records=15,
            jacob_name_getters_and_offline_display_pass=True, plett_surname_relocation_pending=True,
            stored_checks_pending=True, formatting_pending=True, representative_gameplay_pending=True,
            registered_integration_pending=True, evidence=evidence,
        ),
        additional_updates={'editorial_execution_priority_20261104': dict(
            new_credit=0, current_batch='Rafael B261–B280 stored and focused scene checks.',
            next_action='Qualify surname relocation and verify stored scripts and focused scene transitions.',
            native_job_live=False, registered_build_live=False, guide_photos=False,
        )},
        summary=summary, document='docs/editorial_Rafael_B261_B280_display_20261106.md',
        document_text=doc, completed=15359, protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print('Saved the complete offline display checkpoint. Integrated coverage remains 15,359.')


if __name__ == '__main__':
    main()
