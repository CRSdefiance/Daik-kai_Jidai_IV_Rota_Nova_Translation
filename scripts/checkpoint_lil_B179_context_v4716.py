"""Checkpoint uncredited B179 clean-first context/native identity after B178 completion."""
from copy import deepcopy
import gzip
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_context_checkpoint_v4716')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4706/verified_handoff.json')
GLOSS=Path('work/analysis/lil_B179_clean_context_v4707/all14_complete_B179_exchange_and_fresh_glosses.json')
SOURCE=Path('work/analysis/lil_B179_source_v4708/all14_clean_current_complete_context.json')
VOICE=Path('work/analysis/lil_B179_voices_v4709/current3_static_names_voices_and207_catalog_rebind.json')
DISPATCH=Path('work/analysis/lil_B179_dispatches_v4710/all14_source_current_dispatches_no_macros_and2_control_leaves.json')
BRANCH=Path('work/analysis/lil_B179_branches_v4711/original_relative_skip_operand_proof.json')
ENTRY=Path('work/analysis/lil_B179_entry_v4712/source_EV2_B179_action_dependency_and_native_getter_binding.json')
NAMES=Path('work/analysis/lil_B179_names_v4713b/six_original_Barkeep_Patron_Retainer_name_consumers.json')
CONTROL=Path('work/analysis/lil_B179_controls_v4714/one_A000_no_C200_single_end_and2_source_leaves.json')
IDENTITY=Path('work/analysis/lil_B179_role_identity_v4715/source_current_progressive_roles_and_distinct_Retainer_catalogue_binding.json')
NEXT=(
    'Continue B179 from all14 clean-first glosses and completed source/current,three-voice, '
    '28-dispatch,entry,six-name,two-leaf and source-dialogue-identity proofs. Bind approved '
    'サン＝ジョルジェ city and wine terms before exposing the complete predecessor-English '
    'comparison. Use dialogue identities Barkeep92/Patron96/Sailor152;the full catalog has '
    'Retainer152 from a distinct native getter and must not override dialogue source水夫. '
    'Preserve both mappings;do not rename assets or infer a named superior,faction,rank or '
    'relationship. Then author natural-dialogue-v2 from the complete exchange,retaining '
    'working lines with individual reasons. Preserve the unspecified previous drink,rough '
    'challenge/concession,repeated taste questions,personal wine hyperbole,one-serving order, '
    'Barkeep reply,three gulp sounds,delighted another-serving order,joining order and '
    'prospective impersonal city notice. No C200 exists:preserve16 commands,14 preambles, '
    'opaque A0008 raw00a0ffff01221da1 and single end508,logical512/stored512,zero macros; '
    'do not inherit a C200 command or proof. Native layout/complete planes,source/native '
    'credit,reversible relocation,representative actual coverage and registered cumulative '
    'release/startup gates remain. Do not repeat sealed B178 checks without a concrete risk. '
    'Continue B179-B180 (25 physical speeches,not a project denominator),every storyline, '
    'shared shop/town dialogue,random scene,Help and other player-facing prose. Preserve '
    'COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads, '
    'exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 '
    'provenance amendment. Graphics/all18 plaques stay separate;retain the later older-record '
    'technical re-audit/queued0D gap. Preserve every ROM,translation,draft,executed producer, '
    'proof and failure. Full goal active.')
SUMMARY=(
    'V4716 preserves fourteen complete clean-Japanese B179 speeches/fresh contextual glosses '
    'before predecessor-English comparison. Source context moves from a rough challenge '
    'about an unspecified drink and defensive retort to concession,enthusiastic wine '
    'persuasion,repeated curious questions,personal nothing-else-needed hyperbole,a one- '
    'serving trial order,casual service,three gulp sounds,pleased verdict,another-serving '
    'request and a joining order. The impersonal サン＝ジョルジェ notice remains prospective. '
    'No drink type,brand,price,relationship,rank,drunkenness,medical claim,recipe,completed '
    'commercial sale,active boom or earlier scene location is invented. Native city/wine '
    'term binding and complete English comparison remain pending;there is no new B179 '
    'manuscript or review credit.\n\n'
    'All16 clean/current commands and14 complete preambles bind. Twenty-eight source/current '
    'dispatches preserve thirteen progressive/one original null-actor FE and zero FI/FA/FO. '
    'Event179/action180 has no explicit dependency prefix;one getter does not prove natural '
    'eligibility. There are two nontext leaves:opaque A0008 raw00a0ffff01221da1 and single '
    'four-byte end508,logical512/stored512. No C200,predicate,relative site,2000 pause, '
    'resource,presentation word or typed object exists. The isolated A000 structural walk '
    'bridges a nondecode callee and does not execute the effect body.\n\n'
    'Three original static selectors bind through fresh names/voices and the exact207- '
    'catalogue/eight-voice runtime. Six name consumers are read-only with zero scratch/getter '
    'writes and all4MiB preserved. Dialogue labels are Barkeep92/Patron96/Sailor152. Clean '
    'source inline酒場の親父 at15D2A4,酒場の客 at15C5E4 and水夫 at1484D4 bind the current '
    'native pointers/complete Barkeep,Patron,Sailor spans. The separate full-catalog getter '
    'returns Retainer152 from staged pointer02387E48,within unchanged123040-byte payload. '
    'Preserve this genuine consumer distinction;the catalog label does not override dialogue '
    'identity or authorize a named master,faction,rank or relationship. マスター addresses '
    'the source-bound Barkeep in this tavern context. Preserve the failed catalog-equals- '
    'progressive assumption and corrected successor;no name asset or code changed.\n\n'
    'B178 is fully integrated and independently audited in experimental V4701:two revisions/ '
    'eleven retentions,98 atomic negatives,78 regressions,554 batches/114 accepted layers, '
    'byte-exact clean-input patch and whole-ROM equality to reviewed research V4686. Fresh '
    'New Game/town startup passes31 whole frames/five actor controls/six viewed screens. '
    'Existing B178 actual evidence retains14 timing/four original A-indicator RGB differences; '
    '115 upper/portrait/name regions,five components,whole actor,PRNG3306586022 and final RGB '
    'agree without full-RAM,future-world or hardware claims. Main V4595/pushed eff4adb/tag '
    'promoted-v4595 remains unchanged;later work is local. Coverage stays5898 completed '
    'contextual rereads,zero pending credited route drafts,source/prose5901,SC24045/SC364, '
    'historical3740 revisions/2158 retentions and route4299/4299. B179\'s fourteen source '
    'glosses/native research add zero credit. Registry,builder,immutable inputs,accepted '
    'layers,all earlier packages/ROMs/translations/drafts/executed producers/proofs/failures '
    'and full ledger history are preserved. One-space CRLF ledger encoding stays in use. '
    'This checkpoint adds no ROM,emulator run,source/prose or completion credit.\n\n'+NEXT)


def same_except(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}


if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');oldbytes=lp.read_bytes();before=read(lp)
    assert sha(oldbytes)==read(PRIOR)['ledger_sha256']
    gloss,source,names,identity=map(read,[GLOSS,SOURCE,NAMES,IDENTITY])
    assert len(source['records'])==len(gloss['block']['records'])==14 and gloss['no_predecessor_English_exposed']
    assert names['approved_prose_names']==identity['approved_dialogue_roles']=={'92':'Barkeep','96':'Patron','152':'Sailor'}
    assert names['readonly_consumer_count']==6 and names['source_owned_scratch_consumer_count']==0
    paths=[PRIOR,GLOSS,SOURCE,VOICE,DISPATCH,BRANCH,ENTRY,NAMES,CONTROL,IDENTITY,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ledger=deepcopy(before);assert 'lil_B179_clean_context_native_research_v4716' not in ledger
    ledger['lil_B179_clean_context_native_research_v4716']=dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        clean_glosses=str(GLOSS),clean_glosses_sha256=sha(GLOSS.read_bytes()),uncredited_source_objects=14,evidence=evidence,
        prose_manuscript_not_yet_authored=True,terms_and_complete_predecessor_comparison_pending=True,
        exact_dialogue_Sailor152_vs_catalogue_Retainer152_distinction_preserved=True,
        source_prose_reviews_added=0,completion_credit_added=0,new_emulator_runs=0,next=NEXT,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':b['next']=NEXT;same_except(a,b,{'next'})
        else:assert a==b
    same_except(before,ledger,{'latest_checkpoint','lil_B179_clean_context_native_research_v4716','coverage_units'})
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated',
        'retained_wordings_editorially_completed'])==(5898,5901,3740,2158)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5898,5898,0)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    planned={lp:encode_ledger(ledger)};assert len(planned[lp])<100*1024*1024
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(oldbytes,mtime=0))
    section='## V4716: B178 integrated;B179 clean-first context/native identities bound\n\n'+SUMMARY+'\n\nSource packet: '+SOURCE.as_posix()+'. Identity distinction: '+IDENTITY.as_posix()+'. Verified B178: '+PRIOR.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for i,name in enumerate(['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']):
        p=Path('docs')/name;(ROOT/(name+'.before')).write_bytes(p.read_bytes());first,rest=p.read_text(encoding='utf-8').split('\n',1)
        planned[p]=(('# Current editorial handoff - V4716' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged=ROOT/'staged';staged.mkdir();plan=[]
    for i,(p,data) in enumerate(planned.items()):
        out=staged/f'{i}.planned';out.write_bytes(data)
        plan.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(out.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable={p:sha(Path(p).read_bytes()) for p in ['translations/release_stack.json','translations/promoted_build.json',
        'translations/rom_retention_pins.json','scripts/build_integrated_release.py']}
    for r in plan:assert sha(Path(r['target']).read_bytes())==r['before_sha256'] and sha(Path(r['planned']).read_bytes())==r['planned_sha256']
    for r in plan:
        data=Path(r['planned']).read_bytes()
        with Path(r['target']).open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
        assert sha(Path(r['target']).read_bytes())==r['planned_sha256']
    assert all(sha(Path(p).read_bytes())==h for p,h in stable.items())
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4716',ledger_sha256=sha(lp.read_bytes()),evidence=evidence,
        fresh_reread=5898,integrated=5898,pending_credited=0,uncredited_B179_source_glosses=14,source_prose=5901,revised=3740,retained=2158,
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,stable_release_files=stable,
        updated_files={str(Path(r['target']).relative_to(Path.cwd())):r['planned_sha256'] for r in plan},
        all_jobs_terminal=True,ROMs_deleted=0,full_goal_active=True,full_goal_complete=False))
    print('V4716:14 uncredited B179 glosses/native identities checkpointed;5898 completed,main V4595/latest experimental V4701 preserved;full goal active.')
