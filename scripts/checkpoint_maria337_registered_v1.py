"""Publish once-only registered progress and the next exact clean-source checkpoint."""
import os
from pathlib import Path
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint


def main():
    releasepath=Path('work/maria337_release_v1/registered_release_verification.json');release=load(releasepath)
    completepath=Path('work/maria337_release_v1/completion_checkpoint.json');complete=load(completepath)
    censuspath=Path('work/story_source_coverage_20261109_SC3_v9/coverage.json');census=load(censuspath)
    ledger=load('translations/editorial_review_current_v1.json');actual=load(ROOT/'gameplay_review_v1.json')
    ready=load(ROOT/'research_completion_v1/research_completion.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(717,114,52)
    assert complete['new_credit']==337 and complete['counts']==dict(completed=21356,revised=12861,retained=8495)
    assert ledger['records_editorially_completed']==21356 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    assert len(census['records'])==5129 and len(census['missing'])==2737 and census['new_exact_bindings']==337
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for p,h in [(Path('translations/release_stack.json'),release['registry_sha256']),
        (Path(release['candidate']),release['candidate_sha256']),(Path(release['patch']),release['patch_sha256']),
        (Path(release['manifest']),release['manifest_sha256'])]:assert digest(p)==h
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    bindings=load(release['exact_record_bindings'])['records']
    assert len(bindings)==sum(len(r['registered_native_pages']) for r in bindings)==337
    assert ready['all_individual_five_gates_pass'] and actual['all52_selected_pages_two_captions_andboth_host_transitions_directly_viewed']
    packet=load(censuspath.with_name('residual_clean_source_packet.json'));nextgroups=[(g['block'],len(g['records'])) for g in packet['groups'][:16]]
    evidence={str(p):digest(p) for p in [releasepath,completepath,censuspath,Path('translations/maria337_integrated_final_review_v1.json'),
        ROOT/'research_completion_v1/research_completion.json',ROOT/'gameplay_review_v1.json',
        Path('work/maria337_release_v1/own_registered_startup_verification.json'),Path('work/maria337_release_v1/own_registered_name_getters_v1.json'),Path(__file__)]}
    summary=('Maria337 is registered and credited once: 224 revisions/113 justified retentions across12 exchanges and21 scoped name reviews. '
        'Four tutorial page boundaries and eight phrase wraps improve; two mixed-font lines and two corrupt captions are repaired. '
        'All339 body pages,two captions and28 name strings pass. Two emulator runs observe48 source bodies/52 pages,both menu options, '
        'all four tutorial page turns,six FE panels and both sailing returns. The cumulative717-entry/114-layer candidate passes52 checks, '
        'exact clean-input reconstruction,own startup and24 protected getters. Integrated21,356;4,542 native story objects remain '
        '(Lil1,805/Maria2,737). Main and the full objective are unchanged.')
    text=f'''# Maria337 registered checkpoint — November 9, 2026

**337 original source objects are integrated once: 224 revisions and113 justified retentions in12 complete exchanges.** All five individual gates pass. The21 scoped name/role reviews retain28 reviewed strings. `translations/maria337_integrated_final_review_v1.json` and `work/maria337_release_v1/exact_integrated_record_bindings.json` preserve exact clean Japanese/current/final references, findings, changes and retention reasons. Earlier independent drafts, unsuccessful trials, ROMs and all evidence are preserved.

Cumulative [ROM](../work/maria337_release_v1/all_routes_maria337_candidate.nds), SHA-256 `{release['candidate_sha256']}`. [Clean-input patch](../work/maria337_release_v1/all_routes_maria337_candidate.xdelta), SHA-256 `{release['patch_sha256']}`. [Manifest](../work/maria337_release_v1/all_routes_maria337_candidate.manifest.json), SHA-256 `{release['manifest_sha256']}`. The patch exactly reconstructs the ROM from clean `{release['clean_input_sha256']}`. The716-entry predecessor prefix and114 accepted layers remain;52 release checks pass. Only SC3 blocks125–136 change. No new FE controls are inserted and no extra source credit is counted. This is a registered testing candidate; main is unchanged and promotion requires acceptance.

Editorial findings include the unexplained fever encounter and family-loss progression, merchant responsibility and grief, dance context, uncertainty, humor and restored agency. Two old gambling captions (`産es`/`札ecline`) become `I'll play.`/`No, thanks.`. Two full-width-I records contain three corrected letters. Carlo Sinat and Cesare Tony body introductions now agree with current name consumers; Fernando's first name is restored. Unsupported sir and third-person self-reference are removed. Ceremonial Knife, Sun-Crest Sheath and the exact installed Help terminology remain source/current bound. The dating pair retain Man/Woman without invented marriage. See [the prose checkpoint](editorial_Maria337_prose_layout_20261109.md) for full contextual findings and exact reference receipts; do not redo those reviews.

The final V5 formatter covers335 speech bodies/339 pages, with zero warnings or waivers. Four tutorial page boundaries preserve the quantity rule, cargo consequence, equipment recommendation and ship-retention recommendation. Eight phrase fixes keep where she is, on you, the Admiral question tag, dead weight, all price thresholds/range, Supplies holds, over there and each other together. No prose is shortened; zero pages are reclaimed. Thirty-five original and four changed-layout sheets were directly viewed. The final selection reuses327 exact body proofs and refreshes8, with1340 selected alignment cases. All28 name strings and both corrected captions were also viewed. Fifteen exact prior name planes are reused and13 are fresh. Old corrupt-caption provider bytes are verified without approving their ASCII font output; all four target normal/highlight planes and all provider/selection/cancel/compiler guards pass.

All335 stored bodies and339 pages pass complete glyph/control/macro/canary/bounds/pagination checks. Storage uses176 fresh parity pages and163 exact reuses. All335 effective catalogue lookups,430 branch cases,303 full archive loads/cache hits and606 parent handoffs pass. All610 commands and86 relative sites are mapped, every block stays within9216 bytes, and clean/current/block/archive/serialized-ROM inverses are exact. Refer to [the stored checkpoint](editorial_Maria337_stored_20261109.md); no completed check needs repeating unless dependencies or behavior change.

**Observed gameplay is representative, not a natural playthrough.** Two fresh ordinary-controller initialized runs total33,202 frames:48 distinct source bodies/52 pages,106 complete body-plane matches,94 complete header matches and six complete menu samples. All four tutorial page turns and following-source returns, six FE panels and named returns, both repaired I lines, Carlo/Cesare/Fernando introductions, both caption selections and normal A returns pass. All14 actual body/menu/transition sheets were directly viewed. Both complete source-bound hosts return through resupply/departure to sailing. The existing isolated system-only unlock is disclosed and not earned. Original chronology/locations, optional conditions, minigame, branch outcomes, rewards, stats, catalogue UI and hardware remain unvisited. The other287 source bodies have complete offline coverage. Exact IDs and evidence are in `gameplay_review_v1.json`.

The candidate's own fresh31,000-frame startup reaches Hangzhou; all six key frames were viewed. Captain/route3, current staged payload/protected data and24 original protected-name getters pass. Registered Market read-only allocation/pointers, six-section ARM9, ASCII right-bound correction, source25 v2 guard, earlier name stages, fonts, graphics and prior SC0/SC1/SC2 translations remain intact. No promotion, cleanup, commit or push occurred.

Integrated totals:21,356 =12,861 revisions+8,495 retentions. Historical source/prose/draft counts remain21,359. The source census reuses2055 exact covered positions and adds337, leaving2737 of5129 Maria objects; Lil1805 remains separately tracked. Total native story remainder4542 is not a count of all shared/player-facing prose. All earlier unfinished contextual passes, town/shop/random exchanges and names/role labels remain in scope.

**Next: select substantial complete exchanges from `work/story_source_coverage_20261109_SC3_v9/residual_clean_source_packet.json`.** First groups: `{nextgroups}`. Read clean Japanese, seal meanings and independent drafts before exposing current English. Reuse qualified unchanged technical dependencies; every changed text still needs fresh formatting and generated-page review. Preserve early Rafael/tutorial priority, all earlier coverage and the full objective. Deferred graphics artwork and the later older-record technical re-audit remain separate. No guide photos and no live worker.
'''
    mutation=ROOT/'registered_progress_checkpoint_v1'
    checkpoint(mutation=mutation,batch_key='editorial_execution_priority_20261104',batch_updates=dict(new_credit=0,
        current_batch='Maria337 registered and credited once; next complete exchanges in SC3_v9.',current_batch_not_yet_integrated=False,
        all_current_batch_fifth_gates_pending=False,proposed_revisions=224,justified_retentions=113,current_batch_registered_andcredited_once=True,
        native_job_live=False,native_sessions=[],registered_build_live=False,registered_cumulative_build_live=False,registered_profile=release['profile'],
        remaining_native_story_objects=4542,remaining_native_Maria_objects=2737,guide_photos=False,
        next_action='Select complete SC3_v9 residual exchanges; clean meanings and independent drafts before current-English comparison.',current_batch_evidence=evidence),
        summary=summary,document='docs/editorial_Maria337_registered_20261109.md',document_text=text,completed=21356,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    protocol=Path('docs/build_continuity_protocol.md');before=protocol.read_bytes()
    prefix=('Maria337 is registered over Maria330:717 entries,114 accepted layers and52 passing checks. '
        'Use `scripts/build_registered_maria337_v1.py` and `--register`; pure transaction is `dk4tool/patch/maria337_release_v1.py`. '
        'Own only SC3 blocks125–136:337 source objects,335 speech bodies/339 pages andtwo captions. No style objects or new FE continuations. '
        'Complete inverses,exact clean-input patch,own startup and24 protected getters pass. Preserve the716-entry prefix,Market allocation/pointers, '
        'six-section ARM9,ASCII right bounds andv2 source25 guard. Main promotion requires acceptance. '
        'Continue from [the registered checkpoint](editorial_Maria337_registered_20261109.md);older entries below are history.\n\n')
    after=prefix.encode()+before;(mutation/'build_continuity_protocol.before').write_bytes(before)
    pending=protocol.with_name('build_continuity_protocol.Maria337.pending.md');assert not pending.exists();pending.write_bytes(after)
    assert protocol.read_bytes()==before;os.replace(pending,protocol)
    save(mutation/'build_protocol_update.json',dict(path=str(protocol),before_sha256=digest(mutation/'build_continuity_protocol.before'),
        after_sha256=digest(protocol),registered_release=str(releasepath),registered_release_sha256=digest(releasepath),no_release_orcredit_change=True))
    print('Published registered Maria337:21,356 integrated;4,542 native story objects remain;main/full scope preserved.')


if __name__=='__main__':main()
