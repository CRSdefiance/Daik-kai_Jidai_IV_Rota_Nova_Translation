"""Checkpoint reviewed B48 native/stored/control proofs without credit before actual registered release."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B47_v8018 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.checkpoint_Rafael_B48_prose_v8033 import PROOFS as PRIOR_PROOFS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_native_stored_checkpoint_v8044')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8045')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8034/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/rafael_B48_editorial_manuscript_v3.json')
NAMES=Path('translations/rafael_B48_speaker_name_review_v2.json')
KEY='Rafael_SC0B48_source_prose_native_stored_pending_actual_release_v8044'
OLD_KEY='Rafael_SC0B48_source_context_prose_logical_pending_layout_release_v8033'
SCOPE='unfinished_editorial_scope_v8044'
PROOFS=dict(PRIOR_PROOFS)|{
    'plan':'work/analysis/Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json',
    'initial_native':'work/analysis/Rafael_B48_pages_v8036/91_complete_native_paragraphs92_pages364_compiled_alignments4_FE.json',
    'source_names':'work/analysis/Rafael_B48_source_name_planes_v8037/91_complete_source_pages9_names36_literal_alignments4_FE.json',
    'final_native':'work/analysis/Rafael_B48_pages_refined_v8038/91_final_native_paragraphs92_pages4_fresh360_reused_alignments.json',
    'name_sheet':'work/analysis/Rafael_B48_name_review_assets_v8039/review_sheet_receipt.json',
    'native_review':'work/analysis/Rafael_B48_native_review_v8040/91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json',
    'relocation':'work/analysis/Rafael_B48_relocation_v8041/one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json',
    'stored':'work/analysis/Rafael_B48_stored_v8042/all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json',
    'final_controls':'work/analysis/Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json',
}
SUMMARY="""Current registered cumulative ROM remains V8013;mainV4701 is unchanged. Counts remain6,991completed/6,994source-prose records anddrafts/4,369integrated revisions/2,622retentions;SC0 188 androute subset5,391. B47's636manifest batches/114accepted layers/18release checks/110regressions,exact clean-input patch andown-current Rafael startup remain verified. B48 has no completion orsource/prose credit andisnot integrated.

B48's complete contextual draft is now translations/rafael_B48_editorial_manuscript_v3.json:91speeches/42revisions/49individual retentions,32reviewed complete English paths. Whole clean Japanese,B128's45-speech callback context,prior B37's72-speech context,nine identities and500source-native result compositions preceded current English. All182original source/current dispatches and364logical alignments remain verified. R370's effective catalogue English differs fromrawstorage;retain its working words,normalized full-widthI andexactFI. Preserve all source caveats,seven regional treasures/ancient SevenSages andmaps,prospective ambition,uncertain African rumor,character humor/relationships andHans's non-navigator item-information role. SourceR38 stays unnamedsecondperson across paths;do not reintroduce a fixed Cesare addressee. All91formatting gates remain false.

Final automatic plan is work/analysis/Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json. Native full216pxusable width andsource-derived controls00/04/05/06/07/08/0D/4B/71/FE remain. Source00has28objects/27unique bodies;the duplicate is a legitimate two-question-mark source record. The firstv8035assertion expected28unique bodies andstopped before output;immutablev8035 andsource-lockedb correction arepreserved. Native private zero-prefix handling keeps the complete source preamble andunchanged NUL-free bodyguard. Globalprofile,fonts,viewport anddefaultFI7 remain untouched;this exact source/current batchusesmeasuredFI6/FA6/FO10 withonlyoneFI.

The bplan manufactured four short introductory rows inR347solely toend page1at a sentence boundary. Source-lockedc prioritizes avoiding short internal rows beforethat soft page preference. The finald adds soft aren't/you andisn't/it phrase preferences aftervisual inspection caught R140's split tag. R140alone changes fromc:three rows nowkeep aren't you? together,with no prose orrow-count change. Every prior plan/producer ispreserved. The historical weak-before-row andpage-boundary-before-readability findings remain broader retrospective leads;do not mechanically minimize rows orreverse a justified phrase retention.

All91English paragraphs produce92complete native pages:87progressive paragraphs/88pages andfourdistinctFEpages. Initialc compiledproofs run364fresh alignments;finald reuses90exact records/360cases andrunsfourfresh R140cases. Native independent full-glyph masks,first/internal/final characters,bounds,consumption andpage origins pass. R347usesfive full-width rows overtwo original four-row pages;page2starts withcomplete sealed atoriginal[6,0] andendswithshapes. Actualordinary page-turn validation remains pending. FourFEconsumers retain216pxusable width inside228x48logical/228x64physical paper and12pxrowpitch,distinct fromprogressive216x64. The source CP932ellipsisR171 remains intact;no glyph substitute ornew staging isauthored.

All16final body sheets andone name sheet were directly viewed:17final selected sheets,18total including the preserved superseded R140sheet. All91clean Japanese pages/fourCP932FEpages andnine complete style11 names pass independent masks;36name literal cases arefresh. One additional Arcadius Eirene Eudoxios string receivesfourfresh synthetic style11 literal cases. That is explicitly not actualcatalogue UI. ProgressiveArcadiusEudoxios omits the middle asdoes the spoken source. HansLetzel is complete,including the formerly truncated joining-panel final l. Rafael/JanusPasar/Claudio/Julio/Cristina/Arcadius/Cesare/Hans/PortWorker identities retain scoped source-based reasons;full207review,customplayernames,actualheaders andcatalogueUI remain open. No new name asset orbiography isauthored.

All37original line-break-count infos remain withindividual row reasons. Two exact weak-line-ending warnings remain verbatim:R86line1the/Proof andR406line2of/Conquest. Each has an id/source/logicalEnglish/compiled/line-bound exception andwritten reason;no globalweak rule ordiagnostic isremoved. R86keeps the complete title onrow2;R406keeps three fuller rows without adding a short fourth row merely toescape a soft boundary. Allwords,punctuation andsubstitutions survive. Neither exception permits glyph loss,overflow,blank pages,changed source controls orother warnings.

The research-only reconstruction is work/analysis/Rafael_B48_relocation_v8041/SC0_B48_RESEARCH_ONLY.DK4;it isnot a ROM/release. B48changes5252stored/logical/tail0 to4948stored/logical/tail0. All91complete six-byte preambles,163commands,28nested spans,five8000raw predicates,two8100completion queries,threeA000effects,allscene/camera/resource controls andfour-byte endremain. All140relocated native relative cases pass. Clean/predecessor complete block inverses andwhole predecessor archive inverse areexact;342otherSC0blocks areunchanged.

Finalstored validation passes192fresh parity-tail alignments for48records and172exact reused cases for43records. All92stored planes equal directly viewed planes;no extra/blank page,andall fourFEphysical planes remain exact. All91stored body/actor/voice dispatches,fourFEnull actors,sevenrelocated unforced predicates/queries withscratch restoration,44nonrelative control maps and25seeded normal value-carry ends pass. Terminal is4944/fullend4948. Effect bytes arepreserved;full scene-effect bodies are not newly claimed executed orsemantically explained. No B48ROM,full-reference loader/caller proof,actual scene job,formatting approval,policy,atomic stage orregistered release existsyet. No new emulator frames thisturn. Allsessions terminal/reaped;preserveeveryROM,translation,draft,failure,executedproducer andproof."""
NEXT="""Continue from verifiedV8045/current registeredV8013. Use translations/rafael_B48_editorial_manuscript_v3.json andspeaker_name_review_v2.json. Finalplan isv8035d,notb/c;final native binding ispages_refined_v8038,with4fresh/360reused compiledcases. Native reviewv8040 binds17final directlyviewed sheets,twoexact warning exceptions and37infos. Research relocation8041,stored8042andfinalcontrols8043pass. Reuse completedsource/context/identity/branch/current/effective/prose/logical/native/stored/inverse checks unless a newchange orconcrete risk justifies repeating them. All91formatting gates arefalse pendingactual/reference/release.

Next build andpin a complete isolated full research reference fromV8013plus the exact reviewedSC0archive;prove342otherblocks andeveryotherfile/component exact. Bind all343native load/cache paths/686parent modes,all163command maps/28relative operands,originalEV0entry8 andshipped callers. Use own-current Rafael input work/analysis/current_V8013_Rafael_native_v8016/current_native_input.json. Other-route contexts remain historical.

Then use representative paired Japanese/English actual scene tests. B48has78-88speeches across32source text paths;the unforced initialized opening composition predicts78,not an observed path. Preserve the entire163-command B48block afterall original B44initialization inany disclosed fixture,includingallscene/camera/resource/A000effects,queries,branches,fourFEpanels andfullend. Do not forceRAM,party,roles,roster,funds,seed,conditions orresults. Use an input/capture horizon long enough for the full exchange andnormal return rather than repeating the short B47horizon. Observe actualselection rather than assuming78. Focus on4B/71headers,arrival/portrait transitions,assistant/joining effects,R347's two pages/ordinary turn,nextdialogue,andallfourFEpanels including completeHansLetzel,navigatorDeckrestriction,iteminformation andX. OptionalJanus/Cesare/Cristina andevent128/37alternatives may remain explicitly native-only if no distinctdisplay orconcrete unresolved risk warrants another scene;exhaustive natural visits areunnecessary.

Measure actual completebody/name/FEglyphmasks,normal valuecarry,allselected commandresults/UIrequests andtiming/RNG/latercomponents/calendar/RGB without retiming inputsto hide differences. Preserve every measured difference andcausal/future-state limit. Onlythen approve finalformatting,freeze exactsource-bound policy/per-record capacities/twoexact warning scopes,andcomplete meaningful atomic reconstruction/challenges withindependent semantic proof validation beforeonefinalfiles-list commit. Register afterthe completeV8013stack,buildthroughbuild_integrated_release.py,verifyreference equality/exactclean-inputpatch andown-currentstartup. Expectedmanifest637fromcurrent636,accepted114/mainV4701unchanged. Credit91objects/42revisions/49retentions onceonlyafterchecks:projected7082completed/7085source-prose/drafts/4411revisions/2671retentions,SC0 279,route5482.Theseare notcurrentcounts.

Keep thefull objective acrossallfourstorylines,earlierdialogue,sharedshop/town/random/Help/remainingprose,all207names/roles/aliases andretrospectiveprematurewrapping. Preserveeverypriorunfinishedinventory,twelvecontraction/question-tag leads,unscannedrecords beyond558plans,bothinheritedplannerleads andallolderitem/counterpart/displayleads. KeepPasardistinctfromPasha;no globalreplacement. PreserveSailor151-159/Retainerconsumerdistinctions,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス,Trader/PortWorker/Guildmaster,Cristina/Christina,HansRetzel/Letzelconsistency andallotherrecordedleads. Graphics/all18plaques andlaterolder-recordtechnical re-audit remainseparate,includingnormal-endvaluecarry,B35R65source-onlynineteenthcell andallmeasuredtiming/highlight/RNG/component/calendar/RGBlimits. Preserveallartifacts.Fullgoalactive;no separateunifiedpackage,promotion,pruning,commit orpush."""

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==6991 and prior['manifest_batches']==636 and prior['B48_prose_records']==91
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==91 and doc['revisions']==42 and doc['retentions']==49
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert len(names['records'])==9 and all(r['native_name_plane_directly_viewed'] and not r['review']['formatting'] for r in names['records'])
    review=data['native_review'];assert review['manuscript_sha256']==sha(DOC.read_bytes()) and review['names_sha256']==sha(NAMES.read_bytes())
    assert review['native_page_count']==92 and review['original_row_count_infos']==37 and len(review['preserved_warning_exceptions'])==2
    assert len(review['directly_viewed_sheets'])==17 and all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in review['directly_viewed_sheets'])
    assert data['final_native']['plan_sha256']==sha(Path(PROOFS['plan']).read_bytes())
    assert data['final_native']['fresh_compiled_alignment_cases']==4 and data['final_native']['reused_compiled_alignment_cases']==360
    assert data['relocation']['relocated_native_skip_cases']==140 and len(data['relocation']['groups'][0]['command_map'])==163
    assert data['relocation']['complete_clean_source_block_reconstructed_exactly'] and data['relocation']['all_full_predecessor_archive_bytes_reconstructed_exactly']
    assert data['stored']['fresh_native_alignment_cases']==192 and data['stored']['exact_reused_native_alignment_cases']==172
    assert len(data['final_controls']['final_dispatches'])==91 and len(data['final_controls']['relocated_predicates_andqueries'])==7 and len(data['final_controls']['normal_seeded_ends'])==25
    return prior,data
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old and OLD_KEY in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']]
        assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,Path(__file__),*map(Path,PROOFS.values())]}
        pending=dict(status='91-source-context-prose-native-stored-approved-pending-fullreference-actual-policy-atomic-registered-release',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
            file_path='/data/SC0.DK4',block=48,objects=91,revisions=42,retentions=49,current_English_unread=False,
            all91_final_formatting_gates_false=True,native_pages=92,source_commands=163,relative_sites=28,relocated_cases=140,
            final_plan=PROOFS['plan'],final_native=PROOFS['final_native'],viewed_final_sheets=17,
            original_QA_infos=37,exact_warning_exceptions=2,
            stored_fresh_alignment_cases=192,stored_exact_reused_alignment_cases=172,
            native_actual_B48_gameplay_runs=0,all_proofs=PROOFS,current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],
            new_credit=0,new_emulator_runs=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending)
        if OLD_KEY in inventory:inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,native_pages_names_wrapping_stored_andcontrols_now_pass=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],dict(checkpoint=KEY,native_pages_names_wrapping_stored_andcontrols_now_pass=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8044: B48 complete native pages, names and stored reconstruction; actual/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V8044; V8013 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('B48 native/stored checkpoint staged;six targets,zero credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,
                full_goal_all_prior_leads_andnew_native_stored_limits_preserved=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passes;every prior ledger value,candidate,count andunfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('B48 native/stored checkpoint applied;currentV8013 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                B48_native_pages=92,B48_names_native_planes=9,B48_final_viewed_sheets=17,
                B48_stored_fresh_alignment_cases=192,B48_stored_exact_reused_alignment_cases=172,
                B48_all163_commands28_relative_sites140_cases_full_inverses_pass=True,
                B48_actual_gameplay_runs=0,B48_native_font_layout_stored_actual_policy_atomic_registered_integration_pending=False,
                B48_fullreference_actual_policy_atomic_registered_integration_pending=True,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8045/currentV8013:6991completed;B48 91decisions/92pages/nine names/stored controls pass.Fullreference/actual/release pending.Full goal active.')
