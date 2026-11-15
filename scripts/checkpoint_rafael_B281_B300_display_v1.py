"""Save the contextual and offline display checkpoint with zero release credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael3649_registered_v1 import NEXT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B281_B300_v1 import FORMATTING, MACROS, ROOT
from scripts.refine_rafael_B281_B300_visual_v1 import FIRST_SHEETS, PREFERENCES
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.verify_rafael_B281_B300_visual_delta_v1 import FINAL, PLAN, SHEETS
from scripts.write_rafael_B281_B300_contextual_v1 import LABELS, OUT, RELEASE


STYLES = ROOT / 'compiled_style_v2/compiled_style_objects.json'
MENUS = [ROOT / f'B293_C{offset}_native_v1/menu_provider_and_planes.json' for offset in (884, 1906)]
NAME = ROOT / 'zaganos_name_field_v1/native_v1/native_name_fields_verification.json'
FE = ROOT / 'FE_width_probe_v1.json'
DELTA_SHEETS = SHEETS / 'sheet_index.json'


def main():
    review, names, plan, native, original, delta, styles, ternary, binary, name = map(load, (
        OUT, LABELS, PLAN, FINAL, FIRST_SHEETS, DELTA_SHEETS, STYLES, *MENUS, NAME))
    ledger, release, package = map(load, (LEDGER, RELEASE, PACKAGE))
    assert review['runtime'] == native['runtime'] == styles['runtime'] == ternary['runtime'] == binary['runtime']
    assert review['current_ROM_sha256'] == ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert (review['source_objects'], review['proposed_revisions'], review['justified_retentions']) == (245, 202, 43)
    assert review['all_individual_four_prose_gates_pass'] and review['all_fifth_formatting_gates_pending']
    assert len(names['records']) == 17
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN)
    assert native['manuscript_sha256'] == styles['manuscript_sha256'] == digest(FORMATTING)
    assert (len(native['records']), native['pages'], native['fresh_visual_delta_records']) == (240, 248, 24)
    assert (original['pages'], delta['pages']) == (250, 31)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and native['FE_actual_glyph_row_membership_checked']
    assert not plan['failures'] and not any(
        issue['severity'] in ('error', 'warning') for row in plan['records'] for issue in row['base_QA']['issues']
    )
    assert (len(styles['objects']), styles['physical_alternatives'], styles['native_target_slot_cases']) == (11, 76, 88)
    assert all(menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] for menu in (ternary, binary))
    assert (ternary['bridged_modal_returns'], binary['bridged_modal_returns']) == (24, 18)
    assert (ternary['complete_English_caption_style_planes'], binary['complete_English_caption_style_planes']) == (12, 8)
    assert name['original_progressive_andfull_name_getters_pass']
    assert {row['text'] for row in name['versions'][1]['names']['rows']} == {'Zaganos Bey'}
    viewed = [*original['sheets'], *delta['sheets'], *ternary['review_sheets'], binary['review_sheet'], name['review_sheet']]
    assert all(digest(row['path']) == row['sha256'] for row in viewed)
    assert not native['actual_gameplay'] and review['new_credit'] == 0

    summary = (
        'Rafael B281–B300 has 245 contextual decisions, with 202 revisions and 43 justified retentions. '
        'All 248 final dialogue pages, five bear encounter captions and 88 voice slots passed offline native checks. '
        'Stored scripts, focused gameplay and registered integration remain pending. Integrated coverage is 15,494.'
    )
    doc = f"""# Rafael B281–B300 editorial and offline display checkpoint

{summary}

The clean Japanese and Rafael3649 records are cited individually. The London guild reward changes from 100,000 to 10,000 gold coins. Two equinox lines lose a full-width F while keeping the FI substitution. Two bear encounter alternatives recover unreadable leading text, and five interjections use consistent punctuation. The same wording carries the chant from the ruins to the later discussion. The scope includes 17 name or role decisions. Both original name getters and the inspected native name planes pass for Zaganos Bey. {link('Contextual ledger', OUT)}. {link('Name and role ledger', LABELS)}. {link('Name getter and plane evidence', NAME)}.

The initial full offline pass checked and rendered 250 pages. All were inspected in 11 sheets. Two share notices needed a narrower source-specific FE planning width to keep visible text inside the planned rows. The visual pass corrected 24 body layouts and removed two unnecessary second pages. The fresh rendered pages were inspected after those changes. The final evidence reuses 216 byte-identical native records and binds all final pages to their actual compiled bytes. Default FO, FA and both FI paragraphs were also checked on the registered runtime. {link('Final automatic plan', PLAN)}. {link('Final native page evidence', FINAL)}. {link('Visual rechecks', DELTA_SHEETS)}. {link('FE width and parity probe', FE)}. {link('Substitution evidence', MACROS)}.

Both typed menu providers and all five captions passed, including 20 caption planes and 42 bridged selection or cancel results. The final alternate dialogue tables passed all 88 original slot getters across 76 physical entries. These native checks are offline evidence. {link('Three-way menu', MENUS[0])}. {link('Two-way menu', MENUS[1])}. {link('Voice tables', STYLES)}.

Next reconstruct the stored scripts, including the exact Malacca FE parity case, then run focused initialized sequences for the bear menu, voice branches, a representative page turn, the reward notice and Zaganos’s nameplate. Bind the verified dialogue and the qualified surname correction in the registered cumulative release with its clean-input patch. Rafael3649 and the weekend package remain protected. This checkpoint carries no gameplay or release credit.
"""
    paths = (OUT, LABELS, FORMATTING, MACROS, PLAN, PREFERENCES, FINAL, FIRST_SHEETS, DELTA_SHEETS,
             STYLES, *MENUS, NAME, FE, Path(__file__))
    evidence = {**ledger[NEXT]['evidence'], **{str(path): digest(path) for path in paths}}
    checkpoint(
        mutation=ROOT/'B281_B300_display_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(
            new_credit=0, source_only=False, independently_drafted_records=245,
            independent_draft_blocks=list(range(281, 301)), remaining_clean_meanings_anddrafts=0,
            remaining_current_comparisons=0, revisions=202, justified_retentions=43, reviewed_names_and_roles=17,
            contextual_review=str(OUT), contextual_review_sha256=digest(OUT),
            native_page_receipt=str(FINAL), native_page_receipt_sha256=digest(FINAL),
            native_offline_pages=248, native_offline_typed_captions=5, native_offline_style_slots=88,
            all_final_dialogue_pages_directly_viewed=True, fresh_wrap_records=24,
            zaganos_name_getters_and_offline_display_pass=True, stored_checks_pending=True,
            formatting_pending=True, representative_gameplay_pending=True,
            registered_integration_pending=True, evidence=evidence,
        ),
        additional_updates={'editorial_execution_priority_20261104': dict(
            new_credit=0, current_batch='Rafael B281–B300 stored and focused scene checks.',
            next_action='Verify stored scripts and exercise the selected scene transitions before registration.',
            native_job_live=False, registered_build_live=False, guide_photos=False,
        )},
        summary=summary, document='docs/editorial_Rafael_B281_B300_display_20261106.md',
        document_text=doc, completed=15494, protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print('Saved Rafael B281–B300 display checkpoint. Integrated coverage remains 15,494.')


if __name__ == '__main__':
    main()
