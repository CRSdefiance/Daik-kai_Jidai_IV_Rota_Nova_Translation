"""Save the verified tutorial successor and the next batch's completed body-page review."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

RELEASE_ROOT=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104')
DISPLAY_ROOT=Path('work/analysis/Rafael_B51_B60_formatting_20261104')
SOURCE_ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')

if __name__=='__main__':
    release_path=RELEASE_ROOT/'registered_release_verification.json';startup_path=RELEASE_ROOT/'own_registered_startup_verification.json'
    completion_path=RELEASE_ROOT/'completion_checkpoint.json';display_path=DISPLAY_ROOT/'body_display_approval_v4.json'
    release,startup,completion,display=map(load,[release_path,startup_path,completion_path,display_path])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert completion['counts']==dict(completed=10525,revised=6254,retained=4271)
    assert display['body_pages']==253 and display['changed_layout_records']==38
    assert startup['actual_captain_getter']==startup['actual_route_word']==0
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path)
    backup=RELEASE_ROOT/'pins_before_final_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    for rom in Path('work/rtn7').rglob('*.nds'):
        if not any(Path(p['path']).resolve()==rom.resolve() for p in pins):
            pins.append(dict(path=str(rom.resolve()),reason='Preserve all seven-stage build intermediates. SHA256 '+sha(rom.read_bytes())))
    save(pins_path,pins)
    summary=('Four shared tutorials and two catalogue fields are registered and verified: 10525 completions (6254 revisions/4271 retentions). '
        'Experimental 4b10fd67 passes 667 entries/114 accepted layers/seven stages, exact clean-input patch and own Rafael startup; main unchanged. '
        'Next Rafael B51–B60 has 249 prose reviews (102 revisions/147 retentions), 253 final offline body pages and four choice captions visually approved; '
        '38 wrap fixes/three I fixes. Fernan’s F correction passes exclusive ownership/four native planes/eight negatives, pending latest-parent rebase/deployment. '
        'Headers, stored scripts, representative gameplay and integration remain for the 249 records. No live jobs; full scope/all prior work/ROMs retained; no guide photos.')
    document=Path('docs/editorial_rafael_tutorial_release_and249_display_20261104.md')
    text=f'''# Verified tutorial update and next Rafael display checkpoint — 2026-11-04

Rafael’s early story and all tutorials remain first. The full editorial objective is active. Completed work, translations, justified retentions, earlier evidence and all ROMs remain preserved. Graphics artwork and the later older-record technical re-audit remain separate. No main promotion, commit/push, pruning or guide-photo collection.

## Verified cumulative release

Candidate: `{release['candidate']}`

SHA256: `{release['candidate_sha256']}`

Profile: `{release['profile']}`. Parent: `{release['parent']}`, SHA256 `{release['parent_sha256']}`. The immutable canonical main remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `{release['canonical_sha256']}`.

Only six typed ARM9 data spans differ from that verified parent: four shared tutorial paragraphs and the two catalogue middle-name fields. All other internal files/components, code, fonts, pointer tables, allocations and unowned bytes are exact. The complete seven-stage pipeline preserves all earlier runtime/name stages, including ASCII right bounds. Manifest: 667 entries, 114 accepted layers, {release['passing_release_checks']} passing checks. Build54457, release verifier51343 and own-startup verifier80250 are terminal exit0.

Clean-input patch: `{release['patch']}`, SHA256 `{release['patch_sha256']}`. Clean input SHA256: `{release['clean_input_sha256']}`. Whole-ROM reconstruction is byte-exact. Release proof: `{release_path}`. Startup proof: `{startup_path}`. Own 4001-frame Rafael cold boot matches all ten previously reviewed RGB frames; actual captain0/route0, complete staged payload, current getters and protected names pass without historical RAM overlay.

The four panels are credited exactly once: one First Mate wording revision, three justified retentions and four phrase/wrap fixes. Total10525 complete,6254 revisions/4271 retentions; source/prose/draft counters10528 retain their historical difference of three. Pedro de Valdes and Barbarossa Fazul Hayreddin are deployed as two separate name corrections with zero dialogue credit. Progressive names remain unchanged. Completion/bindings: `{completion_path}` and `{RELEASE_ROOT/'integrated_record_bindings.json'}`. The superseded single First Mate draft receives no duplicate credit.

Coverage remains honest: the four special paragraphs and full catalogue UI were not activated live. They have complete native/visual/stored/connected proofs; the 21400-frame ordinary UI run verifies seven existing bodies on the same unchanged consumer. Own startup is actual gameplay, not proof of those conditional paragraphs, natural route completion or hardware behavior. All build intermediates and rejected preparation/reference ROMs are pinned and preserved.

## Next249 records: completed prose and body display

B51–B60 has245 speeches plus four answers in two complete choice objects:102 revisions/147 retentions. The source meanings and drafts preceded current-English extraction. Exact source/current references, individual findings and retentions remain in `{SOURCE_ROOT/'B51_B60_249_contextual_prose_review_v1.json'}`. The English manuscript is `translations/rafael_B51_B60_contextual_editorial_manuscript_v1.json`. Numerical block order is not chronology; branch alternatives remain separate.

All253 final body pages and both complete menu sheets are directly viewed and approved offline. Initial25 sheets cover253 pages; nine refreshed sheets cover42 pages; the final sheet covers four pages for the last two boundary corrections. Native glyphs, complete leading/trailing characters, substitutions, control prefixes, width, consumption and pagination pass. Four menu captions pass16 style planes,12 provider alignments,36 bridged modal returns and14 negative cases. These are native/offline tests, not actual menu-controller or story activation coverage.

Final body proof: `{display_path}`. Combined native receipt: `{DISPLAY_ROOT/'combined_native_v4.json'}`. Final plans/preferences: `{DISPLAY_ROOT/'automatic_v4/automatic_plans.json'}` and `{DISPLAY_ROOT/'visual_preferences_v4.json'}`. There are38 changed layouts and three ASCII-I corrections in two retained speeches. Logical paragraphs are unchanged by layout refinements; native geometry, fonts and runtime stay fixed. Exact compiled bytes permit207 original-native reuses,36 first-refresh reuses and two fresh final records. Do not replay all245 checks.

The private planner stops treating sentence boundaries as broken phrases and penalizes sparse nonterminal middle rows. Record-bound phrase/page preferences preserve the greeting, question tags, phrasal verbs, named expressions and successor-page readability. Three worse projections were rejected because they added pages ending in fragments; the corresponding original one-page layouts remain. One exact QA retention is grammatical: `The whole town chipped in,` ends in a complete phrasal verb. The original warning is archived; only that bound line is retained. Final plans have zero errors/warnings, and every changed page received fresh native and visual checks. The two final page repairs keep enormous profits together and preserve both the Proof predicate and the complete insult noun phrase; the latter conditional still crosses the native page boundary explicitly.

All249 individual formatting gates remain false until remaining header/storage/representative checks pass. This packet has zero new completion credit and zero actual target-story observations. The now-completed tutorial release’s gameplay evidence must not be misattributed to it.

## Names and immediate next steps

Fernan Silveira’s mixed-font initial is source-bound to actor35’s exclusive given-name field. Proposal/ownership: `work/analysis/Rafael_Fernan_name_field_20261104/owned_fields_proposal.json`. Native proof: `work/analysis/Rafael_Fernan_name_native_20261104/native_name_fields_verification.json`. Both original getters, four current/proposed style planes, all character/bounds proofs, eight negatives and whole ARM9 inverse pass. All four planes were directly viewed. The spelling remains Fernan; only the full-width F becomes ordinary ASCII. It is not deployed. Its proof parent is ee04bf6f: rebase the proposal to newly verified4b10fd67 using the six disjoint data spans, exact current fields/actor inputs and code/font dependencies before production. Reuse existing name planes when that dependency proof passes.

Actor40’s full-name middle componentＦong remains a separate source-aware Fong/von review, not an automatic rename. Spoken Antony Kuhn is bound to exact source/current fields. Complete the18 scoped progressive-name/role decisions and name-plane bindings; retain approved names and avoid brother/uncle/feudal implications in generic role labels. Full catalogue metadata and global207-name approval remain separate where unreviewed.

Next: reconcile new4b10fd67 with the uncredited249-record packet (SC0/COMMON/font/code are unchanged; six declared data spans explain ARM9 differences), finish headers and source-owned Fernan field integration, rebuild/store the complete mixed speech/menu blocks, reuse validated branch/loaders, then run representative story/pagination/menu transitions and register the successor. Keep all four choice answers, label-free2000 controls, three FE notices and complete source preambles. Do not restart the completed prose/body review. Preserve later Hodram drafts and every remaining storyline/shared/town/random/player-facing text obligation.
'''
    checkpoint(mutation=RELEASE_ROOT/'release_and249_display_checkpoint_mutation_v1',
        batch_key='Rafael_SC0_B51_B60_contextual_20261104',
        batch_updates=dict(new_credit=0,body_display_approval=str(display_path),body_display_approval_sha256=sha(display_path.read_bytes()),
            offline_native_body_pages=253,all_body_pages_andfour_captions_directly_viewed=True,wrap_findings_resolved=38,
            full_width_I_glyphs_fixed_in_proposed_text=3,Fernan_name_field_native_andvisual_qualified=True,
            latest_registered_parent_reconciliation_pending=True,stored_headers_actual_andregistered_integration_pending=True,
            remaining=['Latest4b10fd67 dependency/name-field rebase','Scoped18 headers/roles andname planes','Complete mixed-block storage/loaders',
                'Representative gameplay/menu/pagination transitions','Registered cumulative successor/patch/once-only credit']),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael_SC0_B51_B60_contextual_20261104',shared_four_tutorials_registered_andcredited_once=True,
            Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True)},
        summary=summary,document=document,document_text=text,completed=10525,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],'out/raphael_natural_v2_accepted_base.nds':release['canonical_sha256']})
    print('Saved verified4b10fd67 and253 reviewed body pages;10525 completions,249 records still uncredited;full goal active.')
