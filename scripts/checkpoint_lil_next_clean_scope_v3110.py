"""Preserve verifiedV3107 and add an uncredited clean-only next-scope inventory."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_next_clean_scope_checkpoint_v3110')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3108/verified_handoff.json')
SOURCE=Path('work/analysis/lil_after_Recruits_Julian_clean_scope_v3109/clean_next_exchange_inventory.json')
SUMMARY=' '.join([
'V3110 preserves the independently verified V3107 completion checkpoint:3990 contextual rereads/integrated/completed,2800 historically revised/1190 retained;source/prose3993 including2163SC2. All2391 reviewed route objects are integrated. Experimental V3103 remains510manifest batches/114acceptedlayers with exactclean-inputpatch reconstruction and31fresh current opening/town framebuffer matches toV3066. V1492 remains promoted.',
'The next clean-only inventory covers LilSC2B81-B100:198speech objects,including191ordinary/sevenFE,andone typed menu atB82offset114. The menu labels have not yet received the new contextual/native-review pass;do not assume editorial choice credit from the object count. All274native commands were inventoried without unclassified blocks. Six nontext blocks85/87/89/90/97/98 containonecommand each andearn noeditorial credit. Fourteen text-bearing complete blocks81/82/83/84/86/88/91/92/93/94/95/96/99/100 have268commands. Exact clean speech references/bytes are mapped;current English references,native speaker identities/FEownership,full clean-exchange context,glosses/localization andevery target gate remain pending. Only first-line source leads were inspected to orient the next scope;no full contextual reread or new translation is claimed.',
'Next bind the14textblocks andtheir source alternatives toV3103,includingprintable selectors6C/72/98/BC andthe distinct sevenFEpanels,derive the typedmenu label count/order/pointers,then read complete clean exchanges before comparing older English. Preserve approved names/runtime substitutions andvalidatednative rules;review each source object individually with justifiedretentions,then integrate checked batches through a cumulative registered successor andexactcleanpatch/currentstartup. No exhaustive naturalplaythrough or individualconditional visit requirement is introduced.',
'COMMON750-752callers,every wider untouched storyline/sharedshop-town/random/help/playerprose,SourceItems/LocalProduct,fivenamedtargetleads,raw rejected-objectclassification includingB141,SC3B109,separategraphics/all18plaques andlater older-record technical re-audit remainopen. Queued0Dvalidationgap staysforlater withoutassertinganolderruntime defect. Every earlier completedfamily,includingB66/B121 andthe199recruitment/Julian objects,remains completed. Preserve allROMs,earliertranslations,executedproducers/proofs/failures andclean/canonicalinputs. This clean-only lead addszero editorial/completion credit andno ROM,registry ornewgameplay changes. Fullgoalactive;alljobsterminal.'
])
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    source=read(SOURCE);assert source['editorial_credit_added']==0 and not source['unclassified']
    assert [b['block'] for b in source['blocks']]==list(range(81,101))
    assert (sum(b['speeches'] for b in source['blocks']),sum(b['FE_panels'] for b in source['blocks']),sum(b['choice_commands'] for b in source['blocks']),sum(len(b['commands']) for b in source['blocks']))==(198,7,1,274)
    nontext=[b['block'] for b in source['blocks'] if not b['speeches']];text=[b['block'] for b in source['blocks'] if b['speeches']]
    assert nontext==[85,87,89,90,97,98] and all(len(b['commands'])==1 for b in source['blocks'] if not b['speeches'])
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3990,3990,0)
    assert ledger['records_with_source_and_prose_pass']==3993 and ledger['records_editorially_completed']==3990
    known={(r['file_path'],r['id']) for r in fresh['record_keys']};rows=[r for b in source['blocks'] for r in b['records']]
    assert len(rows)==198 and not known&{('/data/SC2.DK4',r['id']) for r in rows}
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf8').startswith('# Current editorial handoff - V3107')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    lead=dict(status='clean-only-source-inventory;full-exchange-current-reference-native-context-prose-review-pending',source_inventory=str(SOURCE),source_inventory_sha256=sha(SOURCE.read_bytes()),blocks=list(range(81,101)),text_blocks=text,nontext_blocks=nontext,speeches=198,ordinary_speeches=191,FE_panels=7,typed_menu_objects=1,typed_menu_label_count_not_yet_newly_bound=True,commands=274,text_block_commands=268,nontext_editorial_credit=0,
        full_clean_exchange_context_and_older_English_comparison_still_required=True,source_speech_references=[dict(block=b['block'],id=r['id'],offset=r['offset'],bytes=r['bytes'],source_hex=r['source_hex'],source_preamble_hex=r['source_preamble_hex']) for b in source['blocks'] for r in b['records']],
        no_new_prose_review_or_native_consumer_approval=True,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,full_goal_complete=False)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3107']['path']));inventory['next_clean_only_uncredited_exchange_inventory_v3109']=lead
    inventory['next_focus']='Bind andcontextually review198clean speeches andthe B82typedmenu across14text-bearing B81-B100exchanges. Continue every wider untouched storyline/sharedshop-town/random/help/playerprose;preserve all inherited unfinished leads,graphics separation andlater technical re-audit.'
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3110']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,next_clean_only_speeches=198,next_unreviewed_typed_menus=1,full_goal_complete=False)
    ledger['lil_next_clean_scope_lead_v3110']=lead;ledger['latest_checkpoint']=SUMMARY
    restored=deepcopy(ledger)
    for key in ['unfinished_editorial_scope_v3110','lil_next_clean_scope_lead_v3110']:restored.pop(key)
    restored['latest_checkpoint']=before['latest_checkpoint'];assert restored==before
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V3110:next clean-only scope;V3103 and3990completed reviews preserved\n\n'+SUMMARY+'\n\nNext clean-only inventory: '+SOURCE.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Completed release details remain in the V3107 section below.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf8').split('\n',1);p.write_text(('# Current editorial handoff - V3110' if i==0 else first)+'\n\n'+section+rest,encoding='utf8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,inv,Path('scripts/inventory_lil_after_recruits_julian_clean_v3109.py'),Path(__file__)]}
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3110',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},prior_verified_handoff=str(PRIOR),new_source_prose_reviews=0,new_completed_records=0,source_prose=3993,completed=3990,fresh_reread=3990,fresh_integrated=3990,fresh_pending=0,historical_revised=2800,historical_retained=1190,next_clean_speeches=198,next_typed_menu_objects=1,candidate=ledger['current_integrated_candidate'],new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V3110:next198clean speeches/one menu inventoried withoutcredit;3990completed/3993source-prose,V3103/exactpatch/current31framepairs preserved. Fullgoalactive.')
