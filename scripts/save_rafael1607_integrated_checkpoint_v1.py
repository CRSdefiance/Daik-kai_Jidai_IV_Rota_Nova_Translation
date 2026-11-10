"""Record the once-credited tutorial successor and hand off the independent clean drafts."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A=Path('work/analysis')
ROOT=A/'Rafael1607_extended_release_verified_v1_20261105'
DRAFT=A/'Rafael_B161_B180_clean_20261105/B161_B165_clean_drafts_v1.json'
PACKAGE=A/'Weekend_testing_package_Rafael1424_20261105/package_verification.json'


if __name__=='__main__':
    release,credited,startup,draft,package=map(load,[ROOT/'registered_release_verification.json',
        ROOT/'completion_checkpoint.json',ROOT/'own_registered_startup_verification.json',DRAFT,PACKAGE])
    assert credited['new_credit']==183 and credited['counts']==dict(completed=13452,revised=7651,retained=5801)
    assert release['complete_stack_entries']==683 and release['accepted_layers']==114 and release['passing_release_checks']==26
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert startup['frames']==4001 and startup['actual_captain_getter']==startup['actual_route_word']==0
    assert len(draft['records'])==67 and package['ROM_sha256']==release['parent_sha256']
    short=release['candidate_sha256'][:8]
    summary=(f'Rafael B177–B180 is integrated and credited once: 183 reviews (133 revisions, 50 justified retentions). '
        f'Experimental {short} passed 683 manifest entries, 114 accepted layers, eight final stages, 26 release checks, '
        'exact clean-input patch reconstruction and its own Rafael startup. Integrated total: 13,452. Main and weekend packages preserved. '
        'Next compare the 67 clean-first B161–B165 drafts against current English. The other 491 B166–B176 records remain at clean inventory.')
    text=f"""# Registered Rafael1607 tutorial checkpoint

The registered experimental candidate is `{release['candidate']}`, SHA-256 `{release['candidate_sha256']}`. The adjacent [clean-input patch](../{Path(release['patch']).as_posix()}) reconstructs it byte for byte. The manifest preserves **683 entries, all 114 accepted layers and all eight final stages**, including the ASCII right-bound correction. The verifier passed 26 release checks, including the source-bound B146 percent guard and all four story archives. Only the four owned B177–B180 blocks differ from the previous registered candidate. [Release proof](../{(ROOT/'registered_release_verification.json').as_posix()}).

**183 reviews are credited once**, comprising 133 revisions and 50 justified retentions. The integrated ledger now records **13,452 = 7,651 revisions + 5,801 retentions**. The [individual integrated manuscript](../translations/rafael_B177_B180_integrated_final_review_v1.json) binds each exact source, previous and registered target. The designated main and both previously delivered weekend packages are preserved.

Reuse the [research proof](editorial_Rafael_B177_B180_research_ready_20261105.md). It covers 175 stored speeches, 186 rendered pages, 290 branch cases, 343 archive loads, eight captions and nine retained names or roles. Two disclosed emulator fixtures observed 104 speeches, 115 pages, all nine headers and the default state of all four menus with an ordinary A return. The other 71 speeches remain offline-only. The final registered candidate separately passed its own 4,001-frame Rafael cold boot, the exact startup pixels and both original Fernan name getters. Natural branch activation, original locations, earned story chronology, full route, other menu states and hardware remain unverified for this batch.

Continue with the [67 clean-first B161–B165 drafts](../{DRAFT.as_posix()}). Compare current English only after binding these exact clean records, current names and approved item or institution terms. The remaining 491 B166–B176 records are inventoried. Keep every other storyline, earlier unfinished contextual review, shared town/shop/random scene, speaker label and remaining player-facing text in scope. Deferred artwork and the later older-record technical re-audit stay separate. Preserve all prior ROMs and evidence.
"""
    proof_paths=[ROOT/'registered_release_verification.json',ROOT/'completion_checkpoint.json',ROOT/'own_registered_startup_verification.json',DRAFT,Path(__file__)]
    checkpoint(mutation=ROOT/'documentation_checkpoint',batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0,integrated_subbatch_credit=183,integrated_blocks=[177,178,179,180],
            full_intake_not_complete=True,remaining_current_comparisons=558,remaining_clean_meanings_anddrafts=491,
            next_clean_first_drafts=str(DRAFT),next_clean_first_drafts_sha256=sha(DRAFT.read_bytes()),
            subset_registered_release=str(proof_paths[0]),subset_registered_release_sha256=sha(proof_paths[0].read_bytes()),
            evidence={str(p):sha(p.read_bytes()) for p in proof_paths}),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael B161–B165: 67 independent clean drafts awaiting exact current comparison.',
            next_action='Bind and contextually compare all 67 drafts, then continue B166–B176 in complete exchanges.',
            current_batch_not_yet_integrated=True,prior_B177_B180_integrated_and_credited_once=True,
            native_job_live=False,registered_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael1607_registered_checkpoint_v1_20261105.md',document_text=text,
        completed=13452,protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['parent']:release['parent_sha256'],package['zip']:package['zip_sha256']})
    print('Saved registered Rafael1607 checkpoint and clean-first handoff. Full goal remains active.')
