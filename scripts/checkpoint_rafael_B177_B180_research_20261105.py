"""Record the 183 gated records and the next 67 source-first drafts without credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A=Path('work/analysis')
ROOT=A/'Rafael_B177_B180_research_final_v1_20261105'
RELEASE=A/'Rafael1424_extended_release_verified_v2_20261105/registered_release_verification.json'
REBUILT=A/'Rafael_B177_B180_reconstruction_v2_20261105/reconstruction.json'
DRAFT=A/'Rafael_B161_B180_clean_20261105/B161_B165_clean_drafts_v1.json'
PACKAGE=A/'Weekend_testing_package_Rafael1424_20261105/package_verification.json'
REGISTRY=Path('translations/release_stack.json')


if __name__=='__main__':
    ready,actual,release,rebuilt,draft,package=map(load,
        [ROOT/'research_completion.json',ROOT/'actual_review.json',RELEASE,REBUILT,DRAFT,PACKAGE])
    assert ready['all_individual_five_gates_pass'] and (ready['records'],ready['revisions'],ready['retentions'])==(183,133,50)
    assert actual['all_four_menus_default_cursor_andfollowing_fixture_speech_observed']
    assert (actual['source_speech_variants_observed'],actual['native_body_pages_observed'],actual['offline_only_speech_variants'])==(104,115,71)
    assert len(draft['records'])==67 and {r['block'] for r in draft['records']}==set(range(161,166))
    assert rebuilt['parent_sha256']==release['candidate_sha256']==package['ROM_sha256']
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    registry_digest=sha(REGISTRY.read_bytes())
    assert release['profile'] in load(REGISTRY)['profiles']
    summary=('Rafael B177–B180 has 183 complete five-gate research reviews: 133 revisions and 50 justified retentions. '
        'All 186 body pages, eight captions, nine names, 290 relocated branch cases and 343 archive loads passed. '
        'Disclosed emulator fixtures observed 104 speeches and 115 pages, all nine headers, and all four menus with ordinary A returns. '
        '71 speeches remain offline-only. Registered integration is pending. B161–B165 has 67 new clean-first drafts. '
        'Integrated count 13,269 and the designated main and weekend packages are preserved.')
    text=f"""# Rafael B177–B180 research verification

All 183 individual review gates are sealed. The final manuscript records 133 revisions, 50 justified retentions, seven glyph defects and exact source/current/stored references. See [research completion](../{(ROOT/'research_completion.json').as_posix()}). The nine reviewed speaker names or roles were retained and checked in the original nameplate renderer. This work adds no integration credit.

The pinned research ROM **{rebuilt['research_ROM_sha256'][:8]}** changes only SC0 blocks 177–180 over registered 5d40f920. It preserves all other files, graphics, font, name fields and runtime components. Rebuild and byte-exact inverses cover 318 commands and 58 relocated sites. All 290 native branch cases pass. All 175 catalogue lookups and 343 archive loads pass. The 186 stored pages include 89 fresh parity-dependent renders and 97 exact plane reuses. All eight typed captions preserve the original indices. The one B177 legacy padded current slot required a guarded reader while the new menu bytes satisfy strict alignment.

Two initialized DeSmuME fixtures, 38,482 frames in total, displayed 104 speeches and 115 pages with all nine headers, the FE extra-armor unlock, all four default menus and the following fixture dialogue after ordinary A. The 13 readable gameplay, menu and name sheets were directly viewed. Two menu captures showed partial cyan bands while the glyphs and centering were exact. The checker binds only the observed bands at the exact frames and retains complete glyph and blank-background checks. It required no renderer change or capture rerun. Other menu states, original conditional branches, natural chronology, locations and hardware remain unvisited. The other 71 speeches are offline-only.

Proceed with the registered cumulative transaction and unchanged v6 eight-stage continuation. Preserve the exact B146 relocated percent proof, ASCII right-bound correction, all 114 accepted layers, earlier translations, ROMs and packages. Require exact clean-input reconstruction and own fresh Rafael startup before granting the 183 credits once. No main promotion.

**Next clean intake.** [{DRAFT.name}](../{DRAFT.as_posix()}) contains 67 independent drafts across B161–B165: Claudio helping a child, the Mediterranean relic, the lamp-revealed map and two royal audiences. Current comparisons and approved terms remain pending. The other 491 B166–B176 records in this intake remain at clean inventory. All other routes and remaining prose stay in scope. Deferred artwork and the later older-record technical re-audit stay separate.
"""
    evidence={str(p):sha(p.read_bytes()) for p in [ROOT/'research_completion.json',ROOT/'actual_review.json',REBUILT,DRAFT,PACKAGE,Path(__file__)]}
    checkpoint(mutation=A/'Rafael_B177_B180_research_ledger_20261105',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0,independently_drafted_records=250,independent_draft_blocks=[161,162,163,164,165,177,178,179,180],
            remaining_clean_meanings_anddrafts=491,new_clean_B161_B165_drafts=str(DRAFT),
            new_clean_B161_B165_drafts_sha256=sha(DRAFT.read_bytes()),current_comparisons=183,remaining_current_comparisons=558,
            complete_research_subset='Rafael_SC0_B177_B180_research_20261105',full_intake_not_complete=True),
        new_entries={'Rafael_SC0_B177_B180_research_20261105':dict(new_credit=0,records=183,blocks=[177,178,179,180],
            all_five_research_gates_pass=True,registered_integration_pending=True,research_completion=str(ROOT/'research_completion.json'),
            research_completion_sha256=sha((ROOT/'research_completion.json').read_bytes()),actual_source_variants=104,offline_only_source_variants=71)},
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael B177–B180 183 complete five-gate reviews; registered integration pending.',
            next_action='Verify the registered 183-record successor and then compare B161–B165 with current English.',
            current_batch_not_yet_integrated=True,native_job_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael_B177_B180_research_ready_20261105.md',document_text=text,
        completed=13269,protected={str(REGISTRY):registry_digest,
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            package['zip']:package['zip_sha256']})
    print('Saved 183 research gates and 67 independent clean drafts; no release credit.')
