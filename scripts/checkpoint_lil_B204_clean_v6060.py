"""Record20 uncredited clean glosses while preserving the verified cumulative build."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_clean_checkpoint_v6060')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6061')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6056/verified_handoff.json')
INV=Path('work/analysis/lil_B204_clean_inventory_v6058/all_clean_B204_speeches_before_predecessor_comparison.json')
GLOSS=Path('work/analysis/lil_B204_clean_context_v6059/all20_clean_castle_figurehead_claim_missing_shachihoko_and_letter_glosses.json')
KEY='Lil_B204_clean_source_v6060'
SCOPE='unfinished_editorial_scope_v6060'
NEXT='Continue B204 from complete clean inventory6058 and whole-exchange gloss6059 before reading older English. Bind source actors2/11/124/130/145 and four separate FE letter objects to exact clean/current names,voices,complete preambles and display consumers. Review the おばさん address without inventing an aunt,the source lord/retainer forms without unproved royal/military ranks,and the full ジャム・ジャック・ルドワイヤン signature through approved name consumers. Bind シャチホコ to exact clean item data/current widget and preserve the 南蛮文字 foreign-writing cultural context without inventing a particular language. Keep the apparent figurehead explanation as the writer confident character claim,not objective narrator truth. Preserve the explicit theft accusation and the contrast with the earlier claimed gift. Map all26 commands/six nonspeech leaves,end1308/no tail padding,and actual transition/acquisition/letter scope without borrowing B203 book,FE charm notice,FIfirst-name or currency semantics. Capture the complete Japanese exchange and letter before final English comparison;then author natural American English as complete paragraphs,validate native glyphs/wrapping/bounds/pagination/substitutions and source references,use representative revised English gameplay,and integrate once necessary registered-release checks pass. Keep20 clean glosses uncredited until verified integration. Reuse sealed B203/V6050 checks absent a concrete new risk. Keep all storylines,earlier translations,shared town/shop/random/Help/prose,all207 name/role/alias consumers and retrospective wraps in scope. Preserve every artifact and earlier unresolved lead,including B43 source-item/Local Product,Samwell middle field and Alexandria caller/display. Graphics/all18 plaques and later older-record technical re-audit remain separate/open.'
DETAILS='V6060 records a fresh clean-only B204 inventory and complete20-object gloss before older English. Source1312 stored/logical bytes has no alignment tail,26 commands,16 progressive speeches/four FE letter objects and selectors11x7/145x1/2x3/124x3/130x2/254x4. No FI/FA/FO,typed choices/styles,predicates,relative sites or2000 pauses appear in this inventory. Six exact nonspeech leaves remain uninterpreted beyond their source boundaries:4301,4381,4835,4735,oneA000 and four-byte end1308.0B asks91 about a walk to relieve boredom and hears of a castle to the east. The Japanese castle/loanword recognition needs natural localization. After the outing,02 demands to know where0B has been.0B excuses a heavy object,boasts that it is a genuine made-in-Japan figurehead,and claims a thank-you gift for teaching locals its use.02 conditionally accepts only if it was not stolen and orders departure preparations. A cutaway has7C report a missing shachihoko and foreign-script letter to82;82 complains about morning noise,then explicitly orders the thief found. Four FE letter parts address the Japanese lord,prescribe ship rather than castle use,announce taking one so-called spare instead of thanks,and close with the full source signature. Preserve the conflicting gift claim,unilateral taking,thief accusation and comic cultural misunderstanding. Do not invent an aunt relationship,king/emperor,named castle,specific foreign language,unproven rank,legitimate ownership or arrest. Bind all five actors/voices,names/roles,full signature,shachihoko/item widget,transitions,letter consumers and source gameplay before target prose. These20 clean glosses add no source-prose/completion credit,no ROM or emulator run. Experimental cumulative V6050 and its exact clean-input patch remain verified with591 batches/114 accepted/18 checks. B20322 reviews were integrated once:nine revisions/13 justified retentions. Coverage stays6349 completed/6352 source-prose/3968 integrated revisions/2381 justified retentions/SC24464/SC396/routes4750/4750,zero credited route drafts pending. Main V4701 remains promoted. All earlier root/nested history,ROMs,translations,producers,proofs,failures and unresolved scope remain preserved. The full four-storyline/earlier-dialogue/shared town/shop/random/Help/prose,retrospective premature-wrap and207-entry name/role/alias goal stays active. Graphics/all18 plaques and later older-record technical re-audit remain separate/open.'
def inverse(new):
    d=deepcopy(new);entry=d.pop(KEY);d.pop(SCOPE);d['latest_checkpoint']=entry['previous_latest_checkpoint'];return d
def immutable_checks():
    prior=read(PRIOR);release=read('work/analysis/lil_B203_release_v6051/registered_release_verification.json')
    for k in ['candidate','patch']:assert prior[k+'_sha256']==release[k+'_sha256']==sha(Path(release[k]).read_bytes())
    for p,h in read('releases/all_routes_unified_v6050/immutable_input_audit.json')['inputs'].items():assert sha(Path(p).read_bytes())==h
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(manifest['batches'])==591 and all(manifest['checks'].values())
    return prior
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();prior=immutable_checks();before=LEDGER.read_bytes();assert sha(before)==prior['ledger_sha256'];old=json.loads(before);gloss=read(GLOSS);assert gloss['prior_English_speech_unread'] and len(gloss['records'])==20 and gloss['new_review_credit']==0
        new=deepcopy(old);assert KEY not in new and SCOPE not in new;summary=DETAILS+'\n\n'+NEXT
        inventory=deepcopy(read(old['unfinished_editorial_scope_v6055']['path']));inventory['next_focus']=NEXT;inventory['historical_B204_clean_pending_before_v6060']=inventory.pop('next_Lil_B204_clean_review_pending')
        inventory['Lil_B204_clean_only_uncredited_v6060']=dict(clean_inventory=str(INV),clean_inventory_sha256=sha(INV.read_bytes()),clean_gloss=str(GLOSS),clean_gloss_sha256=sha(GLOSS.read_bytes()),source_speech_objects=20,source_commands=26,prior_English_unread=True,reviewed_target_objects=0,new_source_prose_or_completion_credit=0,actual_names_voices_roles_title_widget_controls_source_paths_and_English_pending=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        evidence={str(p):sha(p.read_bytes()) for p in [INV,GLOSS,PRIOR,Path(__file__),Path('releases/all_routes_unified_v6050/verification.json')]}
        new[SCOPE]=dict(path=str(scope),sha256=sha(scope.read_bytes()),B204_clean_only_uncredited_speech_and_letter_objects=20,retrospective207_names_and_all_wider_editorial_families_preserved=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,previous_latest_checkpoint=old['latest_checkpoint'],evidence=evidence,source_speech_objects=20,new_source_prose_reviews=0,new_completed_records=0,new_ROMs=0,new_emulator_runs=0,goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
        new['latest_checkpoint']=summary;assert inverse(new)==old
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V6060: B204 clean-only whole-exchange gloss;V6050 stays verified\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            target=Path('docs')/name;text=target.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V6060\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[target]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;20 clean-only B204 glosses,no credit or candidate change.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;prior=immutable_checks()
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['records_editorially_completed']==6349 and new['records_with_source_and_prose_pass']==6352 and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_audit.json').exists();save(ROOT/'independent_audit.json',dict(deep_inverse_preserves_all_history=True,all_six_targets_and_immutable_inputs_verified=True,staged_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),full_goal_complete=False));print('Checkpoint deep inverse,six targets and immutable inputs audited.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'independent_audit.json')['staged_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,full_goal_complete=False));print('Six audited checkpoint files applied.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            result={**prior,'previous_verified_handoff':str(PRIOR),'previous_verified_handoff_sha256':sha(PRIOR.read_bytes()),'ledger_sha256':sha(LEDGER.read_bytes()),'all_prior_history_and_current_candidate_exactly_preserved':True,'latest_checkpoint_key':KEY,'next_B204_clean_source_glosses':20,'B204_target_reviews_uncredited':True,'prior_English_B204_speech_unread':True,'new_source_prose_or_completion_credit':0,'goal_turn_classification':'progress','evidence':plan['evidence'],'producer_sha256':sha(Path(__file__).read_bytes())}
            save(VERIFY/'verified_handoff.json',result);print('Verified V6060 clean-only checkpoint:V6050/6349 completed unchanged,B20420 glosses uncredited;full goal active.')
