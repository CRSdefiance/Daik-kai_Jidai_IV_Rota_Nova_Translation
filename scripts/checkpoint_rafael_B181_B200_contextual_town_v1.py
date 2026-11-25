"""Record all contextual decisions and the directly viewed offline town pages."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_rafael_B181_B200_names_v1 import CURRENT, OUT as IDENTITY, ROOT
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.refine_rafael_B188_B200_town_v1 import BASE, DELTA_PLAN
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.seal_rafael_B181_B200_clean_v1 import OUT as SOURCE
from scripts import write_rafael_B181_B187_contextual_v1 as story
from scripts import write_rafael_B188_B200_contextual_v1 as town


REGISTERED = Path('work/analysis/Rafael2165_extended_release_verified_v1_20261105/registered_release_verification.json')
PACKAGE = Path('work/analysis/Weekend_testing_package_Rafael2165_20261105/package_verification.json')
REGISTRY = Path('translations/release_stack.json')
PLAN = ROOT / 'town_plans_v3/automatic_plans.json'
ORIGINAL = ROOT / 'town_native_v1/compiled_native_pages.json'
DELTA = ROOT / 'town_native_delta_v1/compiled_native_pages.json'
VISUAL = ROOT / 'town_offline_visual_v1.json'
KEY = 'Rafael_SC0_B181_B200_clean_20261105'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not VISUAL.exists()
    paths = (SOURCE/'sealed_drafts.json', CURRENT, IDENTITY, story.OUT, town.OUT, REGISTERED, PACKAGE,
             PLAN, BASE, DELTA_PLAN, ORIGINAL, DELTA, story.LABELS, town.LABELS, Path(__file__))
    drafts, current, names, stories, towns, release, package, plan, old_plan, new_subset, original, delta, story_labels, town_labels, _ = [
        load(p) if p.suffix == '.json' else None for p in paths
    ]
    assert drafts['records_count'] == current['records'] == current['original_current_catalogue_lookups'] == 384
    assert (stories['proposed_revisions'], stories['justified_retentions'], towns['proposed_revisions'], towns['justified_retentions']) == (198, 29, 119, 38)
    assert all(not r['review']['formatting'] and all(r['review'][g] for g in ('source','context','localization','naturalness'))
        for d in (stories,towns) for r in d['records'])
    assert len(story_labels['records']) == 10 and len(town_labels['records']) == 19
    assert len(names['fresh_actors']) == 18 and len(names['exact_reused_actors']) == 11
    assert current['current_ROM_sha256'] == release['candidate_sha256'] == package['ROM_sha256']
    assert digest(package['zip']) == package['zip_sha256'] and digest(REGISTRY) == release['registry_sha256']
    assert original['plan_sha256'] == digest(BASE) and delta['plan_sha256'] == digest(DELTA_PLAN)
    assert new_subset['complete_plan_sha256'] == digest(PLAN)
    assert all(p['runtime'] == current['runtime'] for p in (original, delta))
    assert original['font_sha256'] == delta['font_sha256']
    assert not plan['failures']
    for proof, count in ((original,157), (delta,16)):
        assert proof['pages'] == len(proof['records']) == count
        assert proof['fresh_compiled_alignments'] == count * 4
        assert proof['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert proof['complete_consumption_andpagination_exact'] and proof['fullwidth_Latin_not_introduced']
        assert not proof['actual_gameplay'] and proof['formatting_gates_still_false']
    sheets = original['review_sheets'] + delta['review_sheets']
    assert len(sheets) == 26 and all(digest(s['path']) == s['sha256'] for s in sheets)
    assert {Path(r['path']).name for r in delta['review_sheets']} == {
        f'B{b}_part1.png' for b in (188,189,190,194,195,196,198,200)
    }
    rows = {r['id']: (r, ORIGINAL) for r in original['records']}
    rows.update({r['id']: (r, DELTA) for r in delta['records']})
    earlier = {r['id']: r for r in old_plan['records']}
    proofs = []
    for entry in plan['records']:
        ident = entry['id']
        row, receipt = rows.pop(ident)
        assert entry['encoded_hex'] == row['compiled_hex'] and entry['logical_English'] == row['logical_English']
        assert entry['expected_native_pages'] == 1
        assert (receipt == ORIGINAL) == (entry['encoded_hex'] == earlier[ident]['encoded_hex'])
        proofs.append(dict(id=ident, compiled_hex=entry['encoded_hex'], body_proof=str(receipt),
            source_reference=row['source_reference'], current_reference=row['current_reference'],
            final_encoded_page_visually_viewed=True))
    assert not rows and len(proofs) == 157
    save(VISUAL, dict(records=proofs, pages=157, final_updated_pages=16, exact_unchanged_views_reused=141,
        final_source_and_native_encodings_exact=True, final_all_body_pages_directly_viewed=True, inspected_sheets=sheets,
        FE_pages=14, no_actual_gameplay=True, stored_script_and_nameplate_pixels_pending=True, new_credit=0,
        evidence={str(p): digest(p) for p in (PLAN, ORIGINAL, DELTA, Path(__file__))}))
    evidence = {str(p): digest(p) for p in (*paths, VISUAL)}
    summary = (
        'Rafael B181–B200 has all 384 contextual decisions, with 317 proposed revisions and 67 justified retentions. '
        'The 157 town and random-scene pages passed offline native and direct visual checks, including fresh checks for 16 wrap refinements. '
        'Story formatting, nameplate display, stored-script checks and representative gameplay remain pending. '
        'Integrated credit remains 14,010. Rafael2165 remains the weekend candidate.'
    )
    doc = f"""# Rafael B181–B200 contextual review and town layout checkpoint

All 384 clean-first drafts were sealed before extracting the current Rafael2165 ROM text. Each complete exchange now has individual source and current references, a revision or justified retention and four passed prose gates. B181–B187 has 198 proposed revisions and 29 retentions. B188–B200 has 119 proposed revisions and 38 retentions. {link('Story decisions', story.OUT)}. {link('Town and random-scene decisions', town.OUT)}.

The story review preserves Yifa's teacher and senior fellow student, both crown handoffs, Julian's actual grandfather and the conditional date. Two unintended full-width I glyphs and three isolated punctuation inconsistencies have corrections. The 13 Aziza FE panels have a contextual speaker binding and still need native presentation checks, including FO and the separate FI and FA introduction. The scoped role and name review retains 29 exact labels, including the tea pair's Woman and Man. Eighteen getter pairs ran fresh and 11 were reused after exact runtime, actor and font comparisons. {link('Name consumer proof', IDENTITY)}.

The town review found six untranslated lines in the Sao Jorge wine exchange, corrected the Lisbon forecast to Scents and preserved the Amsterdam bread conversation as an offer to teach baking. All 157 town body pages fit on one page each, with zero warnings or errors, across 143 progressive speeches and 14 FE panels. All 18 original and eight revised contact sheets were viewed. The final 16 changed pages passed fresh native checks, and 141 exact unchanged pages retain their existing proof. The failed intermediate preference plan is preserved. {link('Final town layout and visual bindings', VISUAL)}.

Continue with story layout and visuals and the remaining scoped nameplate, stored-script and focused gameplay checks. Use representative actual town and story tests for the distinct FE and progressive presentations and returns. Natural activation, hardware, and registered integration for this batch remain open. Integrated credit is still 14,010. The designated main and the {link('Rafael2165 weekend package', package['zip'])} are preserved.
"""
    checkpoint(
        mutation=ROOT/'contextual_and_town_visual_documentation_checkpoint',
        batch_key=KEY,
        batch_updates=dict(new_credit=0, independently_drafted_records=384, independent_draft_blocks=list(range(181,201)),
            remaining_clean_meanings_anddrafts=0, remaining_current_comparisons=0, current_comparisons=384,
            contextual_comparison_records=384, source_only=False, current_binding_records=384,
            current_binding=str(CURRENT), current_binding_sha256=digest(CURRENT), full_intake_not_complete=True,
            proposed_revisions=317, justified_retentions=67, current_untranslated_record_corrections=6,
            current_mixed_width_Latin_corrections=2, town_body_pages_offline_and_viewed=157,
            town_exact_reused_body_pages=141, town_fresh_refined_body_pages=16, evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B181–B200 story layouts, scoped names, stored scripts and focused gameplay.',
            next_action='Bind and render B181–B187, including 13 Aziza FE panels. Reuse the 157 exact town display proofs while checking remaining names, stored references and representative progression.',
            current_batch_not_yet_integrated=True, native_job_live=False, registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B181_B200_contextual_town_visual_20261106.md',
        document_text=doc, completed=14010, protected={str(REGISTRY): release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'], package['zip']: package['zip_sha256']},
    )
    print('Saved the 384 contextual decisions and the exact final 157 viewed town pages. No new integration credit.')


if __name__ == '__main__':
    main()
