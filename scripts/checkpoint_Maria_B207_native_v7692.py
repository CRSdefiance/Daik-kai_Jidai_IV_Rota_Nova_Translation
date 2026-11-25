"""Transactional pending Maria checkpoint with exact inverse and no completion credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.verify_village_wrap_v608 import read,save
from scripts.draft_Maria_B207_prose_v7687 import CURRENT,CLEAN,CONSUMERS,ENTRY,HEADER,FONTS,CONTROLS,CONTEXT,MANUSCRIPT,NAMES,ROOT as PROSE_ROOT
from scripts.record_Maria_B207_view_v7691 import PLAN,NATIVE,ROOT as VIEW_ROOT
ROOT=Path('work/analysis/maria_B207_native_checkpoint_v7692')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7693')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7667/verified_handoff.json')
PROSE=PROSE_ROOT/'complete_Maria18_decisions13_revisions5_justified_retentions_display_pending.json'
VIEW=VIEW_ROOT/'Maria18_native_paragraphs_andown_selection_viewed_stored_actual_pending.json'
LOGICAL=Path('work/analysis/maria_B207_logical_v7688/all18_Maria_logical_bodies72_fresh_literal_IF_alignments.json')
KEY='Maria_SC3B207_prose_native_pending_v7692'
SCOPE='unfinished_editorial_scope_v7692'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
VALUES=(6837,6840,6840,4277,2560)
SUMMARY="""V7660 remains the registered experimental cumulative ROM:628 batches,114 accepted layers,18 release checks,110 regressions andthe existing exactly reconstructable clean-input patch. Completed counters remain6837 completed,6840 source-prose/drafts,4277 revisions and2560 retentions. SC0 135,SC1 91,SC2 4915,SC3 96 andCOMMON1600 completed/1603 source-prose remain unchanged. Route5237/5237 is a subset,not full-goal completion. Maria's18 new decisions below remain uncredited andunintegrated;all formatting gates stayfalse. MainV4701 andevery prior ROM,translation,draft,executed producer,failure,trace andproof remain preserved.

The earlier17-reference metadata lead omitted opening silenceR4. Full clean SC3B207 has18 speeches,20 commands,1468 stored/logical bytes,zero tail,A0001456/raw00a0ffff6a000110 andcomplete four-byte end1464. All18 Japanese bodies,preambles andcommands match the previously reviewed LilB234 source,butthe Maria header is43530101b4050000(CS0101),differing atbyte2 fromCS0001. Its null-count record IDs areone lower. Do not normalize that header orclaim whole-block equality. Exact Japanese/native-command equality explicitly binds reuse ofthe18 prior clean glosses before current English;no fresh gloss authorship orEnglish-derived source isclaimed. Clean adjacent206/208 wereinspected without credit orassumed narrative continuity.

Own-current Maria NewGame4000 nowbinds actualcaptain3,strict2b6 ARM9,COMMON,directory andall123264 deployed payload bytes at work/analysis/maria_B207_native_v7681/current_native_input.json. This context explicitly requires the existing audited system-only unlock fixture295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949;earned unlock isfalse. Its original donor,unchanged six route slots/footer andexact three historical changed bytes areverified. No historical RAM overlay,savestate,ROM/runtime patch,story/location/RNG/funds/roles/roster/outcome fixture isused. The actual Lil-to-Maria selection andMaria opening sheet wasviewed. This isNewGame/opening evidence,not natural optionalB207 activation. Existing strict captains0/1/2 inputs remainunchanged andcannot substitute forMaria dynamic consumers.

Preserve allfour terminal/reaped4001-frame selection captures. V7671 withoutthe historical unlock openedSoundSetup;V7674/V7677 no-battery retries selectedRafael andfailed strictcaptain3 binding before output. V7680 withthe exact disclosed unlock passes;the separate Maria-only context validates it ratherthan weakening anyother route's no-battery orcaptain guards. The original failed binders/producers remain. Failed7686 compared the six-word native result against a two-word list;7686b checks the complete[0,seed,0,0,0,0] result without changing anynative code,seed orcontract. These aretest setup/assertion failures,not counted negative-control rejections.

Fresh36 source/current speech dispatches bind18 effective predecessor bodies,catalogue route3/mask8,static19/104 andvoices7/0. All bodies passunchanged andhavezero FI/FA/FO macros;no Maria defaults areinvented. Four original getters returnCarloSinat/Trader. Twenty fresh Maria name-literal alignments reusefive exact full native font planes withunchanged ARM9/COMMON/FNT;zero fresh name-font renders areclaimed. Cleanカルロ/シナート,null middle andwhole banter supportCarloSinat. 交易所の親父 supportsTrader here,not Carlo'sfather;separateEuropean regional metadata isexcluded fromboth names anddoesnot establish a surname ornationality. Explicitフィリポ atR8/R15 supports spokenFilippo only. Two contextual name retentions arein translations/maria_B207_speaker_name_review_v1.json;actual optional headers/full catalogueUI andthe broader207-name/role/alias review remainopen.

EV3event207/action208 binds through the original own-Maria event getter;it hasno completion prerequisites orexclusions. Outer eligibility,location,natural activation,earned progress andfull effects remainunproved. Two fresh original wholeB207 loads/cache hits andfour parent modes preserve the full distinctCS0101 header andbegin atpayload+8. Fifty fresh clean/current seeded normal ends preserve the complete four-byte terminal. Two exact isolatedA000 structural proofs arereused bycommand/runtime equality,not whole-block equality orproof ofitem/blessing/ownership/reward semantics.

The complete clean-Japanese exchange isreviewed asfamiliar distracted-merchant banter leading intohistorical papal trade andaconditional discovery. translations/maria_B207_editorial_manuscript_v1.json records13 proposed revisions andfive individually justified retentions atR4/R11/R28/R46/R59. Preserve the silence,Carlo/Filippo familiarity,tentative unspecified recovery,being aboard the companions'ship,apology,merchant great-grandfather,papal direct rule almost toVenice,donation competition,ancestral profits/decline/envy,reported occasional objects,prospective blessings,reflective divine aid andexplicit if-found condition. No invented kinship,rank,nationality,recovery cause,current city/date,modern history,lord-to-lord route,taxes/bribes,authenticated relic,precise site or guaranteed effect/reward. Item106 remainsunchanged;the body introducesno item title,pope ordinal orbiography.

All18 logical paragraphs pass72 fresh actual-Maria native literalI/F alignments;compiled bodies passanother72. The guarded Maria route profile keeps216x64/four-row pages,complete36-cell firstrows and35-cell guarded continuations. All18 fitone original page;13 native page renders arefresh andfive reuse exact compiled-body/ARM9/COMMON/FNT proofs. Allthree sheets wereindividually viewed. Complete first/internal/final glyphs,bounds,canaries,consumption,pair phase andguards pass. Seven informational row-count changes haveindividual reasons;there areno base QA warnings/errors orwaivers. Allprose words/punctuation remain. R4's CP932 ellipses useanexact reused native font plane;the generic offline shade doesnot establish actual counterpart palette. Native previews areoffline CPU checks,not actual optional gameplay. Allformatting gates remainfalse until stored/policy/relocation/representative actual/release checks pass.

The complete four-storyline,earlier translated conversations,shared town/shop,random,Help,remaining player-facing prose,all207 names/roles/aliases andretrospective premature-wrap objective remainsactive. Preserve allprevious completed history andunresolved leads fromthe V7666 scope inventory. Graphics/all18 plaques andthe later older-record technical re-audit remainseparate,including earlier measured timing/RNG/state/RGB limits. No canceled unified test package,automatic promotion,pruning,commit orpush isperformed."""
NEXT="""Continue from Maria SC3B207's18 complete prose decisions,owncaptain3 input andviewed native plans. Do not repeat unchanged clean extraction/gloss bindings,route selections,dispatches/getters,EV entry,header loads,logical/compiled ABI cases ornative pages. Preserve its CS0101 header andexact source/current references;never useaLil/Rafael/Hodram context forMaria. Freeze exact text/source/current/compiled inputs andallbase QA afterfinal contextual cadence review;validate source-owned policy with actual-changing negative cases before anyshared mutation. Map the completeblock forrelocation,prove whole-source/predecessor inverse andallunowned bytes,validate finalstored parity/complete glyphs/bounds/pagination,anduse representative disclosed original-initializer gameplay fordistinctMaria behavior/transitions andconcrete risks. The earlier source-only source-CS0101 load/entry proof isnot actual changed-scene display. Keep the existing system-unlock fixture explicitly disclosed andearned=false. Integrate once necessary checks pass through the full registered cumulative stack andexactly reconstructable clean-input patch,then own-ROM startup/native checks andgrant18 disjoint decisions once. Preserve thefull unfinished inventory,allartifacts,graphics separation andlater technical re-audit. No separate canceled package,automatic promotion,pruning,commit orpush."""
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def gates():
    ledger,prior,prose,native,view=map(read,[LEDGER,PRIOR,PROSE,NATIVE,VIEW])
    assert tuple(ledger[k] for k in COUNTERS)==VALUES and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    candidate=ledger['current_integrated_candidate'];manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert candidate['sha256']==prior['candidate_sha256']==sha(Path(candidate['path']).read_bytes()) and candidate['profile']=='all-routes-unified-v7660'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['batches'])==628 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert prose['revised']==13 and prose['retained']==5 and len(prose['records'])==18 and prose['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in prose['records'])
    assert native['fresh_compiled_alignment_cases']==72 and native['exact_reused_logical_alignment_cases']==72 and view['all_three_native_page_sheets_individually_viewed']
    assert read(CONSUMERS)['actual_original_captain_ID']==read(CONTEXT)['actual_original_captain_ID']==3
    assert read(HEADER)['four_native_parent_modes']==4 and read(CONTROLS)['fresh_normal_terminal_seed_cases']==50
    completed={(f['file_path'],r['id']) for f in ledger['completed_editorial_families'] for r in f['records']}
    assert not completed&{(r['file_path'],r['id']) for r in prose['records']}
    return prior,prose
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,prose=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        scope=old['unfinished_editorial_scope_v7666'];assert sha(Path(scope['path']).read_bytes())==scope['sha256']
        inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(manuscript=str(MANUSCRIPT),native_review=str(VIEW),file_qualified_positions=18,proposed_revisions=13,proposed_retentions=5,own_Maria_context=str(CONTEXT),CS0101_header_preserved=True,existing_system_only_unlock_not_earned=True,source_prose_or_completion_credit_added=0,stored_actual_policy_reference_andrelease_pending=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,Maria_SC3B207_18_prose_decisions_native_reviewed_uncredited=True,full_goal_complete=False))
        put(['formatting_watchlist','Maria_SC3B207_v7692'],dict(status='prose-native-reviewed-stored-actual-policy-release-pending',native_review=str(VIEW),distinct_CS0101_header_preserved=True,all_formatting_gates_false=True,no_new_credit=True))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5237;put(['coverage_units',ri,'next'],NEXT)
        paths=[CURRENT,CLEAN,CONSUMERS,ENTRY,HEADER,FONTS,CONTROLS,CONTEXT,MANUSCRIPT,NAMES,PROSE,LOGICAL,PLAN,NATIVE,VIEW,PRIOR,inv,Path('translations/release_stack.json'),Path('scripts/maria_existing_unlock_contract_v7680.py'),Path('scripts/maria_unlocked_current_context_v7680.py'),Path(__file__)]
        for version,binder in [('7671','7672'),('7674','7675'),('7677','7678'),('7680','7681')]:
            paths.extend([Path('work/analysis/maria_B207_route_run_v'+version+'/terminal.json'),Path('scripts/capture_Maria_B207_context_v'+version+'.py'),Path('scripts/bind_Maria_B207_context_v'+binder+'.py')])
        paths.extend([Path('scripts/prove_Maria_B207_controls_v7686.py'),Path('scripts/prove_Maria_B207_controls_v7686b.py')])
        evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(records=deepcopy(prose['records']),file_qualified_source_current_refs=18,proposed_revisions=13,proposed_retentions=5,reviewed_names=str(NAMES),native_review=str(VIEW),source_prose_or_completion_credit_added=0,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,current_ROM_families_all_five_credit_counters_andprior_records_unchanged=True,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V7692: Maria SC3B207 prose and native review; stored/actual/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7692; V7660 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six-target Maria18 pending checkpoint staged;zero credit,V7660/families/counters unchanged.')
    else:
        staged=ROOT/'staged_checkpoint.json';plan=read(staged);old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES
        for e in plan['files']:
            assert sha(Path(e['planned']).read_bytes())==e['planned_sha256']
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha(staged.read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,zero_credit=True,full_goal_complete=False));print('Deep inverse audit passes;all prior roots/records/families/counters/ROM refs recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha(staged.read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False));print('Six audited checkpoint targets applied;18 uncredited Maria decisions,unchanged V7660.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,Maria_SC3B207_18_uncredited_prose_decisions13_revisions5_retentions=True,own_Maria_captain3_strict_native_context_bound_with_exact_test_unlock=True,new18_logical_andcompiled_native_alignments144=True,all18_distinct_native_pages_viewed_13fresh5exact_reuse=True,distinct_CS0101_preserved_two_loads_four_parent_modes=True,stored_actual_policy_reference_andregistered_integration_pending=True,all_new_formatting_gates_false=True,new_credit=0,pending_checkpoint=str(ROOT/'application_receipt.json'),full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified);print('V7692 verified:Maria18 prose/native decisions pending stored/actual/release;V7660/6837completed unchanged.Full goal active.')
