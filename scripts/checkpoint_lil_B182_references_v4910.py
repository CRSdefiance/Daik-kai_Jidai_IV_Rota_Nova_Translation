"""Stage lossless B182 source/native/actual progress without premature completion credit."""
from copy import deepcopy
from pathlib import Path
import gzip
import json
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B182_reference_checkpoint_v4910')
KEY='lil_B182_contextual_reference_v4910'
PREVIOUS='previous_latest_checkpoint_before_B182_reference_v4910'
MANUSCRIPT=Path('translations/lil_B182_editorial_manuscript_v4.json')
APPROVAL=Path('work/analysis/lil_B182_reference_approval_v4909/approval_receipt.json')
VISUAL=Path('work/analysis/lil_B182_actual_review_v4907/all8_panels_48_fullscreens_conditional_return_and_measured_differences_v2.json')
SCRATCH=Path('work/analysis/lil_B182_predicate500_v4896/all24_aligned_and_unaligned_original500_ownership_cases.json')
WIDER=(
    'Continue every remaining storyline,shared town/shop exchange,random scene,Help and other player prose,including earlier translations,retentions and premature wrapping. '
    'Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalog middle-field lead,B157 provenance,untranslated Sao Jorge alias15E5D4/pointer122504 and wrapping leads682/764/774/775. '
    'Keep graphics/all18 plaques and later older-record technical re-audit/queued0D separate and open. Preserve all ROMs,translations,drafts,executed producers,proofs,failures and complete historical ledger. The full editorial goal remains active.')
NEXT=(
    'Integrate B182 following the entire registered V4867 stack. Start from manuscriptv4 and sealed relocation map/approval4909,not old prose. '
    'The complete source/native/relocation/stored/load/census/end/control and actual gates are sealed;do not repeat without a concrete risk. '
    'Create a source-locked atomic compiler using B180_editorial_v4 conditional map reconstruction,not B181 linear/no-predicate assumptions. '
    'Preserve all25 commands,eight preambles,seven progressive Lady166/167 and one FE,two raw500 predicates,ten relative operands,three alternative A000s,C200 and four-byte end. '
    'Source636 maps to652 stored/logical bytes;predicates512/544 map530/562,effects532/564/576 map550/582/594,C200630 maps646,end632 maps648. '
    'Relocated predicates are halfword aligned:bind the original operand helper2A5BC-2A600,exact scratch word02279600 written at0202A5D8,and exact RNG word02168EB8 written at020D984C. '
    'Use ownership proof4896 with24 clean/current/relocated cases;do not reuse B180 strictly-one-write or aligned0 assumptions. Preserve diagnostic4895 and stopped producers. '
    'Bind8 complete native planes,64 initial plus32 stored alignments,18 consumer/28 formatter negatives,336 target loads/672 modes with exact whole-ROM parent reuse,three censuses,guarded ends and25 mapped paths. '
    'Actual fixtures retain34 stored commands (25 source+9 B22 init),all8 speeches and original selected effect/C200/end. Both rolls52 select source effect532 without forcing;returns4776/4775. '
    'Keep13 timing differences,18 later A-indicator RGB differences x224-240/y360-376,and final RNG3723009301/403514907 disclosed. All115 nontext samples,finalRGB,five native state groups and whole1A04 actor/captain2 agree;no causal PRNG,future-world or full-RAM equivalence claim. '
    'All8 actual panels,2 sheets and48 full screens have been viewed;no additional focus run is required by the checked display findings. '
    'After compiler rejection controls,register cumulatively,build only through build_integrated_release.py,verify exact clean-input patch and current startup,then credit these8 once. '
    'They remain uncredited now. Main V4701 remains promoted;preserve registered V4867 and all earlier ROMs. '+WIDER)
SUMMARY=(
    'V4910 completes the B182 whole-exchange source/prose,native,reference and targeted actual review as8 uncredited objects:6 revisions/2 individually justified retentions. '
    'Read the complete clean Japanese and fresh glosses before predecessor English. Restore reported forthcoming engagement to the duke\'s son,reported engagement-ring cost enough to buy a mountain,admiration for the duke,anticipated princess appearance,increased interest rather than every lady,and the explicit question setting up the unknown-gem joke. '
    'Retain the brisk No idea/ask-at-once reply and natural prospective Gems may catch on in London notice with individual reasons. Source-explicit princess,duke and son remain;no guessed stone,personal name,house,age,currency,marriage date,completed wedding,active boom,shortage,profit or earlier London location.\n\n'
    'Exact V4867 opening RAM binds207 catalog names/eight voices,two Lady selectors,four read-only name consumers,16 source/current dispatches,event182/action183,all25 commands,two500 predicates,ten relative sites,three alternative opaque effects,C200 and end. '
    'Both London aliases and Gems12 bind through current pointers and12 clean/current native category lookups. Native gates preserve full preambles,no substitutions,no typed objects,pauses,resources or presentations. '
    'Eight logical paragraphs pass with3 narrow source/English row-count notes;no other safety waiver. One native sheet viewed:seven216x64 progressive planes and one228x48 logical/228x64 physical FE;all64 initial alignments,18 source-consumer/28 formatter negatives pass. '
    'No manual break,phrase exception,prose shortening,font,metric or guard change. Source636 maps reversibly to652 stored/logical bytes,all335 other blocks exact;32 final stored alignments comprise16 fresh parity cases/16 exact-byte reuses.\n\n'
    'Relocation shifts predicate operands from aligned0 to halfword2. Strict diagnostic4895 stopped on the additional original helper scratch write. Focused proof4896 binds unchanged2A5BC-2A600 and proves all24 aligned/unaligned cases,three threshold results,exact optional scratch02279600=500 at0202A5D8 and original RNG02168EB8 update at020D984C;all other4MiB,actor,inputs,canaries and ABI remain exact. '
    'Owned cleanup is confined to those validated fields in isolated CPU tests;no emulator seed/outcome is forced. Preserve the strict failure and corrected proof. Fresh target336 loads/672 modes,exact whole-ROM parent proof reuse,three entry censuses,poisoned end decodes,eight relocated dispatches,C200/effects and25 source/mapped paths pass.\n\n'
    'Two disclosed Japanese/English9001-frame B22 content cold boots retain34 stored commands,all25 source plus9 original initializers. All8 complete native text planes,distinct portraits/nameplates,FE clearing,selected original effect,C200,end and parent return are observed. '
    'Both unforced roll52/result0 select source effect532. Returns4776/4775;13 command timings differ (7 speech/6 control/end). All115 upper/portrait/name samples agree. All18 later whole-RGB differences are the original A-button indicator within x224-240/y360-376;all2 actual sheets and48 full screens viewed unmasked. '
    'Final9001 RGB,five native state groups and whole1A04 actor/captain2 agree;final RNG seeds differ3723009301/403514907 and remain disclosed without a causal or future-world/full-RAM equality claim. Following tutorial adds no review credit. '
    'No naturally earned event182 eligibility,earlier scene location,full-route or hardware claim. Both sessions55613/45687 are terminal/reaped.\n\n'
    'Registered integration,atomic compiler/rejection controls,clean-input patch and current cumulative startup remain pending. Coverage stays5933 completed contextual rereads,5936 source/prose,3758 integrated revisions/2175 retentions,SC24080 and route4334/4334,zero pending credited route drafts. '
    'B182 has8 approved uncredited objects. Registered V4867 remains563 manifest batches/114 accepted layers,exact candidate/patch;main V4701 and all earlier ROMs,translations and history preserved. Three new research ROMs are pinned. Full goal active.\n\n'+NEXT)

if __name__=='__main__':
    assert not ROOT.exists();doc,approval,visual=map(read,[MANUSCRIPT,APPROVAL,VISUAL])
    assert approval['manuscripts'][str(MANUSCRIPT)]==sha(MANUSCRIPT.read_bytes())
    assert len(doc['records'])==8 and (doc['revised'],doc['retained'])==(6,2) and doc['source_prose_or_completion_credit_added']==0
    assert all(all(r['review'].values()) and r['actual_B22_display_fixture_observed'] for r in doc['records'])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and not visual['visual_review_pending']
    lp=Path('translations/editorial_review_current_v1.json');before=lp.read_bytes();old=json.loads(before)
    prior=read('work/analysis/editorial_handoff_verification_v4874/verified_handoff.json')
    assert sha(before)==prior['ledger_sha256'] and KEY not in old and PREVIOUS not in old
    counts=tuple(old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])
    assert counts==(5933,5936,3758,2175) and old['goal_status']=='active' and not old['full_goal_complete']
    current=old['current_integrated_candidate'];assert current['sha256']==doc['current_ROM_sha256']==sha(Path(current['path']).read_bytes())
    paths=[MANUSCRIPT,APPROVAL,VISUAL,SCRATCH,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    for obj in [doc,approval,read(doc['reference_map'])]:
        for k,v in obj.items():
            if k.endswith('_sha256') and isinstance(v,str) and k[:-7] in obj:
                p=Path(obj[k[:-7]]) if isinstance(obj[k[:-7]],str) else None
                if p is not None and p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
        for p,h in obj.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;evidence[p]=h
    new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        records=doc['records'],revised=6,retained=2,approved_uncredited_objects=8,source_prose_or_completion_credit_added=0,
        source_native_references_and_representative_actual_complete=True,registered_integration_patch_and_startup_pending=True,
        new_emulator_runs=2,total_frames=18002,new_research_ROMs=3,all_generated_ROMs_preserved=True,evidence=evidence,full_goal_complete=False)
    new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(KEY);assert inverse==old
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    targets={lp:encode_ledger(new)};assert len(targets[lp])<100*1024*1024
    section='## V4910: B182 complete exchange and targeted actual review; integration pending\n\n'+SUMMARY+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;text=p.read_text(encoding='utf-8')
        if name=='editorial_handoff_current.md':after='# Current editorial handoff - V4910\n\n'+section+text
        else:
            first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
        targets[p]=after.replace('\n','\r\n').encode('utf-8')
    files=[]
    for i,(target,after) in enumerate(targets.items()):
        raw=target.read_bytes();staged=ROOT/f'{i:02d}.after'
        if target!=lp:(ROOT/f'{i:02d}.before').write_bytes(raw)
        staged.write_bytes(after);files.append(dict(target=str(target.resolve()),before_sha256=sha(raw),staged=str(staged.resolve()),after_sha256=sha(after)))
    save(ROOT/'mutation_plan.json',dict(files=files,ledger_key=KEY,previous_key=PREVIOUS,evidence=evidence,
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,candidate=current,full_goal_complete=False))
    print(dict(staged_files=6,ledger_bytes=len(targets[lp]),approved_uncredited_objects=8,revised=6,retained=2,shared_files_changed=False))
