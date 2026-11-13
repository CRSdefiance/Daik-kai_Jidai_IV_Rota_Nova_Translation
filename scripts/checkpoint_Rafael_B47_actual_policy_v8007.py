"""Checkpoint verified B47 actual, formatting policy and sealed references without release credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B46_v7969 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.Rafael_B47_release_paths_v8006 import proofs,APPROVED,MAP,SEAL
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Rafael_B47_actual_policy_checkpoint_v8007')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8008')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7993/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/rafael_B47_editorial_manuscript_v3.json')
NAMES=Path('translations/rafael_B47_speaker_name_review_v3.json')
KEY='Rafael_SC0B47_actual_policy_references_pending_atomic_release_v8007'
OLD_KEY='Rafael_SC0B47_source_prose_native_stored_pending_actual_release_v7992'
SCOPE='unfinished_editorial_scope_v8007'
PROOFS=proofs()|dict(
    reference_seal=str(SEAL),reference_map=str(MAP),sealed_manuscript=str(APPROVED),
    reference_receipt='work/analysis/Rafael_B47_reference_tools_v8006/reference_seal_receipt.json',
    policy_receipt='work/analysis/Rafael_B47_policy_v8004/prepared15_speeches16_pages_two_exact_warning_exceptions.json')

SUMMARY="""Current registered cumulative ROM remains V7964; main V4701 is unchanged. Counts remain 6,976 completed, 6,979 source/prose records and drafts, 4,361 integrated revisions and 2,615 retentions; SC0 173 and route subset 5,376. The 635 manifest batches, 114 accepted layers, 18 passing release checks, 110 regressions, exact clean-input patch and own-current Rafael startup evidence remain verified. B47 has no completion or source/prose credit and is not integrated.

B47 now has approved translations/rafael_B47_editorial_manuscript_v3.json and sealed v4.json: 15 complete contextual speech decisions, eight revisions and seven individual retentions. All five review gates pass. Clean source, B37 prerequisite context, fresh glosses, branch context and names preceded current English. All six composed source paths remain reviewed; R63/R70 are exclusive and three Janus remarks conditional. Preserve guarded relief, approximate eastern-half Ottoman territory/Pasha's forces, conditional danger, practical trading caution and qualified recruitment, preparation, overwhelm and resolve. Canonical speaker markup adds no prose or compiled-byte change. Earlier drafts and exact source/current references remain.

The isolated full research reference out/Rafael_B47_reference_v7994_RESEARCH_ONLY.nds is pinned and differs from V7964 only in B47 of SC0; every other file/component and342 blocks is exact. All343 native load/cache paths,686 initial parent modes,48 command maps,24 relative operands and original EV0/shipped callers pass. Source and relocated branch cases each cover120 native cases;625 structural compositions/six paths remain offline evidence. Research fixtures preserve the original ten-command B44 initialization plus all48 B47 commands,15 speeches,24 spans,six raw predicates,61FF,A000 and complete end. These are disclosed initialized opening-entry fixtures, not natural B47 activation, earned prerequisites, original location, a full route or hardware verification.

Two ordinary-input cold-boot headless runs are terminal and reaped: clean Japanese and English,16,001 frames each,32,002 total. Both actually select11 speeches and35 of48 B47 commands,45 including setup. The unvisited R17,R63,R92,R122 and Janus header remain explicitly native-only. Across22 speech occurrences/23 complete page observations,88 complete body/name holds match independent native masks;zero eligible partials,unknowns or unresolved/unreturned records. All four body sheets,two transition sheets,the R53 focus sheet and later comparison sheet were directly viewed:eight sheets. No battery,savestate,RAM,seed,condition,result,roster,role,funds or input timing is forced.

R53's Japanese page and both English pages are complete. Ordinary A at4720 advances from complete page1 at4690 to page2 at4750 within the same original command;page2's initial I,original[6,0] native origin and final chance. remain intact. The following R70 displays and returns normally. Source/English normal results are[0,0] at6416/6655:English returns239 frames later. All45 selected command results/UI requests and11 paired upper scenes/portraits/headers match. Preserve24 command-comparison difference rows/four duration differences. R53 lasts241/481 frames and mathematically advances58/116 LCG steps;English is58 steps ahead at B47 exit. This is measured phase arithmetic with original wait/generator code,not a fresh every-call causal trace.

All157 sampled later whole RGB pairs differ. Final state/tasks match;models,persistent objects,calendar and whole actors differ. Final seeds are19668379/4016462114,with English mathematically7833 steps behind in the bounded search. Raw calendars are ticks1900/[1,8,28] versus1123/[0,23,19],using original zero-based fields without invented date interpretation. Preserve every raw result and unmasked screenshot for the later older-record technical re-audit. Do not claim identical future random outcomes,full simulation or complete causality. Incidental B127/Sailor sailing captures receive no new editorial credit.

The scoped names remain Rafael Castor,Janus Pasar,Claudio Manaus and Julio Erneco. Three actual nameplates are verified;Janus has the previously viewed full style11 native nameplane and16 synthetic alignments across four identities,not actual B47 header coverage. Pasar/パサー is distinct from force reference Pasha/パシャ. Valdes/Pasha/Hayreddin have only component retentions;Pedro's middleデ and Hayreddin's omitted source middleファーズル remain wider207-name leads. Full catalogues,custom player names and other consumers remain open.

Frozen policy translations/rafael_B47_native_contract_v1.json and dk4tool/dialogue/rafael_B47_{profile,layout,plan}_v1.py replay all15 plans/16 pages. Only R53 permits8 total rows/two original four-row pages;all others permit4/one page. Global216px/four-row profile,body-NUL guard,source00 preambles andFI6/FA6/FO10 measurements stay unchanged;source macros are zero. Six original row-count infos and two exact weak-line-ending warnings remain. R5 line2 to/get and R63 line2 with/Pasha's have source/id/text/compiled/line-bound exceptions and written reasons. R5/R63 use three fuller rows instead of the inherited four-row solution without losing words. No global warning removal or manual wrap is introduced. All15 positive plans and302 actual-changing expected-guard rejections pass,including meaning,source,preamble,macro,profile,consumer,individual gates,warning scope and other controls.

Sealed references translations/rafael_B47_editorial_relocation_map_v1.json and work/analysis/Rafael_B47_reference_seal_v8006/all15_five_gates_exact_references_approved.json bind the full1284-to1344-byte reconstruction,48 commands,24 fixups,all15 final references and complete clean/predecessor block plus archive inverses. The source-locked reconstruction helper is dk4tool/patch/rafael_B47_reconstruction_v1.py. Preserve pending external-reference flags in the original research map;only the sealed map marks census completion. The first approval producer's list-versus-count schema assertion stopped before output;immutable v8003 and corrected source-locked v8003b remain. No new release ROM,registry change,main promotion,pruning,commit or push occurred."""

NEXT="""Continue from verifiedV8008/current registeredV7964. B47 source/context/prose/native/stored/representative-actual/formatting-policy/reference sealing are complete;do not replay those checks without a concrete new risk. Use scripts/Rafael_B47_release_paths_v8006.py,translations/rafael_B47_editorial_manuscript_v4.json,its source-bound v3 policy,dk4tool/patch/rafael_B47_reconstruction_v1.py and the sealed reference map. Actual proof is work/analysis/Rafael_B47_actual_v7999/paired_source_English_observed_path_complete_pages_names_andR53_transition.json;comparison v8000,waits v8001,focus v8002,approval v8003,policy v8004,302 challenges v8005 and reference seal v8006 are retained.

Next implement B47 speech-only atomic production/configuration,independently validate corrupted semantic proofs with dependency hashes bypassed,complete meaningful precommit rejection tests and permit only one final files-list commit. Adapt the B45 speech-only reconstruction and B46 atomic metadata safeguards:original external_references_complete=False becomes sealedTrue only after census;other source map metadata stays exact. Preserve all15 full preambles,48 commands,24 spans,six raw predicates,61FF,A000,full end,zero macros,342 otherblocks/allotherfiles/components and complete inverses. R53 alone has two pages;four speeches/Janus header stay native-only. All original diagnostics andboth exact waivers must remain source/text/compiled/line bound.

After atomic checks pass,register the stage afterV7964 in the complete release workflow,build the cumulative candidate with scripts/build_integrated_release.py,run the required release/regression checks,verify byte-exact reference equality and clean-input patch reconstruction,and obtain appropriate own-current startup evidence. Profile.batches470 is distinct from manifest635;the expected new manifest count is636. Preserve114 accepted layers and mainV4701. Credit15 objects/eight revisions/seven retentions once only after integration/startup:expected6991 completed/6994 source-prose anddrafts/4369 revisions/2622 retentions,SC0 188,route subset5391. Until then counts stay6976/6979/4361/2615.

Keep the full objective across allfour storylines,earlier translated conversations,broad practical shared shop/town/random capture,Help/remaining prose,all207 names/roles/aliases and retrospective premature wrapping. Preserve every earlier unfinished inventory,twelve contraction/question-tag wrap leads,unscanned records beyond558 plans and the inherited weak-before-row lead. Do not mechanically minimize rows or replace justified phrase retention;B46R23's may challenge remains one example. Preserve the historical JanusPasha counterpart queue while distinguishing Pasar from Pasha;no global replacement. Keep all older item/counterpart/display leads,Sailor151-159 versusRetainer consumers and uncredited incidental B127/Sailor captures. Graphics/all18 plaques and the later older-record technical re-audit remain separate,including normal-end value carry,B35R65's source-only nineteenth cell andall measured timing/highlight/RNG/component/calendar/RGB limits. Preserve every ROM,translation,draft,failure,executed producer and proof. Full goal active;no separate unified package,promotion,pruning,commit orpush."""

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==6976 and prior['manifest_batches']==635 and prior['B47_actual_gameplay_runs']==0
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==15 and doc['revisions']==8 and doc['retentions']==7
    assert all(all(r['review'].values()) for r in doc['records']) and all(all(r['review'].values()) for r in names['records'])
    approval=data['actual_approval'];assert approval['manuscript_sha256']==sha(DOC.read_bytes())
    assert approval['names_sha256']==sha(NAMES.read_bytes()) and approval['actual_complete_holds']==88
    assert len(approval['directly_viewed_sheets'])==8
    assert all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['directly_viewed_sheets'])
    assert data['native_policy_validation']['positive_count']==15 and data['native_policy_validation']['negative_count']==302
    assert data['reference_seal']['manuscript_sha256']==sha(APPROVED.read_bytes())
    assert data['reference_seal']['reference_map_sha256']==sha(MAP.read_bytes())
    assert data['reference_seal']['complete_clean_predecessor_blocks_andwhole_archive_inverse_exact']
    assert len(data['reference_map']['groups'][0]['command_map'])==48
    assert data['RNG_scope_proof']['groups'][0]['later_RGB_differences']==157
    assert data['RNG_scope_proof']['groups'][0]['exit_English_phase']==58
    for g in data['actual_proof']['groups']:
        t=read(f"work/analysis/Rafael_B47_scene_runs_v7998/route0_{g['version']}/terminal.json")
        assert t['terminal'] and t['frames']==16001
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
        pending=dict(status='15-source-context-prose-native-stored-representative-actual-policy-references-approved-pending-atomic-registered-release',
            manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),policy_manuscript=str(DOC),policy_manuscript_sha256=sha(DOC.read_bytes()),
            names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),file_path='/data/SC0.DK4',block=47,
            objects=15,revisions=8,retentions=7,all15_five_gates_true=True,native_pages=16,source_commands=48,relative_sites=24,
            actual_runs=2,actual_frames=32002,actual_speeches_eachlanguage=11,actual_complete_holds=88,
            native_only_unvisited_speech_IDs=data['actual_proof']['native_only_unvisited_speech_IDs'],
            exact_warning_exceptions=2,original_row_infos=6,policy_positive_count=15,policy_negative_count=302,
            all_proofs=PROOFS,all_measured_later_simulation_differences_andlimits_preserved=True,
            current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],
            atomic_production_registered_release_andstartup_pending=True,new_credit=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending)
        if OLD_KEY in inventory:inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,representative_actual_formatting_policy_andreferences_now_approved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],dict(checkpoint=KEY,representative_actual_formatting_policy_andreferences_now_approved=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,
            goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8007: B47 actual, policy and references approved; atomic integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V8007; V7964 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('B47 actual/policy/reference checkpoint staged;six targets,zero credit.Deep inverse audit next.')
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
                full_goal_all_previous_leads_actual_limits_andretrospective_wrap_lead_preserved=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passes;every prior ledger value,candidate,count andunfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:
                    stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('B47 actual/policy/reference checkpoint applied;currentV7964 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                B47_current_English_unread=False,B47_prose_records=15,B47_prose_revisions=8,B47_prose_retentions=7,
                B47_native_pages=16,B47_stored_all16_viewed_pages_exact=True,B47_actual_gameplay_runs=2,
                B47_actual_speeches_eachlanguage=11,B47_actual_complete_holds=88,B47_actual_sheets_viewed=8,
                B47_native_only_unvisited_speech_IDs=data['actual_proof']['native_only_unvisited_speech_IDs'],
                B47_frozen_policy_approved=True,B47_policy_negative_count=302,B47_exact_reference_seal_approved=True,
                B47_frozen_policy_atomic_registered_integration_pending=False,B47_atomic_registered_integration_pending=True,
                new_credit=0,new_emulator_runs=2,new_actual_frames=32002,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8008/currentV7964:6976completed;B47 actual/policy/references approved,302 negative guards;atomic integration pending.Full goal active.')
