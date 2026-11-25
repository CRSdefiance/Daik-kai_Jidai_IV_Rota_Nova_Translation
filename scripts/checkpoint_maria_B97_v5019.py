"""Stage,audit,apply and verify a lossless uncredited Maria checkpoint;no release promotion."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_checkpoint_v5019')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5020')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/maria_B97_editorial_manuscript_v5.json')
APPROVAL=Path('work/analysis/maria_B97_actual_approval_v5018/all32_native_actual_approval_and_remaining_release_gates.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4993/verified_handoff.json')
KEY='Maria_B97_contextual_native_actual_v5019'
PREVIOUS='previous_latest_checkpoint_before_Maria_B97_v5019'
WIDER=('Continue the full fresh editorial goal across all four storylines,earlier translations,shared town/shop exchanges,random scenes,Help and all other player-facing prose. '
    'Revisit premature wrapping with consumer-specific widths and complete exchanges;retain natural wording and meaningful pacing with reasons. COMMON657 and the682/764/774/775 decisions are already resolved;do not repeat passed checks or add duplicate credit. '
    'Keep COMMON750-752 callers,SourceItems/LocalProduct,five named-target leads,exact-record Proof terminology consistency,Samwell full-catalog middle-field lead,B157 provenance and untranslated Sao Jorge alias15E5D4/pointer122504 open. '
    'The incidental COMMON405 rats scene is a practical capture lead with exact clean/current references;its caller,full exchange and live message-ID selection are unreviewed. '
    'Keep graphics/all18 plaques and the later older-record technical re-audit/queued0D separate. Preserve every ROM,translation,draft,executed producer,proof,failure and all historical ledger values. Full goal active.')
NEXT=('Continue Maria SC3B97 from manuscriptv5 and actual approval5018.32 objects have source/context/localization/naturalness/native-format and focused actual approval,23 revisions/9 individually justified retentions,with zero credit until release gates pass. '
    'Do not redo sealed clean-first glosses,bindings,32 current-font matrices,256 alignments,24 source-consumer/42 formatter negatives,or paired actual displays without a concrete risk. '
    'Use exact current Maria captain3 context4997/4999,voices5000,dispatch5001,entry5002,names5003,macros5004,controls5005,terms5006,comparison5007,prose5008 and scoped planner/profile5009-5012. '
    'Use source72-only two-page plan with original216x64 physical viewport/four16px rows. All5 row words and guarded target stay intact. The actual A15401 continuation starts at x6,not the initial zero-indent offline projection. '
    'Current actual proof5017b and seal5018 bind both pages,all33 actual panels,327 complete holds/nontext pairs and original item/hide/end. Keep the initial projection and all stopped producers as diagnostics. '
    'The reversible draft5014 maps1904 stored/1902 logical to2048 stored/2046 logical;all40 commands/32 preambles/eight source leaves remain. Source6000/4620/633E stay8/10/14;A0001750 maps1874,item4820_1884 maps2028,A0001888 maps2032,hide4700_1896 maps2040,end1898 maps2042. '
    'Finish production-scope B97-only reference,whole-SC3 loader/cache,entry census,guarded ends and relocated controls. Check final stored alignments including original FO,source72 page-tail guard and terminal parity spaces. '
    'Then seal exact source/current/compiled/reference/integrated references,create the source-locked atomic compiler and meaningful rejection controls,register after the entire V4987 stack,build only through build_integrated_release.py,verify exact clean-input patch and fresh current startup/regressions,and credit these32 once. '
    'No new main promotion or pruning. '+WIDER)
SUMMARY=('V5019 records32 clean-first whole-exchange Maria SC3B97 decisions as approved uncredited work:23 revisions and9 individually justified retentions. '
    'The scene moves from whispers and identification of the Sao Jorge bandits,through their lost raiding livelihood and devastated village,to revenge,slave trading and military plunder,Maria\'s rejection of indiscriminate attacks,the cycle of conflict,her political alternative and confidence,voluntary invitation,consideration,trust,welcome and tentative ruins/tablet handover. '
    'Restore livelihood rather than an invented starvation prediction,the accusation that Maria talks as though she knows everything,the great powers\' search for Proofs as a pretext for partition,and the at-least-equal confidence. Preserve the source\'s anger,atrocities and character judgments without historical absolution,new casualties,rank,kinship,retaliatory promise or completed Proof. '
    'Retain nine natural reactions/replies with individual reasons. Approved names bind Maria Huamei Li/progressive Maria Li,Xien Yan and Bandit,voices3/5/0;one original FO remains a runtime substitution with measured default Li Clan. Use current Help4/reviewed Help189 Proof of Conquest and approved Sao Jorge;older Proof variants and the separate Japanese city alias remain open.\n\n'
    'Fresh exact-current Maria opening4997 supplies31001-frame context from V4987 with only the existing unearned system-unlock battery fixture;no historical initialized-RAM/code overlay. '
    'Current native proofs bind64 source/current dispatches,six name consumers,20 default/real-FO alignments,event97/action98 and all40 source commands/eight exact nonspeech leaves. Ten633E resource boundary cases,four4820/4700 descriptor cases and eight isolated setup/effect structural cases pass;their full bodies were not executed offline. '
    'All32 native font matrices,256 logical/compiled alignments,24 source-consumer negatives and42 formatter negatives pass. Five native sheets/33 native-or-projected panels were viewed. Nine Japanese/English row-count notes and three exact source/prose/boundary ordinary soft-wrap decisions are documented;mutated source/prose cannot inherit those decisions. No global weak-word waiver,manual breaks,font,width,guard or frozen compiler change.\n\n'
    'Two31000-frame terminal cold boots substitute complete clean/reviewed B97 content into original B33 New Game entry in V4987. Both execute all40 original commands and32 speeches. Source setup/resource,two effects,item176 presentation,hide and normal end are observed. '
    'All33 actual panel pages,327 complete held native planes and327 paired upper/portrait/name samples match;zero paired nontext differences. All six full actual sheets and four full item/final screens were viewed. '
    'R72 needs five rows and an original A continuation. The flat projection initially placed its second-page first row at zero;actual playback exposes the original6px guard indent. A15401 yields the complete final sentence at6px with every glyph,bounds and next Bandit transition intact. '
    'A fresh independent native continuation plane matches all10 complete second-page holds;all11 first-page holds match the four-row plane. Every word and compiled byte is unchanged. Preserve the initial unapproved projection and stopped64/96-canvas/path/optional-export diagnostics. '
    'The source/English item-display whole RGB pair agrees.34 command timings differ;normal ends23222/23822 are measured. At31000 the source run shows incidental Sailor rats dialogue and the English run sailing UI. Whole RGB,actor-span hashes and PRNG words differ347786248/2289475870 and remain disclosed;no causal PRNG,future-world or full-RAM equivalence claim. '
    'This is B97 content/display/transition coverage in a disclosed B33 slot,not naturally selected event97,earned recruitment,earned tablet,full route or hardware proof. The original acquisition caption is not an earned-progression claim. Both sessions60900/30654 are terminal/reaped.\n\n'
    'Draft relocation5014 preserves all40 commands,32 complete preambles and8 leaves,one FO,CS0101 and two trailing alignment zeros:1904 to2048 stored bytes,1902 to2046 logical. Exact inverse recovers every predecessor B97 byte. '
    'Final stored native font matrices match all reviewed targets after owned terminal parity spaces. Two research-only B33 ROMs preserve all302 other SC3 blocks,every other file,component,font,graphic,ARM9 and123040-byte pool;neither is a playable registered release. '
    'Whole-SC3 loader/reference/end/control gates,atomic compiler,registered cumulative integration,clean-input patch and fresh cumulative startup remain pending.\n\n'
    'Coverage stays5966 completed contextual rereads,5969 source/prose,3780 integrated revisions/2186 retentions,SC24113 and route4367/4367,zero pending credited route drafts. These32 are approved but uncredited. '
    'Registered V4987 remains566 manifest batches/114 accepted layers/18 checks,ROM f0b4c48aac9b1ae7e319ee3dc278afdd992c6179ba95a193948e64196dfeadfc and exact patch520cfa6b5c6678fe91162c98fb9b77b6478ed1d63f08c7cd8c07e9e69b407103. Main V4701 remains preserved.\n\n'+NEXT)

def snapshot_before():return json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()))

def audit(plan):
    old=snapshot_before();target=next(r for r in plan['files'] if r['target']==str(LEDGER.resolve()));new=read(target['planned'])
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(KEY);assert inverse==old
    for entry in plan['files']:
        assert sha(Path(entry['target']).read_bytes())==entry['before_sha256']
        assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
    assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and not new['full_goal_complete']
    assert all(new[k]==old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])
    return new

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);args=p.parse_args()
    if args.phase=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==read(PRIOR)['ledger_sha256']
        assert KEY not in old and PREVIOUS not in old and old['goal_status']=='active' and not old['full_goal_complete']
        assert tuple(old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5966,5969,3780,2186)
        doc,approval=map(read,[DOC,APPROVAL]);assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and len(doc['records'])==32 and (doc['revised'],doc['retained'])==(23,9)
        assert all(all(r['review'].values()) for r in doc['records']) and doc['source_prose_or_completion_credit_added']==0
        current=old['current_integrated_candidate'];assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,APPROVAL,PRIOR,Path(__file__),Path(approval['new_practical_unreviewed_scene_lead'])]}
        for k,v in doc.items():
            if k.endswith('_sha256') and k[:-7] in doc and isinstance(doc[k[:-7]],str):
                path=Path(doc[k[:-7]])
                if path.is_file():assert sha(path.read_bytes())==v;evidence[str(path)]=v
        new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=doc['records'],revised=23,retained=9,approved_uncredited_objects=32,source_prose_or_completion_credit_added=0,native_and_focused_actual_complete=True,remaining_release_gates=approval['remaining_gates'],actual_content_scope='Complete B97 in B33 New Game fixture;event97 not naturally selected',new_emulator_runs=2,new_emulator_frames=62000,new_research_ROMs=2,all_jobs_terminal_and_reaped=True,evidence=evidence,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY
        inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(KEY);assert inverse==old
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5019: Maria B97 whole-exchange/native/actual review; registered integration pending\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5019\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(path,after) in enumerate(targets.items()):
            beforebytes=path.read_bytes();planned=ROOT/f'{i:02d}.after';planned.write_bytes(after)
            if path!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(beforebytes)
            files.append(dict(target=str(path.resolve()),before_sha256=sha(beforebytes),planned=str(planned.resolve()),planned_sha256=sha(after)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,ledger_key=KEY,previous_key=PREVIOUS,evidence=evidence,all_counters_and_candidate_unchanged=True,full_goal_complete=False));print('Six files staged;no shared state changed.')
    elif args.phase=='audit':
        assert not (ROOT/'independent_preapplication_audit.json').exists();plan=read(ROOT/'staged_checkpoint.json');new=audit(plan)
        save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,all_original_root_and_nested_history_recovered_by_inverse=True,all_counts_and_candidate_unchanged=True,staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Six staged targets and deep historical inverse audited.')
    elif args.phase=='apply':
        assert not (ROOT/'native_application_receipt.json').exists();plan=read(ROOT/'staged_checkpoint.json');a=read(ROOT/'independent_preapplication_audit.json');assert a['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());audit(plan)
        workspace=Path.cwd().resolve()
        for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve()) and Path(e['planned']).stat().st_size>=Path(e['target']).stat().st_size
        for e in plan['files']:
            with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
        save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,all_before_hashes_verified_before_first_write=True,staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Six audited files applied byte-exactly.')
    else:
        assert not VERIFY.exists();plan=read(ROOT/'staged_checkpoint.json');assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact']
        for e in plan['files']:assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
        old=snapshot_before();new=read(LEDGER);inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(KEY);assert inverse==old
        current=new['current_integrated_candidate'];assert sha(Path(current['path']).read_bytes())==current['sha256']==read(DOC)['current_ROM_sha256']
        for p,digest in plan['evidence'].items():assert sha(Path(p).read_bytes())==digest
        assert new['goal_status']=='active' and not new['full_goal_complete']
        VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=current['path'],candidate_sha256=current['sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,completed=5966,source_prose=5969,revised=3780,retained=2186,approved_uncredited_Maria_B97_objects=32,Maria_proposed_revisions=23,Maria_justified_retentions=9,all32_native_actual_reviews_verified=True,actual_pages=33,actual_matching_holds=327,source72_A_continuation_first_row_indent_px=6,registered_integration_pending=True,main_V4701_preserved=True,new_editorial_credit=0,new_emulator_runs=2,total_new_frames=62000,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())));print('V5019 verified;V4987 remains current.32 Maria records approved but uncredited;full goal active.')
