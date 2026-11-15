"""Record sealed32-actual B175 reference approval without adding review/completion credit."""
from copy import deepcopy
import gzip
import json
import os
from pathlib import Path
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.lil_B175_reference_checkpoint_text_v4537 import SUMMARY,NEXT
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_reference_checkpoint_v4537')
INPUT=Path('translations/lil_B175_editorial_manuscript_v3.json')
DOC=Path('translations/lil_B175_editorial_manuscript_v4.json')
APPROVAL=Path('work/analysis/lil_B175_reference_approval_v4536/approval_receipt.json')
FAMILY='Lil-B175-pirate-encirclement-pride-sea-challenge-unnamed-sword-and-banter32'

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');before_bytes=lp.read_bytes();ledger=json.loads(before_bytes)
    assert sha(before_bytes)==read('work/analysis/editorial_handoff_verification_v4524/verified_handoff.json')['ledger_sha256']
    approval,doc=read(APPROVAL),read(DOC)
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert len(approval['actual_sampled_display_IDs'])==32 and not approval['offline_only_display_IDs']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5865,5833,32)
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
        coverage_note='5865 rereads/5833 integrated/32 pending;B175 native/reference/representative approved. No new review/completion credit;registered integration remains.')
    active=ledger['active_source_prose_drafts'];assert active['route_record_subsets_pending'][str(INPUT)]==[r['id'] for r in doc['records']]
    active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(INPUT)]=[]
    active['route_record_subsets_pending'][str(DOC)]=[r['id'] for r in doc['records']]
    active.update(status='3-reviewed-COMMON-incomplete;32-Lil-B175-reference-approved-pending-registered-release',note=fresh['coverage_note'])
    for unit in ledger['coverage_units']:
        if unit['id']==FAMILY:unit.update(**pending,status=doc['status'],actual_new_cold_boot_runs=2,actual_complete_native_panels=32,registered_release_pending=True)
        elif unit['id']=='all-route-scenes':unit['next']=NEXT
    oldscope=ledger['unfinished_editorial_scope_v4519'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
    inventory=deepcopy(read(oldscope['path']));inventory.update(next_focus=NEXT);inventory['B175_reference_and_actual_coverage_v4537']=pending
    ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4537']={**oldscope,'path':str(inv),'sha256':sha(inv.read_bytes())}
    ledger['lil_B175_reference_reconciliation_v4537']=dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=0,completion_credit_added=0,actual_new_cold_boot_runs=2,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    pins=read('translations/rom_retention_pins.json')
    fixtures=read('work/analysis/lil_B175_display_fixture_v4531/complete_B175_B22_fixtures.json')['fixtures']
    for r in fixtures+[read('work/analysis/lil_B175_research_v4526/research_image_receipt.json')]:
        rom=Path(r['research_ROM']);assert sha(rom.read_bytes())==r['research_ROM_sha256']
        assert any(Path(p['path']).resolve()==rom.resolve() for p in pins)
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before_bytes,mtime=0))
    planned={lp:encode_ledger(ledger)}
    section='## V4537:32 B175 reviews reference/gameplay approved;registered integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for i,name in enumerate(['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']):
        p=Path('docs')/name;first,rest=p.read_text(encoding='utf-8').split('\n',1);(ROOT/(name+'.before')).write_bytes(p.read_bytes())
        planned[p]=(('# Current editorial handoff - V4537' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
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
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4537',evidence=evidence,ledger_sha256=sha(lp.read_bytes()),fresh_reread=5865,
        integrated=5833,pending=32,source_prose=5868,new_source_prose_reviews=0,new_completed_records=0,preserved_release_files=stable_hashes,
        updated_files={str(Path(r['target']).relative_to(Path.cwd())):r['planned_sha256'] for r in mutations},
        new_emulator_runs=2,actual_complete_native_panels=32,reviewed_sheets=6,ROMs_pinned=0,previously_pinned_ROMs_preserved=3,
        ROMs_deleted=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4537:32 B175 records reference/actual-approved;counts and main V4496 unchanged. Three pinned ROMs preserved;registered integration next.')
