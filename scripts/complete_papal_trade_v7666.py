"""Credit36 disjoint integrated decisions once; preserve every prior ledger value by inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.papal_trade_final_paths_v7655 import SEALED,MAP,SEAL,ACTUAL,LATER,VIEW,NAMES,proofs
from scripts.papal_trade_completion_gates_v7666 import gates,RELEASE,START,START_VIEW,REG,PIN,NATIVE,LEAD
from scripts.prepare_papal_trade_checkpoint_v7653 import SUMMARY as PRIOR_DETAILS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_completion_v7666')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7667')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7654/verified_handoff.json')
FINAL=Path('translations/papal_trade_contextual_final_review_v1.json')
KEY='papal_trade_SC0_SC1_completion_v7666'
SCOPE='unfinished_editorial_scope_v7666'
FAMILIES={0:'Rafael-SC0-B246-Carlo-Filippo-papal-trade-whole-exchange18',1:'Hodram-SC1-B237-Carlo-Filippo-papal-trade-whole-exchange18'}
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6801,6804,6804,4251,2550)
AFTER=(6837,6840,6840,4277,2560)
INTRO="""The two complete Rafael SC0B246/Hodram SC1B237 papal-trade exchanges are integrated in registered experimental cumulative V7660 after every V7611 layer. Thirty-six disjoint file-qualified speeches receive source-prose/completion credit once:26 revisions and10 individually justified retentions atR5/R12/R29/R47/R60 perroute. All36 exact clean,predecessor,effective,compiled,stored andintegrated references are in translations/papal_trade_contextual_final_review_v1.json. The ledger nowhas6837 completed,6840 source-prose/drafts,4277 revisions and2560 retentions. File counts areSC0 135,SC1 91,SC2 4915,SC3 96 andCOMMON1600 completed/1603 source-prose. Route5237/5237 is a subset,not the full objective denominator. V7660 has628 batches,114 accepted layers,18 passing release checks,110 regressions andan exactly reconstructable clean-input patch. MainV4701 andthe immutable canonical baseline remain unchanged. Preserve every ROM,translation,draft,executed producer,failure,trace andproof."""
RELEASE_DETAILS="""Both archives are reconstructed andvalidated before one final files-list commit. The production36-record positive matches the approved whole research ROM exactly,and148 actual-changing corruptions reject before anycommit withdependency digests deliberately bypassed. No schema exception,unchanged mutation orstartup failure counts as a rejection. All earlier profiles/layers remain;onlySC0B246 andSC1B237 change fromV7611. V7660's clean-input xdelta reconstructs every ROM byte;all628 batches,114 accepted layers,18 release checks and110 regressions pass.

Own V7660 New Games forRafael/Hodram/Lil andthe inherited-town regression match40 whole-frame pairs andnative actor/captain controls againstV7611. Three strict own-ROM NewGame4000 contexts bind actualcaptains0/1/2,exact2b6 ARM9,COMMON,directory andall123264 deployed bytes. DefaultLil input is work/analysis/current_V7660_native_v7665/current_native_input.json;Rafael/Hodram have separate route0/route1 inputs underthat directory. Never use another route's context oroverlay historical RAM. Both startup sheets wereviewed andthe source/disposable town batteries remain unchanged.

Preserve the original R0/R1 startup runs withtouch-pointer mode andthe stopped7664 core-options assertion. Source controls usedmouse mode,so onlythose two cases were rerun withmatching settings;Lil/town captures were reused. Preserve the stopped7664b assumed-town-captain2 assertion. Measured source/current towncaptains are1/1(Hodram);7664c keeps strict equality withthat independently bound identity. The startup towncapture3200 displaysCopenhagen. The earlier Stockholm shorthand refers to the separate initialized Hodram opening scene/return andisnot this inherited-town capture's location. Historical erroneous plan labels andallfailure/proof versions remain;no ROM,donor,controller schedule orstate waschanged torepair these bookkeeping assumptions. Six own-candidate cold boots total37406 frames include the two preserved mismatched-pointer runs;the four matching regression cases total29404 frames. All sessions areterminal/reaped.

Both18-speech families arecredited once onlyafter these gates. Four contextual Carlo Sinat/Trader name retentions remain scoped to their whole exchanges,exact getters andobserved progressive fixture headers;there isno extra dialogue/name credit orfull207 approval. Full catalogue UI,natural optional activation,original locations,earned progress andfull effects remain unproved. All measured19 command rows/seven durations perroute,3/133 Rafael and53/133 Hodram lateRGB differences,Hodram model/persistent-object/actor/RNG differences andraw calendar limits remain preserved for the later older-record technical re-audit. No fullRAM,everyframe,futuresequence,broadsimulation orcausal-equivalence claim. Graphics/all18 plaques stay separate. No separate unified test package,promotion,pruning,commit orpush isperformed."""
DETAILS=INTRO+'\n\n'+'\n\n'.join(PRIOR_DETAILS.split('\n\n')[1:-1])+'\n\n'+RELEASE_DETAILS
NEXT="""Continue the complete four-storyline,earlier translated dialogue,shared shop/town,random,Help,remaining player-facing prose,207 names/roles/aliases andretrospective premature-wrap objective. Preserve clean-Japanese meaning,facts,tone,characterization,cultural context,approved names,controls andsubstitutions in natural American English. Do not replay completed unchanged papal-trade source/gloss,prose,names,native/stored,actual,reference,production,release orstartup checks.

Next inspect the complete clean Maria SC3 block207 andits surrounding commands/context before consulting current English. The metadata-only lead work/analysis/maria_B207_metadata_lead_v7665c/17_uncredited_SC3B207_metadata_refs_clean_complete_exchange_review_pending.json contains17 uncredited legacy file-qualified references,eight labeledFilippo. These labels/context areunapproved leads,not Japanese glosses orproof of an exact B234/B246/B237 clone. Older English bodies were not exposed orused. Inventory the full clean native scene,write faithful whole-exchange glosses first,andrecheck the live ledger before anynew credit. Bind actual Maria captain3 native/name/entry consumers when needed;never reuseLil/Rafael/Hodram defaults. Use existing own-current strict inputs forcaptains0/1/2 onlywithin their scope.

Retain every earlier completed family andunresolved inventory lead,including widerTrader104 consumers,all207 names/roles/aliases,earlier dialogue andpremature wraps,item99 title/card/mechanics,item50 other-route wording,untranslatedイギリス country labels,Samwell middle/catalogue,Christina/Cristina andother source-specific names,remainingLil andallother route stories,shared town/shop,random andHelp. Source equality or technical coverage grants no automatic editorial approval. Graphics/all18 plaques andthe later older-record technical re-audit remain separate. Preserve every generated ROM andtranslation,all executed/failing producers,all initial/refined layouts,all traces/proofs andthe measured source/English timing/RNG/state/RGB limits. No canceled package,automaticpromotion,pruning,commit orpush. The full goal remains active."""
def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][op['before_length']:])==op['appended_sha256'];del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();before=LEDGER.read_bytes();old=json.loads(before)
    assert sha(before)==read(PRIOR)['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active'
    mapping=read(MAP);image=NdsImage.open(release['candidate']);rows=[];byroute={};changed={(r['file_path'],r['id']):r for r in release['stage']['changed_records']}
    for route,path in SEALED.items():
        doc=read(path);spec=mapping['groups'][route];file=spec['file_path'];n=spec['block'];block=IlnkContainer.parse(image.read_file(file)).blocks[n]
        assert sha(block)==spec['target_block_sha256'] and len(block)==1508 and doc['current_ROM_sha256']==read(PRIOR)['candidate_sha256']
        refs={r['id']:r for r in spec['all_object_references']};records=deepcopy(doc['records'])
        for r in records:
            ref=refs[r['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);body=value[1:];command=next(c for c in spec['command_map'] if c['new_offset']==at-5)
            assert block[at:at+len(value)+1]==value+b'\0' and changed[(file,r['id'])]['new_offset']==at and block[:at].count(b'\0')==ref['new_record_index'] and block[at-5:at+1].hex()==r['source_complete_preamble_hex']
            template=body.decode('cp932');assert ' '.join(template.split())==r['english'].split('}',1)[1] and all(r['review'].values()) and r['actual_record_observed']
            history=['current_reference','current_hex','current_record_index','current_native_extent','current_raw_storage_English','current_effective_paragraph','current_effective_runtime_template_hex','current_expanded_runtime_hex','registered_integration_pending','source_prose_or_completion_credit_added','formatting_reason']
            r['historical_preintegration_fields']={k:deepcopy(r[k]) for k in history if k in r};newref=dict(block=n,offset=at,bytes=len(value),record_index=ref['new_record_index'],header_offset=at-5)
            r.update(current_reference=newref,integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),current_record_index=ref['new_record_index'],current_native_extent=command['new_extent'],integrated_command_extent=command['new_extent'],current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=body.hex(),current_effective_paragraph=' '.join(template.split()),current_expanded_paragraph=' '.join(template.split()),current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if r['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-reference-representative-and-registered-release',actual_complete_display_proof=str(ACTUAL),actual_representative_scene_evidence_is_separate=True,formatting_reason=r['formatting_reason']+' Registered cumulativeV7660,exact clean-input reconstruction,all18 release checks110 regressions,40 matching startup frame pairs andown strictcaptain0/1/2 contexts nowpass. All natural-activation/full-mechanic andmeasured late timing/RNG/state/RGB limits remain;full207/four-storyline/earlier-wrap review active.')
        assert len(records)==18 and Counter(r['editorial_decision'] for r in records)=={'revise':13,'retain-wording':5};byroute[route]=records;rows.extend(records)
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6801 and len(keys)==36 and not oldkeys&keys
    fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6801 and not fresh['pending_record_keys']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    paths=[*SEALED.values(),MAP,SEAL,RELEASE,START,START_VIEW,REG,PIN,NATIVE,LEAD,PRIOR,*map(Path,proofs().values()),Path('translations/papal_trade_editorial_release_v1.json'),Path('work/analysis/papal_trade_atomic_challenges_v7658/atomic_validation_receipt.json'),Path('work/analysis/papal_trade_regressions_v7660/terminal.json'),Path('work/analysis/papal_trade_startup_pointer_tools_v7663b/source_locked_matching_pointer_controls.json'),Path('work/analysis/papal_trade_town_scope_tools_v7664c/actual_Hodram_town_captain1_source_current_binding.json'),Path('scripts/papal_trade_completion_gates_v7666.py'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(p):sha(p.read_bytes()) for p in SEALED.values()},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=26,retained=10,source_prose_and_completion_credit_added_once=36,all36_exact_clean_predecessor_effective_compiled_stored_integrated_refs_bound=True,all36_actual_single_original_four_row_pages_complete=True,paired_source_English_speech_occurrences=72,complete_English_body_holds=133,complete_English_name_holds=133,offline_only_object_IDs=[],all40_commands_preambles_A000_ends_source_tail0_target_tail2_andfull_inverse_preserved=True,scoped_Carlo_Trader_andspoken_Filippo_no_assets_orfull207_approval=True,all_measured_late_differences_andnatural_activation_limits_preserved=True,late_RGB_differences=[3,53],later_samples_each_route=133,all148_production_corruptions_reject_before_single_two_file_commit=True,own_ROM_matching_startup_frame_pairs=40,own_ROM_actual_captains=[0,1,2],inherited_town_captain1_Copenhagen_capture3200_scope_explicit=True,all_prior_ROMs_translations_failed_producers_andfull_objective_preserved=True,full_goal_complete=False,evidence=evidence,summary=summary))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[k]['/data/SC0.DK4']==117 and new[k]['/data/SC1.DK4']==73 and new[k]['/data/SC2.DK4']==4915
        put([k,'/data/SC0.DK4'],135);put([k,'/data/SC1.DK4'],91)
    append(['completed_editorial_families'],[dict(id=FAMILIES[r],file_path=f'/data/SC{r}.DK4',blocks=[[246,237][r]],record_IDs=[x['id'] for x in byroute[r]],final_review=str(FINAL),records=byroute[r],revised_count=13,retained_count=5,fresh_revisions=13,fresh_retentions=5,actual_verification_scope=DETAILS) for r in [0,1]])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=r['file_path'],id=r['id']) for r in rows]
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6837,fresh_pass_records_integrated=6837,latest_contextual_manuscript=str(SEALED[1]),latest_completed_family=FAMILIES[1],latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILIES[r],records=18,final_review=str(FINAL),new_revisions=13,justified_retentions=5,new_completed_records=18,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=18,actual_pages=18,offline_only_objects=0,prior_paired_source_English_content_runs_reused_without_replay=True) for r in [0,1]])
    for path in SEALED.values():
        if str(path) not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[str(path)])
        put(['active_source_prose_drafts','route_record_subsets_pending',str(path)],[])
    put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5201
    for k,v in dict(reviewed_route_records=5237,completed_route_records=5237,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILIES[r],status='complete-contextual-current-native-reference-representative-and-registered-release',file_path=f'/data/SC{r}.DK4',blocks=[[246,237][r]],completion_credit_added=18,final_review=str(FINAL),actual_original_optional_activation=False,actual_objects=18,actual_pages=18,offline_only_objects=0,full_goal_complete=False) for r in [0,1]])
    put(['formatting_watchlist','papal_trade_SC0_SC1_v7666'],dict(status='36-source-prose-native-stored-actual-reference-registered-release-pass',final_review=str(FINAL),two_exact_R33_warnings16_infos_all_base_QA_preserved=True,full_commands_opaque_A000_end_andseparate_tails_preserved=True,all_timing_RNG_components_RGB_limits_andstartup_failures_preserved=True,full207_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    put(['papal_trade_SC0_SC1_actual_reference_pending_release_v7653','registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    scope=old['unfinished_editorial_scope_v7653'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=36,revisions=26,retentions=10,registered_candidate=release['candidate'],all_late_measurements_names_full207_andbroader_source_scope_preserved=True)
    inventory['papal_trade_SC0_SC1_actual_reference_pending_release_v7653']['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded_history=True,new_credit_here=0)
    inventory['next_Maria_SC3_B207_metadata_only_lead_v7665c']=dict(path=str(LEAD),sha256=sha(LEAD.read_bytes()),uncredited_legacy_references=17,clean_complete_context_gloss_controls_andcurrent_English_review_all_pending=True,no_automatic_clone_orother_route_approval=True,new_credit=0)
    inventory['later_papal_trade_technical_reaudit_v7666']=dict(actual=str(ACTUAL),later=str(LATER),late_RGB_differences=[3,53],late_samples_each_route=133,all19_command_rows_seven_durations_each_route_models_actors_RNG_limits_retained=True,failed_final_frame_pointer_mode_andtown_identity_assumptions_andall_successors_preserved=True,no_broad_simulation_orcausal_claim=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5237,completed_route_records=5237,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_prior_leads_names_completed_history_andfull_four_storyline_objective_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=36,new_completed_records=36,revised=26,retained=10,new_current_candidate_emulator_runs=6,new_current_candidate_frames=37406,matching_regression_runs=4,matching_regression_frames=29404,all_prior_source_English_fixture_runs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7666: Rafael B246 andHodram B237 integrated in cumulative V7660; full editorial goal active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;prefix=('# Current editorial handoff - V7666; V7660 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all36_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six completion targets staged:36 disjoint objects/26 revisions/10 retentions. Deep inverse audit next.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);release=gates()
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_record_andcounter=True,all_six_before_andplanned_hashes_verified=True,exactly36_disjoint_new_records=True,full_goal_complete=False));print('Deep inverse audit passes;every prior root,record,count andhistory value recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited completion targets applied;36 decisions integrated once.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True);native=read(NATIVE)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_prior_roots_records_history_andcounts_recover_exactly=True,exactly36_new_disjoint_source_prose_completed_records=True,completed=6837,source_prose=6840,revised=4277,retained=2560,SC0=135,SC1=91,SC2=4915,SC3=96,reviewed_routes=5237,completed_routes=5237,all628_batches114_accepted18_checks110_regressions_verified=True,all148_production_rejections_before_commit=True,all36_actual_single_pages72_source_English_speech_occurrences133_English_body133_headers_bound=True,all40_startup_frame_pairs_andstrict_own_captains0_1_2_verified=True,inherited_town_Hodram_captain1_Copenhagen3200_scope_corrected=True,late_RGB_differences_by_route=[3,53],later_samples_each_route=133,all_timing_RNG_models_actors_andbroad_equivalence_limits_preserved=True,current_native_input=native['default_Lil_input'],current_native_input_sha256=sha(Path(native['default_Lil_input']).read_bytes()),route_native_inputs=native['contexts'],next_Maria_SC3B207_17_metadata_leads_clean_context_andcurrent_English_unreviewed=True,metadata_lead=str(LEAD),metadata_lead_sha256=sha(LEAD.read_bytes()),full207_names_earlier_dialogue_wraps_all_four_storylines_shared_town_random_Help_remaining_prose_active=True,graphics_andlater_older_record_reaudit_separate=True,main_V4701_preserved=True,all_sessions_terminal_andreaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7666 verified:V7660 cumulative;6837 completed/6840 source-prose,26 revisions10 retentions counted once. Full goal active;Maria clean block207 next.')
