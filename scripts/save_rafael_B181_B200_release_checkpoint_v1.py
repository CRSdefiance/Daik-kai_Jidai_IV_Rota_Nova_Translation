"""Record the reviewed B181–B200 batch and the exact next clean intake."""
from pathlib import Path
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.finalize_rafael_B181_B200_research_v1 import SOURCE
from scripts.qualify_rafael_B201_B220_clean_census_v1 import OUT as NEXT_CENSUS
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint


A=Path('work/analysis')
RESEARCH=A/'Rafael_B181_B200_research_final_v3_20261106/research_completion.json'
PARENT=A/'Rafael2165_extended_release_verified_v1_20261105/registered_release_verification.json'
PACKAGE=A/'Weekend_testing_package_Rafael2165_20261105/package_verification.json'
RELEASE=A/'Rafael2549_extended_release_verified_v1_20261106/registered_release_verification.json'
REGISTRY=Path('translations/release_stack.json')
INTAKE='Rafael_SC0_B181_B200_clean_20261105'
BATCH='Rafael_SC0_B181_B200_research_20261106'
NEXT='Rafael_SC0_B201_B220_clean_20261106'
PRIORITY='editorial_execution_priority_20261104'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    research,parent,package,census=map(load,(RESEARCH,PARENT,PACKAGE,NEXT_CENSUS))
    assert research['all_individual_five_gates_pass']
    assert (research['records'],research['revisions'],research['retentions'])==(384,317,67)
    assert (research['actual_source_variants'],research['offline_only_source_variants'],research['scoped_public_names'])==(148,236,29)
    assert (census['clean_objects'],census['independent_drafts'],census['remaining_clean_drafts'])==(403,138,265)
    assert census['source_only_no_current_English_extracted'] and census['zero_already_credited_keys']
    assert parent['candidate_sha256']==package['ROM_sha256'] and digest(package['zip'])==package['zip_sha256']
    integrated=sys.argv[1:]==['--integrated']
    protected={str(REGISTRY):digest(REGISTRY),parent['canonical_base']:parent['canonical_sha256'],
        parent['candidate']:parent['candidate_sha256'],parent['patch']:parent['patch_sha256'],
        package['zip']:package['zip_sha256']}
    files=[RESEARCH,PARENT,PACKAGE,NEXT_CENSUS,Path(__file__)]
    new_entries={}
    changes=dict(new_credit=0, independently_drafted_records=384,current_comparisons=384,
        contextual_comparison_records=384,remaining_current_comparisons=0, remaining_clean_meanings_anddrafts=0,
        latest_research_subset=BATCH,next_clean_intake=NEXT,all_384_individual_five_research_gates_pass=True,
        all_384_offline_and_stored_pages_pass=True,observed_speeches=148,observed_pages=148,
        observed_headers=29,offline_only_speeches=236,focused_gameplay_pending=False)
    if integrated:
        release,credit=map(load,(RELEASE,RELEASE.with_name('completion_checkpoint.json')))
        assert credit['new_credit']==384 and credit['counts']==dict(completed=14394,revised=8407,retained=5987)
        assert release['registry_sha256']==protected[str(REGISTRY)] and release['parent_sha256']==parent['candidate_sha256']
        assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(688,114,26)
        assert release['only_owned_SC0_blocks_changed']==list(range(181,201))
        assert release['clean_input_patch_byte_exact'] and release['all_eight_registered_final_stages_preserved']
        assert not release['own_registered_startup_pending']
        protected.update({release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256']})
        files.extend((RELEASE,RELEASE.with_name('completion_checkpoint.json')))
        summary=(f"Rafael B181–B200 is registered and credited once, with 317 revisions and 67 justified retentions. "
            f"Experimental {release['candidate_sha256'][:8]} passed 688 entries, 114 accepted layers, eight final stages, 26 checks, "
            "exact clean-input reconstruction and its own Rafael startup. Integrated total is 14,394. "
            "B201–B220 has 403 clean objects and 138 clean drafts. Rafael2165 remains the weekend package.")
        release_detail=(f"The {link('registered experimental ROM',release['candidate'])} has SHA-256 `{release['candidate_sha256']}`. "
            f"Its {link('clean-input patch',release['patch'])} rebuilt it byte for byte. All 26 release checks and the exact ROM's own Rafael startup passed. "
            f"{link('Release verification',RELEASE)}.")
        count, suffix=14394,'registered'
        changes.update(integrated_subbatch_credit=384,integrated_blocks=list(range(181,201)),full_intake_not_complete=False,
            registered_integration_pending=False,subset_registered_release=str(RELEASE),subset_registered_release_sha256=digest(RELEASE))
    else:
        summary=('Rafael B181–B200 has 384 five-gate reviews with 317 revisions and 67 justified retentions. '
            'All 384 pages passed offline and stored checks. The initialized emulator fixtures showed 148 pages, all 27 FE panels and 29 nameplates. '
            'Registered verification is pending. Integrated credit remains 14,010. B201–B220 has 138 clean drafts.')
        release_detail='The research ROM changes only the reviewed 20 SC0 blocks. Registered release verification and completion credit are pending.'
        count,suffix=14010,'research_ready'
        changes.update(integrated_subbatch_credit=0,full_intake_not_complete=True,registered_integration_pending=True)
        new_entries[BATCH]=dict(new_credit=0,records=384,blocks=list(range(181,201)),proposed_revisions=317,justified_retentions=67,
            all_individual_five_research_gates_pass=True,observed_speeches=148,observed_pages=148,offline_only_speeches=236,
            observed_headers=29,registered_integration_pending=True,focused_gameplay_pending=False,
            current_review=research['manuscript'],current_review_sha256=research['manuscript_sha256'],
            evidence={str(p):digest(p) for p in files})
        new_entries[NEXT]=dict(new_credit=0,source_records=403,typed_captions=21,source_only=True,
            independently_drafted_records=138,independent_draft_blocks=list(range(201,209)),remaining_clean_meanings_anddrafts=265,
            remaining_current_comparisons=403,current_comparisons=0,full_intake_not_complete=True,
            evidence={str(NEXT_CENSUS):digest(NEXT_CENSUS)})
    doc=f"""# Rafael B181–B200 {suffix.replace('_',' ')} checkpoint

{summary}

{release_detail}

All 384 bodies were viewed and checked, including two corrected full-width I glyphs, six translated wine lines, the Scents notice and 42 fresh visual refinements across story and town. Stored proof covers 42 relocated branch sites, 210 native branch cases, 384 original catalogue reads and all 343 archive loads. Two initialized emulator runs displayed 148 pages across story and town, including all 27 FE panels, all 13 forecasts and all 29 scoped nameplates. The other 236 speeches remain offline-only. Original event activation, economic effects, locations, chronology and physical hardware remain open. {link('Five-gate evidence',RESEARCH)}.

B201–B220 contains 382 speeches and 21 captions across ten choice menus. The 138 clean drafts include all 12 captions for the six independent merchant offers in B208. Continue the other 265 clean drafts before comparing the registered English. {link('Clean intake',NEXT_CENSUS)}.

The designated main and the {link('Rafael2165 weekend ZIP',package['zip'])} are preserved. Keep the deferred artwork and later technical re-audit separate.
"""
    changes['evidence']={str(p):digest(p) for p in files}
    checkpoint(mutation=SOURCE/f'{suffix}_documentation_checkpoint',batch_key=INTAKE,batch_updates=changes,
        additional_updates={PRIORITY:dict(new_credit=0,
            current_batch='Rafael B201–B220 clean-first dialogue and menu intake.',
            next_action='Continue clean drafts, then bind all complete exchanges to the verified cumulative ROM.',
            current_batch_not_yet_integrated=True,guide_photos=False)},
        new_entries=new_entries,summary=summary,document=f'docs/editorial_Rafael_B181_B200_{suffix}_20261106.md',
        document_text=doc,completed=count,protected=protected)
    print(f'Saved {suffix} B181–B200 checkpoint and B201–B220 clean intake.')


if __name__=='__main__':
    main()
