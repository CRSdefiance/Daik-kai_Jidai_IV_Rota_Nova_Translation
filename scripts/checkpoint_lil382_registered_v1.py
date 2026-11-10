"""Archive the completed batch and publish an exact, credit-preserving handoff."""
import ast
import gzip
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts import save_editorial_progress_checkpoint_v10 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Lil382_residual_A_clean_20261110')
RELEASE=Path('work/lil382_residual_A_release_v1')
ARCHIVE=Path('translations/editorial_checkpoints/Lil382_registered_20261110_v1')
BATCH='Lil_SC2_residual_A_382_clean_20261110'


def main():
    assert not ARCHIVE.exists()
    rp=RELEASE/'registered_release_verification.json';release=load(rp)
    complete=load(RELEASE/'completion_checkpoint.json')
    actual=load(ROOT/'gameplay_review_v1.json')
    censuspath=Path('work/story_source_coverage_20261110_SC2_v3/coverage.json');census=load(censuspath)
    assert complete['new_credit']==382 and complete['counts']==dict(completed=24475,revised=14600,retained=9875)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(726,114,61)
    assert len(census['records'])==6720 and len(census['missing'])==1423 and census['new_exact_bindings']==382
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert (actual['distinct_source_body_objects'],actual['distinct_body_pages'],actual['frames'])==(211,217,82563)
    package=Path('releases/all_routes_editorial_20261110_lil382_candidate')
    checksums=load(package/'checksums.json')
    assert {str(p.relative_to(package)).replace('\\','/') for p in package.rglob('*') if p.is_file() and p.name!='checksums.json'}==set(checksums)
    for name,h in checksums.items():assert digest(package/name)==h
    assert load(package/'release_manifest.json')['candidate_sha256']==release['candidate_sha256']
    final=Path('translations/lil382_residual_A_integrated_final_review_v1.json');doc=load(final)
    assert doc['all382_individual_five_gates_pass'] and len(doc['records'])==382
    assert all(all(r['review'].values()) for r in doc['records'])
    ledger=load('translations/editorial_review_current_v1.json')
    assert ledger[BATCH]['new_credit']==382 and ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    files=[p for p in ROOT.rglob('*') if p.is_file() and p.suffix in ['.json','.txt']
           and 'checkpoint' not in str(p.relative_to(ROOT)).lower() and 'pytest_temp' not in str(p.relative_to(ROOT)).lower()]
    files += [p for p in RELEASE.rglob('*.json') if p.is_file()]
    files += [censuspath,censuspath.with_name('residual_clean_source_packet.json')]
    files += [Path(f'work/lil382_repository_qa_v{i}/pytest.xml') for i in [1,2,3]]
    ARCHIVE.mkdir(parents=True);artifacts={}
    for p in sorted(set(files)):
        relative=p.relative_to(Path('work'))
        dest=(ARCHIVE/relative).with_suffix(p.suffix+'.gz');dest.parent.mkdir(parents=True,exist_ok=True)
        raw=p.read_bytes();dest.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));assert gzip.decompress(dest.read_bytes())==raw
        artifacts[str(p)]=dict(archive=str(dest),source_sha256=digest(p),archive_sha256=digest(dest))
    producers=sorted(set(Path('scripts').glob('*lil382*.py'))|{
        Path('scripts/approve_scoped_clean_offline_v2.py'),Path('scripts/check_scoped_clean_menus_v3.py'),
        Path('scripts/check_scoped_route_loaders_v1.py'),Path('scripts/record_editorial_contact_visual_review_v1.py'),
        Path('scripts/bind_reviewed_fixture_menu_returns_v2.py'),Path('dk4tool/patch/lil382_release_v1.py'),
        Path('dk4tool/script/reviewed_credited_context_rebuild_v1.py')})
    for p in producers:ast.parse(p.read_bytes(),filename=str(p))
    archive_manifest=ARCHIVE/'archive_manifest.json'
    save(archive_manifest,dict(artifacts=artifacts,producers={str(p):digest(p) for p in producers},
        all_selected_artifacts_lossless=True,earlier_archives_andlocal_generated_artifacts_preserved=True,
        raw_ROM_RAM_captures_andplanes_not_in_git_archive=True,all382_individual_five_gates_pass=True,
        registered_andcredited_once=True,new_credit=0,full_goal_complete=False))
    summary=('Lil residual A is registered and credited once: 382 contextual reviews, 257 revisions, 125 justified retentions and 34 scoped names. '
        'All 386 body pages, four captions and 42 name strings pass. Thirty layouts improve and five pages are reclaimed. '
        'Three initialized emulator samples observe 211 bodies/217 pages, six page turns, two FE returns and both default menu returns; '
        '167 bodies remain offline-only. The cumulative 726-entry/114-layer candidate passes 61 release checks, exact clean-input reconstruction, '
        'own startup, 24 protected getters and 27 repository tests. Integrated 24,475; native Lil remainder 1,423. '
        'The test ROM and patch package are ready. Main awaits acceptance; full editorial goal remains active; no worker is live.')
    document='docs/editorial_Lil382_registered_20261110.md'
    text=f'''# Lil382 cumulative candidate — November 10, 2026

{summary}

Use [the testing ROM](../out/promotion_ready_20261110_lil382_v1/Translation_DS_Lil382_promotion_candidate.nds) and adjacent manifest. ROM SHA-256: `{release['candidate_sha256']}`. [Standalone clean-input patch and release notes](../releases/all_routes_editorial_20261110_lil382_candidate/README.md). Patch SHA-256: `{release['patch_sha256']}`. This successor preserves all 725 predecessor entries and all 114 accepted layers, including early Rafael/tutorial work, Market format and both pointers, six-section ARM9, ASCII right bounds, source25 v2 and B164R99 padding correction. Main stays V4701 pending explicit acceptance; the canonical baseline is unchanged. Earlier ROMs, translations, drafts, retentions, failures and evidence remain preserved.

Thirty complete clean-source SC2 groups are reviewed: B0–B19, B21, B115 and B235–B242. The 382 eligible source objects comprise 364 ordinary bodies, 14 physical personality alternatives and four captions. The nine earlier B115 context objects are retained without duplicate credit. Clean meanings and independent English drafts were sealed before current-English extraction. Exact source/current/registered references, individual findings, revisions, justified retentions and all five gates are in `translations/lil382_residual_A_integrated_final_review_v1.json`. The 34 scoped names retain 42 consumer strings. Full catalogue UI layouts, future conditional role assignments and the broader name review remain separate.

The contextual decisions restore Gerhard's refusal to lose and his parting with the object; starboard-quarter naval orders; Aziza's two-million demand/one-million settlement, father's accidental death, grief and keepsake motive, voluntary retirement and recruitment; Manuel's three-stanza sea/mother poem; Maria/Xien's cross-story opposition to slave trading, pillage and indiscriminate revenge; Fernando as Jam's gambling opponent; Francisca's precious birthday glass rose and uncertain thief/price; Gabriel's escape; and the distinct figurehead attempts, refusal and blessing. Good reactions, voices, humor, source uncertainty and cultural context are retained for individual reasons. No invented romance, kinship, rank, killer, shipwreck or arrest. Approved names and exact item/commodity/Proof terminology remain bound. Twelve mixed-width punctuation records receive ASCII proposals; the original fonts and source controls remain unchanged.

Final plan is `plan_v7/automatic_plans.json`: 378 bodies/386 pages plus four separately checked captions, zero errors, warnings or failures. Thirty actual final byte layouts improve relative to v1; 391 pages become 386 without shortening prose or changing widths, fonts or runtime. Viewed refinements keep short tags and phrases together and improve page density. The eight remaining two-page paragraphs retain complete continuations; B115R102's emphatic final sentence remains on page two after the valid one-page attempt failed packing limits. The Demon-Piercing Arrow title keeps its ordinary soft wrap rather than adding a page or shortening its exact name. Failed plans and superseded preferences are preserved.

All final pages are directly viewed and bound to native pixels. There are 1,512 selected alignments, two complete style objects/16 native slots/18 compiler negatives, two menus/four captions/12 alignments/36 bridged returns/16 normal-highlight planes/14 negatives and 42 name planes (16 fresh, 26 exact compatible reuse). Storage passes all 386 pages (180 fresh parity-sensitive, 206 exact reuse), 555 native relative cases, 378 native effective-body lookups, 336 SC2 archive loads/cache hits and 672 parent handoffs. Every relevant native instruction, control, substitution, complete first/internal/final glyph, canary, bound, allocation and pagination guard passes.

The initial common allocator stopped at B115's earlier relocated context before emitting a ROM. The narrowly scoped successor preserves all nine context objects, verifies exact credited source bindings, uses declared current-coordinate projections and proves both the actual canonical Japanese and current-parent inverses. Its actual-clean inverse partitions nested 0100 commands at exclusive command boundaries. Five ownership/source/macro mutations are rejected. No completed prose or visual checks were repeated. The final pure release transaction freshly reconstructs all 30 groups and every individual registered reference, whole archive and serialized parent inverse. Eight production-scope mutations are rejected. The native census initially stopped at the already partially credited B294 exchange; v2 preserves its one credited line explicitly as context alongside the 15 remaining source objects.

Three bounded initialized emulator samples run 82,563 frames, observing 211 bodies/217 pages, both effective voice4 objects, all four captions, six two-page turns, two FE message/A returns and both default menu/A returns. All 24 actual body/menu/transition contact sheets are directly viewed. The 167 other bodies, including 12 personality alternatives and the Frozen Rose handover notice, are offline-only. The initial selection purpose mentioned Frozen Rose, but B241 was not copied: no actual handover claim is made. Requested DOWN inputs preceded menu opening; only cursor index 0 was observed. Both native cursor styles and return indices are checked separately offline. Complete Lil B22 host setup/cleanup remains intact; each sample reaches resupply and the following native steering tutorial. Free sailing, natural optional activation, original conditional outcomes/rewards/geography/chronology, full-route playthroughs and hardware are unvisited. No savestate, battery, RAM, roster or conditional override was used in these three Lil samples.

The cumulative candidate's separate own 31,000-frame Maria cold boot reaches Hangzhou with six directly viewed captures and 24 original protected-name getter results. The preexisting system-only route unlock is disclosed and unearned; no story progression is inferred from it. All 27 selected repository tests pass with terminal exit 0. The first two attempts had temporary-directory setup errors; the third uses a fresh directory beneath an existing workspace parent. No product test assertion was waived. The first package producer hit the out-junction write permission boundary after creating a valid prefix; v2 verifies that exact prefix and resumes the remaining work. Both patch reconstructions are byte-exact; package checksums pass. These failures remain preserved.

Integrated counts are 24,475 = 14,600 revisions + 9,875 retentions. Native Lil census has 5,297 covered of 6,720 positions, leaving 1,423; native Maria remains 5,129/5,129. The next residual packet begins at B243. Reuse this census and completed checks. [Durable evidence archive](../{archive_manifest.as_posix()}) preserves exact compressed JSON/TXT receipts, plans, failures and references; raw ROM/RAM/captures/planes remain local. The patch package supports exact clean-input reconstruction independently of those historical work folders. No worker is live.

This is progress on the full goal, not completion. Every unfinished storyline/contextual pass, earlier translation, shared shop/town exchange, random scene, remaining player-facing text and broader speaker-label/name review stays in scope. Keep early Rafael/tutorial priorities, no guide photos, deferred graphics artwork and the later older-record technical re-audit. Do not promote main without user acceptance.
'''
    protected={'translations/release_stack.json':release['registry_sha256'],
        release['candidate']:release['candidate_sha256'],release['manifest']:release['manifest_sha256'],
        release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256'],
        str(final):digest(final),'translations/promoted_build.json':digest('translations/promoted_build.json')}
    evidence={str(p):digest(p) for p in [rp,RELEASE/'completion_checkpoint.json',censuspath,archive_manifest,package/'release_manifest.json',ROOT/'research_completion_v1/research_completion.json',ROOT/'gameplay_review_v1.json',ROOT/'offline_display_approval_v1.json',ROOT/'final_layout_delta_v1.json']}
    # This scoped extension preserves the already-earned 382 credits while clearing
    # obsolete pending flags. All other atomic checkpoint/prefix/hash guards remain.
    checkpoint_source=checked_text(previous.source, {
        "        assert key in prior and isinstance(prior[key],dict) and prior[key].get('new_credit',0)==0":
            "        assert key=='Lil_SC2_residual_A_382_clean_20261110' and isinstance(prior[key],dict) and prior[key]['new_credit']==382",
        "        assert value['new_credit']==0 and key not in [batch_key,'latest_checkpoint']":
            "        assert value['new_credit']==382 and key not in [batch_key,'latest_checkpoint']",
    })
    env={**previous.checkpoint.__globals__,'__file__':__file__}
    exec(compile(checkpoint_source,__file__+'::same-atomic-checkpoint-preserving-registered382-credit','exec'),env)
    env['checkpoint'](mutation=ROOT/'registered_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Lil382 registered and credited once; cumulative testing ROM and clean-input patch ready.',
            current_batch_not_yet_integrated=False,current_batch_registered_andcredited_once=True,all_current_batch_fifth_gates_pending=False,
            proposed_revisions=257,justified_retentions=125,current_batch_evidence=evidence,no_batch_worker_live=True,guide_photos=False,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Test the new cumulative candidate for acceptance; continue remaining1423 native Lil source objects from B243 without restarting completed source/display/release checks. Preserve full shared/player-facing/name scope.'),
        additional_updates={BATCH:dict(new_credit=382,registered_release_verification_sha256=digest(rp),
            native_rendering_pending=False,direct_visual_review_pending=False,stored_checks_pending=False,gameplay_pending=False,
            all_fifth_gates_pending=False,all_current_batch_fifth_gates_pending=False,all_individual_fifth_gates_still_pending=False,
            final_formatting_bodies=378,final_formatting_pages=386,source_bound_layout_changes=30,pages_reclaimed=5,
            provisional_formatting_superseded_by_final_approved_plan=True,all_individual_five_gates_pass=True,
            registered_integration_pending=False,no_batch_worker_live=True,full_goal_complete=False,evidence=evidence)},
        summary=summary,document=document,document_text=text,completed=24475,protected=protected)
    for p,item in artifacts.items():assert digest(p)==item['source_sha256']
    print('PASS registered Lil382 handoff, durable evidence archive and credit-preserving checkpoint; full goal active.')


if __name__=='__main__':main()
