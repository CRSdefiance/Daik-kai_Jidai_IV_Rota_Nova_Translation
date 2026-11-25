"""Record the uncredited clean B172 lead and preserve completed cumulative state."""
import gzip
import json
import os
from pathlib import Path
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B172_clean_lead_v4362')
SOURCE=Path('work/analysis/lil_B172_clean_context_v4361/all27_complete_B172_exchange_and_fresh_glosses.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4360/verified_handoff.json')
LP=Path('translations/editorial_review_current_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    before=LP.read_bytes();ledger=json.loads(before);prior,source=map(read,[PRIOR,SOURCE])
    assert sha(before)==prior['ledger_sha256'] and (prior['integrated'],prior['pending'],prior['source_prose'])==(5762,0,5765)
    assert source['all27_clean_source_read_and_individually_glossed_before_predecessor_English'] and source['no_predecessor_English_exposed']
    assert source['total_editorial_objects']==len(source['block']['records'])==27
    assert source['source_prose_or_completion_credit_added']==source['new_emulator_runs']==0
    record=dict(block=172,clean_source_objects=27,source_commands=38,nonrelative_nonspeech_leaves=11,
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_transcript=source['source_transcript'],source_transcript_sha256=source['source_transcript_sha256'],
        source_selectors=[2,26,201],source_macro_counts={'FI':0,'FA':0,'FO':0},
        source_A000_hex='00a0ffff010cc960',source_A000_raw_hex_words=['0C01','60C9'],
        source_C200_precedes_A000_then6240_and_single_end1880=True,
        source_names_and_city_retained_as_Japanese_until_approved_bindings=True,
        source_names_voices_terms_current_English_native_layout_reference_actual_release_pending=True,
        no_current_English_exposed=True,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,full_goal_complete=False)
    assert 'lil_B172_clean_source_lead_v4362' not in ledger
    ledger['lil_B172_clean_source_lead_v4362']=record
    after=encode_ledger(ledger)
    assert {k:v for k,v in json.loads(after).items() if k!='lil_B172_clean_source_lead_v4362'}==json.loads(before)
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    note=('V4362 records an uncredited clean-first B172 lead:all27 Japanese speeches were read and individually glossed as a complete exchange before predecessor English exposure. The source-named ユリアン flatters 美華,learns she wants 新羅の金冠,hears it is apparently in 京城 and not sold in shops,and asks for a date if he obtains it. Preserve her qualified I will think about it,his overeager promise interpretation and departure,Lil\'s wry overheard reaction,curiosity,independent search plan,and the final reversal asking Lil to show the crown. Bind approved actor/item/town names later;add no established romance,biological kinship,rank,precise location,source-country exposition,magic item power,earned progress or actual date agreement.\n\n'
        'Clean B172 is1884 bytes,SHA-256 feb4596dcc453b242d6e13aedb93aa1908699ea00f2d23750ff230be457ca59e. Retain38 commands:27 progressive speeches and11 leaves;selectors02/1A/C9,zero FI/FA/FO,FE,typed choices,relative sites,predicates or2000 pause. Preserve6000,45FF,6329,4651,6340,4620,632A,C200,A000,6240 andsingle end1880. C200 precedes the source A000 raw00a0ffff010cc960 (hex words0C01/60C9),then6240;no packed quest/recruitment semantics are inferred. No new ROM,English manuscript,editorial/completion credit or emulator run. Clean glosses: '+SOURCE.as_posix()+'.\n\n'
        'B171 remains complete in experimental V4353;the V4358c full audit and V4360 exact-value storage audit pass. Coverage stays5762 integrated/completed,5765 source/prose,3659 historically revised/2103 retained,zero pending and4163 completed route objects. V4353 retains547 manuscript batches/114 accepted layers and its byte-exact clean-input patch. Main remains V4303. Current-ledger writes use scripts.editorial_ledger_storage_v1.encode_ledger;all prior ledger values and exact pre-formatting bytes remain preserved.\n\n'
        'Next: Bind B172 clean/current source commands,preambles,three actors and original names/voices,source entry,resources,presentation,C200 and later A000. Reconcile exact reviewed crown/town terminology,then compare predecessor English only after the saved27 clean glosses. Review the complete exchange,retain working wording with individual reasons,validate native formatting and representative behavior,then register cumulative integration. B173-B180 has134 physical speech leads after this27-speech clean lead,not a full-project denominator;no B172 coverage credit is added yet. Every wider storyline,shared town/shop exchange,random scene,Help and other player-facing prose remains open. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell middle-field lead and B157 provenance amendment. Graphics/all18 plaques and the later older-record technical re-audit/queued0D gap remain separate. Preserve every ROM,translation,draft,producer,proof and failure. Full editorial goal active.')
    planned={LP:after}
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;first,rest=p.read_text(encoding='utf-8').split('\n',1)
        if name=='editorial_handoff_current.md':first='# Current editorial handoff - V4362'
        planned[p]=(first+'\n\n## V4362: B172 clean-first27-gloss lead; B171 complete\n\n'+note+'\n\n'+rest).encode('utf-8')
    stable={str(p):sha(p.read_bytes()) for p in [Path('translations/release_stack.json'),Path('translations/promoted_build.json'),Path('scripts/build_integrated_release.py'),Path('out/all_routes_combined_v4353_candidate.nds'),Path('out/all_routes_combined_v4353_candidate.xdelta')]}
    stage=ROOT/'staged';stage.mkdir();mutations=[]
    for i,(p,data) in enumerate(planned.items()):
        backup=ROOT/f'{i}.before';backup.write_bytes(p.read_bytes());target=stage/f'{i}.planned';target.write_bytes(data)
        mutations.append(dict(path=str(p),before_copy=str(backup),before_sha256=sha(p.read_bytes()),planned=str(target),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',mutations)
    for row in mutations:
        assert Path(row['path']).resolve().is_relative_to(Path.cwd().resolve())
        assert sha(Path(row['path']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
    for row in mutations:
        data=Path(row['planned']).read_bytes()
        with Path(row['path']).open('r+b') as f:
            f.write(data)
            if f.seek(0,os.SEEK_END)!=len(data):f.truncate(len(data))
            f.flush();os.fsync(f.fileno())
        assert sha(Path(row['path']).read_bytes())==row['planned_sha256']
    assert all(sha(Path(p).read_bytes())==v for p,v in stable.items())
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4362',ledger_sha256=sha(after),before_ledger_sha256=sha(before),
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),prior_verified_handoff=str(PRIOR),prior_verified_handoff_sha256=sha(PRIOR.read_bytes()),
        all_prior_ledger_values_preserved=True,clean_glosses=27,fresh_reread=5762,integrated=5762,pending=0,source_prose=5765,
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,updated_files={r['path']:r['planned_sha256'] for r in mutations},
        preserved_release_files=stable,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4362 clean B172 lead saved:27 glosses,no English exposure or credit;5762 integrated/0 pending;V4353 candidate,V4303 main preserved.')
