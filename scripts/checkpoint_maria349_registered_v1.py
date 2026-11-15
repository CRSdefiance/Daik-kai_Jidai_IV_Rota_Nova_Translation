"""Publish the cumulative testing checkpoint, preserving earlier credit and full scope."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B275_B285_clean_20261110')
OUT=Path('work/maria349_B275_B285_release_v1')

def main():
    rp,cp=OUT/'registered_release_verification.json',OUT/'completion_checkpoint.json'
    release,complete=map(load,[rp,cp]);actual=load(ROOT/'gameplay_review_v1.json')
    censuspath=Path('work/story_source_coverage_20261110_SC3_v16/coverage.json');census=load(censuspath)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(724,114,59)
    assert complete['new_credit']==349 and complete['counts']==dict(completed=23778,revised=14181,retained=9597)
    assert len(census['records'])==5129 and len(census['missing'])==315 and census['new_exact_bindings']==349
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    registry,prior=map(load,['translations/release_stack.json',OUT/'release_stack_before_Maria349.json'])
    assert registry['latest_promoted_build']==prior['latest_promoted_build']
    delta=load(ROOT/'final_layout_delta_v1.json');assert delta['final_changed_record_count']==10 and delta['pages_reclaimed']==3
    package=Path('releases/all_routes_editorial_20261110_maria349_candidate/release_manifest.json')
    assert load(package)['candidate_sha256']==release['candidate_sha256']
    evidence={str(p):digest(p) for p in [rp,cp,censuspath,package,Path('translations/maria349_B275_B285_integrated_final_review_v1.json'),
        *[ROOT/p for p in ['research_completion_v1/research_completion.json','gameplay_review_v1.json','offline_display_approval_v1.json',
            'stored_v1/stored_native_verification.json','stored_catalogue_all_v1/all_stored_effective_body_bindings.json',
            'final_layout_delta_v1.json','registered_preparation_v1/qualification.json','registered_semantic_checks_v1/qualification.json']],
        OUT/'own_registered_startup_verification.json',OUT/'own_registered_name_getters_v1.json',OUT/'own_startup_visual_v1/receipt.json',Path(__file__)]}
    summary=('Maria B275–B285 is registered and credited once:349 contextual reviews,184 revisions,165 justified retentions and19 scoped names. '
        'All347 body pages,eight captions and21 name strings pass. Three initialized emulator samples observe191 bodies/193 pages,allthree menus,two page turns,seven FE returns andthree sailing returns. '
        'Ten final layouts improve andthree pages are reclaimed. The cumulative724-entry/114-layer candidate passes59 release checks,exact clean-input reconstruction,own startup and24 protected getters. '
        'Integrated23,778;2,120 native story objects remain (Maria315;Lil1,805). Main awaits acceptance;full editorial scope remains active.')
    document='docs/editorial_Maria349_B275_B285_registered_20261110.md'
    text=f'''# Combined Maria349 candidate — November 10, 2026

{summary}

Use [the cumulative test ROM](../work/maria349_B275_B285_release_v1/all_routes_maria349_B275_B285_candidate.nds) and its adjacent manifest. ROM SHA256:`{release['candidate_sha256']}`. Clean-input patch SHA256:`{release['patch_sha256']}`;clean input SHA256:`{release['clean_input_sha256']}`. Standalone GitHub package:`releases/all_routes_editorial_20261110_maria349_candidate/`. This is prepared for testing andpromotion acceptance;main remains V4701. All723 predecessor entries and114 accepted layers remain intact,including early Rafael/tutorial work,the Market Trade-screen fix,speaker-name work,ASCII rightbounds,six-section ARM9,source25v2 andB164R99 padding repair. No graphics artwork change.

This batch covers11 complete SC3 groups B275–B285:179 ordinary bodies,162 physical personality alternatives and8 captions. All349 clean meanings andindependent drafts were sealed before current-English extraction. Every source/current/registered reference,individual finding,revision andjustified retention isbound in`translations/maria349_B275_B285_integrated_final_review_v1.json`;allfive individual gates pass. Nineteen scoped name reviews retain21 strings. The review corrects weapons/armor smuggling,wokou pirates,a real Nagasaki priest distinct fromthe later impostors,the1000-coin Macao informant,tomorrow's arrival,the alternative lies nextweek OR Hangzhou,more than100 claimed Jesuits,a former actor impersonating a magistrate,the governor completely fooled andnearly losing his head,Westerners/Japanese andthe guardians' village far northeast OF China. It preserves uncertainty about the future scheme,the Forbidden City andillustrated-map rumor. It distinguishes Maria's injury,crew injury andthe treatment roles;no invented kinship,rank,poison,death orarrest outcome. Magistrate/Priest archetype labels retain their staged identities. Actor25 isYifaSol;Mihwa's existing reading isretained inthis scoped review without inventing nationality orsurname. Broader names review remains open.

All347 finalbody pages,8 captions and21 name strings were directly viewed. Ten finalcompiled layouts differ frominitial plans,350 pages become347 without prose shortening,andthree further closing-phrase boundaries improve. An exact complete-word as/soon soft wrap isdocumented because itkeeps the full paragraph onone page;the original warning remains inhistory andno native glyph,width,canary,bounds orcontrol guard iswaived. All341 bodies/1364 selected alignments,27 complete style objects/216 slots/243 compiler negatives,8 captions/18 alignments/66 modal returns/32 normal-highlight planes/23 negatives andallscoped names pass. Exact matching338 body proofs are reused after direct baseline review;only3 final changed layouts are rerendered. Allsuperseded plans/pages/producers remain preserved.

Storage passes347 pages,341 effective native lookups,330 relocated branch cases,303 loads and606 handoffs,plus whole clean/current/command/block/archive/serialized-ROM inverses. Eight production scope mutations are rejected whilecaller images stay exact. Three initialized emulator samples run77043 frames:191 bodies/193 pages,12 effective voice4 alternatives,all3menus/8captions,2page turns,7FE returns,7FI substitutions and3sailing returns. All21 actual review sheets aredirectly viewed. The150 remaining bodies/other physical style alternatives haveoffline native/stored checks. These bounded hosts preserve setup/cleanup butconcatenate conditional samples;they donot establish natural activation,original outcomes/rewards/geography/chronology,fullroutes orhardware. The reused observer's inherited Maria359 scope label denotes itsrunner version;exact fixture manifests/ROMs andobserved source IDs areMaria349. No guide photos.

The new candidate's own31000-frame title/NewGame/Maria opening reaches Hangzhou. Allsix startup checkpoints areviewed;unchanged opening/town captures match priorapproved RGB exactly. Its ownsnapshot verifiescaptain3/route3,123264 staged bytes andboth original getters for12 protected actors. The clean-input patch reconstructs the candidate byteforbyte. The724-entry manifest passes59release checks andpreserves the entire accepted prefix. All27 selected repository tests pass without setup errors.

Integrated23,778=14,181 revisions+9,597 retentions;historicalsource/prose/draft count23,781. Native story remainder2,120=Maria315+Lil1,805;shared/player-facing inventories remain separate. Next clean source:`work/story_source_coverage_20261110_SC3_v16/residual_clean_source_packet.json`. Preserve allpriorcoverage,ROMs,translations,retentions,drafts andevidence. Continue every unfinished storyline andshared/shop/town/random/player-facing prose,with earlyRafael/tutorial priority,names,wraps andglyph consistency. Deferred artwork andlater older-record technical re-audit remain separate. Fullgoalactive;no worker islive.
'''
    checkpoint(mutation=ROOT/'registered_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria349 B275–B285 registered andcredited once;combined candidate ready for testing andpromotion acceptance.',
            current_batch_not_yet_integrated=False,current_batch_registered_andcredited_once=True,all_current_batch_fifth_gates_pending=False,
            proposed_revisions=184,justified_retentions=165,qualified_scoped_names=19,current_batch_actual_gameplay_observations=191,current_batch_actual_gameplay_pages=193,
            current_batch_evidence=evidence,native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,no_batch_worker_live=True,guide_photos=False,previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Hand off combined testing candidate andcommit/push;continue SC3_v16 residual without repeating completed checks.'),
        summary=summary,document=document,document_text=text,completed=23778,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    continuity=Path('docs/build_continuity_protocol.md');old=continuity.read_text(encoding='utf-8')
    prefix=('Maria349 B275–B285 is registered over Maria359:724 entries,114 accepted layers and59 release checks. '
        'Use`scripts/build_registered_maria349_v1.py` and`--register`;pure transaction:`dk4tool/patch/maria349_release_v1.py`. '
        'All349 source objects,347body pages,exact clean-input patch,own startup and24protected getters pass. '
        'Preserve the723-entry prefix,Market format/both pointers,six-section ARM9,ASCII rightbounds,source25v2 andB164R99 correction. '
        'Main requires acceptance. Continue from[the registered checkpoint](editorial_Maria349_B275_B285_registered_20261110.md);older entries arehistory.\n\n')
    assert not old.startswith(prefix);continuity.write_text(prefix+old,encoding='utf-8',newline='\n')
    save(OUT/'handoff_checkpoint.json',dict(document=document,summary=summary,evidence=evidence,new_credit=0,full_goal_complete=False))
    print('Published23778 integrated reviews;2120 native story objects remain;724-entry cumulative testing candidate ready;main unchanged.')

if __name__=='__main__':main()
