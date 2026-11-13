"""Stage,audit,apply and verify native-approved work without premature coverage credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B204_native_checkpoint_text_v6133 import DETAILS,NEXT
ROOT=Path('work/analysis/lil_B204_native_checkpoint_v6133');VERIFY=Path('work/analysis/editorial_handoff_verification_v6134')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v6116/verified_handoff.json')
DOC=Path('translations/lil_B204_editorial_manuscript_v6.json');APPROVAL=Path('work/analysis/lil_B204_native_approval_v6132/all20_source_prose_current_native_approval.json')
FONT=Path('work/analysis/lil_B204_fonts_v6131/all20_progressive_FE_native_planes_and160_alignment_cases.json')
CAPACITY=Path('work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json')
KEY='Lil_B204_native_review_v6133';SCOPE='unfinished_editorial_scope_v6133'
def inverse(value):
    d=deepcopy(value);entry=d.pop(KEY);d.pop(SCOPE);d['latest_checkpoint']=entry['previous_latest_checkpoint'];return d
def gates():
    v,a,f,c,doc=map(read,[PRIOR,APPROVAL,FONT,CAPACITY,DOC]);validate_natural_dialogue_batch(doc)
    for k in ['candidate','patch']:assert sha(Path(v[k]).read_bytes())==v[k+'_sha256']
    assert doc['current_ROM_sha256']==v['candidate_sha256'] and a['manuscript_sha256']==sha(DOC.read_bytes())
    assert a['all20_five_gates_approved'] and a['all20_uncredited_pending_relocation_actual_English_and_registered_release'] and (a['revised'],a['retained'])==(12,8)
    assert len(a['formatter_negative_controls'])==28 and len(a['source_consumer_negative_controls'])==24 and a['covered_native_alignment_cases']==160
    assert len(f['cases'])==20 and f['new_native_alignment_calls']==40 and f['exact_input_byte_identical_reused_native_alignment_cases']==120
    for s in a['viewed_sheets']:assert s['viewed_after_original_detail_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256']
    assert len(c['cases'])==8 and c['native_observed_row_ASCII_characters']==36 and c['native_observed_text_capacity_px']==216
    assert Path('dk4tool/dialogue/lil_B204_profile.py').exists() and Path('work/analysis/lil_B204_fonts_v6124/DK4_MES_B204_R0062_complete_native.png').exists()
    for path,h in a['evidence'].items():assert sha(Path(path).read_bytes())==h
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return v,doc
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();v,doc=gates();before=LEDGER.read_bytes();assert sha(before)==v['ledger_sha256'];old=json.loads(before);new=deepcopy(old);assert KEY not in new and SCOPE not in new
        summary=DETAILS+'\n\n'+NEXT;ROOT.mkdir(parents=True)
        inv=deepcopy(read(old['unfinished_editorial_scope_v6115']['path']));inv['next_focus']=NEXT
        inv['Lil_B204_native_approved_uncredited_v6133']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),objects=20,revised=12,retained=8,all20_current_native_planes_and160_alignment_cases_pass=True,twelve_individual_row_count_reasons=True,actual_revised_English_relocation_and_registered_release_pending=True,previous_B204_target_unwritten_flags_are_historical_and_superseded_here=True,new_completion_credit=0)
        inv['FE_bitmap_vs_text_capacity_v6125']=dict(proof=str(CAPACITY),proof_sha256=sha(CAPACITY.read_bytes()),bitmap_width_px=228,measured_text_capacity_px=216,caught_failed228px_host_plan_preserved=True,native_ROM_geometry_unchanged=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inv
        scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inv);new[SCOPE]=dict(path=str(scope),sha256=sha(scope.read_bytes()),uncredited_B204_native_approved_objects=20,incomplete_COMMON=3,incomplete_credited_route_drafts=0,retrospective207_names_and_all_wider_editorial_families_preserved=True,full_goal_complete=False)
        paths=[DOC,APPROVAL,FONT,CAPACITY,PRIOR,Path(doc['source_context']),Path(doc['control_contract']),Path(__file__),Path('scripts/lil_B204_native_checkpoint_text_v6133.py'),Path('dk4tool/dialogue/lil_B204_profile_v2.py'),Path('dk4tool/dialogue/lil_B204_layout_v4.py'),Path('scripts/lil_current_font_oracles_v6122.py')];evidence={str(p):sha(p.read_bytes()) for p in paths}
        refs=[dict(id=r['id'],file_path=r['file_path'],source_reference=r['source_reference'],source_hex=r['source_hex'],current_reference=r['current_reference'],current_hex=r['current_hex'],english=r['english'],compiled_hex=r['compiled_hex'],decision=r['editorial_decision'],reason=r['localization_note'],retention_justification=r.get('fresh_retained_wording_justification'),source_meaning=r['source_meaning'],source_and_native_approved_not_yet_integrated=True,new_credit=0) for r in doc['records']]
        new[KEY]=dict(summary=summary,next=NEXT,previous_latest_checkpoint=old['latest_checkpoint'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),approval=str(APPROVAL),evidence=evidence,records=refs,revised_drafts=12,retained_drafts=8,new_source_prose_reviews=0,new_completed_records=0,new_ROMs=0,new_emulator_runs=0,goal_turn_classification='progress',previous_goal_turn_classification='progress',no_live_emulator_job_or_wait=True,full_goal_complete=False)
        new['latest_checkpoint']=summary;assert inverse(new)==old
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V6133: B204 whole-exchange English and native formatting approved; actual/release pending\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text('utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V6133\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,all20_approved_drafts_uncredited=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged:20 native-approved B204 drafts,exact source/current findings and unchanged cumulative release/counts.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;v,doc=gates()
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['records_editorially_completed']==6350 and new['records_with_source_and_prose_pass']==6353 and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(deep_inverse_preserves_every_prior_root_and_nested_value=True,all_six_targets_and_native_review_evidence_verified=True,staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),no_duplicate_or_premature_review_credit=True,full_goal_complete=False));print('Six targets,all old history,20 uncredited approvals and current V6110 audited.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as f:f.write(Path(e['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all6_audited_targets_applied_exactly=True,all_before_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited checkpoint files applied;all historical values and compression retained.')
        else:
            assert read(ROOT/'application_receipt.json')['all6_audited_targets_applied_exactly'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=v['candidate'],candidate_sha256=v['candidate_sha256'],patch=v['patch'],patch_sha256=v['patch_sha256'],profile=v['profile'],all_prior_root_and_nested_history_preserved=True,B204_source_prose_native_approved_uncredited_objects=20,B204_revised_drafts=12,B204_retained_drafts=8,all20_current_native_planes160_covered_alignments24_source_and28_formatter_negatives_pass=True,FE_228px_bitmap_vs216px_text_capacity_proven_and_caught_failure_preserved=True,completed=6350,source_prose=6353,revised=3969,retained=2381,SC2=4464,SC3=96,reviewed_routes=4750,completed_routes=4750,new_ROMs=0,new_emulator_runs=0,no_live_emulator_jobs=True,full_goal_active=True,full_goal_complete=False,main_V4701_preserved=True,broader207_name_review_all_storylines_shared_town_random_Help_prose_wraps_and_prior_leads_preserved=True,producer_sha256=sha(Path(__file__).read_bytes())));print('V6133 checkpoint verified:20 uncredited B204 native approvals;V6110 and all counts/history/full scope preserved.')
