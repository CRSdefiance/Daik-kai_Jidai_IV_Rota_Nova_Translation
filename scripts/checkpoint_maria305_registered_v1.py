"""Publish registered mixed305 progress, preserving full scope and earlier evidence."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B176_B195_clean_20261110')
OUT = Path('work/maria305_B176_B195_release_v1')


def main():
    rp = OUT/'registered_release_verification.json'
    cp = OUT/'completion_checkpoint.json'
    census_path = Path('work/story_source_coverage_20261110_SC3_v12/coverage.json')
    release, complete, census = map(load, [rp, cp, census_path])
    ledger = load('translations/editorial_review_current_v1.json')
    actual = load(ROOT/'gameplay_review_v1.json')
    ready = load(ROOT/'research_completion_v1/research_completion.json')
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (720,114,55)
    assert complete['new_credit'] == 305 and complete['counts'] == dict(completed=22386,revised=13405,retained=8981)
    assert ledger['records_editorially_completed'] == 22386 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert len(census['records']) == 5129 and len(census['missing']) == 1707 and census['new_exact_bindings'] == 305
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for p,h in [('translations/release_stack.json',release['registry_sha256']), (release['candidate'],release['candidate_sha256']),
        (release['manifest'],release['manifest_sha256']), (release['patch'],release['patch_sha256'])]:
        assert digest(p) == h
    assert Path(release['candidate']).read_bytes() == Path(release['exact_clean_reconstruction']).read_bytes()
    assert len(load(release['exact_record_bindings'])['records']) == 305
    assert ready['all_individual_five_gates_pass'] and actual['all135_actual_pages_seven_captions_andthree_host_transitions_directly_viewed']
    registry = load('translations/release_stack.json')
    prior = load(OUT/'release_stack_before_Maria305.json')
    assert registry['latest_promoted_build'] == prior['latest_promoted_build']
    packet = load(census_path.with_name('residual_clean_source_packet.json'))
    next_groups = [(g['block'],len(g['records'])) for g in packet['groups'][:12]]
    paths = [rp,cp,census_path,Path('translations/maria305_B176_B195_integrated_final_review_v1.json'),
        ROOT/'research_completion_v1/research_completion.json', ROOT/'gameplay_review_v1.json',
        ROOT/'stored_v1/stored_native_verification.json', ROOT/'reconstruction_v1/reconstruction.json',
        ROOT/'registered_preparation_v2/qualification.json', ROOT/'registered_semantic_checks_v1/qualification.json',
        OUT/'own_registered_startup_verification.json', OUT/'own_registered_name_getters_v1.json',
        OUT/'own_startup_visual_v1/receipt.json', Path(__file__)]
    evidence = {str(p):digest(p) for p in paths}
    summary = ('Maria B176–B195 is registered and credited once: 205 revisions, 100 justified retentions and 27 scoped names. '
        'All 302 body pages, 11 captions and 31 name strings pass. Representative emulator QA observes 127 bodies, '
        '132 unique pages, seven captions, 12 FE panels, five page turns and three sailing returns. '
        'The 720-entry cumulative candidate preserves 114 accepted layers and passes 55 release checks, exact clean-input '
        'reconstruction, own startup and 24 protected getters. Integrated: 22,386. Native story remainder: 3,512 '
        '(Maria 1,707; Lil 1,805). Main and full scope remain unchanged.')
    document = 'docs/editorial_Maria305_B176_B195_registered_20261110.md'
    text = f'''# Maria305 B176–B195 registered checkpoint — November 10, 2026

{summary}

The previous turn completed representative display review and all five gates. This turn integrated the approved batch, checked its own startup, registered the cumulative successor and added 305 disjoint source records exactly once. No worker is live. Continue from this release; preserve every earlier translation, draft, justified retention, ROM and evidence file.

The cumulative [ROM](../work/maria305_B176_B195_release_v1/all_routes_maria305_B176_B195_candidate.nds) has SHA-256 `{release['candidate_sha256']}`. The [clean-input patch](../work/maria305_B176_B195_release_v1/all_routes_maria305_B176_B195_candidate.xdelta) has SHA-256 `{release['patch_sha256']}`. Its [manifest](../work/maria305_B176_B195_release_v1/all_routes_maria305_B176_B195_candidate.manifest.json) has SHA-256 `{release['manifest_sha256']}`. The whole ROM is reconstructed byte for byte from clean input `{release['clean_input_sha256']}`. The original 719 manifest entries, 114 accepted layers and every prior profile remain intact; the successor has 720 entries and 55 passing checks. Only the 19 reviewed SC3 blocks change. Main promotion still requires user acceptance.

Exact clean Japanese/current/registered references, individual findings and justified retentions are in `translations/maria305_B176_B195_integrated_final_review_v1.json` and the release's `exact_integrated_record_bindings.json`. Scope: 272 ordinary bodies, 22 physical crew-message alternatives and 11 captions across 19 complete exchanges, with block 192 already credited earlier. All five individual gates pass. Twenty-seven name reviews bind 54 getters and 31 strings; they do not confer global name-table or catalogue-UI approval.

Editorial changes restore first-person Emilio/Julian speech, matching parrot echoes, the still-Japanese Guan Yu reply, source-supported clue details and uncertainty, gold-seal/retainer ancestry, the Iceland guess and consistent letter signatures. Installed Minotaur Axe, Holy Spear of Ares and Empress Gown terms are preserved. Exact approved names and native substitutions remain intact. [The research checkpoint](editorial_Maria305_B176_B195_research_ready_20261110.md) retains the detailed findings and honest gameplay limits without repeating their history here.

Formatting uses logical prose and `plan_v8/automatic_plans.json`: 26 source-bound layout changes comprise seven earlier page/phrase improvements, 17 additional phrase refinements and two scoped FE guard reserves. One actual blank-row defect in B177R66 is repaired; B184R16 was a matching unfailed risk. Both survive final storage checks. No prose is shortened, source width/font changed, new FE control inserted or page reclaimed. Narrow layout retentions remain individually justified, including the indented Muramasa opening. All 294 bodies/302 pages, 11 captions and 31 name strings were directly reviewed. Native proof selection explicitly reuses 277 exact body proofs and renders 17 changed bodies afresh; it is not a new monolithic rerun.

All 397 commands and 34 relative sites, complete clean/current/block/archive/serialized-ROM inverses, 9,216-byte allocation bounds, 302 stored pages, 294 native effective lookups, 170 native branch cases, 303 loads/cache hits and 606 parent handoffs pass. Three complete style objects preserve 22 physical alternatives/24 aliased slots and 27 compiler rejection cases. Five complete menu objects preserve source indices and pass their 30 provider alignments, 96 bridged returns, 44 current/target style planes and 36 rejection cases. Registration rehearses the complete finalizer without writes and compares every computed final artifact, then reruns the original pure mixed-object reconstruction. Eight changing-input production checks reject while preserving both caller ROMs. The first preparation failed on relative versus absolute producer identity before producing a candidate; its retained successor fixes that evidence-key mismatch without changing prose, bytes or guards.

Actual gameplay consists of three disclosed initialized runs totaling 63,843 frames: 127 distinct source bodies, 132 unique pages and 135 page occurrences, seven captions in three menu objects, 12 FE panels, five two-page turns, 18 source-bound header actors and three ordinary returns to sailing. All 20 review artifacts were directly viewed. Remaining 167 bodies, four captions, four FE panels and 19 physical style alternatives have offline checks only. Each sampled crew-message object uses the observed fallback156/voice4 context; future role assignments remain unvisited. The isolated system-only unlock is disclosed and not earned. Fixtures retain native host setup/effects/cleanup and selected display commands; entire original story scene control flow, original event conditions/locations/branch outcomes, rewards, earned chronology, full routes, catalogue UI and hardware remain unvisited. Guide photographs are not collected.

The candidate's own 31,000-frame ordinary Maria startup reaches Hangzhou. All six key frames were viewed; the opening/town frames match the prior approved RGB exactly. Its own RAM proves captain3/route3, all 123,264 staged bytes, protected data and both original getters for 12 protected names (24 checks). The Market read-only allocation and both pointers, six-section ARM9, ASCII right-bound correction, source25 v2 guard, inherited B164R99 padding correction, earlier fonts/graphics/names and the other three story archives remain exact. The canonical prefix and its completed checks are explicitly reused; fresh SC3 and final four-archive guards are identified as fresh execution. No main promotion, cleanup, commit or push occurred.

Integrated totals are 22,386 = 13,405 revisions + 8,981 justified retentions; historical source/prose/draft total is 22,389. Census v12 reuses 3,117 exact Maria positions and adds 305, leaving 1,707 of 5,129 native SC3 objects. Lil's 1,805 remain separately tracked, for 3,512 native story objects still in scope. These figures exclude separate shared/player-facing inventories and do not establish whole-project completion. Next clean residual exchanges: `{next_groups}` from `work/story_source_coverage_20261110_SC3_v12/residual_clean_source_packet.json`. Seal clean meanings and independent drafts before consulting current English. Full story/town/shop/random/player-prose/name/wrap/glyph scope, earlier unfinished contextual passes and early Rafael/tutorial priority persist. Deferred graphics artwork and the later older-record technical re-audit remain separate.
'''
    mutation = ROOT/'registered_progress_checkpoint_v1'
    checkpoint(mutation=mutation, batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria305 B176–B195 registered and credited once; next exchanges in SC3_v12.',
            current_batch_not_yet_integrated=False,current_batch_registered_andcredited_once=True,
            all_current_batch_fifth_gates_pending=False,proposed_revisions=205,justified_retentions=100,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,registered_profile=release['profile'],remaining_native_story_objects=3512,
            remaining_native_Maria_objects=1707,guide_photos=False,current_batch_evidence=evidence,
            next_action='Select substantial complete SC3_v12 exchanges; seal clean meanings and independent drafts before current comparison.'),
        summary=summary,document=document,document_text=text,completed=22386,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    protocol = Path('docs/build_continuity_protocol.md')
    before = protocol.read_bytes()
    prefix = ('Maria305 B176–B195 is registered over Maria390 B152–B175: 720 entries, 114 accepted layers and 55 checks. '
        'Use `scripts/build_registered_maria305_v1.py` and `--register`; the pure transaction is `dk4tool/patch/maria305_release_v2.py`. '
        'It preserves all source/current/compound/command/relative/inverse guards for 305 source objects in 19 complete SC3 groups: '
        '272 ordinary bodies, 22 physical4100 alternatives and 11 captions. All302 pages pass; no new FE controls or padding amendment. '
        'Exact clean-input patch, own startup and24 protected getters pass. Preserve the719-entry prefix, Market allocation/pointers, '
        'six-section ARM9, ASCII right bounds, source25 v2 and inherited B164R99 correction. Main promotion requires acceptance. '
        'Continue from [the registered checkpoint](editorial_Maria305_B176_B195_registered_20261110.md); earlier entries are history.\n\n')
    (mutation/'build_continuity_protocol.before').write_bytes(before)
    pending = protocol.with_name('build_continuity_protocol.Maria305.pending.md')
    assert not pending.exists()
    pending.write_bytes(prefix.encode()+before)
    assert protocol.read_bytes() == before
    os.replace(pending,protocol)
    save(mutation/'build_protocol_update.json',dict(path=str(protocol),
        before_sha256=digest(mutation/'build_continuity_protocol.before'),after_sha256=digest(protocol),
        registered_release=str(rp),registered_release_sha256=digest(rp),no_release_orcredit_change=True))
    print('Published registered Maria305:22386 integrated,3512 native story objects remain; main and full scope preserved.')


if __name__ == '__main__':
    main()
