"""Record the verified B201–B220 batch at the registered integration boundary."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.finalize_rafael_B201_B220_research_v1 import FINAL, REBUILT, ROOT, SOURCE, checksum
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint


REGISTRY=Path('translations/release_stack.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
RELEASE=Path('work/analysis/Rafael2549_extended_release_verified_v1_20261106/registered_release_verification.json')
PACKAGE=Path('work/analysis/Weekend_testing_package_Rafael2549_20261106/package_verification.json')
READY=ROOT/'research_completion.json'
ACTUAL=ROOT/'actual_review.json'
KEY='Rafael_SC0_B201_B220_clean_20261106'


def main():
    ready,rebuilt,registered,package,actual,ledger=map(load,(READY,REBUILT,RELEASE,PACKAGE,ACTUAL,LEDGER))
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert ready['new_credit']==0 and (ready['records'],ready['revisions'],ready['retentions'])==(403,299,104)
    assert (ready['body_pages'],ready['typed_labels'],ready['scoped_public_names'])==(383,21,41)
    assert (ready['actual_source_variants'],ready['actual_pages'],ready['actual_menus'],ready['actual_name_headers'])==(173,174,6,33)
    assert (actual['offline_only_speech_variants'],actual['offline_only_caption_count'])==(209,8)
    assert actual['all_six_menu_instances_default_cursor_and_following_fixture_speech_observed']
    assert rebuilt['parent_sha256']==registered['candidate_sha256']==package['ROM_sha256']
    assert checksum(registered['patch'])==registered['patch_sha256']
    assert all(checksum(p)==h for p,h in ready['evidence'].items())
    summary=(
        "Rafael B201–B220 passed all five review gates for 403 records, with 299 revisions and 104 justified retentions. "
        "All 383 pages, 21 captions and 41 name or role bindings passed offline checks. Emulator fixtures showed "
        "174 pages, 33 speaker headers and six menus with ordinary A returns. Registered integration is pending. "
        "Integrated total remains 14,394 and Rafael2549 remains the weekend candidate."
    )
    doc=f"""# Rafael B201–B220 research verification

{summary}

The final source-bound review restores the normal-width glyphs in Istanbul, Rafael’s stammer and the 50,000-coin offer. The text keeps the namahage call, the castle letter’s separately indented signature, the parrot chase’s three sound rows and its five echoes. The earring pitch turns the page between sentences. Each exact source/current/stored reference, retention and formatting decision is in the {link('final manuscript',FINAL)}. See the {link('five-gate receipt',READY)}.

The research ROM changes only SC0 B201–B220. Native checks cover 382 complete catalogue reads, 104 relocated branch sites with 520 cases, all 343 archive loads and all ten original menu objects. The label-free 2000 command is preserved. All 383 final offline pages and 42 caption style planes were inspected. The 41 name and role decisions cover 29 distinct public nameplate strings. The original name data remains intact.

Three initialized emulator fixtures showed 173 speeches across 174 pages, 33 distinct actor headers, all seven town forecasts, both staged panels, and 13 captions across six exact menu instances. Pressing A reached the next fixture speech in each menu. The other 209 speeches and eight captions received offline checks. Alternate choices, original event activation, economic effects and hardware remain unobserved. {link('Focused gameplay scope',ACTUAL)}.

Proceed with the registered cumulative append, exact clean-input reconstruction and candidate-specific startup. Preserve the verified B146 percent-relocation proof and the registered ASCII right-bound repair. Rafael and tutorials remain first. Deferred artwork and the older-record technical re-audit stay separate. {link('Rafael2549 weekend package',package['zip'])}.
"""
    evidence={**ledger[KEY]['evidence'],**{str(p):checksum(p) for p in (READY,ACTUAL,REBUILT,FINAL,Path(__file__))}}
    checkpoint(
        mutation=SOURCE/'research_ready_documentation_v1',batch_key=KEY,
        batch_updates=dict(new_credit=0,all_individual_five_research_gates_pass=True,
            fifth_formatting_gate_pending=False,stored_checks_pending=False,focused_gameplay_pending=False,
            registered_integration_pending=True,full_intake_not_complete=True,
            source_speech_variants=382,typed_captions=21,complete_body_pages=383,scoped_public_names=41,
            observed_speeches=173,observed_pages=174,observed_menus=6,observed_headers=33,
            offline_only_speeches=209,offline_only_captions=8,
            final_review=str(FINAL),final_review_sha256=checksum(FINAL),
            research_completion=str(READY),research_completion_sha256=checksum(READY),evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael B201–B220 registered cumulative integration.',
            next_action='Register the exact mixed-menu transaction, verify its clean-input patch and cold-boot the registered ROM.',
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael_B201_B220_research_ready_20261106.md',
        document_text=doc,completed=14394,protected={str(REGISTRY):registered['registry_sha256'],
            registered['canonical_base']:registered['canonical_sha256'],registered['candidate']:registered['candidate_sha256'],
            registered['patch']:registered['patch_sha256'],package['zip']:package['zip_sha256'],
            rebuilt['research_ROM']:rebuilt['research_ROM_sha256']},
    )
    print('Recorded all 403 research-complete records at the registered integration boundary.')


if __name__=='__main__':
    main()

