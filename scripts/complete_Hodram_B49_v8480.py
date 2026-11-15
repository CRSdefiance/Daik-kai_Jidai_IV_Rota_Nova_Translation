"""Credit sixteen disjoint B49 decisions once after registered release/startup,with full ledger inverse."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B49_profile_v2 import validate_approved_batch,validate_runtime
from dk4tool.dialogue.hodram_B49_names_v2 import validate_scoped_names
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_Rafael_B50_v8184 import COUNTERS,digest
from scripts.Hodram_B49_release_paths_v8450 import DOC,NAMES,SEAL,proofs,observed_scope
from scripts.prepare_Hodram_B49_checkpoint_v8473 import NEXT as prior_next
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_completion_v8480')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8481')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8474/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
CONFIG=Path('translations/hodram_B49_editorial_release_v3.json')
RELEASE=Path('work/analysis/Hodram_B49_release_v8476/registered_release_verification.json')
START=Path('work/analysis/Hodram_B49_registered_binding_v8478/own_Hodram_startup_andstrict_captain1_context.json')
VIEW=Path('work/analysis/Hodram_B49_registered_startup_view_v8479/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
POSITIVE=Path('work/analysis/Hodram_B49_atomic_positive_v8465/atomic_positive.json')
NEGATIVE=Path('work/analysis/Hodram_B49_atomic_challenges_v8457/semantic_rejections.json')
BINDING=Path('work/analysis/Hodram_B49_pin_semantics_v8465b/semantic_binding.json')
REG=Path('work/analysis/Hodram_B49_registration_v8475/registration_receipt.json')
FINAL=Path('translations/hodram_B49_contextual_final_review_v1.json')
KEY='Hodram_SC1B49_completion_v8480'
FAMILY='Hodram_SC1B49_wristband_trade_v8480'
SCOPE='unfinished_editorial_scope_v8480'
NEXT_KEY='Hodram_next_clean_exchange_selection_v8480'
BEFORE=(7205,7208,7208,4474,2731)
AFTER=(7221,7224,7224,4481,2740)

INTRO='Hodram SC1B49 is complete in registered experimental cumulative V8475:16 decisions,14 speeches andtwo typed choices,seven revisions andnine individually justified retentions credited once. Totals7221completed/7224source-prose-and-drafts/4481integrated revisions/2740retentions;SC0368/SC1141/SC24915/SC3197/COMMON1600complete1603source-prose;route subset5621 isnot a full-goal denominator. All643manifest batches/114accepted layers/18release checks/110regressions,whole tested-reference equality,exact clean-input patch andown registered Hodramstartup pass. MainV4701/canonicalbaseline unchanged;preserve every ROM,translation,draft,executed producer,proof andfailure. No separate requested testpackage,promotion,pruning,commit orpush. Full objective remains active.'
DETAILS="""The complete clean Japanese exchange and individual glosses precede the prior English. Preserve Lil's playful bargaining, the regional Proof of Supremacy, hearsay that the wristband is somewhere in the New World, the conditional trade, Hodram's silence and qualified denial, repeated delight and the outgoing Heavenly Wristband notice. Item84 Heavenly Wristband and item148 Ullr's Bow stay distinct; the later bow-acquisition UI follows original effects. Do not invent item powers, price, rarity, relationships, ranks, earned possession, eligibility, location or chronology. Both original typed responses retain their wording and source order; only No.'s three storage spaces are removed. Two scoped name retentions keep Hodram Bergstrom's progressive getter distinct from full Hodram Joakim Bergstrom, and retain Lil Argot. No name asset or duplicate207-name credit is added.

All sixteen individual natural-dialogue-v2 gates and source/current/final references are bound. Fourteen native single pages use the full216px width, complete leading/internal/trailing characters and original progressive/FE consumers. Preserve source-qualified silence and mixed ellipsis, the three balanced New World direction rows, seven source line-count infos andzero warnings orwaivers. The formatter owns ordinary breaks. Full36commands/fourteen six-byte preambles/eight relatives40cases/one raw query/one22byte typed menu/two item148layouts andhide waits/seven opaque effects/full four-byte end andseparate tails survive both clean/current block inverses, whole archive andwhole in-memory predecessor inverse. All324otherSC1blocks/allother files/components/fonts/names/123264staged payload remainexact. All325load-cache paths/650parentmodes/326actions andshipped callers bind independently.

Existing actual evidence is reused through byte-exact registered/reference ROM equality. Whole initialized scripts20002frames plus bounded possession-tail accept/decline40004frames coverall14unique source/English speeches,both typedchoices,34page occurrences and200complete body-name-orabsent-FE-header holds. Four menus/twelve owned backing samples/twenty-four visible labels preserve centering,bounds,blankguards,backgrounds,selected highlights,dismissal andresult forwarding; later sailing All right. callbacks remain separate. Focused original FEpaint9862frames binds two CPU/WRAM/TCM snapshots andfour complete bitmap/palette/bankDVRAM/RGB holds; temporary stackcontext isdistinct from persistent view/header/palette. Total69868frames/eight runs is disclosed initialized-fixture coverage,not natural optional activation,original location,earned inventory/trade eligibility,customnames,fullroute,hardware,everyframe causality,future-random-outcome orbroad simulation proof. No controller,RNG,inventory,roles,flags,funds orresults wereforced.

Whole-script source5213/English5216 returns[0,0],two duration differences andPRNG differences at324/416/424/980 persist;final seeds both1633251573,five sampled components/actors match,79of81laterRGBpairs match withPorttooltip/sailinghighlight differences. Tailaccept hasone durationdifference,matching observed boundary seeds butunequal final seeds996112413/155404999,78of81laterRGBpairs match withA-prompt/sailinghighlight/Depart-highlight differences. Taildecline hasfour durationdifferences,twelve boundaryPRNG differences at758/820/904/908/910/952/960/962/966/974/976/980,matching finalseed3478759668 andall69laterRGBpairs match. Bothtails havezero UIrequest differences,five sampled components/actors/captain1 match;rawcalendar0/[0,0,0] staysuninterpreted. All231laterRGBpairs/five visible differences wereindependently recomputed anddirectly viewed;matching samples do not prove future outcomes orcausality. All older Gerhard/Rafael/Hodram/B48 limitations remain.

Frozen445dependency/838policyrejection gates andindependent native/actual/menu/FE/control/loader/caller/comparison readers pass. One complete NDS object commits only after every gate; original input object/files/components/bytes remainexact beforecommit. Fourteen actual-changing semantic failures makezero commits withonlyproduction digests bypassed;all frozen/native/source/semantic gates stay active. Their unchanged predicates arebound to the corrected config byexact module/nondependency-metadata equivalence;they are reused,not claimed asrerun. Three fresh wrong-memory lifecycle inputs reject withallguards active. The preceding six-record stage still produces byte-exactV8377;all515earlier dependencies/524current dependencies andprior50semantic/fouralias checks remainbound. Five exactbuilderforms/sixteen actualchanging builders pluspreserved historical forms pass,withfull original417-source inverse. Preserve failed atomicv1/8449 andfailed registrationV8459. Only the already validated compiler planning-field binding andone accidentally mutable builder digest werecorrected in immutable successors;no prose/layout/QA/native guard wasweakened. Current configurationv3 ispassed explicitly. Own V8475ordinary coldboot4001frames/six exactstartup PNGpairs/wholeactors/currentAdernkatz12+Blades8/runtimefontCOMMONdirectory/123264payload pass without replaying optional scenes.

Allfour storylines, earlier translated dialogue, sharedtown/shop/random scenes, Help/remainingprose, all207names/roles/aliases/customnames andretrospective prematurewraps remainopen. Preserve every copied lead,family,history andmeasured technical limit. Graphics/all18plaques andlaterolder-record technicalre-audit stayseparate."""
NEXT="""Continue from verifiedV8481/currentregisteredV8475. B49'ssixteen disjoint decisions areintegrated andcredited once;reuse every completed source/context/prose/layout/native/stored/actual/menu/FE/policy/atomic/release/clean-patch/startup proof withoutunchanged replay. UseowncurrentV8475captain1 input work/analysis/current_V8475_Hodram_native_v8478/current_native_input.json with scripts/Hodram_B49_registered_route_context_v8478.py forRAM-dependent work;never overlay historicalRAM orborrowcaptain2. Preserve all timing/PRNG/component/calendar/RGB/fixture-entry limits,failedV8459 profile,allROMs/translations/drafts/producers/proofs,mainV4701 andcanonicalbaseline. No separateuserpackage,promotion,pruning,commit orpush.

Select andextract the next complete clean-Japanese Hodram exchange andits source context before reading current English. B50 hasnot yet received a new clean-first editorial pass atthis checkpoint. Resolve source event/prerequisite/speaker/relative/query/typed-choice/item/effect/FE boundaries asneeded,gloss the whole exchange,then assess earlier wording withindividual revisions orjustified retentions. Preserve approved Rafael,Hodram,Joakim,Maria,Camille names andfull cultural/factual/character voice intent. Keep broad practicaltown/random capture andrepresentative gameplay/focused concrete risks;do not require exhaustive naturalplaythroughs orindividual conditional visits. Fullfourstory/shared/Help/207names/earlierwrap objective staysactive;graphics andlater older-record technicalre-audit separate.

"""+prior_next.rsplit('\n\n',1)[-1]

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][op['before_length']:])==op['appended_sha256'];del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    release,start,view,positive,negative,binding,reg,doc,seal=map(read,[RELEASE,START,VIEW,POSITIVE,NEGATIVE,BINDING,REG,DOC,SEAL])
    manifest=read(release['manifest']);registry=read('translations/release_stack.json');candidate=Path(release['candidate'])
    assert sha(candidate.read_bytes())==release['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']==manifest['candidate_sha256']
    assert manifest['profile']==reg['profile']=='all-routes-unified-v8475' and len(manifest['batches'])==643 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==reg['registry_after_sha256'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==candidate.read_bytes()
    assert view['viewed'] and len(view['six_whole_RGB_pairs'])==6 and view['whole_actors_equal'] and view['target_family12_andprotected_Blades8_measured_inactual_coldboot_RAM']
    assert start['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass'] and start['actual_original_captain_ID']==1 and start['actual_frames']==4001
    assert positive['one_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and positive['canonical_source_path_withcomplete_V8377_memory'] and positive['planned_output_sha256']==release['candidate_sha256']
    assert negative['negative_count']==14 and all(c['rejected'] and c['commit_calls']==0 for c in negative['cases']) and binding['prior14_semantic_cases_reused_not_rerun'] and binding['new_lifecycle_rejection_count']==3
    assert seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['name_review_sha256']==sha(NAMES.read_bytes()) and reg['release_config']==str(CONFIG) and reg['release_config_sha256']==sha(CONFIG.read_bytes())
    rows=doc['records']+doc['typed_choice_records'];assert len(rows)==16 and Counter(r['decision'] for r in rows)=={'revision':7,'retention':9} and all(all(r['review'][g] for g in ['source','context','localization','naturalness','formatting']) for r in rows)
    validate_approved_batch(doc);validate_scoped_names(read(NAMES));validate_runtime(NdsImage.open(candidate));data={k:read(p) for k,p in proofs().items()}
    assert observed_scope(data)==seal['observed_scope']==positive['report']['actual_scope']==release['actual_scope_limits']
    assert release['only_SC1_B49_change_324_otherblocks_andall_other_files_components_exact'] and release['whole_ROM_equals_pinned_approved_reference'] and candidate.read_bytes()==Path(doc['reference_ROM']).read_bytes()
    return release

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR);before=LEDGER.read_bytes();old=json.loads(before);doc=read(DOC);seal=read(SEAL)
    assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and KEY not in old
    originals=doc['records']+doc['typed_choice_records'];oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in originals}
    assert len(oldkeys)==7205 and len(keys)==16 and not oldkeys&keys
    bank=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC1.DK4')).blocks;mapping=read(proofs()['relocation'])['groups'][0];rows=[]
    for original in originals:
        row=deepcopy(original);target=row['final_reference'];raw=bytes.fromhex(row['final_hex']);block=bank[49];at=target['offset'];typed='option_index' in row
        assert target['block']==49 and sha(block)==target['target_block_sha256'] and block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==target['record_index']
        command=next(c for c in mapping['all_target_commands'] if c['offset']==target['header_offset']);assert command['word']==(0x2100 if typed else 0x4000)
        body=raw.decode('cp932') if typed else raw[1:].decode('cp932');row['pre_integration_review_record_preserved']=deepcopy(original)
        row.update(predecessor_reference=deepcopy(original['current_reference']),predecessor_hex=original['current_hex'],reviewed_against_predecessor_ROM=doc['current_ROM'],reviewed_against_predecessor_ROM_sha256=doc['current_ROM_sha256'],current_reference=deepcopy(target),current_hex=raw.hex(),current_text_hex=raw.hex(),current_record_index=target['record_index'],current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],current_raw_storage_English=body,current_English=' '.join(body.split()),current_stored_English=body,current_reference_ROM=release['candidate'],current_reference_ROM_sha256=release['candidate_sha256'],completed_candidate_reference=deepcopy(target),completed_candidate_sha256=release['candidate_sha256'],integrated_reference=dict(**target,stored_hex=raw.hex(),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True,registered_integration_pending=False,individually_activated_in_current_build=False,current_observation_scope='Exact tested reference ROM equals registered V8475;disclosed initialized whole/bounded-tail scenes andfocusedFE/menu tests,not natural optional activation orlegitimately earned trade eligibility.',actual_proofs=dict(whole=proofs()['actual'],bounded_tail=proofs()['tail_actual'],menu=proofs()['menu_actual'],FE=proofs()['FE_geometry']),editorial_unit_kind='typed-choice' if typed else 'speech')
        assert all(row[k]==original[k] for k in ['english','source_hex','source_reference','source_meaning','context','localization_note','retention_reason','review','decision']);rows.append(row)
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,CONFIG,DOC,NAMES,SEAL,RELEASE,START,VIEW,POSITIVE,NEGATIVE,BINDING,REG,Path(__file__),*map(Path,proofs().values())]}
    ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=7,retained=9,source_prose_and_completion_credit_added_once=16,physical_speeches=14,typed_choice_labels=2,actual_speech_page_occurrences_both_versions=34,actual_complete_body_andname_orabsent_header_holds=200,actual_visible_choice_label_samples=24,actual_original_optional_activation=False,all_actual_scope_limits_preserved=True,source_current_compiled_stored_actual_andintegrated_refs_bound=True,all36commands14preambles8relatives_query_typedmenu_effects_fullend_andtails_preserved=True,both_clean_source_andfull_predecessor_inverses_exact=True,policy_expected_rejections=838,atomic_semantic_rejections=14,prior14_semantic_cases_reused_byexact_binding_not_rerun=True,new_all_guard_lifecycle_rejections=3,seven_original_infos_zero_warnings_orwaivers_preserved=True,new_registered_startup_frames=4001,all_prior_scope_graphics_separation_later_audit_preserved=True,summary=summary,evidence=evidence,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for key,value in zip(COUNTERS,AFTER,strict=True):put([key],value)
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC1.DK4']==125;put([key,'/data/SC1.DK4'],141)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC1.DK4',blocks=[49],record_IDs=[r['id'] for r in rows],records=rows,final_review=str(FINAL),revised_count=7,retained_count=9,fresh_revisions=7,fresh_retentions=9,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC1.DK4',id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=7221,fresh_pass_records_integrated=7221,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=16,physical_speeches=14,typed_choices=2,final_review=str(FINAL),new_revisions=7,justified_retentions=9,new_completed_records=16,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_unique_speech_displays=14,actual_typed_options=2,offline_only_objects=0,all_source_English_fixture_proofs_reused_without_replay=True)])
    if str(DOC) not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[str(DOC)])
    put(['active_source_prose_drafts','route_record_subsets_pending',str(DOC)],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5605
    for key,value in dict(reviewed_route_records=5621,completed_route_records=5621,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-native-stored-actual-registered-release',file_path='/data/SC1.DK4',blocks=[49],completion_credit_added=16,final_review=str(FINAL),actual_original_optional_activation=False,actual_speeches=14,actual_typed_options=2,full_goal_complete=False)])
    put(['formatting_watchlist',FAMILY],dict(status='fourteen-complete-singlepages-two-typedchoices-originalFE-sourcequalified-ellipsis-fullwidth-registered-pass',final_review=str(FINAL),seven_original_row_infos_zero_warnings_orwaivers=True,all_scope_andprior_leads_preserved=True,full_goal_complete=False))
    current=deepcopy(old['current_integrated_candidate']);current.update(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False,**{f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    pending=dict(status='select-next-complete-clean-Japanese-exchange-before-current-English',source_positions_credited=0,completion_credit_added=0,whole_four_story_shared_town_shop_random_Help_names_andwrap_objective_active=True,full_goal_complete=False)
    oldpending=prior['pending_source_batch'];marker=dict(completion=KEY,final_review=str(FINAL),records=16,all_prior_pending_notes_historical_not_deleted=True,new_credit_added_here=0)
    put([oldpending,'registered_integration_completed_by'],marker);put([NEXT_KEY],pending)
    prior_scope=old[prior['unfinished_scope']];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256'];inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT;inventory[NEXT_KEY]=deepcopy(pending);inventory[KEY]=dict(final_review=str(FINAL),completed_objects=16,revisions=7,retentions=9,registered_candidate=release['candidate'],all_previous_limits_andfull_objective_preserved=True)
    if oldpending in inventory:inventory[oldpending]['registered_integration_completed_by']=marker
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5621,completed_route_records=5621,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory);put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,next_clean_exchange_not_yet_selected=True,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,new_source_prose_reviews=16,new_completed_records=16,revised=7,retained=9,new_current_candidate_emulator_runs=1,new_current_candidate_frames=4001,all_prior_actual_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
    assert {historical_key(r) for r in new[fp[0]]['record_keys']}=={historical_key(r) for r in new[fp[0]]['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V8480; V8475 current\n\n' if name=='editorial_handoff_current.md' else '')+'## V8480: Hodram B49 sixteen decisions integrated once in cumulative V8475\n\n'+summary+'\n\n';targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for index,(path,value) in enumerate(targets.items()):
        planned=ROOT/f'{index:02d}.after';planned.write_bytes(value)
        if path!=LEDGER:(ROOT/f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all16_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Staged B49completion:16disjoint decisions/7revisions/9retentions;deep inverse audit next.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        release=gates();plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256'] and sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest_ in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest_
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_family_record_counter_candidate=True,exactly16_disjoint_new_records=True,full_goal_complete=False));print('Deep inverse audit passed;all earlier records/counters/candidate/scope recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly16_decisions_credited_once=True,current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False));print('Applied V8475:7221completed/7224source-prose/4481revised/2740retained;full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();prior=read(PRIOR);verified=deepcopy(prior)
            assert len({historical_key(r) for family in new['completed_editorial_families'] for r in family['records']})==7221
            verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),**dict(zip(COUNTERS,AFTER,strict=True)),completed=7221,source_prose=7224,revised=4481,retained=2740,SC0=368,SC1=141,SC2=4915,SC3=197,reviewed_routes=5621,completed_routes=5621,manifest_batches=643,accepted_layers=114,release_checks=18,regressions=110,Hodram_B49_completed_once=True,Hodram_B49_atomic_registered_integration_pending=False,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=NEXT_KEY,next_clean_exchange_not_selected=True,new_uncredited_source_positions=0,physical_speeches_pending=0,typed_choice_labels_pending=0,new_credit=16,new_emulator_runs=1,new_actual_frames=4001,all_sessions_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified);print('VerifiedV8481/currentV8475:7221completed,16B49decisions credited once;nextclean exchange notselected;full objective active.')
