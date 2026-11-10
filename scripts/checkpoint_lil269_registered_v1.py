"""Archive the registered269-review successor and preserve all earlier credits and evidence."""
import ast
import gzip
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts import save_editorial_progress_checkpoint_v10 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path('work/Lil269_B243_B282_clean_20261110')
RELEASE = Path('work/lil269_B243_B282_release_v1')
ARCHIVE = Path('translations/editorial_checkpoints/Lil269_registered_20261110_v1')
BATCH = 'Lil_SC2_B243_B282_clean_20261110'


def main():
    assert not ARCHIVE.exists()
    rp = RELEASE / 'registered_release_verification.json'
    release = load(rp)
    complete = load(RELEASE / 'completion_checkpoint.json')
    actual = load(ROOT / 'gameplay_review_v1.json')
    censuspath = Path('work/story_source_coverage_20261110_SC2_v4/coverage.json')
    census = load(censuspath)
    assert complete['new_credit'] == 269 and complete['counts'] == dict(completed=24744, revised=14704, retained=10040)
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (727, 114, 62)
    assert len(census['records']) == 6720 and len(census['missing']) == 1154 and census['new_exact_bindings'] == 269
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    residual = load(censuspath.with_name('residual_clean_source_packet.json'))
    partial = next(g for g in residual['groups'] if g['block'] == 294)
    assert (len(partial['records']), len(partial['complete_clean_context_records']), len(partial['preserved_credited_context_records'])) == (15, 16, 1)
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert (actual['distinct_source_body_objects'], actual['distinct_body_pages'], actual['frames']) == (139, 141, 64563)
    package = Path('releases/all_routes_editorial_20261110_lil269_candidate')
    checksums = load(package / 'checksums.json')
    assert {str(p.relative_to(package)).replace('\\', '/') for p in package.rglob('*') if p.is_file() and p.name != 'checksums.json'} == set(checksums)
    for name, h in checksums.items():
        assert digest(package / name) == h
    final = Path('translations/lil269_B243_B282_integrated_final_review_v1.json')
    doc = load(final)
    assert doc['all269_individual_five_gates_pass'] and len(doc['records']) == 269
    assert all(all(r['review'].values()) for r in doc['records'])
    ledger = load('translations/editorial_review_current_v1.json')
    assert ledger[BATCH]['new_credit'] == 269 and ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    protocol = Path('docs/build_continuity_protocol.md')
    before = protocol.read_bytes()
    lead = ('Lil269 B243–B282 is registered over Lil382:727 entries,114 accepted layers and62 release checks. '
        'Use `scripts/build_registered_lil269_v1.py` and `--register`; pure transaction:`dk4tool/patch/lil269_release_v1.py`. '
        'All269 source reviews,264 body pages,seven captions,exact clean-input patch,own startup and24 protected getters pass. '
        'Preserve all726 predecessor entries,Market format/both pointers,six-section ARM9,ASCII right bounds,source25v2 andB164R99 correction. '
        'Native Lil remainder is1,154; next complete clean groups begin at B283. The B294 residual packet retains15 new objects '
        'and one earlier credited context object in its full16-object exchange; do not drop or recredit that context. '
        'Full goal active; main requires acceptance. Continue from [the registered checkpoint](editorial_Lil269_registered_20261110.md); earlier entries are history.\n\n')
    assert before.startswith(b'Lil382 residual A is registered')
    (RELEASE / 'continuity_before.txt').write_bytes(before)
    content = lead.encode('utf-8') + before
    sibling = protocol.with_name(protocol.name + '.Lil269.pending')
    assert not sibling.exists()
    sibling.write_bytes(content)
    assert protocol.read_bytes() == before
    os.replace(sibling, protocol)
    assert protocol.read_bytes() == content
    save(RELEASE / 'continuity_update.json', dict(path=str(protocol), before_sha256=digest(RELEASE / 'continuity_before.txt'),
        after_sha256=digest(protocol), prior_contents_preserved_as_exact_suffix=True, new_credit=0))
    oldarchive = Path('translations/editorial_checkpoints/Lil269_offline_20261110_v3/archive_manifest.json')
    prior = load(oldarchive)['artifacts']
    files = [p for p in ROOT.rglob('*') if p.is_file() and p.suffix in ['.json', '.txt']]
    files += [p for p in RELEASE.rglob('*') if p.is_file() and p.suffix in ['.json', '.txt']]
    files += [censuspath, censuspath.with_name('residual_clean_source_packet.json'), Path('work/lil269_repository_qa_v1_pytest.xml')]
    ARCHIVE.mkdir(parents=True)
    artifacts, reused = {}, 0
    for p in sorted(set(files)):
        raw = p.read_bytes()
        old = prior.get(str(p))
        if old and digest(p) == old['source_sha256']:
            assert digest(old['archive']) == old['archive_sha256'] and gzip.decompress(Path(old['archive']).read_bytes()) == raw
            artifacts[str(p)] = {**old, 'reused_from': str(oldarchive)}
            reused += 1
        else:
            dest = (ARCHIVE / p.relative_to(Path('work'))).with_suffix(p.suffix + '.gz')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
            assert gzip.decompress(dest.read_bytes()) == raw
            artifacts[str(p)] = dict(archive=str(dest), source_sha256=digest(p), archive_sha256=digest(dest))
    producers = sorted(set(Path('scripts').glob('*lil269*.py')) | {
        Path('dk4tool/patch/lil269_release_v1.py'), Path('scripts/rebuild_reviewed_editorial_batch_v6.py'),
        Path('scripts/check_editorial_stored_explicit_captain_v1.py'), Path('scripts/check_scoped_route_loaders_v1.py'),
        Path('scripts/analyze_rafael_B201_B220_menu_actual_v1.py')})
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, exact_prior_artifacts_reused=reused,
        previous_archive=str(oldarchive), previous_archive_sha256=digest(oldarchive),
        producers={str(p): digest(p) for p in producers}, all_selected_artifacts_lossless=True,
        earlier_archives_andlocal_generated_artifacts_preserved=True, raw_ROM_RAM_captures_andplanes_not_in_git_archive=True,
        all269_individual_five_gates_pass=True, registered_andcredited_once=True, new_credit=0, full_goal_complete=False))
    summary = ('Lil B243–B282 is registered and credited once:269 contextual reviews,104 revisions,165 justified retentions and25 scoped names. '
        'All264 body pages,seven captions and24 name strings pass. Sixteen layouts change,one page is reclaimed and the riddle truncation is fixed. '
        'Three initialized emulator samples observe139 bodies/141 pages,two page turns,21 FE returns and allthree menus;123 bodies remain offline-only. '
        'The cumulative727-entry/114-layer candidate passes62 release checks,exact clean-input reconstruction,own startup,24 protected getters and27 repository tests. '
        'Integrated24,744;native Lil remainder1,154. Testing ROM/patch ready;main awaits acceptance;full goal active;no worker live.')
    document = Path('docs/editorial_Lil269_registered_20261110.md')
    text = f'''# Lil269 cumulative candidate — November 10, 2026

{summary}

Use [the testing ROM](../out/promotion_ready_20261110_lil269_v1/Translation_DS_All_Routes_Lil269_20261110_candidate.nds) and adjacent manifest. ROM SHA-256:`{release['candidate_sha256']}`. [Standalone clean-input patch and notes](../{package.as_posix()}/README.md). Patch SHA-256:`{release['patch_sha256']}`. This successor preserves every726-entry predecessor batch and114 accepted layers, including early Rafael/tutorial work, Market format/both pointers, six-section ARM9, ASCII right bounds, source25v2 andB164R99 correction. Main stays V4701 pending explicit acceptance; the canonical baseline and earlier testing ROMs remain unchanged. The previous goal turn was progress (complete offline display). This turn is progress (storage, representative gameplay, registered integration and once-only credit). Keep the full goal active.

Forty complete clean-source SC2 groups B243–B282 are reviewed:246 ordinary bodies,16 physical personality alternatives andseven captions. Exact source/current/registered references, individual findings,104 revisions,165 justified retentions andallfive gates are in `translations/lil269_B243_B282_integrated_final_review_v1.json`. Clean meanings and independent drafts were sealed before current-English extraction in earlier turns. Preserve those seals, all earlier translations and individual retentions. The scoped25-name review includes24 native strings; full catalogue UI, future role assignments, unconsumed metadata and the broader name review remain separate.

The editorial decisions restore the still-Japanese expedition transport/tavern instructions, Indian Ocean directions, the visited-New-World sailor's rumor, source uncertainty and approved Yuris/Plett/Jacob/Gabriel spellings and identities. The source distinguishes Fernando's ruin alerts, Patron versus Barkeep, floating-ice puzzle directions and two wrong-answer style branches, unnamed figureheads and their blessing/refusal exchanges, Julian's refusal despite a locating reward, Peralonso's deception without romance, Yuris's stolen ship, Plett captured alive, Jacob's cargo and Gabriel/Zaganos reports. All amounts, advances/balances, share changes andLuck/Charm notices remain. Good reactions, humor, character voices and clear clues are retained for individual reasons. No invented kinship, deity title, romance, rank or confirmed death.

Final plan is `plan_v13/automatic_plans.json`:262 bodies/264 pages plus seven captions, zero errors/warnings/failures. Sixteen final layouts change relative to the first plan;14 preserve identical prose andtwo keep the reviewed longer collapsing synonym for the older voice. One figurehead page is reclaimed; the expedition and stolen-ship paragraphs keep coherent two-page continuations. The observed FE riddle consumption failure (108/125 bytes, inserted blank row, lost final question) is fixed with the qualified record-specific FE36 reserve. The matching B251R165 long-row risk receives that reserve too; no separate observed truncation there is claimed. Every final page is directly viewed andbound to native pixels. Earlier failed phrase trials and packing attempts remain preserved and unwaived; no good prose is shortened for fit. Fonts, physical widths, controls and runtime remain unchanged.

Storage freshly reconstructs all40 groups/766 commands/198 relative sites, proving actual clean/current block, whole archive andserialized NDS inverses. Allother files/components match the parent. Every264 stored page passes (117 fresh parity-sensitive,147 exact native reuse),990 native branch cases,262 complete-buffer effective lookups,336 SC2 loads/cache hits and672 handoffs. Source/current style/menu objects recompile exactly;16 slots/18 style negatives,18 menu alignments/60 bridged returns/28 normal-highlight planes/22 menu negatives and24 name strings remain qualified. Every first/internal/final glyph, canary, bound, allocation, macro andpagination guard passes.

Three bounded initialized Lil samples run64,563 frames andobserve139 bodies/141 unique pages, both effective style4 tables, allseven captions, two page turns and21 FE returns between selected bodies. The riddle's full question andnormal A return are directly seen. Actual three-choice cursor indices1/2 andtwo-choice No index1 are seen, with following A returns; the figurehead menu default0 also passes. All18 body/menu/transition sheets are directly viewed andtheir exact original capture tiles checked. The123 other bodies, including14 other personality alternatives, remain offline-only. These samples concatenate source conditional alternatives without their outcomes. The complete native B22 setup/cleanup reaches resupply andthe following steering tutorial. Original event activation, locations, geography, chronology, rewards/stats, branch outcomes, numeric menu return registers/cancellation, free sailing, full-route playthroughs andhardware remain unvisited; return values/cancellation have separate offline checks. No savestate, battery, RAM, roster, RNG orcondition-result override was used in these Lil samples.

The exact cumulative candidate separately passes its own31,000-frame Maria cold boot toHangzhou, six directly viewed captures andboth original getters for12 protected actors. Its preexisting isolated system unlock is disclosed andunearned. All27 fresh repository tests andeight production-scope rejections pass. The first menu analysis used a Maria-only battery wrapper andstopped beforeoutput; the original strict no-battery analyzer correctly binds these Lil samples without replay. The first registration call stopped before registry mutation because the separate getter proof had notyet been generated; all24 getter cases then passed andregistration succeeded. These ordering/wrapper failures are preserved. Both clean-input reconstructions are byte-exact; package checksums pass. Main is unchanged.

Integrated counts are24,744 =14,704 revisions +10,040 retentions. Native Lil census has5,566 exact covered of6,720 positions, leaving1,154; native Maria remains5,129/5,129. Next complete groups begin atB283. The updated residual packet preserves all16 B294 context objects:15 new andone earlier credited line. Its narrow context-preservation correction uses the prior complete context, prevents losing that earlier line andadds no duplicate credit. Reuse the native inventory andcompleted checks.

[Durable evidence archive](../{archive.as_posix()}) preserves every current JSON/TXT receipt, failed/superseded plan, raw-reference ledger, comparison and release proof, reusing earlier compressed artifacts by exact hash. Raw ROM/RAM/captures/planes stay preserved locally. The patch package reconstructs the candidate independently of old work folders. No worker is live.

Continue the remaining full editorial scope from the verified B283 checkpoint: every unfinished storyline/contextual pass, earlier translation, shared shop/town exchange, random scene, player-facing text andbroader speaker-label/name review. Keep early Rafael/tutorial priorities, no guide photos, deferred graphics artwork andthe later older-record technical re-audit. Keep the goal active until that full scope is complete. Do not promote main without user acceptance.
'''
    protected = {'translations/release_stack.json': release['registry_sha256'], release['candidate']: release['candidate_sha256'],
        release['manifest']: release['manifest_sha256'], release['patch']: release['patch_sha256'],
        release['canonical_base']: release['canonical_sha256'], str(final): digest(final),
        'translations/promoted_build.json': digest('translations/promoted_build.json')}
    evidence = {str(p): digest(p) for p in [rp, RELEASE / 'completion_checkpoint.json', censuspath, archive,
        package / 'release_manifest.json', ROOT / 'research_completion_v1/research_completion.json',
        ROOT / 'gameplay_review_v1.json', ROOT / 'offline_display_approval_v1.json', ROOT / 'final_layout_delta_v2.json']}
    checkpoint_source = checked_text(previous.source, {
        "        assert key in prior and isinstance(prior[key],dict) and prior[key].get('new_credit',0)==0":
            "        assert key=='Lil_SC2_B243_B282_clean_20261110' and isinstance(prior[key],dict) and prior[key]['new_credit']==269",
        "        assert value['new_credit']==0 and key not in [batch_key,'latest_checkpoint']":
            "        assert value['new_credit']==269 and key not in [batch_key,'latest_checkpoint']",
    })
    env = {**previous.checkpoint.__globals__, '__file__': __file__}
    exec(compile(checkpoint_source, __file__ + '::same-atomic-checkpoint-preserving-earned269-credit', 'exec'), env)
    env['checkpoint'](mutation=ROOT / 'registered_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil269 registered and credited once; cumulative testing ROM and clean-input patch ready.',
            current_batch_not_yet_integrated=False, current_batch_registered_andcredited_once=True, all_current_batch_fifth_gates_pending=False,
            proposed_revisions=104, justified_retentions=165, current_batch_evidence=evidence, no_batch_worker_live=True,
            guide_photos=False, previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            next_action='Continue remaining1154 native Lil positions from complete B283 source context; retain B294 earlier credited context. Full shared/player-facing/name scope remains active; main acceptance is separate.'),
        additional_updates={BATCH: dict(new_credit=269, registered_release_verification_sha256=digest(rp),
            native_rendering_pending=False, direct_visual_review_pending=False, stored_checks_pending=False, gameplay_pending=False,
            all_fifth_gates_pending=False, all_current_batch_fifth_gates_pending=False, all_individual_fifth_gates_still_pending=False,
            final_formatting_bodies=262, final_formatting_pages=264, source_bound_layout_changes=16, pages_reclaimed=1,
            provisional_formatting_superseded_by_final_approved_plan=True, all_individual_five_gates_pass=True,
            registered_integration_pending=False, no_batch_worker_live=True, full_goal_complete=False, evidence=evidence)},
        summary=summary, document=document, document_text=text, completed=24744, protected=protected)
    for p, item in artifacts.items():
        assert digest(p) == item['source_sha256']
    print(dict(registered_records=269, lossless_artifacts=len(artifacts), prior_artifacts_reused=reused,
        integrated=24744, native_Lil_remaining=1154, new_checkpoint_credit=0, full_goal_complete=False))


if __name__ == '__main__':
    main()
