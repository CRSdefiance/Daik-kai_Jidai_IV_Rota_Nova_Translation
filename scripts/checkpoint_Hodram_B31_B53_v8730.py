"""Audited zero-credit source/prose/native/stored checkpoint; complete goal preserved."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_checkpoint_v8730')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8731')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8716/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B31_B53_contextual_native_stored_pending_names_actual_andrelease_v8730'
SCOPE='unfinished_editorial_scope_v8730'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
COUNTS=[7234,7237,7237,4489,2745]
PROOFS={
 'source_gloss':'work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json',
 'source_controls':'work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json',
 'source_names':'work/analysis/Hodram_B31_actor34_names_v8719/source_names_native_getters_andplanes.json',
 'source_display':'work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json',
 'source_view':'work/analysis/Hodram_B31_B53_source_view_v8721/direct_source_view_andscoped_name_findings.json',
 'current':'work/analysis/Hodram_B31_B53_current_v8722/current_effective.json',
 'prose':'work/analysis/Hodram_B31_B53_prose_v8723/contextual_review.json',
 'manuscript':'translations/hodram_B31_B53_editorial_manuscript_v2.json',
 'names':'translations/hodram_B31_B53_speaker_name_review_v1.json',
 'logical':'work/analysis/Hodram_B31_B53_logical_v8724/logical_paragraphs.json',
 'plan':'work/analysis/Hodram_B31_B53_layout_v8725/automatic_plans.json',
 'pages':'work/analysis/Hodram_B31_B53_pages_v8726/compiled_native_pages.json',
 'native_view':'work/analysis/Hodram_B31_B53_native_review_v8727/native_body_review.json',
 'relocation':'work/analysis/Hodram_B31_B53_relocation_v8728/reconstruction.json',
 'stored':'work/analysis/Hodram_B31_B53_stored_v8729/stored_pages_controls_andreferences.json',
 'own_input':'work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json',
 'registered_release':'work/analysis/Hodram_B52_release_v8705/registered_release_verification.json',
 'registered_startup':'work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
}
SUMMARY="""Current verified experimental cumulative ROM remains V8704. Counts remain7,234 completed/7,237 credited source-prose and drafts/4,489 integrated revisions/2,745 justified retentions;SC0 368/SC1 154/SC2 4,915/SC3 197/COMMON1,600 completed and1,603 source-prose;route subtotal5,634 is not the full-goal denominator. B52's five decisions remain credited exactly once. Preserve every ROM,translation,draft,executed producer,proof andfailure. No new ROM,emulator capture,registry stage,promotion,separate requested package,pruning,commit orpush. Full all-four-storyline/earlier translated dialogue/shared town-shop/random/Help/remaining prose/all207 names-roles-aliases-customnames/retrospective premature-break objective remains active. Roughly20,000 remaining candidates remains a planning estimate,not an audited prose denominator. Graphics/all18plaques andlater older-record technical re-audit stay separate.

B31/B53 now have three uncredited contextual revisions in translations/hodram_B31_B53_editorial_manuscript_v2.json. Clean gloss8714,controls8718,names8719,complete Japanese pages8720 anddirect view8721 preceded all earlier English in8722. B31's two source speeches are alternate branches,not consecutive repeated lines. The existing Then face me yourself. shifts agency away from この俺が相手になろう;the revision says I'll take you on myself. The irritated complaint becomes You just won't quit,will you? rather than the unsupported intelligence judgment fool. The longer variant keeps the before-clause andan unnamed man you really ought to fear;do not identify him from lore. B53's existing price on your head invents a monetary bounty. The revision says Looks like you've finally ended up wanted by the Ottoman Empire.You'd better watch yourself.,preserving apparent/reported status,culmination,undesirable development andgruff practical caution without a bounty,crime,warrant,rank,pursuer,location oroutcome. All four prose gates pass;all formatting gates remain false pending the remaining workflow. No source-prose counter orcompletion credit is added atthis stage.

Fresh ownV8704 native source proofs bind18commands/three complete six-byte preambles/four relative sites20structural cases/one unforced raw8000 query/eight paired opaque structural decodes/50normal seeded ends/four original EV1 entry getters. B31 source query returns[2,1,0,0,0,0] in the own opening snapshot andcomposes the long variant;value0 composes the short variant only as a structural argument. Do not name the raw operand as a plot predicate,assume it is universally boolean,force flags orclaim actual event activation. Both original normal ends192and132 preserve the carried value. The explicit52->31->53 prerequisite chain doesnot establish continuous conversation,original location,chronological proximity,either B52 choice's completion effect orunnamed-man identity. Preserve6311/6000/633F/623F/A000 structurally without invented effect semantics.

Actor34 now has two fresh original getters andvoice1,with complete current style11 literal planes:progressive Barbarossa Hayreddin versus full getter Barbarossa Ｆazul Hayreddin. Exact clean fields areバルバロッサ/ハイレディン/ファーズル;the current middle pointer resolves in the actual deployed pool to8265617a756c (Ｆazul). This is a real consumer difference,not a silently unused field. Full source composition,romanization,mixed-width leading F andrelevant catalogue UI review remain open;do not delete it,replace it with historical lore orpromote earlier Hayreddin-component approval into full-name approval. Progressive components/order are provisional. Actor113 Port Worker remains a scoped justified role retention;two getters/voice0/nameplane are reused only through exact code/COMMON/font/wholeactors/fields. Wider113 contexts/all207 names remain open.

Three fresh source dispatches/twelve source alignments/three complete Japanese pages andthree fresh current dispatches/twenty current relative cases/one unforced current query pass. Logical8724 andcompiled8726 each pass twelve guarded alignments. The unchanged full216px Hodram formatter produces2/4/3 rows andone complete page per English speech;zero QAissues,warnings orwaivers. All first/internal/final characters,apostrophes,punctuation,bounds,consumption,pagination andindependent native font planes pass andwere directly viewed. Review notes accept the ordinary really/ought to fear.andended up/wanted by phrase continuations in their complete sentences. No authored ordinary breaks,padding,shortening,narrowed viewport,font changes orglobal guard/QA weakening.

Research relocation8728 expands B31from196to228stored bytes andB53from136to156. All18commands/three fullpreambles/four relocated relative operands20fresh native cases/one query/eight opaquecontrols/two normal fullends remain. Every323unowned block/all other files/components,the complete current archive,each complete clean/current block inverse andwhole in-memory NDS inverse pass. No ROM is written. Stored8729 binds all three final references andoriginal dispatches;no parity tails are needed,so12 exact compiled alignments/pages are explicitly reused without replay. The fresh target query matches[2,1,0,0,0,0] unforced. This remains offline native evidence,not actual B31/B53 headers,branch visits,outer eligibility,originallocation,earned chronology,opaque effect semantics,fullroute orhardware coverage.

Continue from verifiedV8731/currentV8704 without repeating completed B52 integration/startup orunchanged B31/B53 source/prose/native work. The next B31/B53 tasks are the actor34 source full-name/consumer decision,independent reconstruction/references/loader binding,representative initialized complete-script source/English gameplay andconcrete focused risks,then natural-dialogue-v2 formatting/policy/frozen/atomic/shared registered integration/exact clean-input patch/own startup andthree once-only completion decisions. Preserve every earlier B52/B51/B50/B49/Gerhard/Rafael/Hodram/Lil timing,RNG,RGB,calendar,following-command,fixture andoffline/actual limitation. No current B31/B53 actual gameplay orrelease approval is claimed."""
NEXT='Continue B31/B53 from source/native/stored evidence8729 in strict ownV8704 captain1 context. Resolve actor34 full-name consumers without lore orsilently deleting the source middle field;independently bind reconstruction/references/loaders,then representative complete-script gameplay/focused risks andformal registered integration. Keep every full-scope lead andall prior artifacts;no repeat B52 completion ornew promotion/package.'

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
    assert data['source_controls']['native_relative_cases']==20 and data['source_controls']['opaque_structural_decode_pairs']==8
    assert data['source_view']['all3_complete_Japanese_panels_first_internal_final_glyphs_andnative_bounds_directly_viewed']
    assert data['prose']['revisions']==3 and data['prose']['retentions']==0
    assert data['native_view']['all_three_complete_bodies_visually_read'] and not data['plan']['failures']
    assert all(not r['base_QA']['issues'] for r in data['plan']['records']) and all(not r['review']['formatting'] for r in data['manuscript']['records'])
    assert data['relocation']['other323_blocks_byte_exact'] and data['relocation']['whole_inmemory_NDS_inverse_andall_other_files_components_exact']
    assert data['stored']['complete3stored_first_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass']
    assert data['stored']['fresh_native_alignment_cases']==0 and data['stored']['exact_reused_alignment_cases']==12
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
        pending=dict(status='three-contextual-revisions-native-stored-reviewed-fullname-actual-independent-policy-registered-pending',file_path='/data/SC1.DK4',blocks=[31,53],
            physical_speeches=3,typed_choice_labels=0,proposed_revisions=3,justified_retentions=0,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,
            records_with_exact_source_current_compiled_andstored_references=deepcopy(records),stored_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True,all_formatting_gates_false=True,full_name_open_finding=deepcopy(data['source_view']['full_name_open_finding']),
            source_commands=18,source_relative_sites=4,source_rawqueries=1,opaque_controls=8,source_seeded_end_cases=50,source_relative_cases=20,current_relative_cases=20,relocated_relative_cases=20,
            source_dispatches=3,current_dispatches=3,stored_dispatches=3,source_alignment_cases=12,logical_alignment_cases=12,compiled_alignment_cases=12,stored_exact_reused_alignment_cases=12,
            complete_source_pages=3,complete_English_pages=3,automatic_fullwidth_px=216,QAissues=0,warnings=0,waivers=0,
            actual_B31_B53_emulator_runs=0,actual_B31_B53_frames=0,source_positions_credited=0,new_credit=0,full_goal_complete=False)
        descriptor=old[prior['unfinished_scope']];assert sha(Path(descriptor['path']).read_bytes())==descriptor['sha256']
        scope=deepcopy(read(descriptor['path']));assert KEY not in scope
        ROOT.mkdir(parents=True);scope[KEY]=deepcopy(pending);scope['latest_next_focus_v8730']=NEXT
        scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,scopepath,Path(__file__),*map(Path,PROOFS.values())]}
        put('latest_checkpoint',SUMMARY+'\n\n'+NEXT)
        put(SCOPE,dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),all_prior_scope_keys_values_history_andfull_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,new_uncredited_contextual_revisions=3,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put(KEY,dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,goal_turn_classification='progress',
            preceding_status_only_goal_turn_revalidated_andfollowed_by_concrete_editorial_andnative_progress=True,
            prior_clean_gloss_checkpoint_retained_as_historical_state=prior['pending_source_batch'],all_new_jobs_terminal=True))
        new[KEY]['inverse_operations']=deepcopy(ops)
        assert inverse(new,ops)==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8730; V8704 current\n\n' if name=='editorial_handoff_current.md' else '')
            prefix+='## V8730: B31/B53 agency and bounty revisions; source/native/stored review, names and actual/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
            targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        protected=[Path(prior[k]) for k in ['candidate','patch','manifest']]+[Path('translations/release_stack.json'),Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds')]
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,protected={str(p):sha(p.read_bytes()) for p in protected},inverse_operations=ops,unchanged_counters=COUNTS,new_credit=0,full_goal_complete=False))
        print('V8730 staged:three uncredited revisions/native/stored proof,six exact targets. Inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert inverse(new,plan['inverse_operations'])==old and [new[k] for k in COUNTERS]==COUNTS
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and not new['full_goal_complete']
        for row in plan['files']:
            assert sha(Path(row['planned']).read_bytes())==row['planned_sha256'] and sha(Path(row['target']).read_bytes())==row['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in {**plan['evidence'],**plan['protected']}.items():assert sha(Path(path).read_bytes())==digest
        descriptor=old[prior['unfinished_scope']];oldscope=read(descriptor['path']);newscope=read(new[SCOPE]['path'])
        assert all(newscope[k]==v for k,v in oldscope.items()) and set(newscope)-set(oldscope)=={KEY,'latest_next_focus_v8730'}
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            for i,row in enumerate(plan['files'][1:],start=1):
                original=gzip.decompress((ROOT/f'{i:02d}.before.gz').read_bytes());assert sha(original)==row['before_sha256'] and Path(row['planned']).read_bytes().endswith(original)
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),every_prior_ledger_value_family_record_counter_andcandidate_recovers_exactly=True,
                every_prior_scope_key_andvalue_anddocument_byte_preserved=True,protected_ROMs_patch_registry_unchanged=True,new_credit=0))
            print('V8730 audit:whole oldledger inverse,allscope keys,allold documentbytes,counters/candidate/registry/ROMs exact.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for row in plan['files']:
                target,planned=Path(row['target']),Path(row['planned']);assert target.is_relative_to(Path.cwd().resolve()) and planned.is_relative_to(ROOT.resolve())
                with target.open('r+b') as stream:stream.write(planned.read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(target.read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_registry_orcompletion_counter_change=True,new_credit=0,full_goal_complete=False))
            print('V8730 applied;currentV8704 andall7234completed unchanged;fullgoalactive.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,next_clean_exchange_not_selected=False,
                Hodram_B31_B53_contextual_native_stored_checkpoint=deepcopy(new[KEY]),new_uncredited_source_positions=3,physical_speeches_pending=3,typed_choice_labels_pending=0,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_research_ROMs=0,all_new_native_jobs_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8731/currentV8704:three contextual revisions/native/stored complete;names/independent/actual/policy/registered pending;zero completion credit;fullgoalactive.')
