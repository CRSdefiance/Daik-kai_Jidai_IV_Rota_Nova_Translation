"""Reversibly record the source-specific name retention without new dialogue credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Maria_B36_v7826b import COUNTERS,AFTER,INTRO,DETAILS,NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_source_checkpoint_v7865')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7866')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7863/verified_handoff.json')
PROOF=Path('work/analysis/Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Rafael_SC0B45_clean_gloss_pending_v7865'
SCOPE='unfinished_editorial_scope_v7865'
FINDING="Current registered experimental V7857 and verified completionV7863 contain the integrated Lil B218 R27 wrap improvement. The complete632-batch/114-accepted-layer stack passes18 release checks and110 regressions,equals the reviewed reference,and reconstructs byte for byte from its clean-input patch. All6938 completed/6941 source-prose anddrafts/4347 integrated wording revisions/2591 retentions remain;the B218 retrospective update adds no duplicate credit. MainV4701 and every earlier artifact remain.\n\nThe next fresh main-story source review returns to Rafael's SC0 catalogue. Complete clean B45 has12 stored speeches,24 native commands,764 stored/762 logical bytes andtwo zero tail bytes. No source record overlaps the completed ledger. All12 Japanese speeches were read and freshly glossed before any current B45 English body was exposed. This is source-only progress,not a completed translation or new source/prose credit.\n\nSource EV0 event45/category5/action46 selectsB45 and lists no explicit completion prerequisites or exclusions. The reviewed openingB44/event44 has no direct completion-dependency edge to45. Neither numeric adjacency nor those empty lists proves immediate chronology,natural eligibility/activation or original scene location. The dialogue itself refers to Lisbon andCeuta.\n\nRafael looks for the companion mentioned asフリオ,finds him at the trading facility,and learns about selling trade goods,obtaining local trading agreements by paying the ruler through a palace/governor's office,using the minimum fee early on,andhandling future agreements himself. The companion says he arranged Ceuta's agreement;one FE information panel states FO's Ceuta market share is20percent andthat trading depends onshare. The companion invites an optional sale andRafael agrees. Preserve the conditional cargo/sale/early-fee qualifications andthe difference between agreeing andhaving completed a profitable sale. Do not invent kinship,rank,fee amount,deadline,guaranteed mechanics orcompany ownership.\n\nOriginal speakers/selectors are00 and06 plus one FE system panel. Native names/voices,Julio's exact approved forms,Rafael's current substitutions andboth progressive/FE consumers still require binding. Source macros areFI0/FA0/FO1. Preserve the complete leading00 selector andsix-byte preamble;FE is a display selector,not a character. The 20percent/company panel needs its own native percent/substitution/bounds check. The source also contains0100/0200/0300/0400 relative controls,61FF/6300/6328/632B/8000/C281 andcomplete ends;their original native behavior,conditions andbranches remain to be reviewed. Do not assume all12 stored speeches execute together.\n\nThe remaining12 retrospective wrap candidates remain open and are rebound offline toV7857. The original558-plan scan doesnot cover all6938 completed records. Retain the source-supported151-159 水夫/Sailor progressive nameplates while reviewing separate配下/Retainer full-name andother consumers. Continue all four storylines andearlier translations,broad practical shop/town/random scenes,Help andall remaining player prose,all207 names/roles/aliases andevery unfinished inventory/counterpart/item/display lead. Preserve all ROMs,translations,drafts,failed producers,proofs andmeasured limits. Graphics/all18 plaques andlater older-record technical re-audit stay separate. No canceled separate unified test package,promotion,pruning,commit orpush."
NEXT="Continue from verifiedV7866/currentV7857 andRafael's source-only B45 packet work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json plus work/analysis/Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json. All12 clean Japanese speeches areglossed;current B45 English remains unread. First bind the original event/branch/control scope andsource names/roles. Capture Rafael's own currentV7857 NewGame context when needed;verify actualcaptain0 andthe full current runtime/payload rather than using Lil's orMaria's RAM. Measure original0/6 getters andFO substitution,keep approvedRafael,andresolveJulio fromclean/source consumers without inventing relationship orrank.\n\nThen compare all12 current effective English speeches asacomplete exchange against the clean glosses,binding catalogue routes and original controls before drafting natural-dialogue-v2 prose. Preserve the local trading-rights meaning ofagreement,conditional Lisbon cargo andoptional sale,early minimum-fee advice,Ceuta20percent market-share information andFO order. Treat the oneFE panel andpercent handling separately fromprogressive dialogue. Native branches/relative spans,complete first/final glyphs,bounds,pagination andrepresentative actual paths need their own source/current evidence;no generic wrap orall-lines-played assumption. Add credit only after necessary contextual/native/actual/registered integration checks.\n\nB218's wrap isalready integrated andverified inV7857;do not replay unchanged checks. For future Lil native work use work/analysis/current_V7857_Lil_native_v7860/current_native_input.json. Other routes' earlier snapshots remain correctly labelled historical;obtain own current contexts when needed. Review the12 remaining contraction/question-tag candidates ascomplete exchanges,extend beyond the558 recorded markup plans,andretain ordinary wraps with reasons.\n\nKeep the full four-storyline/earlier-dialogue/shared shop-town-random/Help/remaining-prose/207-name objective intact. Preserve all earlier unfinished inventories,role/item/counterpart/display leads,normal-end value-carry andsource-only nineteenth-cell findings for the later technical re-audit. Graphics/all18 plaques remain separate. Preserve every generated ROM andearlier translation. MainV4701 stays;no canceled separatepackage,automaticpromotion,pruning,commit orpush."
SUMMARY=FINDING

def restore(value):
    new=deepcopy(value);entry=new.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(new,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return new

def gates():
    prior,proof=map(read,[PRIOR,PROOF])
    source=read(proof['source_packet'])
    assert proof['source_packet_sha256']==sha(Path(proof['source_packet']).read_bytes())
    assert len(proof['records'])==12 and proof['all12_complete_clean_Japanese_speeches_read_before_current_English']
    assert proof['no_current_English_comparison_localized_manuscript_orcomplete_prose_approval']
    assert all(r['current_English_body_unread'] and r['review']['source'] and not r['review']['formatting'] for r in proof['records'])
    assert source['live_ledger_sha256']==prior['ledger_sha256'] and source['source_only_no_current_English_exposed_orused']
    assert len(source['groups'])==1 and source['groups'][0]['block']==45 and source['groups'][0]['physical_speech_objects']==12
    assert source['groups'][0]['completed_coverage_overlap']==0 and not source['inventory_failures']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    assert not proof['new_credit'] and not proof['new_emulator_runs']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    return prior,proof

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,proof=gates()
    if mode=='stage':
        assert not ROOT.exists()
        before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and KEY not in old
        assert tuple(old[k] for k in COUNTERS)==AFTER and old['goal_status']=='active' and not old['full_goal_complete']
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        oldscope=old['unfinished_editorial_scope_v7862'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(proof=str(PROOF),proof_sha256=sha(PROOF.read_bytes()),finding=FINDING,
            clean_source_speeches=12,fresh_source_glosses=12,current_English_bodies_unread=True,all_prior_inventories_andfull_scope_preserved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(proof=str(PROOF),finding=FINDING,native_names_macros_branches_current_English_andall_display_gates_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        index=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',index,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,scope,Path(__file__),
            Path('work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json'),
            Path('scripts/inventory_Rafael_next_clean_v7864.py'),Path('scripts/gloss_Rafael_B45_clean_v7864b.py')]}
        new[KEY]=dict(summary=FINDING,next=NEXT,proof=str(PROOF),evidence=evidence,inverse_operations=ops,
            clean_source_speeches=12,fresh_source_glosses=12,no_source_prose_orcompletion_credit=True,
            new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_native_getter_executions=0,
            clean_Japanese_only_no_current_English_orlocalized_prose_exposed=True,
            full_scope_remaining12_wrap_leads_andnames_remain_open=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7865: Rafael B45 clean-source review begun; V7857 current\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7865; V7857 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six Rafael clean-source checkpoint targets staged;all counts andcurrentROM unchanged.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER
        assert new['goal_status']=='active' and not new['full_goal_complete']
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                all_prior_roots_families_counters_currentROM_andhistory_recover_exactly=True,zero_credit=True,full_goal_complete=False))
            print('Deep inverse andall six before/planned hashes pass;zero credit.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_orcredit_change=True,full_goal_complete=False))
            print('Six audited Rafael clean-source checkpoint targets applied;V7857/6938completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                Rafael_B45_clean_source_review_pending=True,Rafael_B45_fresh_clean_glosses=12,Rafael_B45_current_English_bodies_unread=True,
                recorded_markup_plans_scanned=558,completed_records_not_in_markup_scan=6380,
                pending_Rafael_source_gloss=str(PROOF),pending_Rafael_source_gloss_sha256=sha(PROOF.read_bytes()),
                Rafael_B45_own_current_route0_context_pending=True,
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_native_getter_executions=0,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('V7866 verified:Rafael B45 clean12 glosses/current English unread;V7857/6938complete remain.Fullobjective active.')
