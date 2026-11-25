"""Publish concise registered progress while preserving all earlier work and credit."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B216_B252_clean_20261110')
OUT=Path('work/maria363_B216_B252_release_v1')

def main():
    rp,cp=OUT/'registered_release_verification.json',OUT/'completion_checkpoint.json'
    censuspath=Path('work/story_source_coverage_20261110_SC3_v14/coverage.json')
    release,complete,census=map(load,[rp,cp,censuspath])
    ledger=load('translations/editorial_review_current_v1.json')
    actual=load(ROOT/'gameplay_review_v1.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(722,114,57)
    assert complete['new_credit']==363 and complete['counts']==dict(completed=23070,revised=13778,retained=9292)
    assert ledger['records_editorially_completed']==23070 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    assert len(census['records'])==5129 and len(census['missing'])==1023 and census['new_exact_bindings']==363
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
        release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']}
    assert all(digest(p)==h for p,h in protected.items())
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    assert len(load(release['exact_record_bindings'])['records'])==363
    assert actual['all273_actual_pages_twelve_captions_andthree_host_transitions_directly_viewed']
    registry,prior=map(load,['translations/release_stack.json',OUT/'release_stack_before_Maria363.json'])
    assert registry['latest_promoted_build']==prior['latest_promoted_build']
    evidence={str(p):digest(p) for p in [rp,cp,censuspath,Path('translations/maria363_B216_B252_integrated_final_review_v1.json'),
        *[ROOT/p for p in ['research_completion_v1/research_completion.json','gameplay_review_v1.json','offline_display_approval_v1.json',
            'stored_v1/stored_native_verification.json','registered_preparation_v1/qualification.json','registered_semantic_checks_v1/qualification.json']],
        OUT/'own_registered_startup_verification.json',OUT/'own_registered_name_getters_v1.json',OUT/'own_startup_visual_v1/receipt.json',Path(__file__)]}
    summary=('Maria B216–B252 is registered and credited once:363 reviews,202 revisions,161 justified retentions and29 scoped names. '
        'All353 body pages,12 captions and31 name strings pass. Three initialized emulator samples observe252 bodies/254 unique pages '
        '(273 occurrences),all12 captions,two page turns,32 distinct FE panels andthree sailing returns. Three native FE wrap defects arefixed. '
        'The cumulative722-entry/114-layer candidate passes57 release checks,exact clean-input reconstruction,own startup and24 protected getters. '
        'Integrated23,070;2,828 native story objects remain (Maria1,023;Lil1,805). Main awaits acceptance;full scope remains active.')
    document='docs/editorial_Maria363_B216_B252_registered_20261110.md'
    text=f'''# Maria363 registered candidate — November 10, 2026

{summary}

Use [the cumulative ROM](../{release['candidate'].replace(chr(92),'/')}) (SHA256 `{release['candidate_sha256']}`), its adjacent manifest and clean-input patch. The patch SHA256 is `{release['patch_sha256']}` and reconstructs the complete ROM from clean `{release['clean_input_sha256']}`. Every721-entry predecessor batch,114 accepted layers,earlier profile andruntime fix is preserved. Main remains V4701 until acceptance. This is the candidate prepared for promotion andtesting;the research ROM is not the handoff.

The batch covers37 complete SC3 groups:266 ordinary bodies,85 physical style alternatives and12 captions. Clean meanings andindependent drafts precede existing-English comparison. Exact source/current/registered references,individual findings andretention reasons arein `translations/maria363_B216_B252_integrated_final_review_v1.json`. Allfive individual gates pass. B242R11 restores the working “We must find Jacob's fleet.” after direct review;the quest already establishes his bounty. Earlier proposals remain preserved. Twenty-nine scoped name reviews qualify31 strings;future roster assignments andfull catalogue UI remain unvisited.

All353 final body pages andallnames/captions aredirectly viewed. Fifteen source-bound layouts differ fromthe initial plan,including three FE-specific guard reserves. Native rendering exposed truncated B221R8/R11 text andan extra B221R183 blank row;exact36-cell planning reserves fix these without shortening prose orchanging the engine. The complete question “Where are you from?” retains phrase continuity. Allnative controls,13 FI/FA occurrences,complete leading/internal/trailing characters,bounds,canaries,allocation andpagination pass. Stored checks cover351 effective bodies,131 fresh parity-dependent pages,222 exact reused pages,940 relative cases,303 loads and606 handoffs. Fullclean/current/command/block/archive/NDS inverses pass. No new FE command,padding amendment,font orengine change occurs.

Actual QA isthree disclosed initialized samples/97,683 frames:252 distinct bodies,254 unique pages,273 page occurrences,allfive menus/12 captions,ten effective voice4 style objects,two page turns,34 dismissals of32 distinct FE panels andthree sailing returns. All30 actual body/menu/transition sheets aredirectly viewed. The forest choice returns toanother menu before dialogue;both A presses andboth complete menu planes pass the focused check. The99 remaining bodies,75 other physical style alternatives andruntime selector216 have offline checks only. These hosts retain original setup andcleanup butconcatenate source samples;they do not establish natural activation,earned geography/chronology,original branch/reward/stat outcomes,full routes orhardware. No guide photos arecollected.

The candidate's own31,000-frame title/NewGame/Maria opening reaches Hangzhou. Allsix startup checkpoints areviewed;the opening/town frames match the earlier approved RGB exactly. Its own snapshot proves captain3/route3,all123,264 staged bytes andboth original name getters for12 protected actors. Preserve the Market format andboth pointers,six-section ARM9,registered ASCII right-bound correction,source25v2 andinherited B164R99 fix. Deferred graphics artwork isseparate andunchanged inthis candidate.

Integrated23,070 =13,778 revisions+9,292 retentions. Historical source/prose/draft count23,073. CensusSC3_v14 reuses3,743 exact Maria positions andadds363,leaving1,023 Maria objects plus1,805 Lil objects. Separate shared/player-facing inventories remain. Continue substantial complete exchanges from `work/story_source_coverage_20261110_SC3_v14/residual_clean_source_packet.json`,with clean meanings/drafts before current English. Preserve every storyline,earlier unfinished contextual pass,town/shop/random prose,speaker names,wrap/glyph review,early Rafael/tutorial priority andlater older-record technical re-audit. No worker remains live after this checkpoint.
'''
    mutation=ROOT/'registered_progress_checkpoint_v1'
    checkpoint(mutation=mutation,batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria363 B216–B252 registered andcredited once;next exchanges inSC3_v14.',
            current_batch_not_yet_integrated=False,current_batch_registered_andcredited_once=True,all_current_batch_fifth_gates_pending=False,
            proposed_revisions=202,justified_retentions=161,native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],
            registered_build_live=False,registered_cumulative_build_live=False,registered_profile=release['profile'],
            remaining_native_story_objects=2828,remaining_native_Maria_objects=1023,guide_photos=False,current_batch_evidence=evidence,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Test the cumulative candidate;continue complete SC3_v14 exchanges clean-first without repeating completed checks.'),
        summary=summary,document=document,document_text=text,completed=23070,protected=protected)
    protocol=Path('docs/build_continuity_protocol.md');before=protocol.read_bytes()
    prefix=('Maria363 B216–B252 is registered over Maria321:722 entries,114 accepted layers and57 checks. '
        'Use `scripts/build_registered_maria363_v1.py` and `--register`;pure transaction:`dk4tool/patch/maria363_release_v1.py`. '
        'All363 source objects,353 body pages,clean-input patch,own startup and24 protected getters pass. '
        'Preserve the721-entry prefix,Market format/pointers,six-section ARM9,ASCII right bounds,source25v2 andB164R99 correction. '
        'Main requires acceptance. Continue from [the registered checkpoint](editorial_Maria363_B216_B252_registered_20261110.md);older entries arehistory.\n\n')
    (mutation/'build_continuity_protocol.before').write_bytes(before)
    pending=protocol.with_name('build_continuity_protocol.Maria363.pending.md');assert not pending.exists()
    pending.write_bytes(prefix.encode()+before);assert protocol.read_bytes()==before;os.replace(pending,protocol)
    save(mutation/'build_protocol_update.json',dict(before_sha256=digest(mutation/'build_continuity_protocol.before'),after_sha256=digest(protocol),no_release_orcredit_change=True))
    print('Published Maria363:23070 integrated,2828 native story objects remain;main andfull scope preserved.')

if __name__=='__main__':main()
