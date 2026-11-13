"""Publish the registered390-object checkpoint with exact coverage and no new credit delta."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B152_B175_clean_20261109')
OUT=Path('work/maria390_B152_B175_release_v1')


def main():
    rp=OUT/'registered_release_verification.json';release=load(rp)
    cp=OUT/'completion_checkpoint.json';complete=load(cp)
    censuspath=Path('work/story_source_coverage_20261110_SC3_v11/coverage.json');census=load(censuspath)
    ledger=load('translations/editorial_review_current_v1.json');actual=load(ROOT/'gameplay_review_v1.json')
    ready=load(ROOT/'research_completion_v1/research_completion.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(719,114,54)
    assert complete['new_credit']==390 and complete['counts']==dict(completed=22081,revised=13200,retained=8881)
    assert ledger['records_editorially_completed']==22081 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    assert len(census['records'])==5129 and len(census['missing'])==2012 and census['new_exact_bindings']==390
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for p,h in [(Path('translations/release_stack.json'),release['registry_sha256']),(Path(release['candidate']),release['candidate_sha256']),
        (Path(release['patch']),release['patch_sha256']),(Path(release['manifest']),release['manifest_sha256'])]:assert digest(p)==h
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    bindings=load(release['exact_record_bindings'])['records']
    assert len(bindings)==sum(len(r['registered_native_pages']) for r in bindings)==390
    assert ready['all_individual_five_gates_pass'] and actual['all83_current_pages_five_captions_andfour_host_transitions_directly_viewed']
    registry=load('translations/release_stack.json');prior=load(OUT/'release_stack_before_Maria390.json')
    assert registry['latest_promoted_build']==prior['latest_promoted_build']
    packet=load(censuspath.with_name('residual_clean_source_packet.json'))
    nextgroups=[(g['block'],len(g['records'])) for g in packet['groups'][:12]]
    paths=[rp,cp,censuspath,Path('translations/maria390_B152_B175_integrated_final_review_v1.json'),
        ROOT/'research_completion_v1/research_completion.json',ROOT/'gameplay_review_v1.json',ROOT/'wine_reply_contextual_amendment_v1.json',
        ROOT/'stored_v3/stored_native_verification.json',ROOT/'reconstruction_v3/reconstruction.json',
        ROOT/'reconstruction_v2/FE_storage_alignment.json',OUT/'own_registered_startup_verification.json',
        OUT/'own_registered_name_getters_v1.json',OUT/'own_startup_visual_v1/receipt.json',Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B152–B175 is registered andcredited once:154 revisions/236 justified retentions across24 exchanges and47 scoped name reviews. '
        'Eleven phrase wraps,one premature page,one stored FE blank row andone reopened wine reply are corrected. All373 body pages,17 captions and33 name strings pass. '
        'Four initialized runs verify83 distinct current bodies,five captions,all17 town forecasts,27 FE panels andfour sailing returns. '
        'The719-entry/114-layer cumulative candidate passes54 checks,exact clean-input reconstruction,own startup and24 protected getters. '
        'Integrated22,081;3,817 native story objects remain (Lil1,805/Maria2,012). Main andfull scope are unchanged.')
    document='docs/editorial_Maria390_B152_B175_registered_20261110.md'
    text=f'''# Maria390 B152–B175 registered checkpoint — November 10, 2026

{summary}

All390 original objects now have five individual gates andonce-only integration credit. Exact clean Japanese/current/final references,individual findings,revisions andjustified retentions are in `translations/maria390_B152_B175_integrated_final_review_v1.json` andthe release's `exact_integrated_record_bindings.json`. Full meanings,independent drafts andearlier work remain preserved. Source coverage is24 complete SC3 B152–B175 exchanges:373 bodies and17 captions in8 menus. Names cover47 scoped actors/94 getter references,not a global207-name approval.

Cumulative [ROM](../work/maria390_B152_B175_release_v1/all_routes_maria390_B152_B175_candidate.nds),SHA256 `{release['candidate_sha256']}`. [Clean-input patch](../work/maria390_B152_B175_release_v1/all_routes_maria390_B152_B175_candidate.xdelta),SHA256 `{release['patch_sha256']}`. [Manifest](../work/maria390_B152_B175_release_v1/all_routes_maria390_B152_B175_candidate.manifest.json),SHA256 `{release['manifest_sha256']}`. Clean input:`{release['clean_input_sha256']}`. The patch reconstructs the entire candidate byte forbyte. Preserve all718 predecessor entries and114 accepted layers;54 release checks pass. Only the24 reviewed SC3 blocks change. No main promotion occurred;acceptance remains required.

Editorial findings include seven still-Japanese wine lines,Scents versus Spices,collecting paintings versus painting,unsupported gender/kinship/rank details,hearsay treated asfact,full-width punctuation and50000,the ambiguous delegation caption,private asides andritual repetition. Exact installed Wits,Artwork,China andGlassmaking Guide terms are retained. Namahage andgiyaman preserve their cultural context. Prices andbranch meanings remain exact;predicted popularity does not guarantee trade outcomes. Earlier natural tea-shopping andother good dialogue retain individual reasons.

The full wine exchange exposed one unjustified retention:So what? answered awkwardly with Not atall. Clean 悪いか！ directly asks whether there is a problem. The saved independent draft Got a problem with that? was restored andfreshly tested with both surrounding utterances. This changes the final tally from153/237 to154/236 without adding another source record. Preserve `wine_reply_contextual_amendment_v1.json`,the initial gameplay andevery prior draft ashistory;old captures do not approve changed words.

Final plan:`plan_wine_v4/automatic_plans.json`;native/visual approval:`offline_display_approval_v2.json` and`final_native_v2.json`. All373 final pages have exact native glyph/control/substitution/row/bounds/pagination checks anddirect visual approval. Eleven phrase refinements andone reclaimed124-character bargaining aside preserve every word. Name rendering covers33 strings (18 exact prior planes/15 fresh);all17 captions have source/current/target provider checks,48 alignments,150 bridged returns,68 normal/highlight planes and57 compiler negatives. Logical prose contains no authored ordinary line breaks. Native source widths/fonts remain unchanged.

The stored Calicut dye forecast's automatic trailing space created an extra blank row. `reviewed_FE_storage_padding_v2.py` replaces exactly B164R99 block byte660,20→00,retaining its44-byte command,all offsets/extents/native results/scopes andbranch operands. Four malformed-owner controls reject. The pure registered transaction freshly rebuilds all24 blocks andapplies only this exact source/current-bound padding owner. All679 commands/122 relative sites,9216-byte allocation bounds andcomplete clean/current/block/archive/serialized-ROM inverses pass. No new FE continuation orstyle control is added.

For the wine amendment,one new native page/four alignments were rendered while372 exact body proofs were reused. Only B152 was rebuilt;the other23 groups,including the qualified FE correction,remain exact. Fourteen stored bodies were checked afresh,with359 exact stored-record proofs and610 unchanged branch cases reused;all373 effective-body catalogue lookups andthe new archive's303 loads/606 handoffs pass. See `stored_v3/stored_native_verification.json` for provenance rather than calling those reused cases fresh execution.

Actual gameplay totals four initialized runs/63,284 frames. The current83-body selection combines80 exact compatible earlier body/command/font/runtime proofs withthree fresh corrected wine-context pages. Five captions across two menu objects showboth two-choice options andallthree delegation indices;12 other captions remain offline-only. All17 town forecasts,27 FE panels,the complete wine exchange,the reclaimed aside,50000,Wits,Namahage,Glassmaking Guide andordinary A returns are observed. All24 actual contact sheets were directly viewed. Every host retains seven setup commands andall40 original nonspeech commands andreturns through resupply/departure/sailing. The existing isolated system-only unlock is disclosed andnot earned. Other290 bodies remain offline-only;original conditions/chronology/locations,rewards/stat effects,full route,catalogue UI andhardware remain unvisited. `gameplay_review_v1.json` distinguishes historical plane totals (including the superseded reply) fromthe83 selected current pages.

The cumulative candidate's own31,000-frame startup reaches Hangzhou;all six key frames were viewed. Its own RAM proves captain3/route3,all123264 staged bytes,protected data andboth original getters for12 protected names (24 checks). Market read-only allocation/pointers,six-section ARM9,ASCII right bounds,source25 v2 guard,all earlier name/font/graphics layers andSC0/SC1/SC2 translations remain intact. Eight production scope mutations reject while preserving caller/canonical images. No cleanup,promotion,commit orpush occurred.

Integrated22,081 =13,200 revisions+8,881 retentions;historical source/prose/draft22,084. Censusv11 reuses2727 Maria positions andadds390,leaving2012 of5129. Lil1805 remains separately tracked;native story remainder3817 excludes separate shared/player-facing inventories. Earlier unfinished contextual passes,allstorylines,town/shop/random/player prose andspeaker-label localization remain in scope. Next clean residual groups:`{nextgroups}` from `work/story_source_coverage_20261110_SC3_v11/residual_clean_source_packet.json`. Seal meanings andindependent drafts before current English. Preserve early Rafael/tutorial priority,no guide photos,deferred graphics artwork andthe later older-record technical re-audit. No worker is live.
'''
    mutation=ROOT/'registered_progress_checkpoint_v1'
    checkpoint(mutation=mutation,batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria390 B152–B175 registered andcredited once;next complete exchanges in SC3_v11.',
            current_batch_not_yet_integrated=False,current_batch_registered_andcredited_once=True,all_current_batch_fifth_gates_pending=False,
            proposed_revisions=154,justified_retentions=236,native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],
            registered_build_live=False,registered_cumulative_build_live=False,registered_profile=release['profile'],
            remaining_native_story_objects=3817,remaining_native_Maria_objects=2012,guide_photos=False,
            next_action='Select substantial complete SC3_v11 residual exchanges;clean meanings andindependent drafts before current comparison.',current_batch_evidence=evidence),
        summary=summary,document=document,document_text=text,completed=22081,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    protocol=Path('docs/build_continuity_protocol.md');before=protocol.read_bytes()
    prefix=('Maria390 B152–B175 is registered over Maria335 B137–B151:719 entries,114 accepted layers and54 checks. '
        'Use `scripts/build_registered_maria390_v1.py` and `--register`;pure transaction is `dk4tool/patch/maria390_release_v1.py`. '
        'Own only SC3 B152–B175:390 source objects,373 bodies/pages and17 captions inboth qualified menu arities. '
        'Preserve the exact B164R99 odd-length FE padding correction through `reviewed_FE_storage_padding_v2.py`:block byte660,20→00,unchanged44-byte command. '
        'Do not apply the older even-length two-byte removal helper. Complete inverses/four owner negatives,source-bound reconstruction,current planes andrepresentative gameplay remain required. '
        'No styles ornew FE controls. Exact clean-input patch,own startup and24 protected getters pass. Preserve all718 prefix entries,Market pointers/allocation,six-section ARM9,ASCII bounds andsource25 v2 guard. '
        'Main promotion requires acceptance. Continue from [the registered checkpoint](editorial_Maria390_B152_B175_registered_20261110.md);older entries arehistory.\n\n')
    after=prefix.encode()+before;(mutation/'build_continuity_protocol.before').write_bytes(before)
    pending=protocol.with_name('build_continuity_protocol.Maria390.pending.md')
    assert not pending.exists();pending.write_bytes(after);assert protocol.read_bytes()==before;os.replace(pending,protocol)
    save(mutation/'build_protocol_update.json',dict(path=str(protocol),before_sha256=digest(mutation/'build_continuity_protocol.before'),
        after_sha256=digest(protocol),registered_release=str(rp),registered_release_sha256=digest(rp),no_release_orcredit_change=True))
    print('Published registered Maria390:22081 integrated,3817 native story objects remain;main andfull scope preserved.')


if __name__=='__main__':main()
