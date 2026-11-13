"""Checkpoint clean Hodram/source/current-native/name concern proofs without newcredit;full goalactive."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B50_v8184 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_source_checkpoint_v8194')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8195')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8185/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v1.json')
KEY='Hodram_SC1B137_B45_B46_source_native_pending_surname_current_prose_release_v8194'
OLD_KEY='Hodram_SC1B137_B45_B46_clean_gloss_pending_native_context_current_andrelease_v8184'
SCOPE='unfinished_editorial_scope_v8194'
PROOFS={'source137': 'work/analysis/Hodram_B137_clean_context_v8180/complete_clean_SC1_B137_EV1_andcoverage_before_current_English.json', 'source45': 'work/analysis/Hodram_next_clean_v8178/complete_clean_SC1_B45_EV1_andcoverage_before_current_English.json', 'source46': 'work/analysis/Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json', 'clean_names': 'work/analysis/Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json', 'gloss': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json', 'prior_B44': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/27_prior_clean_B44_source_refs_exact_no_new_credit.json', 'current_input': 'work/analysis/current_V8172_Hodram_native_v8187/current_native_input.json', 'startup': 'work/analysis/Hodram_current_binding_v8187/own_Hodram_startup_andstrict_captain1_context.json', 'startup_view': 'work/analysis/Hodram_current_startup_view_v8189/own_Hodram_startup_sheet_viewed.json', 'controls': 'work/analysis/Hodram_B137_B45_B46_source_controls_v8188/three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json', 'picture': 'work/analysis/Hodram_B46_pigment_v8190b/original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json', 'paths': 'work/analysis/Hodram_B137_B45_B46_source_paths_v8191/11_structural_compositions_all60_commands28_source_memberships.json', 'native_names': 'work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json', 'names': 'translations/hodram_B137_B45_B46_speaker_name_review_v1.json', 'surname_source': 'work/analysis/Hodram_B137_B45_B46_name_review_v8193/five_clean_surname_mentions_selfintro_andprior_name_decision.json'}
SUMMARY='Currentregisteredcumulative remainsV8172;mainV4701 unchanged. Counts7171completed/7174source-prose-anddrafts/4455integratedrevisions/2716retentions;SC0368,SC191,SC24915,SC3197,COMMON1600complete/1603source-prose,routesubset5571. B50 is completeandcreditedonce;639manifest/114accepted/18releasechecks/110regressions/fullreference/exactcleanpatch/ownstartupverified. Fullgoalactive. No separateunifiedtestpackage,promotion,pruning,commit orpush. PreserveallROMs/translations/producers/proofs/failures.\n\nNextHodramSC1B137/B45/B46sourcecontext/nativephase isnowverifiedwithzero newcredit. All28firstcleanglosses,sixcleanidentities,27exactpriorB44sourcecallbacks were read/bound beforecurrentdialogueEnglish. B13721speechapology/staffing/Mediterreaneanrouteplanning,B45oneAmsterdam invitation,B46six-speechmap-decipheringkey/first-findchallenge. Exacteventgraph137requires44;45excludes46;46requires137and45,notproof oftotalchronology/outereligibility/naturalactivation. FreshordinaryownV8172HodramNewGame4001frames/captain1,exactcurrent123264pool/2b6/COMMON/directory/nativecontext anddirectstartupview pass. Hodram/Joakim/Bergstrom fields andHodramBergstromheader viewed;noneofthenewoptionalscenes hasbeenactivated. Owninput work/analysis/current_V8172_Hodram_native_v8187/current_native_input.json. Rafaelowninput8175also remainscurrent;otherroutes historicaluntilrebound/recaptured.\n\nAll60cleancommands/28completepreambles/threewholeterminals andtails pass undercurrentdecodedcode. Eightrelative sites/40native structuralprevious-result cases,twounforced8000results and75seedednormalvaluecarryends pass. Sourceactors01/02/09/10/12/71;0x71 isPortWorkerspeakerstate,notliteralq. ZeroFE/FI/FA/FO inthenewthreeblocks. NativeEV1getterbinds44/45/46/137withall4MiB/ABI/actors/events/RNGunchanged;doesnot proveeligibility. RawB137offset8460080ffff400102a3 returns[2,0,0,0,0,0];B46offset3380080ffff000009a0 returns[2,1,0,0,0,0]intheordinaryopeningcontext. Do notcallraw8000boolean ortypedmenuwithoutconsumerproof. Elevenstructuralcompositionsretain3distinctcommandpathsforB137,1forB45,3forB46;eachhasexactlyonecompleteTEXTpath:all21/1/6speeches respectively. Conditionalpathschangeeffects,nottextmembership. Everyoriginalcommand/paragraphisinstructuralunion;theoreticalrawclassesarenotforcedgamestates orproofallpathsattainable. AlloriginalA000/4800/4700andothercontrolsremainopaque/preservedwherefullbodieswerenotexecuted.\n\nFreshsourceB46 original4800at1400048b5a8usesdescriptor[0,181,1,5],layout[0,0,0]. Cleanitem181紅色の顔料/currentregisteredRedDye andoriginalcategory0bounds/callto4A930areexact. B50had4821/layout[2,0,1];do notreuseitsactualcardgeometryasproofthisdifferent4800behavior. Legacy8190probeexcludedsourc4800initswhitelistandfailedbeforedescriptorlogic;preserveitsproducer/root. Source-lockedsuccessor8190bpermitsonlyexact4800andretainsall4MiB/ABI/owner/input/output/extent/boundaryguards. Noresourcebody/cardbounds/inventoryaward,naturalactivation,newitemasset orduplicateitemcreditclaimed. B46identifiesakeybutdoesnotexplicitlygiveanewmap orstateHodramhaswon/acceptedthecontest.\n\nSixfreshcurrentstaticvoices,12originalprogressive/fullnamegetters and24syntheticFI/FA/FOalignments pass withoutunownedmutation. CurrentHodrameditablecaptainobjectisusedforactor1;syntheticdefaultsHodram6/Bergstrom9/BergstromFleet15aremeasured,notRafael6/6/10. Sourcehaszeromacros;noneadded. Nativeheaders:HodramBergstrom,LilArgot,CamilleOverijssel,GerhardArdelknatts,CharlesRochefort,PortWorker. FullgettersretainHodramJoakimBergstrom,CamilleMarinusOverijssel,CharlesJeanRochefort;PortWorkerdoesnotexposeEuropeasafamilynamesuffix. Completeglyph/nameplane/bounds/actualnewsceneheaderchecksremainpending. Initialnamepacket translations/hodram_B137_B45_B46_speaker_name_review_v1.json recordsfiveindividualsource-contextretentionswithformattingfalse. Gerhardgivennameisretained;familynamespellingnotautomaticallyapproved:sourceアーデルンカッツhasn-before-kwherecurrentArdelknattshask-before-n. Ardelnkattsisaminimalproposal,notshippedorcanonicallyverified. FiveexactcleansurnamementionsinSC2B27/B74andpriorLilB222retentionarebound;priorapprovalaloneisnotfreshjustification. OfficialJapanesewebreferencesdidnotestablishdecisiveLatinspelling;garbledlegacycrewpagewasnotusedasreliableevidence. Resolvebyfullsource/currentconsumerreviewandjudgment;do notimposeunavailableexternalLatinasanewmandatorygate orinventhistoricalidentity/rank/biography. Broader207/PortWorkerconsumerleadsstayopen.\n\nCurrentEnglishDIALOGUEbodiesB137/B45/B46remainunconsulted;noEnglishmanuscript/source-prose/completioncredit. No28-pagefont/layout/actualnewscene/frozenpolicy/atomic/registeredreleaseapprovalisyetclaimed. AllpreviousB50timing/RNG/component/byte/calendar/RGB/activationlimits,allfourstories/sharedtown-shop/random/Help/remainingprose/retrospectivewraps/namealiases,graphics/all18plaquesandlaterolder-recordtechnicalre-auditremainopen/preserved.'
NEXT='ContinuefromverifiedV8195/currentV8172. ReusefreshHodramowncaptain1input8187/sourcecontrols8188/source4800RedDye8190b/structuralpaths8191/namesvoicesdefaults8192. Initialnameeditorialpacket8193hasfiveindividualretentionsandonependingGerhardsurname-orderconcern;allformattingfalse. Reviewregistered/currentArdelknattsconsumersandtheircompletecleancontexts,thendecidejustifiedretentionoracorrectionwithglobalconsistencytests. Donotautosignoffbecauseolderapprovedretentionexists,dontinventGermanhistoricalidentity,anddonotrequireunavailableoriginalLatinproofasamandatoryexternalgate. Preserveallpriornameassets/approvalartifacts. ApprovedHodram/Joakim/Camillecannotbechanged. Nativecurrenttable/gettersaretechnicalevidence,notsubstituteforfreshlocalization. The28bodyglosses/sourceidentities/graph/nativepathsarecompleteenoughtobegincurrentbodymapping/effectiveconsumercomparisonwhenready;anysurnameassetdecisionstaysanexplicitregistereddependency ratherthanasilentglobalrename. Reviewfull28Englishconversationprogressionagainstcleansource,retainworkingwordingwithindividualreasons,andpreserveCharlesbluntness,Camillehesitantapology,Hodramformalrestraint,Gerhardpracticalfleetadvice,Lilfinancialcompetitivebravado andHodrammapkeyconfusion. No newrank,kinship,romance,permanentalliance,guaranteedrecruitment,completedtraderoutes,mapownership,giftoraccepted/woncontest. Thenownroute-awareautomaticlayoutwithvalidatednativewidth/4rows/fullfirst-internal-lastglyphs/bounds/pagination/storedparity/fullcontrols. Preserveall60commands/eightrelativeoperands/twonevaluatoroperands/threefullends. Usefreshfocusedactual4800/layout0/hide4700,silences,andrepresentativescenes/transitions/normalreturns. All28speechesbelongtoeverysourcedtextpath;distinguishunvisitedconditionaleffectsfromactualspeechcoverage. Native/actualfont/headerproofs,frozenpolicy/atomic/registeredcumulative/exactcleanpatch/ownstartupmustpassbeforeonce-onlycredit. Noneofthe28newobjectsiscredited.\n\nKeepfullobjectiveallfourstories/earliertranslateddialogue/sharedshops-towns/random/Help/remainingprose/all207names-roles-aliases/retrospectiveearlybreaks. Preserveeverypriorunfinishedinventory,12contraction/questiontagleads,unscannedbeyond558plans,weak-before-row/page-before-readability/phrasecoherence. KeepPasardistinctfromPasha,Cristina/Christina,HansRetzel/Letzel,Trader/PortWorker/Guildmaster,Sailor151-159versusRetainerconsumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andallrecordeditem/counterpart/displayleads. Graphics/all18plaques andlaterolder-recordtechnicalre-audit separate:normalendcarry,B35R65/B48R129source19thcells,B48stalerelocationlabel,B47correctedregistrationreceipt,B50checkpoint8149blocklabelcompanion,andalltiming/highlight/RNG/component/byte/calendar/RGB/fixture-reentrylimits. PreserveallROMs/translations/drafts/failures/executedproducers/proofs. MainV4701unchanged;no separateunifiedpackage,promotion,pruning,commit orpush. Fullgoalactive.'

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==7171 and prior['manifest_batches']==639
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==data['current_input']['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==28 and doc['source_only_no_current_body_orname_comparison_no_localized_manuscript'] and all(r['current_English_body_not_yet_consulted'] for r in doc['records'])
    assert len(names['records'])==6 and sum(r['decision']=='retention' for r in names['records'])==5 and sum(r['decision']=='pending-surname-review' for r in names['records'])==1 and all(not r['review']['formatting'] for r in names['records'])
    gerhard=next(r for r in names['records'] if r['actor_ID']==16);assert not gerhard['review']['localization'] and not gerhard['review']['naturalness']
    assert data['startup']['actual_original_captain_ID']==1 and data['startup']['actual_frames']==4001 and data['startup']['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert data['startup_view']['viewed'] and data['startup_view']['startup_proof_sha256']==sha(Path(PROOFS['startup']).read_bytes())
    assert data['controls']['source_relative_sites']==8 and data['controls']['source_native_relative_cases']==40 and data['controls']['source_raw_predicate_query_count']==2 and data['controls']['normal_seeded_end_cases']==75
    assert sum(len(g['all_original_source_commands']) for g in data['controls']['groups'])==60 and sum(len(g['complete_source_speech_preambles']) for g in data['controls']['groups'])==28
    assert data['paths']['structural_compositions_evaluated']==11 and all(g['distinct_complete_text_path_count']==1 for g in data['paths']['groups'])
    assert data['picture']['current_English']=='Red Dye' and data['picture']['native_picture_case']['original_picture_boundary_calls'][0]['layout']==[0,0,0]
    assert len(data['native_names']['native_twelve_progressive_andfull_getters']['rows'])==12 and data['native_names']['measured_default_macro_lengths']==dict(FI=6,FA=9,FO=15)
    assert len(data['surname_source']['records'])==5
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
        pending=dict(status='28-clean-glosses-current-Hodram-native-controls-paths-item-names-pass-pending-surname-body-English-native-layout-actual-release',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
            file_path='/data/SC1.DK4',blocks=[137,45,46],objects=28,current_English_body_unconsulted=True,
            source_commands=60,source_relative_sites=8,source_relative_cases=40,raw_predicate_query_count=2,seeded_end_cases=75,
            structural_compositions=11,distinct_text_paths_each_block=1,static_names=6,current_name_getters=12,synthetic_macro_alignments=24,
            five_preliminary_name_retentions_one_surname_concern=True,name_font_layout_actual_headers_pending=True,
            own_Hodram_actual_startup_frames=4001,new_optional_scene_gameplay_runs=0,
            current_native_input=PROOFS['current_input'],all_proofs=PROOFS,current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],
            new_credit=0,new_emulator_runs=1,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending)
        if OLD_KEY in inventory:inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,own_Hodram_context_source_controls_paths_item_andnative_name_getters_now_pass=True,surname_editorial_concern_andbodyEnglish_native_actual_release_pending=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],dict(checkpoint=KEY,own_Hodram_context_source_controls_paths_item_andnative_name_getters_now_pass=True,surname_editorial_concern_andbodyEnglish_native_actual_release_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8194: Hodram clean-source/current-native controls, item andnames bound; surname/body/prose/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V8194; V8172 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('Hodram source/native checkpoint staged;six targets,zero credit.Deep inverse audit next.')
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
            print('Hodram source/native checkpoint applied;currentV8172 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                strict_own_Hodram_current_input=PROOFS['current_input'],Hodram_source_native_checkpoint=dict(blocks=[137,45,46],objects=28,commands=60,relative_sites=8,relative_cases=40,raw_predicates=2,seeded_ends=75,static_names=6,native_getters=12,synthetic_alignments=24,source4800_layout=[0,0,0],name_surname_concern_pending=True,current_dialogue_English_unconsulted=True,new_optional_scene_runs=0),
                new_credit=0,new_emulator_runs=1,new_actual_frames=4001,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8195/currentV8172:7171completed;Hodram60commands/28cleanglosses/8relatives/2rawpredicates/currentcaptain1/names-item bound.Surname/bodyEnglish/layout/actual/release pending.Full goal active.')
