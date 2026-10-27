"""Stage and seal the reference-ready handoff without adding review/completion credit."""
import argparse
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_checkpoint_v4155')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4137/verified_handoff.json')
APPROVAL=Path('work/analysis/lil_B167_reference_approval_v4154/approval_receipt.json')
NEXT='Build and test the atomic B167 compiler, register the complete cumulative V4110-plus-B167 profile, build through the integrated builder, reconstruct the clean-input patch exactly and verify current startup/town. Complete B167 credit only after those gates. Continue B168-B180 and all wider editorial families; preserve the separate graphics and later older-record re-audit.'
SUMMARY='''V4155 makes all 29 Lil B167 reviews reference-ready: 16 revisions and 13 justified retentions for the complete clean-first Shipwright sail lesson and accept/refuse labels. Native approval V4135 and final phrase-flow wording remain unchanged. Exact source/current references, context, glosses, findings and retention reasons are preserved. All source sail orientation, wind tradeoffs, supplementary sail types/restrictions, mast-order reasoning and characterization remain complete; approved current Refit terms and original names stay bound.

Relocation preserves all 46 commands, 12 relative spans/60 target native cases, 27 complete speech preambles, the whole typed menu, two original Cesare queries, two resources and separate refusal/lecture ends at source430/2172. Every predecessor logical byte restores exactly; all 335 other SC2 blocks and every other file/component remain exact. Stored block2176 becomes2052 bytes. All 27 stored targets/108 native alignment cases pass, including44 fresh parity-tail cases/11 planes and64 exact reused cases/16 planes. Both current/research images pass336 complete original loads/cache hits and672 parent modes each; three entry censuses and four guarded end decodes pass. Twenty-seven relocated actor dispatches, two unforced copied-state predicates, six opaque leaves and two typed getter phases pass. Native structural/getter tests establish no natural eligibility or full event effects. Original0D and printable6D remain executable selectors; generic Shipwright names retain their two read-only paths. The later older-record technical re-audit stays open.

Four new14401-frame Japanese/English cold boots exercise the complete B167 content at initialized B22 entry. No B167 command or effect is omitted and no branch/query is flattened or forced; the original nine B22 initialization commands/four A000s remain. Okay returns option0 with22 speeches/40 observed commands and source end2172; No thanks returns option1 with6 speeches/23 commands and source end430. All25 distinct speeches and28 English observations match complete native ink/gray planes and paired source portrait/name/upper regions. All five actual sheets, eight English full screens and three Japanese counterparts were viewed. Both complete menu labels and visible selection association pass; permitted per-version blink states are recorded without a false global-frame animation-equivalence claim. Both town-return frames match Japanese RGB exactly. Source/English exits are8375/8374 and4534/4533. All four unforced Cesare queries return0; final type0 state is[0,0] even after menu option1 because the later membership query owns its second word. Seven of twelve relative sites are actually observed. The alternative Cesare remarks R45/R131 and remaining branch sites retain complete offline native evidence without actual-display or byte-identical-reuse claims. The initialized town is Amsterdam, not a stated source port. No natural source-event167 eligibility, complete playthrough or hardware claim.

All29 five-gate, reference and representative approvals are sealed in manuscript13/choice3 and the source relocation map. The atomic compiler, rejection checks, registered cumulative integration, exact clean-input patch and fresh startup remain pending. No additional source/prose or completion credit is added:5602 fresh rereads,5573 integrated/completed,29 pending;source/prose5605 including3749 SC2 and64 SC3;route reviewed/completed4003/3974;historical completed3551 revised/2022 retained. Verified experimental V4110 remains541 manuscript batches/114 accepted layers. V4046 remains promoted main; the immutable construction baseline and every earlier ROM/translation/draft/producer/proof/failure remain preserved.

Remaining B168-B180 contains321 physical speeches and zero typed choice-command leads; this is not a full project denominator. All wider storylines, shared shop/town dialogue, random scenes, Help and other player-facing prose remain open. Preserve COMMON750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell's full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate; retain the later older-record technical re-audit/queued0D gap. Full goal active; all jobs terminal.'''
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stage',action='store_true');parser.add_argument('--seal',action='store_true');a=parser.parse_args();assert a.stage!=a.seal
    lp=Path('translations/editorial_review_current_v1.json')
    if a.stage:
        assert not ROOT.exists();l=read(lp);before=deepcopy(l);assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
        f=l['contextual_story_natural_dialogue_pass_v1871'];assert (f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(5602,5573,29)
        approval=read(APPROVAL)
        for p,h in approval['manuscripts'].items():assert sha(Path(p).read_bytes())==h
        assert approval['all29_source_native_reference_and_representative_rules_approved'] and approval['new_emulator_runs']==4
        paths=[PRIOR,APPROVAL,Path(approval['reference_map']),*map(Path,approval['manuscripts']),*map(Path,approval['evidence'])]
        evidence={str(p):sha(p.read_bytes()) for p in paths}
        ROOT.mkdir(parents=True)
        l['lil_B167_references_ready_v4155']=dict(summary=SUMMARY,evidence=evidence,approved_manuscripts=approval['manuscripts'],reference_map=approval['reference_map'],reference_map_sha256=approval['reference_map_sha256'],native_actual_references_ready=True,registered_release_and_startup_pending=True,next=NEXT,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=4,full_goal_complete=False)
        l['latest_checkpoint']=SUMMARY
        docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
        assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4136')
        staged=[]
        for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
        planned=ROOT/(lp.name+'.planned');save(planned,l);staged.append(dict(target=str(lp),before_sha256=sha(lp.read_bytes()),planned=str(planned),planned_sha256=sha(planned.read_bytes())))
        section='## V4155: B167 references and representative choices approved; registered release pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Next: '+NEXT+'\n\n'
        for i,p in enumerate(docs):
            first,rest=p.read_text(encoding='utf-8').split('\n',1);data=(('# Current editorial handoff - V4155' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
            planned=ROOT/(p.name+'.planned');planned.write_bytes(data);staged.append(dict(target=str(p),before_sha256=sha(p.read_bytes()),planned=str(planned),planned_sha256=sha(data)))
        stable=[Path('translations/release_stack.json'),Path('translations/promoted_build.json'),Path('scripts/build_integrated_release.py')]
        save(ROOT/'staged_checkpoint.json',dict(files=staged,evidence=evidence,preserved_release_files={str(p):sha(p.read_bytes()) for p in stable},prior_verified_handoff=str(PRIOR),producer_sha256=sha(Path(__file__).read_bytes()),no_new_credit=True))
        print('V4155 exact checkpoint staged; native file application and independent audit pending.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');assert not (ROOT/'checkpoint_receipt.json').exists()
        for r in plan['files']:assert sha(Path(r['target']).read_bytes())==sha(Path(r['planned']).read_bytes())==r['planned_sha256']
        for p,h in {**plan['evidence'],**plan['preserved_release_files']}.items():assert sha(Path(p).read_bytes())==h
        before=read(ROOT/(lp.name+'.before'));current=read(lp)
        assert {k:v for k,v in before.items() if k!='latest_checkpoint'}=={k:v for k,v in current.items() if k not in ['latest_checkpoint','lil_B167_references_ready_v4155']}
        save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4155',evidence=plan['evidence'],updated_files={r['target']:r['planned_sha256'] for r in plan['files']},preserved_release_files=plan['preserved_release_files'],prior_verified_handoff=str(PRIOR),staged_checkpoint=str(ROOT/'staged_checkpoint.json'),staged_checkpoint_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),new_source_prose_reviews=0,new_completed_records=0,fresh_reread=5602,integrated=5573,pending=29,source_prose=5605,new_actual_cold_boot_runs=4,all_jobs_terminal=True,registered_release_and_startup_pending=True,full_goal_complete=False))
        print('V4155 sealed:29 reference-ready reviews,25 actual/2 offline speeches; no additional credit; registered release pending.')
