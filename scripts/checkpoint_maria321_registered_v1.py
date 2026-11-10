"""Publish registered321 progress while retaining all earlier scope and evidence."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B196_B215_clean_20261110')
OUT = Path('work/maria321_B196_B215_release_v1')


def main():
    rp, cp = OUT/'registered_release_verification.json', OUT/'completion_checkpoint.json'
    censuspath = Path('work/story_source_coverage_20261110_SC3_v13/coverage.json')
    release, complete, census = map(load,[rp,cp,censuspath])
    ledger = load('translations/editorial_review_current_v1.json')
    actual = load(ROOT/'gameplay_review_v1.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks']) == (721,114,56)
    assert complete['new_credit'] == 321 and complete['counts'] == dict(completed=22707,revised=13576,retained=9131)
    assert ledger['records_editorially_completed'] == 22707 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert len(census['records']) == 5129 and len(census['missing']) == 1386 and census['new_exact_bindings'] == 321
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for path,h in [('translations/release_stack.json',release['registry_sha256']),
        (release['candidate'],release['candidate_sha256']),(release['manifest'],release['manifest_sha256']),
        (release['patch'],release['patch_sha256'])]: assert digest(path) == h
    assert Path(release['candidate']).read_bytes() == Path(release['exact_clean_reconstruction']).read_bytes()
    assert len(load(release['exact_record_bindings'])['records']) == 321
    assert actual['all178_actual_pages_four_captions_andthree_host_transitions_directly_viewed']
    registry, prior = map(load,['translations/release_stack.json',OUT/'release_stack_before_Maria321.json'])
    assert registry['latest_promoted_build'] == prior['latest_promoted_build']
    packet = load(censuspath.with_name('residual_clean_source_packet.json'))
    nextgroups = [(g['block'],len(g['records'])) for g in packet['groups'][:12]]
    paths = [rp,cp,censuspath,Path('translations/maria321_B196_B215_integrated_final_review_v1.json'),
        *[ROOT/p for p in ['research_completion_v1/research_completion.json','gameplay_review_v1.json',
            'stored_v1/stored_native_verification.json','reconstruction_v1/reconstruction.json',
            'registered_preparation_v1/qualification.json','registered_semantic_checks_v1/qualification.json',
            'name_header_transition_v1.json']],OUT/'own_registered_startup_verification.json',
        OUT/'own_registered_name_getters_v1.json',OUT/'own_startup_visual_v1/receipt.json',Path(__file__)]
    evidence = {str(p):digest(p) for p in paths}
    summary = ('Maria B196–B215 is registered and credited once: 171 revisions, 150 justified retentions and 24 scoped names. '
        'All 325 body pages, four captions and 28 name strings pass. Representative emulator QA observes 156 bodies/162 unique pages, '
        'four captions, six page turns, one FE return and three sailing returns. The 721-entry cumulative candidate preserves114 accepted '
        'layers and passes56 release checks, exact clean-input reconstruction, own startup and24 protected getters. '
        'Integrated22,707;3,191 native story objects remain (Maria1,386;Lil1,805). Main andfull scope remain unchanged.')
    document = 'docs/editorial_Maria321_B196_B215_registered_20261110.md'
    text = f'''# Maria321 B196–B215 registered checkpoint — November 10, 2026

{summary}

This turn integrated the previously approved321-record batch, verified the candidate's own startup andregistered it before adding321 disjoint source records exactly once. The full goal remains active. No worker is live. All earlier ROMs,translations,retentions,drafts andevidence remain preserved.

Use the cumulative [ROM](../work/maria321_B196_B215_release_v1/all_routes_maria321_B196_B215_candidate.nds), SHA256 `{release['candidate_sha256']}`; [clean-input patch](../work/maria321_B196_B215_release_v1/all_routes_maria321_B196_B215_candidate.xdelta), SHA256 `{release['patch_sha256']}`; and [manifest](../work/maria321_B196_B215_release_v1/all_routes_maria321_B196_B215_candidate.manifest.json), SHA256 `{release['manifest_sha256']}`. The patch reconstructs the whole candidate byte forbyte from clean `{release['clean_input_sha256']}`. The exact720-entry predecessor prefix,114 accepted layers andevery old profile are preserved; the successor has721 entries/56 passing checks. Only18 SC3 groups change. ARM9,COMMON,other story archives,names,font andgraphics remain exact toMaria305. Main promotion still requires acceptance.

Exact Japanese/current/registered references,individual findings andretentions arein `translations/maria321_B196_B215_integrated_final_review_v1.json` and `exact_integrated_record_bindings.json` beside the ROM. Scope:296 ordinary bodies,21 physical crew-message alternatives andfour captions across18 complete exchanges. Allfive individual gates pass. Twenty-four name reviews bind48 getters/28 strings; this doesnot grant global name-table,full catalogue UI orfuture roster approval. The inherited draft-only provisional-label flag iscleared in the integrated copy after source-bound name/term review andregistration; alloriginal drafts andfinal review artifacts remain untouched.

[The research checkpoint](editorial_Maria321_B196_B215_research_ready_20261110.md) retains the contextual corrections,justified retentions andexact display evidence. Nineteen source-bound layouts improve andone premature Jam letter page isreclaimed without shortening prose. The additional strength-of-mind refinement receives two fresh native/visual pages;316 matching body proofs are reused. All325 final pages,four captions and28 names aredirectly viewed. Complete mixed-object compilation,433 commands/24 relative sites,allsource/current/block/archive/NDS inverses,allocation,317 effective lookups,120 branch cases,303 loads and606 handoffs pass. The pure registered transaction rehearses every original finalizer guard without writes,compares allcomputed artifacts andpasses eight production-scope rejections while preserving both caller images. No new FE control,padding amendment,font orengine change occurs.

Actual coverage isthree disclosed initialized runs:156 distinct bodies,162 unique pages (178 occurrences),allfour captions inboth menus,figurehead cursor0/1,six page turns,one Frozen Rose FE return andthree sailing returns. The161 remaining bodies,figurehead success/FI Spirit panel andunsampled voice alternatives have offline checks. Source-bound test hosts retain all47 original setup/effect/cleanup commands. They do not claim natural activation,original geographical progression,earned chronology,rewards,numeric modal registers,complete original branches,full routes orhardware. The extra+4-frame Priest capture remains unapproved animation evidence; two later complete holds pass andno ROM change orreplay isneeded. All22 actual review sheets aredirectly viewed. No guide photos arecollected.

The candidate's own31,000-frame ordinary Maria New Game reaches Hangzhou. Allsix checkpoints areviewed; opening/town RGB matches prior approved frames exactly. Its own RAM proves captain3/route3,all123,264 staged bytes,protected data andboth original getters for12 protected actors. Preserve the Market read-only16-byte format/both pointers,six-section ARM9,ASCII right-bound correction,source25v2 andinherited B164R99 correction. The canonical prefix/proofs areexplicitly reused; the changed SC3 andfinal four-archive guards run fresh. No main promotion,cleanup,commit orpush occurs.

Integrated22,707 =13,576 revisions+9,131 retentions; historical source/prose/draft22,710. Census v13 reuses3,422 exact Maria positions andadds321, leaving1,386 of5,129. Lil's1,805 remain,for3,191 native story objects; separate shared/player-facing inventories stillremain. Next clean groups:`{nextgroups}` from `work/story_source_coverage_20261110_SC3_v13/residual_clean_source_packet.json`. Select substantial complete exchanges andseal clean meanings/independent drafts before current English. Preserve fullstory/town/shop/random/player-prose/name/wrap/glyph scope,earlier unfinished contextual passes andearly Rafael/tutorial priority. Deferred graphics artwork andlater older-record technical re-audit remain separate.
'''
    mutation = ROOT/'registered_progress_checkpoint_v1'
    checkpoint(mutation=mutation,batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria321 B196–B215 registered andcredited once;next exchanges inSC3_v13.',
            current_batch_not_yet_integrated=False,current_batch_registered_andcredited_once=True,
            all_current_batch_fifth_gates_pending=False,proposed_revisions=171,justified_retentions=150,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,registered_profile=release['profile'],remaining_native_story_objects=3191,
            remaining_native_Maria_objects=1386,guide_photos=False,current_batch_evidence=evidence,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Select substantial complete SC3_v13 exchanges;seal clean meanings andindependent drafts before current comparison.'),
        summary=summary,document=document,document_text=text,completed=22707,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    protocol = Path('docs/build_continuity_protocol.md'); before = protocol.read_bytes()
    prefix = ('Maria321 B196–B215 is registered over Maria305 B176–B195:721 entries,114 accepted layers and56 checks. '
        'Use `scripts/build_registered_maria321_v1.py` and `--register`;pure transaction:`dk4tool/patch/maria321_release_v1.py`. '
        'Preserve allsource/current/compound/command/relative/inverse guards for321 source objects in18 complete SC3 groups:296 ordinary bodies,21 physical4100 alternatives andfour captions. '
        'All325 pages,exact clean-input patch,own startup and24 protected getters pass. No new FE control orpadding amendment. '
        'Preserve the720-entry prefix,Market allocation/pointers,six-section ARM9,ASCII right bounds,source25v2 andinherited B164R99 correction. '
        'Main requires acceptance. Continue from [the registered checkpoint](editorial_Maria321_B196_B215_registered_20261110.md);older entries arehistory.\n\n')
    (mutation/'build_continuity_protocol.before').write_bytes(before)
    pending = protocol.with_name('build_continuity_protocol.Maria321.pending.md'); assert not pending.exists()
    pending.write_bytes(prefix.encode()+before); assert protocol.read_bytes() == before
    os.replace(pending,protocol)
    save(mutation/'build_protocol_update.json',dict(path=str(protocol),before_sha256=digest(mutation/'build_continuity_protocol.before'),
        after_sha256=digest(protocol),registered_release=str(rp),registered_release_sha256=digest(rp),no_release_orcredit_change=True))
    print('Published registered Maria321:22707 integrated,3191 native story objects remain;main andfull scope preserved.')


if __name__ == '__main__':
    main()
