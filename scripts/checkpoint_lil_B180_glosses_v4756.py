"""Stage an uncredited clean-first B180 lead without changing completed coverage."""
from copy import deepcopy
import gzip
from pathlib import Path
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.lil_B179_completion_text_v4753 import NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B180_clean_checkpoint_v4756')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4754/verified_handoff.json')
PACKET=Path('work/analysis/lil_B180_clean_context_v4755/all11_complete_B180_exchange_and_fresh_glosses.json')
KEY='lil_B180_clean_first_glosses_v4756'
NEXT=(
    'Continue B180 from all11 clean-Japanese speeches and fresh complete-exchange glosses; '
    'do not repeat sealed B179 checks without a concrete risk. Bind current/source '
    'mapping,two static speakers/voices,complete preambles,22 dispatches,ten relative '
    'sites,two8000 raw500 predicate fields,three A000 leaves,C200570,end572 and native '
    'event context. Bind approved リスボン and 香料 terms before exposing the complete '
    'predecessor English. Preserve the respectfully mentioned person without invented '
    'gender,name,rank or relationship,the pleasant-scent observation,shared recognition, '
    'explicit uncertainty,confident speaker prediction,first-to-acquire urgency,future '
    'proposal to ask,warm agreement and mutual courteous farewells. The closing FE '
    'notice remains impersonal/prospective;do not infer earlier scene location,actual '
    'inquiry/acquisition,earned fashion or packed control semantics. Author natural '
    'American dialogue as a complete exchange,retain working English with individual '
    'reasons,then finish native layout/reversible relocation,representative actual '
    'tests and registered cumulative release/exact patch/startup gates before credit. '+
    PREVIOUS_NEXT[PREVIOUS_NEXT.index('Investigate separate untranslated'):])
SUMMARY=(
    'V4756 preserves all11 complete clean-Japanese B180 speeches with fresh individual '
    'glosses before predecessor English. The polite exchange progresses through a '
    'pleasant scent on a respectfully mentioned person,shared recognition,curiosity, '
    'explicit lack of identification,a confident fashion prediction,comic urgency to '
    'acquire it before others,a proposal to ask at a future encounter,warm assent and '
    'mutual gracious farewells. No third-person gender,name,rank,kinship,romance,brand, '
    'ingredient,price,supplier,gift,appointment,completed inquiry/acquisition,monopoly '
    'or earlier location is invented. The impersonal リスボン/香料 notice remains '
    'prospective;approved terms and current roles remain to bind.\n\n'
    'Clean B180 stored/logical576 has28 native commands,11 speeches (ten progressive/'
    'one FE),static selectors166/167,zero FI/FA/FO,ten relative sites,two8000 predicate '
    'objects with raw500 fields,three distinct A000 leaves472/504/516,C200570 and end572. '
    'Speech starts at8;there is no leading A000. No typed-choice/actor-style object or '
    '2000 pause exists. Preserve the conditional structure;do not inherit B179 linear '
    'A000/end-only assumptions or infer predicate/effect semantics. Native current/'
    'source,voices,names,branches,predicates,effects,entry,terms,layout,actual and release '
    'gates remain. This checkpoint adds no review credit,manuscript,ROM or emulator run.\n\n'
    'B179 is fully integrated and independently audited in experimental V4749:8 '
    'revisions/6 justified retentions,101 atomic negatives,78 regressions,555 batches/'
    '114 accepted layers,whole-ROM equality to reviewed V4734,exact clean-input patch '
    'and fresh31-frame/five-actor startup checks/six viewed screens. Preserve its eight '
    'timings/four A-indicator RGB differences,115 matching upper/name/portrait samples, '
    'five components,whole actor/captain2,PRNG403514907 and final RGB without full-RAM/'
    'future-world/hardware claims. Coverage stays5912 completed contextual rereads,zero '
    'pending credited route drafts,source/prose5915,4059 SC2/64 SC3,historical3748 '
    'revisions/2164 retentions and route4313/4313. B180 glosses are11 uncredited objects, '
    'not a project denominator. Main V4701/pushed4d63fd3/tag promoted-v4701,registry, '
    'builder,pins,immutable inputs,accepted layers,all earlier packages/ROMs/translations/'
    'drafts/executed producers/proofs/failures and full ledger history remain preserved. '
    'Separate Sao Jorge alias15E5D4/pointer122504 stays open. Graphics/all18 plaques and '
    'the later older-record technical re-audit/queued0D gap remain separate and open. '
    'One-space CRLF ledger encoding stays in use. Full goal active.\n\n'+NEXT)

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');prior,packet=map(read,[PRIOR,PACKET])
    before=lp.read_bytes();old=read(lp)
    assert sha(before)==prior['ledger_sha256'] and prior['all_jobs_terminal'] and prior['full_goal_active']
    assert KEY not in old and packet['no_predecessor_English_exposed'] and packet['total_editorial_objects']==11
    assert len(packet['block']['records'])==11 and all(r['fresh_source_gloss'] for r in packet['block']['records'])
    assert packet['source_prose_or_completion_credit_added']==0
    for p,h in packet['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    assert sha(Path(packet['source_transcript']).read_bytes())==packet['source_transcript_sha256']
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4753')
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PACKET,Path(packet['source_transcript']),Path(__file__)]}
    new=deepcopy(old)
    new[KEY]=dict(summary=SUMMARY,packet=str(PACKET),packet_sha256=sha(PACKET.read_bytes()),
        uncredited_objects=11,manuscript_authored=False,source_prose_or_completion_credit_added=0,
        no_predecessor_English_exposed=True,evidence=evidence,next=NEXT,full_goal_complete=False)
    new['latest_checkpoint']=SUMMARY
    assert {k:v for k,v in new.items() if k not in [KEY,'latest_checkpoint']}=={k:v for k,v in old.items() if k!='latest_checkpoint'}
    planned={lp:encode_ledger(new)}
    assert len(planned[lp])<100*1024*1024
    section='## V4756: B179 integrated;B180 clean-first fragrance exchange\n\n'+SUMMARY+'\n\nSource packet: '+PACKET.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for i,p in enumerate(docs):
        (ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        planned[p]=(('# Current editorial handoff - V4756' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged=ROOT/'staged';staged.mkdir();plan=[]
    for i,(p,data) in enumerate(planned.items()):
        q=staged/f'{i}.planned';q.write_bytes(data)
        plan.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(q.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable=['translations/release_stack.json','translations/promoted_build.json','translations/rom_retention_pins.json',
        'scripts/build_integrated_release.py','out/all_routes_combined_v4749_candidate.nds',
        'out/all_routes_combined_v4749_candidate.xdelta','out/all_routes_combined_v4749_candidate.manifest.json',
        'out/raphael_natural_v2_accepted_base.nds','work/clean.nds']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4756',evidence=evidence,
        preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},
        uncredited_B180_objects=11,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,
        all_jobs_terminal=True,full_goal_complete=False))
    print('Staged B180 clean-first checkpoint;all11 glosses uncredited,all coverage/history unchanged. Independent apply required.')
