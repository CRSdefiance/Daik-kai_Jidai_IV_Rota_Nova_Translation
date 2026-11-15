"""Save the two complete offline blocks and next clean drafts without integration credit."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A=Path('work/analysis')
ROOT=A/'Rafael_B166_B167_current1674_20261105'
VISUAL=ROOT/'offline_display_package_v1/visual_review.json'
RECONSTRUCTION=ROOT/'reconstruction_v1/reconstruction.json'
STORED=ROOT/'stored_native_v1/stored_native_verification.json'
STORED_TERMINAL=ROOT/'stored_native_gc_v1/completion.json'
LOOKUP=ROOT/'stored_catalogue_v1/all186_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
DRAFT=A/'Rafael_B161_B180_clean_20261105/B168_clean_drafts_v1.json'
PROSE=Path('translations/rafael_B166_B167_contextual_review_v5.json')
NAMES=Path('translations/rafael_B166_B167_scoped_names_review_v1.json')
RELEASE=A/'Rafael1674_extended_release_verified_v1_20261105/registered_release_verification.json'
PACKAGE=A/'Weekend_testing_package_Rafael1607_20261105/package_verification.json'
REGISTRY=Path('translations/release_stack.json')
BATCH='Rafael_SC0_B166_B167_offline_20261105'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    evidence_paths=(PROSE,NAMES,VISUAL,RECONSTRUCTION,STORED,STORED_TERMINAL,LOOKUP,LOADERS,DRAFT,RELEASE,PACKAGE)
    prose,names,visual,rebuild,stored,terminal,lookup,loaders,draft,release,package=map(load,evidence_paths)
    assert len(prose['records'])==186 and (prose['proposed_revisions'],prose['justified_retentions'])==(146,40)
    assert len(names['records'])==24 and prose['all_individual_four_prose_gates_pass']
    assert all(not r['review']['formatting'] for r in prose['records']+names['records'])
    assert len(prose['current_glyph_defect_records'])==5 and len(prose['current_width_punctuation_records'])==2
    assert visual['all_body_and_name_sheets_directly_viewed'] and visual['body_pages']==187
    assert rebuild['changed_blocks']==[166,167] and rebuild['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert rebuild['all_other_files_components_exact']
    assert rebuild['parent_sha256']==release['candidate_sha256']
    assert package['ROM_sha256']==release['parent_sha256']
    assert rebuild['research_ROM_sha256']==digest(rebuild['research_ROM'])
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==digest(RECONSTRUCTION)
    assert terminal['terminal'] and terminal['completed_without_exception'] and not terminal['garbage_collection']['errors']
    assert stored['complete_stored_pages']==187 and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['fresh_relocated_native_relative_cases']==740
    assert lookup['stored_sha256']==digest(STORED) and len(lookup['records'])==186
    assert lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,4,682)
    assert draft['complete_blocks']==[168] and draft['records_count']==47 and draft['all_five_gates_pending']
    assert digest(REGISTRY)==release['registry_sha256']
    summary=('Rafael B166–B167 has 186 complete contextual decisions, with 146 proposed revisions and 40 justified retentions. '
        'All 187 body pages and 24 default nameplates passed offline and direct visual checks. '
        'Stored parity, 740 branch cases, 343 archive loads and all 186 catalogue lookups passed. '
        'Focused gameplay, Eirene’s in-scene header and registered integration are pending. '
        'B168 has 47 new clean-first drafts. Integrated total remains 13,519.')
    doc=f"""# Rafael B166–B167 offline and stored checkpoint

The [individual contextual ledger](../{PROSE.as_posix()}) contains 186 complete-exchange decisions with exact Japanese and current English references, 146 proposed revisions and 40 justified retentions. It restores the royal audience’s intent, Eirene’s first-person disclosure, Al Ferid Shin’s full introduction and Charlotte’s separate pronunciation guide. Four mixed-width Latin cases and one corrupted initial glyph were corrected. Two width-inconsistent question reactions were normalized. The scoped name review binds 24 public nameplates and the two mentioned names. The previously recorded Dinis full-catalogue デ issue remains a separate field correction.

All 187 final pages were directly reviewed. The king’s page turn follows the complete condition about showing the Pope the seven Proofs. The modal checks preserve the source-authored Eirene headings, the speakers’ left and right positions, the two intentional ellipses and the letter’s Portuguese, pronunciation aid, translated reading and signature. An FE expansion trial exposed a bare I immediately before a break being converted into another glyph. The final native plans avoid that boundary and pass all four alignments. [Offline evidence](../{VISUAL.as_posix()}).

The pinned research ROM `{rebuild['research_ROM_sha256'][:8]}` changes only SC0 B166–B167 over registered Rafael1674. Exact inverses preserve the unowned files, font, graphics, runtime and name tables. All 187 stored planes match their reviewed previews. The original catalogue returns all 186 new stored bodies byte for byte before macro expansion. All 740 relocated branch cases and 343 archive loads passed, with four fresh parent modes and 682 exact reused modes. [Reconstruction](../{RECONSTRUCTION.as_posix()}) and [stored proof](../{STORED.as_posix()}).

Next run focused gameplay for the Pope’s two-page exchange, the staged Eirene and Claudio alternation, the letter sequence, the closing transition and Al’s recruitment. Check the four actor-8 progressive headers against their exact clean presentation commands before deciding whether any scoped alias correction is needed. These are pending runtime checks. The 24 nameplate previews establish only the default header strings. Keep natural activation, original location, chronology and hardware separate from any initialized fixtures. Once ready, register the cumulative successor with all 114 accepted layers, the ASCII right-bound correction, exact clean-input patch and own startup.

The [47 clean B168 drafts](../{DRAFT.as_posix()}) cover Angelo’s recruitment and the linked Mediterranean trade advice. They are ready for current-English binding. B169–B176 has 258 remaining clean drafts and all 305 B168–B176 current comparisons remain open. Preserve the designated main and the Rafael1607 weekend ZIP. Keep the remaining full editorial scope active and deferred artwork and the older-record technical re-audit separate.
"""
    evidence={str(p):digest(p) for p in (*evidence_paths,Path(__file__))}
    checkpoint(mutation=ROOT/'offline_checkpoint_ledger_v1',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0,independently_drafted_records=483,
            independent_draft_blocks=[161,162,163,164,165,166,167,168,177,178,179,180],
            remaining_clean_meanings_anddrafts=258,current_comparisons=436,remaining_current_comparisons=305,
            latest_offline_subset=BATCH,next_clean_first_drafts=str(DRAFT),next_clean_first_drafts_sha256=digest(DRAFT),
            full_intake_not_complete=True),
        new_entries={BATCH:dict(new_credit=0,records=186,blocks=[166,167],proposed_revisions=146,justified_retentions=40,
            all_four_prose_gates_pass=True,all_fifth_gates_pending=True,all_187_offline_and_stored_pages_pass=True,
            registered_integration_pending=True,focused_gameplay_pending=True,research_ROM_sha256=rebuild['research_ROM_sha256'],
            current_review=str(PROSE),current_review_sha256=digest(PROSE),evidence=evidence)},
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,current_batch=summary,
            next_action='Test source-staged FE and actor 8 alias in focused gameplay, then register B166–B167. Bind the B168 clean drafts.',
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael_B166_B167_stored_checkpoint_20261105.md',
        document_text=doc,completed=13519,protected={str(REGISTRY):release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            package['zip']:package['zip_sha256']})
    print('Saved 186 contextual/stored reviews and 47 new clean drafts. Integrated credit remains 13,519.')


if __name__=='__main__':
    main()
