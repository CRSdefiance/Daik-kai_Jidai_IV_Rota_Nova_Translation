"""Publish the cumulative testing checkpoint while preserving earlier credit and the full goal."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B253_B274_clean_20261110')
OUT=Path('work/maria359_B253_B274_release_v1')

def main():
    rp,cp=OUT/'registered_release_verification.json',OUT/'completion_checkpoint.json'
    release,complete=map(load,[rp,cp]);actual=load(ROOT/'gameplay_review_v1.json')
    censuspath=Path('work/story_source_coverage_20261110_SC3_v15/coverage.json');census=load(censuspath)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(723,114,58)
    assert complete['new_credit']==359 and complete['counts']==dict(completed=23429,revised=13997,retained=9432)
    assert len(census['records'])==5129 and len(census['missing'])==664 and census['new_exact_bindings']==359
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    registry,prior=map(load,['translations/release_stack.json',OUT/'release_stack_before_Maria359.json'])
    assert registry['latest_promoted_build']==prior['latest_promoted_build']
    delta=load(ROOT/'final_layout_delta_v1.json');assert delta['final_changed_record_count']==34
    evidence={str(p):digest(p) for p in [rp,cp,censuspath,Path('translations/maria359_B253_B274_integrated_final_review_v1.json'),
        *[ROOT/p for p in ['research_completion_v1/research_completion.json','gameplay_review_v1.json','offline_display_approval_v1.json',
            'stored_v1/stored_native_verification.json','stored_catalogue_all_v1/all_stored_effective_body_bindings.json',
            'final_layout_delta_v1.json','registered_preparation_v1/qualification.json','registered_semantic_checks_v1/qualification.json']],
        OUT/'own_registered_startup_verification.json',OUT/'own_registered_name_getters_v1.json',OUT/'own_startup_visual_v1/receipt.json',Path(__file__)]}
    summary=('Maria B253–B274 is registered and credited once: 359 contextual reviews, 219 revisions, 140 justified retentions and18 scoped names. '
        'All350 body pages, ten captions and21 name strings pass. Three initialized emulator samples observe164 bodies/165 pages, '
        'allfive menus, one page turn, eleven FE returns andthree sailing returns. Thirty-four final layouts improve andone page is reclaimed. '
        'The cumulative723-entry/114-layer candidate passes58 release checks, exact clean-input reconstruction, own startup and24 protected getters. '
        'Integrated23,429;2,469 native story objects remain (Maria664;Lil1,805). Main awaits acceptance;full editorial scope remains active.')
    document='docs/editorial_Maria359_B253_B274_registered_20261110.md'
    text=f'''# Combined Maria359 candidate — November 10, 2026

{summary}

Use [the cumulative test ROM](../{release['candidate'].replace(chr(92),'/')}) and its adjacent manifest. ROM SHA256: `{release['candidate_sha256']}`. The clean-input patch SHA256 is `{release['patch_sha256']}`; clean input SHA256 is `{release['clean_input_sha256']}`. The standalone GitHub package is `releases/all_routes_editorial_20261110_maria359_candidate/`. This is prepared for testing and promotion. Main remains V4701 pending acceptance. Every722-entry predecessor batch and114 accepted layers remain intact, including Rafael/tutorial work, the Market Trade-screen correction, ASCII right bounds, source25v2, six-section ARM9 andthe B164R99 padding repair. No artwork changes are included.

The latest batch covers22 complete SC3 groups:218 ordinary bodies,131 physical personality alternatives andten captions. All359 clean meanings andindependent drafts were sealed before current-English comparison. Exact source/current/registered references, individual findings andretention reasons arein `translations/maria359_B253_B274_integrated_final_review_v1.json`;allfive individual gates pass. Eighteen scoped name reviews retain21 validated strings. The review preserves the one-month Lime Drops loan,20,000-coin reward,scurvy rumor,30-day demonstration against a normal40-day journey,uncertain ruins clues,Chinese palace cuisine,Islamic boarding tactics andthe game's own carronade description. It avoids invented relationships andjoint gift-giving. Source B271R223 retains actor18, verified asCharles Rochefort, despite the Japanese line's feminine wording.

All350 final body pages,21 name strings andten captions were directly viewed. Two full-width I letters andone full-width question mark are corrected. Thirty-four final compiled layouts differ fromthe initial plan;351 planned pages become350 without shortening prose. The cure explanation fits one page, while London's final strange-people thought stays together onits second page. The exact cure article-ending soft wrap is documented andnative-checked;no native glyph,bounds,width orcontrol guard is waived. `final_layout_delta_v1.json` corrects the informational35-layout tally in the preserved v1 research receipt to34;no text,ROM,proof orreview gate changes. All349 bodies/1,396 selected alignments,18 complete style objects/144 slots/162 compiler negatives,ten captions/30 alignments/90 modal returns/40 normal-highlight planes/35 compiler negatives andallscoped name strings pass.

Storage passes350 pages,349 effective native body lookups,1,015 relocated branch cases,303 loads and606 handoffs,plus complete clean/current/command/block/archive/serialized-ROM inverses. Eight production scope mutations are rejected while caller images remain exact. Three initialized emulator samples run70,803 frames:164 distinct bodies/165 pages,allfive menus/ten captions,twelve effective voice4 alternatives,one London page turn,eleven FE returns andthree sailing returns. All22 body/menu/transition sheets aredirectly viewed. The185 remaining bodies and119 other physical personality alternatives have offline native/stored checks only. These disclosed hosts preserve setup andcleanup but concatenate conditional samples;they do not establish natural activation,original event outcomes,rewards,earned geography orchronology,full routes orhardware. No guide photos are collected.

The candidate's own31,000-frame title/NewGame/Maria opening reaches Hangzhou. Allsix startup checkpoints areviewed;the unchanged opening/town captures match prior approved RGB exactly. Its own snapshot verifies captain3/route3,123,264 staged bytes andboth original getters for12 protected actors. The complete clean-input patch reconstructs the candidate byte for byte. The723-entry manifest passes58 release checks, preserving the entire accepted prefix. Selected repository tests total27 passing after two temporary-directory setup errors were rerun successfully;the errors did not indicate code failures.

Integrated23,429 =13,997 revisions+9,432 retentions;historical source/prose/draft count23,432. Native story remainder2,469 =Maria664+Lil1,805;shared/player-facing inventories remain separate. Next clean Maria source is `work/story_source_coverage_20261110_SC3_v15/residual_clean_source_packet.json`. Preserve prior coverage,ROMs,translations,retentions andevidence. Continue unfinished contextual reviews across every storyline andshared/shop/town/random/player-facing prose,with early Rafael/tutorial priority,names,wraps andtext glyph consistency. Deferred graphics artwork andthe later older-record technical re-audit remain separate. The full goal remains active. No batch worker islive.
'''
    checkpoint(mutation=ROOT/'registered_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria359 B253–B274 registered andcredited once;combined candidate prepared for testing andpromotion.',
            current_batch_not_yet_integrated=False,current_batch_registered_andcredited_once=True,all_current_batch_fifth_gates_pending=False,
            proposed_revisions=219,justified_retentions=140,qualified_scoped_names=18,current_batch_actual_gameplay_observations=164,current_batch_actual_gameplay_pages=165,
            current_batch_evidence=evidence,native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,no_batch_worker_live=True,guide_photos=False,previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Hand off the combined testing candidate;continue from SC3_v15 residual scope without repeating completed checks.'),
        summary=summary,document=document,document_text=text,completed=23429,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    continuity=Path('docs/build_continuity_protocol.md');old=continuity.read_text(encoding='utf-8')
    prefix=('Maria359 B253–B274 is registered over Maria363:723 entries,114 accepted layers and58 release checks. '
        'Use `scripts/build_registered_maria359_v1.py` and `--register`;pure transaction:`dk4tool/patch/maria359_release_v1.py`. '
        'All359 source objects,350 body pages,clean-input patch,own startup and24 protected getters pass. '
        'Preserve the722-entry prefix,Market format/pointers,six-section ARM9,ASCII right bounds,source25v2 andB164R99 correction. '
        'Main requires acceptance. Continue from [the registered checkpoint](editorial_Maria359_B253_B274_registered_20261110.md);older entries arehistory.\n\n')
    assert not old.startswith(prefix);continuity.write_text(prefix+old,encoding='utf-8',newline='\n')
    save(OUT/'handoff_checkpoint.json',dict(document=document,summary=summary,evidence=evidence,new_credit=0,full_goal_complete=False))
    print('Published23429 integrated reviews;2469 native story objects remain;723-entry cumulative candidate ready for testing;main unchanged.')

if __name__=='__main__':main()
