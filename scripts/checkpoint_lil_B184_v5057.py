"""Stage,audit,apply and verify an uncredited native checkpoint losslessly."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from scripts.checkpoint_maria_B97_v5019 import WIDER

ROOT=Path('work/analysis/lil_B184_checkpoint_v5057')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5058')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B184_editorial_manuscript_v4.json')
APPROVAL=Path('work/analysis/lil_B184_native_approval_v5056/all9_source_prose_current_native_approval.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5035/verified_handoff.json')
KEY='Lil_B184_contextual_native_v5057'
PREVIOUS='previous_latest_checkpoint_before_Lil_B184_v5057'
NEXT=('Continue Lil SC2B184 from approved manuscriptv4,native approval5056 and exact wrap comparison5055. '
    'Nine objects have clean-source/context/localization/naturalness/current-native-format approval:4 revisions/5 individually justified retentions,zero credit. '
    'Do not repeat sealed clean-first glosses,names/voices/source contracts,72 native alignments,18 consumer/28 formatter negatives or six exact-boundary mutation controls without a concrete risk. '
    'Preserve the couple roles164/165 without marital,age or kinship invention;household tea running low,buy-tomorrow request,willing future agreement,personal calm and gentle dependence hyperbole. '
    'Keep Tea31 and both Sofala aliases bound;the separate FE forecast stays prospective,with no earned boom,city shortage,price,profit,medical effect or earlier household location. '
    'Use exact source/prose-bound layoutv2. R14 now uses two safe rows without changing words:the complete-word soft break after this keeps catch on sooner intact. Only R14 bytes change from initial native draft;the other8 targets and all weak/protected lists stay exact. '
    'Retain initial native5051,three-row finding5052,all prior drafts/producers and both stopped author/schema diagnostics. Do not generalize the one reviewed ordinary boundary to mutated source/prose or other records. '
    'Next produce the reversible12-command relocation and verify final stored native phase/alignment. Source432 stored/logical bytes has nine complete preambles,A0008 raw00a0ffff011f22a1,C200426,end428 and no trailing bytes after the four-byte end. '
    'No source substitutions,predicates,relative operands,typed choices,resources,pictures or pauses exist. Do not inherit Maria B97 FO,item,pagination or two trailing zeros. '
    'Create a one-block reference on complete V5030 and test loaders,entry census,guarded end and relocated dispatch/C200/A000. '
    'Use paired disclosed B22 content cold boots with original B22 initialization and all12 original B184 commands;inventory exact fixture counts and observe both couple portraits/nameplates,all9 speeches,FE transition,C200,end and parent return. '
    'Measure actual timing,RGB,RNG and native state without forcing equality. No natural event184 eligibility,earned fashion,full route or hardware claim. '
    'Then create the atomic compiler/rejection checks,register after the full V5030 stack,build with the sole registered builder,verify exact clean-input patch and fresh startup,and count9 once. '
    'Current V5030 and main V4701 remain preserved;no promotion or pruning. '+WIDER)
SUMMARY=('V5057 completes nine clean-first whole-exchange Lil SC2B184 source/prose/current-native reviews as approved uncredited work:4 revisions and5 individually justified retentions. '
    'Restore the wonder that something so delicious did not catch on sooner,the man\'s explicit agreement and dry criticism,and the polite household buy-tomorrow request with a willing first-person reply. '
    'Retain five natural pleased/earnest/relaxed/hyperbolic/forecast turns with individual contextual reasons. In particular,Tea may catch on in Sofala is an idiomatic tentative forecast and remains. '
    'Clean role labelsカップル男/カップル女 bind current Man in a Couple/Woman in a Couple through all four original progressive/catalogue consumers and live deployed-pool pointers. No marriage,age or kinship is invented. '
    'Tea31 and both Sofala aliases bind source/current pointers and unchanged commodity metadata. Household supply is distinct from city shortage,trade cargo or a trading tip;personal calm is not a medical/gameplay bonus.\n\n'
    'Fresh V5030 Lil New Game RAM supplies current actor207/eight-voice and native context without battery,savestate or initialized-RAM/code overlay. '
    'All18 clean/current speech dispatches,12 source commands,nine full preambles and three nonrelative leaves are bound. A0008 raw00a0ffff011f22a1,C200426,end428 and432 stored/logical bytes remain. '
    'There are8 progressive objects and one null-actor FE,no FI/FA/FO,predicates,relatives,typed choices,pauses,resources or item presentations. The original scene/effect/UI bodies remain explicit offline boundaries,not observed B184 outcomes.\n\n'
    'Visual review rejected an initially technically clean R14 layout:an overconservative weak-this penalty forced3 rows and split catch/on despite room for2. '
    'The frozen source/prose-bound v2 successor permits that exact complete-word ordinary boundary after this. All words stay intact;catch on sooner remains together in2 readable rows. '
    'Only R14 compiled bytes change;all8 other targets,weak/protected lists,font,width,guard,phase and controls remain exact. Six source/prose mutation controls prove the narrow decision does not transfer. '
    'All9 final native panels on2 sheets were viewed as one exchange;72 logical/compiled alignments,18 consumer and28 formatter negatives pass. Four Japanese/English row-count notes are narrow and do not waive glyph,bounds,pagination or control safety. '
    'No authored break,prose shortening,global weak-word waiver,font/metric/width change or frozen compiler edit. Preserve initial5051,finding5052,all drafts and stopped preparer/schema diagnostics.\n\n'
    'No ROM or new emulator run is produced here. Relocation,final stored alignment,reference/load/end/control checks,paired B22 content display/transition tests,atomic compiler,registered integration and clean-input patch/startup remain pending. '
    'Native/offline evidence is not actual scene gameplay,natural event184 selection,earned fashion,full-route or hardware coverage. '
    'Coverage stays5998 completed contextual rereads,6001 source/prose,3803 integrated revisions/2195 retentions,SC24113/SC396 and routes4399/4399;zero pending credited route drafts. These9 approved B184 objects remain uncredited. '
    'Registered V5030 stays567 manifest batches/114 accepted layers/18 checks,ROM24ce9f1b7e7808003a49b9501485c86cc46eddd34dc260b5b4abd806b29d0d9d,patch6fda4e3b1e1dcd11e59a06c01672472bb5cf4468635153728462dec89ddcc65d. '
    'Main V4701 and every earlier ROM,translation,proof and historical value remain preserved.\n\n'+NEXT)

def before_ledger():
    return json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()))

def inverse(value):
    result=deepcopy(value);result['latest_checkpoint']=result.pop(PREVIOUS);result.pop(KEY)
    return result

def audit(plan):
    for entry in plan['files']:
        assert sha(Path(entry['target']).read_bytes())==entry['before_sha256']
        assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
    target=next(e for e in plan['files'] if e['target']==str(LEDGER.resolve()))
    new=read(target['planned']);old=before_ledger();assert inverse(new)==old
    for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    return new

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);args=parser.parse_args()
    if args.phase=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'] and KEY not in old and PREVIOUS not in old
        assert old['goal_status']=='active' and not old['full_goal_complete']
        assert tuple(old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5998,6001,3803,2195)
        doc,approval=map(read,[DOC,APPROVAL]);assert approval['manuscript_sha256']==sha(DOC.read_bytes())
        assert len(doc['records'])==9 and (doc['revised'],doc['retained'])==(4,5) and doc['source_prose_or_completion_credit_added']==0
        assert all(all(r['review'].values()) for r in doc['records'])
        current=old['current_integrated_candidate'];assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,APPROVAL,PRIOR,Path(__file__)]}
        for k,v in doc.items():
            if k.endswith('_sha256') and k[:-7] in doc and isinstance(doc[k[:-7]],str):
                p=Path(doc[k[:-7]])
                if p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
        fields=['id','file_path','block','source_record_index','source_reference','current_reference','source_hex','current_hex',
            'source_complete_preamble_hex','source_Japanese','source_meaning','english','speaker','context','editorial_decision',
            'localization_note','fresh_retained_wording_justification','review','compiled_hex','source_prose_or_completion_credit_added']
        records=[{k:deepcopy(r[k]) for k in fields if k in r} for r in doc['records']]
        new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=records,
            revised=4,retained=5,approved_uncredited_objects=9,source_prose_or_completion_credit_added=0,native_formatting_review_complete=True,
            remaining_gates=['reversible-relocation','final-stored-native-alignments','one-block-reference-and-load-control-checks','paired-content-gameplay-and-transition','atomic-compiler','registered-cumulative-release','clean-input-patch','fresh-current-startup'],
            actual_B184_gameplay_observed=False,new_ROMs=0,new_emulator_runs=0,evidence=evidence,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5057: Nine Lil B184 native reviews; retroactive wrapping remains in scope\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5057\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data);previous=path.read_bytes()
            if path!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(previous)
            files.append(dict(target=str(path.resolve()),before_sha256=sha(previous),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,all_counters_candidate_registry_and_main_unchanged=True,full_goal_complete=False))
        print('Six targets staged;shared state unchanged.')
    elif args.phase=='audit':
        assert not (ROOT/'independent_preapplication_audit.json').exists();plan=read(ROOT/'staged_checkpoint.json');audit(plan)
        save(ROOT/'independent_preapplication_audit.json',dict(all_before_planned_and_evidence_hashes_exact=True,full_nested_inverse_recovers_every_historical_value=True,
            staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
        print('Six targets and complete historical inverse pass.')
    elif args.phase=='apply':
        assert not (ROOT/'native_application_receipt.json').exists();plan=read(ROOT/'staged_checkpoint.json')
        assert read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());audit(plan)
        workspace=Path.cwd().resolve()
        for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve()) and Path(e['planned']).stat().st_size>=Path(e['target']).stat().st_size
        for e in plan['files']:
            with Path(e['target']).open('r+b') as f:f.write(Path(e['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
        save(ROOT/'native_application_receipt.json',dict(all6_targets_exact=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False))
        print('Six audited targets applied exactly.')
    else:
        assert not VERIFY.exists();plan=read(ROOT/'staged_checkpoint.json');assert read(ROOT/'native_application_receipt.json')['all6_targets_exact']
        for e in plan['files']:assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
        new=read(LEDGER);assert inverse(new)==before_ledger()
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        current=new['current_integrated_candidate'];assert sha(Path(current['path']).read_bytes())==current['sha256']==read(DOC)['current_ROM_sha256']
        assert new['goal_status']=='active' and not new['full_goal_complete']
        VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=current['path'],candidate_sha256=current['sha256'],
            all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,completed=5998,source_prose=6001,revised=3803,retained=2195,
            approved_uncredited_Lil_B184_objects=9,Lil_proposed_revisions=4,Lil_justified_retentions=5,all9_source_prose_current_native_reviews_verified=True,
            native_alignment_cases=72,consumer_negatives=18,formatter_negatives=28,exact_boundary_mutation_controls=6,
            actual_B184_gameplay_pending=True,registered_integration_pending=True,main_V4701_preserved=True,new_editorial_credit=0,new_ROMs=0,new_emulator_runs=0,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5057 verified;V5030 remains current. Nine B184 native approvals remain uncredited;full goal active.')
