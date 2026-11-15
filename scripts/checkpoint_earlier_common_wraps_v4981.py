"""Stage,audit,apply and post-verify four retrospective findings without duplicate credit."""
from copy import deepcopy
from pathlib import Path
import argparse,gzip,json,os
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.checkpoint_lil_B182_references_v4910 import WIDER
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/earlier_common_wraps_checkpoint_v4981')
VERIFY=Path('work/analysis/editorial_handoff_verification_v4982')
KEY='earlier_COMMON_wraps_context_native_v4981'
PREVIOUS='previous_latest_checkpoint_before_earlier_wraps_v4981'
DOC=Path('translations/earlier_common_wraps_editorial_manuscript_v1.json')
APPROVAL=Path('work/analysis/earlier_common_wraps_approval_v4979/four_retentions_one_reflow_source_native_approval.json')
COPIES=Path('work/analysis/earlier_common_wraps_copies_v4980/all7336_native_copies_and_letter_sequences.json')
NATIVE=Path('work/analysis/earlier_common_wraps_review_v4978/whole_context_four_retentions_two_reflows_and8_native_planes.json')
NEXT=(
    'Continue from the four retrospective COMMON findings in manuscript earlier_common_wraps_editorial_manuscript_v1,approval4979 and7336-copy proof4980. '
    'All four English paragraphs are justified retentions;only775 is an approved offline reflow proposal.682/764/774 retain exact current layouts with individual reasons. '
    'Do not repeat passed clean/context/native/copy checks without a concrete risk. Keep the initial774 three-row assumption and stopped4977/4977b proofs as diagnostics. '
    'The100-character774 paragraph cannot fit three complete-word rows at the validated34/34/35 budgets;35-character imagined first line exceeds the conservative nonfinal budget. '
    '775 becomes And I\'ll write you a letter / of recommendation to thank you for / selling us so many popular goods. Two generated terminal spaces stay inside35 final cells;no extra allocation padding before LF is used. '
    'The reviewed for ending is an ordinary complete-word soft wrap,not a global weak-ending waiver. '
    'Build a source-locked single-message atomic release stage after the complete V4966 stack,preserving the exact105-byte allocation,all3668 table/selection/NUL boundaries and every other COMMON payload,story,font,graphic,component and executable byte. '
    'Check representative display and transition through the recommendation branch775->780->766 using disclosed focused evidence where natural earned eligibility is impractical;do not claim an earned recommendation or full transaction from the60 supplied offline selector/funds/stock-letter cases. '
    'Keep other conditional observations offline. Then build through the sole registered builder,verify the exact clean-input patch and current startup,and record the formatting correction without duplicate contextual-review credit. '
    'Do not promote or prune. Continue broader earlier wrapping and the full editorial objective. '+WIDER)
SUMMARY=(
    'V4981 revisits COMMON682/764/774/775 from clean Japanese and their original conditional exchanges before predecessor comparison. All four wordings remain natural and faithful,with individual reasons. '
    'Retain682 exact:the current break keeps of my worries together;fuller prototype splits my / worries without saving a row. Retain764 exact:the complete first sentence occupies line1;the prototype strands This before isn\'t without saving a row. '
    'Retain774 exact:the100-character introduction offer requires four complete-word rows at current safe widths. Exhaustive1/2/3-row partitions fail. The initially imagined first row was35 characters,over the34-cell nonfinal budget;the prototype still takes four rows and splits thank / you. '
    'The existing layout keeps a letter of introduction and to thank you together. Its following779 small-town explanation and766 farewell remain distinct from775->780->766 any-town recommendation. '
    'Only775 has a justified reflow proposal,from four to three rows without a prose change:And I\'ll write you a letter / of recommendation to thank you for / selling us so many popular goods. '
    'Two generated terminal spaces preserve the exact105-byte allocation/NUL and stay inside35 final cells. No extra pre-LF allocation padding is needed;normal phase repair remains generated. '
    'The complete-word for boundary is a scoped ordinary soft wrap. No authored break,padding,width,font,metric,runtime filter,guard or historical compiler change.\n\n'
    'Eight complete current/reviewed native228x64 planes were viewed with current1px font offset,row pitch16,original expansion/wrapper and complete glyph/bounds/one-page checks. '
    'Fourteen unowned or unsafe compiler inputs are rejected. The one-message research COMMON proposal preserves all3668 native metadata/NUL boundaries,all other payloads and blocks,and inverts to every current COMMON byte. '
    'All7336 fresh native warm/cold copies plus ten sequenced selections pass with explicit host file-I/O contracts. '
    'Thirteen supplied Square-state selectors,eleven funds fragments and36 stock/letter fragments match clean/current instructions and results. '
    'The sole broad-span difference is the already registered Investment title literal020BCA3C,now bound exactly to its live Investment text and existing owner;every other selected word is clean-exact. '
    'No new ROM,emulator run,natural eligibility,earned letter,complete transaction,source/prose or completion credit is claimed. Representative transition,atomic stage,registered build,patch and startup remain pending.\n\n'
    'V4966 remains the current verified cumulative candidate with565 manifest batches/114 accepted layers/18 checks and exact clean-input patch. Main V4701 remains preserved. '
    'Coverage remains5966 contextual rereads,5969 source/prose,3780 integrated revisions/2186 retentions,SC24113 and route4367/4367. '
    'These four entries were already credited;the retrospective findings add zero duplicate credit. Every historical ledger value,ROM,translation,draft,executed producer,proof and diagnostic is retained. Full goal active.\n\n'+NEXT)

def evidence_audit(entry,current):
    assert sha(Path(current['path']).read_bytes())==current['sha256']=='9cff9a828870c520bb53a6a2b41107a08043414c670221c2cd257385b5604c7c'
    for p,h in entry['evidence'].items():assert sha(Path(p).read_bytes())==h
    doc,a,c,n=map(read,[DOC,APPROVAL,COPIES,NATIVE])
    assert a['manuscript_sha256']==sha(DOC.read_bytes()) and c['approval_sha256']==sha(APPROVAL.read_bytes())
    assert a['all8_current_and_reviewed_complete_native_planes_viewed'] and a['all14_unsafe_or_unowned_inputs_rejected']
    assert len(a['negative_controls'])==14 and all(r['rejected'] for r in a['negative_controls'])
    assert c['complete_native_copy_cases']==len(c['cases'])==7336 and len(c['sequenced_cache_cases'])==10
    assert a['intro774_exhaustive_complete_word_partitions_at1_2_3_rows']=={'1':[],'2':[],'3':[]}
    assert entry['records']==doc['records'] and doc['retained_exact_layout_IDs']==[682,764,774] and doc['reflow_IDs']==[775]
    image=NdsImage.open(current['path']);arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    assert sha(arm)==a['source_ARM9_sha256'] and sha(common)==a['source_COMMON_sha256']
    target=Path(a['target_COMMON']).read_bytes();assert sha(target)==a['target_COMMON_sha256']==c['target_COMMON_sha256']
    before,after=[owned_entries(raw,arm,a['directory_sha256']) for raw in [common,target]]
    assert [x.message_id for x,y in zip(before,after,strict=True) if x.text!=y.text]==[775]
    for row in doc['records']:
        assert all(row['review'].values()) and row['fresh_retained_wording_justification'] and row['layout_review_reason']
        assert row['current_hex']==before[row['message_id']].text.hex() and row['target_hex']==after[row['message_id']].text.hex()
        assert b' '.join(bytes.fromhex(row['current_hex']).split())==b' '.join(bytes.fromhex(row['target_hex']).split())
    assert n['retained_exact_layout_IDs']==[682,764,774] and n['proposed_reflow_IDs']==[775]
    for row in n['records']:
        for case in row['native_cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    assert sha(Path(a['viewed_sheet']).read_bytes())==a['viewed_sheet_sha256']
    assert entry['source_prose_or_completion_credit_added']==0 and entry['new_ROMs']==entry['new_emulator_runs']==0
    manifest=read(current['manifest']);registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==565 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['stage','audit','apply','post'],required=True);mode=p.parse_args().mode
    lp=Path('translations/editorial_review_current_v1.json')
    if mode=='stage':
        assert not ROOT.exists();before=lp.read_bytes();old=json.loads(before)
        assert sha(before)==read('work/analysis/editorial_handoff_verification_v4973/verified_handoff.json')['ledger_sha256']
        assert KEY not in old and PREVIOUS not in old
        rows=read(DOC)['records'];all_old=[r for f in old['completed_editorial_families'] for r in f['records']]
        assert all(sum(r.get('message_id')==row['message_id'] for r in all_old)==1 for row in rows)
        paths=[DOC,APPROVAL,COPIES,NATIVE,Path(__file__)]
        evidence={str(p):sha(p.read_bytes()) for p in paths}
        new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,next=NEXT,records=rows,evidence=evidence,
            reviewed_retentions=4,exact_layout_retentions=[682,764,774],proposed_reflow_IDs=[775],source_prose_or_completion_credit_added=0,
            new_ROMs=0,new_emulator_runs=0,registered_release_and_representative_transition_pending=True,goal_turn_classification='progress',full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY
        evidence_audit(new[KEY],old['current_integrated_candidate']);ROOT.mkdir(parents=True)
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={lp:encode_ledger(new)}
        section='## V4981:four earlier wrapping leads reviewed;one native-approved reflow pending integration\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            q=Path('docs')/name;text=q.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V4981\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest
            targets[q]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            assert target!=lp or len(data)<100*1024*1024
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=lp:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),staged=str(planned.resolve()),after_sha256=sha(data)))
        save(ROOT/'mutation_plan.json',dict(files=files,evidence=evidence,all_old_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,full_goal_complete=False))
        print('Staged six files;four retrospective findings,one reflow pending;zero duplicate credit.');raise SystemExit(0)
    plan=read(ROOT/'mutation_plan.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()))
    ledger_row=next(r for r in plan['files'] if Path(r['target'])==lp.resolve());new=read(ledger_row['staged'])
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);entry=inverse.pop(KEY);assert inverse==old
    assert new['goal_status']=='active' and not new['full_goal_complete'] and new['current_integrated_candidate']==old['current_integrated_candidate']
    assert Path(ledger_row['staged']).read_bytes()==encode_ledger(new)
    for row in plan['files']:
        assert sha(Path(row['staged']).read_bytes())==row['after_sha256']
        assert sha(Path(row['target']).read_bytes())==row['after_sha256' if mode=='post' else 'before_sha256']
    evidence_audit(entry,new['current_integrated_candidate'])
    receipt=dict(ledger_sha256=ledger_row['after_sha256'],candidate=new['current_integrated_candidate']['path'],candidate_sha256=new['current_integrated_candidate']['sha256'],
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,retained_wordings=4,retained_exact_layouts=[682,764,774],
        source_native_approved_reflow_IDs=[775],new_editorial_credit=0,new_emulator_runs=0,new_ROMs=0,
        representative_registered_build_patch_and_startup_pending=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
    VERIFY.mkdir(parents=True,exist_ok=True)
    if mode=='audit':
        assert not (VERIFY/'pre_apply_audit.json').exists();save(VERIFY/'pre_apply_audit.json',receipt)
    elif mode=='apply':
        assert read(VERIFY/'pre_apply_audit.json')==receipt and not (VERIFY/'applied_handoff.json').exists()
        for row in plan['files']:
            data=Path(row['staged']).read_bytes()
            with Path(row['target']).open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(row['target']).read_bytes())==row['after_sha256']
        save(VERIFY/'applied_handoff.json',receipt)
    else:
        assert read(VERIFY/'applied_handoff.json')==receipt and not (VERIFY/'verified_handoff.json').exists()
        save(VERIFY/'verified_handoff.json',receipt)
    print(dict(mode=mode,files=6,all_history_preserved=True,duplicate_credit=0,reflow_pending=[775],full_goal_active=True))
