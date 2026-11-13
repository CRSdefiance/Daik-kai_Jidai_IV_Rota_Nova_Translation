"""Audited zero-credit source/prose/native/stored checkpoint; complete goal preserved."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_checkpoint_v8746')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8747')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8731/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B31_B53_allfive_gates_actual_reviewed_pending_policy_atomic_andrelease_v8746'
SCOPE='unfinished_editorial_scope_v8746'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
COUNTS=[7234,7237,7237,4489,2745]
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS as ACTUAL_PROOFS
PROOFS={**ACTUAL_PROOFS,
 'actual_review':'work/analysis/Hodram_B31_B53_actual_review_v8744/qualified_actual_review.json',
 'formatting':'work/analysis/Hodram_B31_B53_format_v8745b/formatting_approval.json',
 'manuscript':'translations/hodram_B31_B53_editorial_manuscript_v4.json',
 'names':'translations/hodram_B31_B53_speaker_name_review_v3.json',
 'registered_release':'work/analysis/Hodram_B52_release_v8705/registered_release_verification.json',
 'registered_startup':'work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
}
SUMMARY="""Current verified experimental cumulative ROM remains V8704. Counts remain7,234 completed/7,237 credited source-prose anddrafts/4,489 integrated revisions/2,745 justified retentions;SC0 368/SC1 154/SC2 4,915/SC3 197/COMMON1,600 completed and1,603 source-prose;route subtotal5,634 isnot the full-goal denominator. B52 remains credited exactly once. Full all-four-storyline/earlier translated dialogue/shared town-shop/random/Help/remaining prose/all207 names-roles-aliases-customnames/retrospective premature-break objective remainsactive. Preserve every ROM,translation,draft,executed producer,proof andfailure. Five new research ROMs are pinned(one complete two-block reference,four initialized source/English fixtures);none is a registered candidate,new parent,promotion orseparate requested package. Registry/currentrelease/mainV4701/canonicalbaseline remainunchanged;no pruning,commitorpush. Roughly20,000remainingcandidates remains onlya planningestimate. Graphics/all18plaques andlater older-record technical re-audit stayseparate.

B31/B53's three revisions remain unintegrated/uncredited. Latest translations/hodram_B31_B53_editorial_manuscript_v4.json andnamesv3 passallfive individual gates andstandard natural-dialogue-v2 validation withdialogue-relocatable-v1. Keep You just won't quit,will you?Fine.I'll take you on myself. andthe longer before you cross a man you really ought to fear.clause;sourcefirst-person agency isrestored without inventing the unnamedman's identity. Keep Looks like you've finally ended up wanted by the Ottoman Empire.You'd better watch yourself.;the unsupported bounty isremoved andようだ/とうとう/されちまった arepreserved. Actual editable prose retains proper spaces. All approved words,source/current/compiled/stored/final references,native pages andindividual reasons remain exact. Three full216px automatic pages use2/4/3rows,zero QAissues,warnings orwaivers,no authored ordinary breaks,padding,shortening,narrowed viewport,font/metrics/guard change.

Clean-first source/gloss8714,controls8718,source names8719,source dispatch/pages8720 anddirectview8721 preceded currentEnglish8722. Reuse allcompleted source/prose/logical/compiled/stored work8723-8729 without unchanged replay. Eighteen commands,three complete six-byte preambles,four relative sites20cases,one unforced8000query,eight opaque structural pairs,50seeded normalends andfour EV1getters bind. Source52->31->53 prerequisites donot prove continuousconversation,original location,earnedchronology,either B52choiceeffect orunnamedmanidentity. Preserve6311/6000/633F/623F/A000 structurally withoutinvented effectsemantics. B31's two speeches arealternate variants;neither flags norpredicates wereforced.

Source namecomposition8732 executes anexplicit clean-only ordinary actor34fixture withactualoriginalcode,getters,fieldreads,ABI/ring/unowned4MiB guards. Originalprogressive isバルバロッサ・ハイレディン;originalfull isバルバロッサ・ファーズル・ハイレディン. The middle fieldisnot unused. Scoped8735retention preserves Barbarossa Hayreddin andBarbarossa Fazul Hayreddin in the game's establishedorder;do notdelete the middlefield,reorderfromhistory,add rank/kinship orreplace namesfromlore. Currentfullgetter retains exact Ｆazul bytes8265617a756c,withno nameasset change. Sourcefull has19CP932glyphs:the literal216pxstyle11testwraps finalンto[0,16]. Original8733stopped onits erroneousone-row assumption;8733b checksall19codes/positions underunchangedgeometry. Both source/current literal sheets wereviewed. Actual complete progressiveheaders for34/113areverified;actual fullcatalogueUI,wider113contexts/all207/customnames remainopen.

Independent18-command-atom reconstruction8734 equals the sparse two-block/archive result andseparately computesallfouroffsets. B31196->228stored bytes/B53136->156;every323unownedblock/allotherfiles/components,both clean/currentblock inverses,complete parentarchive andwholeNDS inversepass. Reference8736 isexact independentlyreconstructed target. Native loaders8737 pass325complete loads/cachehits,650initialparentmodes,326actions. References8738 bindall18commands/allthreefinalreferences/bothoriginalEV1blockentries/complete unchanged decodedsection-overlay caller census;reuseonlythrough exactnames,bases,lengths andpayload hashes. Four whole-block fixtures8739retain eightoriginalHodram openinginitializers34bytes,thenconstant-shift every selected source/target command by34. No speech,relative,query,opaquecontrol ornormalend isomitted. Bothlanguagesusecurrent Englishnames/UI/code/font;these arenot natural optional-event visits.

Four terminal/reaped coldboots8740total24,004frames. Audits8742/B31 andqualified8742b/B53 verify76complete body-name holds/fourpageoccurrences/twoobserveduniqueutterances:long B31R0018 andB53R0007 inbothlanguages. Sourcequery returns[2,1] unforced,selectinglong B31. ShortR0013remainsoffline-only withcomplete pages/branches/preamble/consumer proofs;do notforceitscondition orclaim anactualvisit. B31returns[0,1]at4016inbothlanguages;B53returns[0,0]at4013inboth. Complete nameplates/portraits/first-internal-finalglyphs,sourcepayloads,selectedflow,bounds,pagination andcallback/coreintegritypass. The four actualdialogue/transition sheetsweredirectlyviewed.

Preserve a corrected audit mistake:original8742wrongly equatednormalend's persistentresultsecondword withthe interpreter's r3carried mode. B53shows priorparserresult[3,0] andr3mode1 before[0,0]end. Own50seededendcases preserveinitialresultwordindependentlyofr3;unchanged50callerfragments preserveallsixresultwords. Qualified8742brestores thatchannelcheck without changingROM,captures orpixelguards. CompletedB31audit remainsvalid becauseboth independentlyrecorded channels happen tobe1;itscapturenowneednotbereplayed. Keep stoppedB53audit,incorrectpreparer andqualifiedreader,alongwiththe laterolder-recordtechnicalre-audit. This isanaudit correction,notanemulator/ROMfix.

Comparison8743/qualifiedreview8744 retainallmeasured differences:two B31decodedlengthchanges(0300span68->78,longspeech98->120) andone B53speech86->104;no commandduration,UIrequest,boundaryRNG orfollowingcommanddifferences. Eachpairhasallfivenativecomponents/wholeactors/captain1/rawcalendar/finalseed3325064553matching;all34laterRGBpairsperblock(68total)match. Six followingoriginalcachecommandsperlanguage match. These arebounded observations through6001frames,not every-framecausality,broadfuturesimulation,original eligibility/location/earnedprogress,fullcatalogueUI,customnames,fullroute orhardwareproof. Earlier B52/B51/B50/B49/Gerhard/Rafael/Hodram/Lil timing,RNG,RGB,calendar,following-command andfixture limits remainintact.

Formattingwriter8745 completed immutable manuscriptv4/namesv3 thenstopped whilebuilding itsreceipt bycalling read_bytes ona stringpath. Qualifiedreader8745b revalidates both complete outputs,standardv2,allwords/bytes/references/gates,andwritesonlythe missingreceipt withPath-normalized evidence. The stoppedwriter/emptyoriginalreceiptroot andallpartial-complete artifacts remain;no nativeprobe,actualcapture orapproval isreplayed. Latest approval work/analysis/Hodram_B31_B53_format_v8745b/formatting_approval.json.

Continue fromverifiedV8747/currentV8704. Required next work isfrozen source-qualified compiler/native policy andmeaningful changed-input checks,independent productionevidence readers,one whole-NDSatomiccommit,shared registered cumulativebuild/exactclean-inputpatch/ownstartup,thenexactlythreeonce-onlycompletion decisions. Reuseallcompleted source/native/independent/loader/reference/actual/name/formatproofs. Do notrepeat B52integration/startup orunchanged B31/B53captures. Retain thefullunfinishedscope andallpreviousartifacts;no promotion orseparatepackage."""
NEXT='Continue B31/B53 from qualifiedactual8744/format8745b withimmutable manuscriptv4/namesv3 in strict ownV8704 captain1 context. Freeze source-qualified compiler/native policy,validate meaningful changedinputs andindependent productionreaders,thenwholeNDSatomic/sharedregisteredintegration/exactcleanpatch/ownstartup andthree once-onlycredits. ActualshortB31 andfullcatalogueUI remainunvisited;allfullscope leads stayactive.'

def inverse(value,operations):
    result=deepcopy(value)
    for op in reversed(operations):
        if op['existed']:result[op['key']]=deepcopy(op['before'])
        else:del result[op['key']]
    return result

def gates():
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==7234 and prior['candidate_sha256']==data['manuscript']['current_ROM_sha256']==data['registered_release']['candidate_sha256']
    for k,p in [('candidate','candidate_sha256'),('patch','patch_sha256'),('manifest',None)]:
        path=Path(prior[k]);assert path.exists()
        if p:assert sha(path.read_bytes())==prior[p]
    assert data['source_controls']['complete_source_commands']==18 and data['source_controls']['normal_seeded_end_cases']==50
    assert data['formatting']['all3_five_gates_true'] and data['formatting']['standard_natural_dialogue_v2_validation_pass']
    assert data['formatting']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and data['formatting']['names_sha256']==sha(Path(PROOFS['names']).read_bytes())
    assert all(all(r['review'].values()) for r in data['manuscript']['records']) and not data['plan']['failures'] and all(not r['base_QA']['issues'] for r in data['plan']['records'])
    assert (data['actual_review']['total_runs'],data['actual_review']['total_frames'],data['actual_review']['total_holds'])==(4,24004,76)
    assert data['actual_review']['offline_only_text_IDs']==['DK4_MES_B31_R0013'] and data['actual_review']['all_four_sheets_directly_viewed']
    assert data['independent']['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    assert data['loaders']['fresh_native_whole_loads_andcache_hits']==325 and data['loaders']['fresh_initial_parent_modes']==650
    assert data['relocation']['other323_blocks_byte_exact'] and data['relocation']['whole_inmemory_NDS_inverse_andall_other_files_components_exact']
    assert data['stored']['complete3stored_first_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass']
    assert data['registered_startup']['viewed'] and data['registered_startup']['whole_actors_equal']
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and [old[k] for k in COUNTERS]==COUNTS and old['goal_status']=='active' and not old['full_goal_complete']
        completed={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};assert len(completed)==7234
        records=data['manuscript']['records'];assert not completed&{historical_key(r) for r in records} and len(records)==3
        new=deepcopy(old);ops=[]
        def put(k,v):
            ops.append(dict(key=k,existed=k in new,before=deepcopy(new.get(k))));new[k]=deepcopy(v)
        pending=dict(status='three-contextual-revisions-allfivegates-native-stored-independent-names-andactual-reviewed-frozen-policy-atomic-registered-pending',file_path='/data/SC1.DK4',blocks=[31,53],
            physical_speeches=3,typed_choice_labels=0,proposed_revisions=3,justified_retentions=0,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,
            records_with_exact_source_current_compiled_andstored_references=deepcopy(records),stored_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True,all_formatting_gates_false=False,all_five_individual_gates_true=True,full_name_resolution=deepcopy(data['names']['full_name_resolution']),
            source_commands=18,source_relative_sites=4,source_rawqueries=1,opaque_controls=8,source_seeded_end_cases=50,source_relative_cases=20,current_relative_cases=20,relocated_relative_cases=20,
            source_dispatches=3,current_dispatches=3,stored_dispatches=3,source_alignment_cases=12,logical_alignment_cases=12,compiled_alignment_cases=12,stored_exact_reused_alignment_cases=12,
            complete_source_pages=3,complete_English_pages=3,automatic_fullwidth_px=216,QAissues=0,warnings=0,waivers=0,
            actual_B31_B53_emulator_runs=4,actual_B31_B53_frames=24004,actual_body_andname_holds=76,actual_unique_text_IDs=['DK4_MES_B31_R0018','DK4_MES_B53_R0007'],offline_only_text_IDs=['DK4_MES_B31_R0013'],registered_integration_andcredit_pending=True,source_positions_credited=0,new_credit=0,full_goal_complete=False)
        descriptor=old[prior['unfinished_scope']];assert sha(Path(descriptor['path']).read_bytes())==descriptor['sha256']
        scope=deepcopy(read(descriptor['path']));assert KEY not in scope
        ROOT.mkdir(parents=True);scope[KEY]=deepcopy(pending);scope['latest_next_focus_v8746']=NEXT
        scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,scopepath,Path(__file__),*map(Path,PROOFS.values())]}
        put('latest_checkpoint',SUMMARY+'\n\n'+NEXT)
        put(SCOPE,dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),all_prior_scope_keys_values_history_andfull_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,new_uncredited_contextual_revisions=3,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put(KEY,dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,goal_turn_classification='progress',
            prior_goal_turn_was_concrete_editorial_andnative_progress=True,current_turn_independent_names_actual_andformat_progress=True,
            prior_clean_gloss_checkpoint_retained_as_historical_state=prior['pending_source_batch'],all_new_jobs_terminal=True))
        new[KEY]['inverse_operations']=deepcopy(ops)
        assert inverse(new,ops)==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8746; V8704 current\n\n' if name=='editorial_handoff_current.md' else '')
            prefix+='## V8746: B31/B53 agency and bounty revisions; allfivegates, names andrepresentative actual verified;policy/atomic/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
            targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        protected=[Path(prior[k]) for k in ['candidate','patch','manifest']]+[Path('translations/release_stack.json'),Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds'),Path('translations/rom_retention_pins.json'),Path(data['reference']['research_ROM'])]+[Path(f['research_ROM']) for f in data['fixtures']['fixtures']]
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,protected={str(p):sha(p.read_bytes()) for p in protected},inverse_operations=ops,unchanged_counters=COUNTS,new_credit=0,full_goal_complete=False))
        print('V8746 staged:three uncredited revisions/native/stored proof,six exact targets. Inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert inverse(new,plan['inverse_operations'])==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and not new['full_goal_complete']
        for row in plan['files']:
            assert sha(Path(row['planned']).read_bytes())==row['planned_sha256'] and sha(Path(row['target']).read_bytes())==row['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in {**plan['evidence'],**plan['protected']}.items():assert sha(Path(path).read_bytes())==digest
        descriptor=old[prior['unfinished_scope']];oldscope=read(descriptor['path']);newscope=read(new[SCOPE]['path'])
        assert all(newscope[k]==v for k,v in oldscope.items()) and set(newscope)-set(oldscope)=={KEY,'latest_next_focus_v8746'}
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            for i,row in enumerate(plan['files'][1:],start=1):
                original=gzip.decompress((ROOT/f'{i:02d}.before.gz').read_bytes());assert sha(original)==row['before_sha256'] and Path(row['planned']).read_bytes().endswith(original)
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),every_prior_ledger_value_family_record_counter_andcandidate_recovers_exactly=True,
                every_prior_scope_key_andvalue_anddocument_byte_preserved=True,protected_ROMs_patch_registry_unchanged=True,new_credit=0))
            print('V8746 audit:whole oldledger inverse,allscope keys,allold documentbytes,counters/candidate/registry/ROMs exact.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for row in plan['files']:
                target,planned=Path(row['target']),Path(row['planned']);assert target.is_relative_to(Path.cwd().resolve()) and planned.is_relative_to(ROOT.resolve())
                with target.open('r+b') as stream:stream.write(planned.read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(target.read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_registry_orcompletion_counter_change=True,new_credit=0,full_goal_complete=False))
            print('V8746 applied;currentV8704 andall7234completed unchanged;fullgoalactive.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,next_clean_exchange_not_selected=False,
                Hodram_B31_B53_actual_names_allfivegates_checkpoint=deepcopy(new[KEY]),new_uncredited_source_positions=3,physical_speeches_pending=3,typed_choice_labels_pending=0,
                new_credit=0,new_emulator_runs=4,new_actual_frames=24004,new_research_ROMs=5,all_new_native_jobs_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8747/currentV8704:three contextual revisions/allfivegates/independent/names/actual complete;frozenpolicy/atomic/registered pending;zero completion credit;fullgoalactive.')
