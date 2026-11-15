"""Preserve a reversible zero-credit six-outcome-draft checkpoint after V8300 integration."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Hodram_three_blocks_v8305 import COUNTERS,AFTER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcomes_checkpoint_v8321')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8322')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8306/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B47_B48_six_prose_source_display_logical24_pending_compiled_actual_andrelease_v8321'
SCOPE='unfinished_editorial_scope_v8321'
PROOFS={
 'manuscript':'translations/hodram_B47_B48_editorial_manuscript_v1.json',
 'names':'translations/hodram_B47_B48_speaker_name_review_v1.json',
 'source_controls':'work/analysis/Hodram_B47_B48_source_controls_v8314/two_EV1_entries15_commands6_preambles7_opaque_effect_pairs50_complete_seeded_ends.json',
 'source_display':'work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json',
 'current':'work/analysis/Hodram_B47_B48_current_v8317c/six_exact_source_current_effective_refs_after_whole_clean_gloss_andnative_source_view.json',
 'prose':'work/analysis/Hodram_B47_B48_prose_v8318/six_contextual_decisions_three_revisions_three_justified_retentions.json',
 'logical':'work/analysis/Hodram_B47_B48_logical_v8320/six_logical_paragraphs24_guarded_alignments_distinct_FE_one_FI.json',
 'artifact':'work/analysis/Hodram_B48_artifact_identity_v8313/clean_notice_anditem148_established_Ullr_Bow_identity_not_current_dialogue_review.json',
 'own_input':'work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json',
 'release':'work/analysis/Hodram_three_blocks_release_v8301/registered_release_verification.json',
}
SUMMARY="""Registered cumulative V8300 remains current after Hodram28 completed once:7199 completed/7202 source-prose-and-drafts/4471 integrated revisions/2728 justified retentions. SC0 368,SC1 119,SC2 4915,SC3 197,COMMON1600 complete/1603 source-prose;route subset5599 is not a full-goal denominator. V8300 contains641 manifest batches and114 accepted layers;18 release checks,110 regressions,exact tested-reference equality,clean-input xdelta reconstruction andfresh own Hodram4001-frame startup/six PNG pairs pass. MainV4701/canonical baseline unchanged. Preserve every ROM,translation,draft,executed producer,proof andfailure. No separate user test package,promotion,pruning,commit orpush.

The next two complete clean Hodram outcomes,SC1B47/B48,now have six exact source/current/effective references andsix contextual prose decisions:three revisions andthree individually justified retentions. Complete Japanese glosses preceded current English. Remove the unsupported unfairness accusation;restore Lil's adamant best-in-the-world expectation;preserve the instruction that the addressee wait in Amsterdam. Retain the rueful You win... Oh well.,the qualified Lil Argot/Ullr's Bow discovery notice,andthe playful chuckle/taunt withone real FI substitution. The source musical note is preserved as source evidence andits playful function is expressed by the retained laugh/taunt;it is not an executable control orproof of singing. No new rank,relationship,conquest,present world supremacy,player acquisition orhandover. Four prose gates pass on all six;all formatting gates remain false. These six receive zero new completion orsource-prose-counter credit until required validation/integration.

Source-only8314 binds both original EV1 entries,all15 commands,six complete preambles,seven isolated opaque-effect decoder pairs and50 complete normal-end cases carrying the initial value. No relative or8000 query sites. Event47 excludes48;event48 hasno corresponding exclusion. Entry getters are not outer eligibility,total chronology,ordinary activation orcomplete effect semantics. B47 retains61FF;B48 retains6302/6000/633D/623D andtwo complete A000 bodies. Opaque effects were bridged forstructural decoding,not executed asgameplay.

Source-display8316b passes six original dispatches/24 guarded alignments,five complete progressive pages andone distinct FE page. The six-page source sheet was directly viewed. FE usesoriginal24310 withnull actor,notactor254 orfallback208. Original typed-paper geometry228x48/288stride,6x12 metrics and16physicalpitch bind offline;incidentalr1 isnot geometry. Lil's clean fieldsリル/アーゴット andcurrentLil/Argot support retaining Lil Argot. Prior two getters/style11 nameplane anddefaultFI6/FA9/FO15 reuseexactcomplete ARM9/COMMON/font/wholeactors viaownV8300captain1 context. LocalFE oracle binds full12byte Gerhard name inverse toprevious2b6 ARM9 andprotectedBlades8;no globalguard/font/viewport change oroldRAMoverlay. Source♪ andexpandedHodram render completely. These are native/offline tests,not new scene gameplay,FE palette/actual geometry ortransition observations.

Current8317c binds six stored/effective English bodies throughcurrent dispatch andall467 cataloguekeys/targets/routes/calls;no catalogue match. All nonspeech effect bytes andfull terminals matchclean. Prose8318 savesnatural-dialogue-v2 manuscripts andscoped name retention. Logical8320 passes20progressive+4original-nullactorFE alignments,one FI andall literal leading/internal/trailing bytes,ABI/scratch/unowned4MiB guards. It doesnot prove compiled wraps,glyphs,pagination,stored relocation oractual effects. Preserved8316 stopsatstale2b6 catalogueguard;8316b changesonly exacttargethash afterfullnameinverse. Preserved8317 syntax failure and8317b AST-repair failure producedno output;8317c removesonlysurplusparenthesis,changesoutputsuffix andproves allnumerictokens exact.

Full goal remains active across allfour stories,earlier translatedstory dialogue,sharedshops/towns/randomscenes,Help/remainingprose,all207names/roles/aliases andretrospectivepremature wraps. All previous scope leads andmeasured actual/offline limits are preserved in the copied inventory andprior handoff. Graphics/all18plaques andlater older-record technical re-audit remain separate. Roughly20000 lexicalcandidates isnot anexact player-facing remainingcount orpercentage."""
NEXT="""Continue from verifiedV8322/currentregisteredV8300. Reuse completed Hodram28 integration/source/native/actual/policy/release/startup evidence;do not repeat without changedinput orconcrete risk. For nextsix B47/B48,use manuscriptv1/namesv1,sourcecontrols8314,source/nativeview8316b,current8317c,prose8318 andlogical8320. No moreclean-first/currentcomparison orlogicalalignment repetition isneeded forunchangedwords.

Next apply automatic natural-dialogue-v2 full-native-width formatting withone sourceFI anddistinctFE consumer. Preserve originalcompiled/native guards,complete first/internal/final characters,wordcoherence,bounds andsingle/multiple-page behavior asappropriate;do notshorten goodprose solely tofit. FE bitmap228px isnot automatically usable228px:retain prior source-bound terminal/break-pair measurements (RafaelB45V7880/V7881b usable216) andverify exactcurrentcode/geometry before reuse. Nativeoriginal effect semantics/61FF versusFE/scene controls/twoA000 bodies,actualFE palette/geometry,notice-to-Lil transition andnormal return requirefocused source/current tests. Preserve whole scripts anddisclose anyfixture;no outerflags/roster/conditions/RNG/result forcing orartificial eligibility claims. Then stored relocation/nativecommands/load-caller checks,frozen scoped policy/atomic validation,registered cumulative integration/clean-input patch/startup andcredit6once onlyafter necessary gates. No exhaustive naturalplaythroughs orindividualconditional visits required.

Keep every previous unfinishedfamily/lead,including12 contraction/questiontag leads,unscanned beyond558plans,weak-before-row/page-before-readability,COMMON750-752,preLF6435,item/label/counterpart/name consistency,all207labels/customnames;all measured Gerhard/Rafael/Hodram timing/RNG/components/calendars/RGB/fixture-entry limits andnormalendcarry. Owncaptain1 input8303 iscurrent;otherroute snapshots remainhistorical untilproperly rebound/recaptured. Keep full objective,allartifacts,graphics separation andlater older-record re-audit intact."""

def restore(value):
    result=deepcopy(value)
    for op in reversed(value[KEY]['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()};doc=data['manuscript'];logical=data['logical'];source=data['source_display']
    assert len(doc['records'])==6 and doc['revised']==3 and doc['retained']==3 and all(not r['review']['formatting'] and all(r['review'][k] for k in ['source','context','localization','naturalness']) for r in doc['records'])
    assert logical['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and logical['fresh_native_alignment_cases']==24 and logical['FE_null_actor_alignment_cases']==4
    assert sha(Path(source['review_sheet']['path']).read_bytes())==source['review_sheet']['sha256'] and len(source['records'])==6
    assert data['current']['source_six_page_sheet_directly_viewed']==source['review_sheet'] and data['source_controls']['normal_seeded_end_cases']==50
    assert data['release']['candidate_sha256']==prior['candidate_sha256']==data['own_input']['current_ROM_sha256'] and sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    for p in [doc,logical,data['current'],source]:
        for path,digest in p.get('evidence',{}).items():assert sha(Path(path).read_bytes())==digest
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER and old['goal_status']=='active'
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        pending=dict(status='six-whole-outcome-prose-reviewed-source-native-display-logical24-pass-compiled-actual-policy-release-pending',file_path='/data/SC1.DK4',blocks=[47,48],records=6,proposed_revisions=3,justified_retentions=3,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,
            all_four_prose_gates_true=True,all_formatting_gates_false=True,current_English_bodies_compared=True,source_FE_one_FI_andmusical_note_function_reviewed=True,new_credit=0,full_goal_complete=False)
        oldpending=prior['pending_source_batch'];put([oldpending,'superseded_by_source_prose_checkpoint'],dict(checkpoint=KEY,previous_flags_historical_not_deleted=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        inventory=deepcopy(read(old[prior['unfinished_scope']]['path']));assert sha(Path(old[prior['unfinished_scope']]['path']).read_bytes())==old[prior['unfinished_scope']]['sha256']
        inventory[KEY]=deepcopy(pending);inventory['next_focus']=NEXT
        if oldpending in inventory:inventory[oldpending]['superseded_by_source_prose_checkpoint']=dict(checkpoint=KEY,previous_flags_historical_not_deleted=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,new_uncredited_Hodram_prose_drafts=6,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,scope,Path(__file__),*map(Path,PROOFS.values())]}
        put([KEY],dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,goal_turn_classification='progress',all_sessions_terminal_andreaped=True))
        new[KEY]['inverse_operations']=deepcopy(ops)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8321; V8300 current\n\n' if name=='editorial_handoff_current.md' else '')+'## V8321: six Hodram outcome prose decisions;compiled display andactual tests next\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n';targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False));print('V8321 staged:six targets/zero-credit six drafts;deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'] and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),every_prior_value_counter_candidate_andfamily_recovers_exactly=True,new_credit=0));print('Deep inverse audit passed;all prior records/counters/candidate recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for e in plan['files']:
                assert Path(e['target']).is_relative_to(Path.cwd().resolve()) and Path(e['planned']).is_relative_to(ROOT.resolve())
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_registry_orcompletion_counter_change=True,new_credit=0,full_goal_complete=False));print('V8321 applied;currentV8300/count7199 unchanged;full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();verified=deepcopy(prior)
            verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                next_clean_exchange_not_selected=False,Hodram_next_outcomes_checkpoint=deepcopy(new[KEY]),new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_research_ROMs=0,
                all_sessions_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified);print('VerifiedV8322/currentV8300:7199completed;six contextual outcomes drafted/source native/logical24pass;compiled/actual/release pending.Full objective active.')
