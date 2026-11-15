"""Record sealed10-actual B177 reference approval without adding review/completion credit."""
from copy import deepcopy
import gzip
import json
import os
from pathlib import Path
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.lil_B177_reference_checkpoint_text_v4641 import SUMMARY,NEXT
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B177_reference_checkpoint_v4641')
INPUT=Path('translations/lil_B177_editorial_manuscript_v5.json')
DOC=Path('translations/lil_B177_editorial_manuscript_v6.json')
APPROVAL=Path('work/analysis/lil_B177_reference_approval_v4640/approval_receipt.json')
FAMILY='Lil-B177-tomato-red-passion-youthful-love-dry-Cook-cook-sell-and-prospective-Genoa-fashion10'

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');before_bytes=lp.read_bytes();ledger=json.loads(before_bytes)
    assert sha(before_bytes)==read('work/analysis/editorial_handoff_verification_v4628/independent_verified_handoff.json')['ledger_sha256']
    approval,doc=read(APPROVAL),read(DOC)
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert len(approval['actual_sampled_display_IDs'])==10 and not approval['offline_only_display_IDs']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5885,5875,10)
    assert len(fresh['pending_contextual_families'])==1
    pending=fresh['pending_contextual_families'][0];assert pending['id']==FAMILY and pending['manuscript']==str(INPUT)
    paths=[APPROVAL,DOC,Path(__file__)]
    for key in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','postscene_native_state_proof']:
        p=Path(doc[key]);assert sha(p.read_bytes())==doc[key+'_sha256'];paths.append(p)
    for p,h in approval['evidence'].items():assert sha(Path(p).read_bytes())==h;paths.append(Path(p))
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    pending.update(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],pending=NEXT,
        actual_sampled_display_IDs=approval['actual_sampled_display_IDs'],offline_only_display_IDs=[],new_emulator_runs=2,
        reference_approval=str(APPROVAL),reference_approval_sha256=sha(APPROVAL.read_bytes()))
    fresh.update(latest_contextual_manuscript=str(DOC),latest_pending_contextual_family=FAMILY,
        coverage_note='5885 rereads/5875 integrated/10 pending;B177 native/reference/representative approved. No new review/completion credit;registered integration remains.')
    active=ledger['active_source_prose_drafts'];assert active['route_record_subsets_pending'][str(INPUT)]==[r['id'] for r in doc['records']]
    active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(INPUT)]=[]
    active['route_record_subsets_pending'][str(DOC)]=[r['id'] for r in doc['records']]
    active.update(status='3-reviewed-COMMON-incomplete;10-Lil-B177-reference-approved-pending-registered-release',note=fresh['coverage_note'])
    for unit in ledger['coverage_units']:
        if unit['id']==FAMILY:unit.update(**pending,status=doc['status'],actual_new_cold_boot_runs=2,actual_complete_native_panels=10,registered_release_pending=True)
        elif unit['id']=='all-route-scenes':unit['next']=NEXT
    oldscope=ledger['unfinished_editorial_scope_v4623'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
    inventory=deepcopy(read(oldscope['path']));inventory.update(next_focus=NEXT);inventory['B177_reference_and_actual_coverage_v4641']=pending
    ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4641']={**oldscope,'path':str(inv),'sha256':sha(inv.read_bytes())}
    ledger['lil_B177_reference_reconciliation_v4641']=dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=0,completion_credit_added=0,actual_new_cold_boot_runs=2,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    previous_ledger=json.loads(before_bytes)
    def same_except(a,b,allowed):
        assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}
    same_except(previous_ledger,ledger,{'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
        'unfinished_editorial_scope_v4641','lil_B177_reference_reconciliation_v4641','latest_checkpoint'})
    oldfresh=previous_ledger['contextual_story_natural_dialogue_pass_v1871']
    same_except(oldfresh,fresh,{'pending_contextual_families','latest_contextual_manuscript','latest_pending_contextual_family','coverage_note'})
    same_except(oldfresh['pending_contextual_families'][0],pending,{'manuscript','manuscript_sha256','manuscripts','pending',
        'actual_sampled_display_IDs','offline_only_display_IDs','new_emulator_runs','reference_approval','reference_approval_sha256'})
    oldactive=previous_ledger['active_source_prose_drafts']
    same_except(oldactive,active,{'manuscripts','route_record_subsets_pending','status','note'})
    assert active['manuscripts']==oldactive['manuscripts']+[str(DOC)]
    assert active['route_record_subsets_pending']=={**oldactive['route_record_subsets_pending'],str(INPUT):[],str(DOC):[r['id'] for r in doc['records']]}
    for a,b in zip(previous_ledger['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']==FAMILY:
            same_except(a,b,{'manuscript','manuscript_sha256','manuscripts','pending','actual_sampled_display_IDs','offline_only_display_IDs',
                'new_emulator_runs','reference_approval','reference_approval_sha256','status','actual_new_cold_boot_runs','actual_complete_native_panels','registered_release_pending'})
        elif a['id']=='all-route-scenes':same_except(a,b,{'next'})
        else:assert a==b
    same_except(read(oldscope['path']),inventory,{'next_focus','B177_reference_and_actual_coverage_v4641'})
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5875,5888,3733,2142)
    assert len(encode_ledger(ledger))<100*1024*1024
    pins=read('translations/rom_retention_pins.json')
    fixtures=read('work/analysis/lil_B177_display_fixture_v4635/complete_B177_B22_fixtures.json')['fixtures']
    for r in fixtures+[read('work/analysis/lil_B177_research_v4630/research_image_receipt.json')]:
        rom=Path(r['research_ROM']);assert sha(rom.read_bytes())==r['research_ROM_sha256']
        assert any(Path(p['path']).resolve()==rom.resolve() for p in pins)
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before_bytes,mtime=0))
    planned={lp:encode_ledger(ledger)}
    section='## V4641:10 B177 reviews reference/gameplay approved;registered integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for i,name in enumerate(['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']):
        p=Path('docs')/name;first,rest=p.read_text(encoding='utf-8').split('\n',1);(ROOT/(name+'.before')).write_bytes(p.read_bytes())
        planned[p]=(('# Current editorial handoff - V4641' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged=ROOT/'staged';staged.mkdir();mutations=[]
    for i,(path,data) in enumerate(planned.items()):
        output=staged/(str(i)+'.planned');output.write_bytes(data)
        mutations.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(output.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',mutations)
    stable=['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py','translations/rom_retention_pins.json']
    stable_hashes={p:sha(Path(p).read_bytes()) for p in stable}
    for row in mutations:
        assert sha(Path(row['target']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
    for row in mutations:
        data=Path(row['planned']).read_bytes()
        with Path(row['target']).open('r+b') as stream:
            stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
        assert sha(Path(row['target']).read_bytes())==row['planned_sha256']
    assert all(sha(Path(p).read_bytes())==h for p,h in stable_hashes.items())
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4641',evidence=evidence,ledger_sha256=sha(lp.read_bytes()),fresh_reread=5885,
        integrated=5875,pending=10,source_prose=5888,new_source_prose_reviews=0,new_completed_records=0,preserved_release_files=stable_hashes,
        updated_files={str(Path(r['target']).relative_to(Path.cwd())):r['planned_sha256'] for r in mutations},
        new_emulator_runs=2,actual_complete_native_panels=10,reviewed_sheets=2,ROMs_pinned=0,previously_pinned_ROMs_preserved=3,
        ROMs_deleted=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4641:10 B177 records reference/actual-approved;counts and main V4541 unchanged. Three pinned ROMs preserved;registered integration next.')
