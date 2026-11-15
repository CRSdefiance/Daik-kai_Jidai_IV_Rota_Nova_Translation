"""Combine the fresh corrected exchange with exact unchanged gameplay evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'gameplay_review_v1.json';assert not out.exists()
    priorpath=ROOT/'initial_gameplay_review_v1.json';prior=load(priorpath)
    newpath=ROOT/'reconstruction_v3/reconstruction.json';new=load(newpath)
    oldpath=ROOT/'reconstruction_v2/reconstruction.json';old=load(oldpath)
    native=load(new['native']);oldnative=load(old['native'])
    byid={r['id']:r for r in native['records']};oldbyid={r['id']:r for r in oldnative['records']}
    terminalpath=ROOT/'wine_display_run_v1/terminal.json';terminal=load(terminalpath)
    pixelpath=ROOT/'wine_display_pixels_v1/focused_actual_pixels.json';pixel=load(pixelpath)
    runpath=ROOT/'wine_display_run_v1/run_plan.json';run=load(runpath)
    transitionpath=ROOT/'wine_transition_review_v1/receipt.json';transition=load(transitionpath)
    assert terminal['terminal'] and terminal['frames']==pixel['frames']==10721
    assert (pixel['selected_utterances'],pixel['selected_pages'],pixel['complete_body_planes'],pixel['complete_header_planes'])==(3,3,6,6)
    assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
    report,observer=map(load,[terminal['report'],terminal['observer']])
    assert digest(terminal['report'])==terminal['report_sha256'] and digest(terminal['observer'])==terminal['observer_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and verified_existing_unlock(report)
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    fixturepath=Path(run['fixture']);fixture=load(fixturepath)
    assert digest(fixturepath)==run['fixture_sha256'] and digest(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
    assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
    assert len(fixture['original_initializers'])==7 and len(fixture['source_bound_QA_host_opening_exit'])==40
    assert fixture['padded_QA_block_bytes']<=9216 and transition['source_complete_hosts_reach_resupply_departure_andfinal_sailing']
    assert len(transition['runs'])==1 and transition['runs'][0]['frames']==10721
    controls=load(fixture['inputs']);assert digest(fixture['inputs'])==fixture['inputs_sha256']
    calls=pixel['ordered_selected_source_calls'];ids=[f'DK4_MES_B152_R{i:04d}' for i in [5,8,12]]
    assert [c['id'] for c in calls]==ids and [c['page'] for c in calls]==[1,1,1]
    for left,right in zip(calls,calls[1:]):
        pushes=[c for c in controls if left['frame']<c['start']<right['frame'] and c['buttons']==['A']]
        assert len(pushes)==1 and pushes[0]['duration']==16
    assert byid[ids[1]]['logical_English']=='Got a problem with that?'
    assert byid[ids[0]]['logical_English']=="Hey, you're still drinking that stuff?"
    assert byid[ids[2]]['logical_English']=="Not at all. But wine's the thing now. Wine!"
    current=NdsImage.open(new['research_ROM']);previous=NdsImage.open(old['research_ROM'])
    assert digest(new['research_ROM'])==new['research_ROM_sha256'] and digest(old['research_ROM'])==old['research_ROM_sha256']
    for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert current.read_file(p)==previous.read_file(p)
    assert native['runtime']==oldnative['runtime'] and native['font_sha256']==oldnative['font_sha256']
    texts={r['id']:(g,r) for g in new['groups'] for r in g['text_records']}
    candidates={};oldfixtures={};evidence=[priorpath,newpath,oldpath,Path(new['native']),Path(old['native']),terminalpath,pixelpath,runpath,
        transitionpath,fixturepath,Path(terminal['report']),Path(terminal['observer']),Path(fixture['inputs']),Path(__file__)]
    for index in range(3):
        path=ROOT/f'display_pixels_menu{index}_v1/focused_actual_pixels.json';body=load(path)
        fixtureplan=load(ROOT/f'display_run_menu{index}_v1/run_plan.json');f=load(fixtureplan['fixture'])
        assert digest(fixtureplan['fixture'])==fixtureplan['fixture_sha256']
        for sample in body['body_pages']:candidates.setdefault(sample['id'],[]).append((sample,f))
        evidence.append(path)
    reused=[];selected=[]
    for ident in prior['observed_body_IDs']:
        if ident in ids:continue
        assert byid[ident]['compiled_hex']==oldbyid[ident]['compiled_hex'] and byid[ident]['expanded_native_hex']==oldbyid[ident]['expanded_native_hex']
        sample,f=candidates[ident][0];group,text=texts[ident]
        bound=next(r for r in f['selected_records'] if r['id']==ident)
        copied=next(c for c in f['copied_commands'] if c['fixture_offset']==bound['fixture_offset'])
        command=next(c for c in group['all_target_commands'] if c['offset']==text['new_offset']-5)
        assert copied['whole_command_hex']==command['whole_command_hex']
        display=byid[ident]['complete_native_English_display'];plane=display if byid[ident]['kind']=='system-FE' else display['pages'][0]
        assert sample['native_plane_sha256']==plane['native_plane_sha256']==digest(plane['native_plane'])
        assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
        reused.append(dict(id=ident,compiled_hex=byid[ident]['compiled_hex'],stored_command_hex=command['whole_command_hex'],
            source_reference=byid[ident]['source_reference'],current_reference=byid[ident]['current_reference'],
            native_plane_sha256=plane['native_plane_sha256'],capture=sample['capture'],
            entire_command_runtime_font_macro_andnative_plane_dependencies_exact=True))
        selected.append(dict(id=ident,page=1,source='exact-compatible-initial-gameplay',capture=sample['capture'],native_plane_sha256=plane['native_plane_sha256']))
    assert len(reused)==80
    fresh=[]
    for ident in ids:
        sample=next(p for p in pixel['body_pages'] if p['id']==ident)
        plane=byid[ident]['complete_native_English_display']['pages'][0]
        assert digest(sample['native_plane'])==sample['native_plane_sha256']==plane['native_plane_sha256']
        assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
        fresh.append(dict(id=ident,capture=sample['capture'],native_plane_sha256=plane['native_plane_sha256']))
        selected.append(dict(id=ident,page=1,source='fresh-corrected-whole-exchange',capture=sample['capture'],native_plane_sha256=plane['native_plane_sha256']))
    assert {r['id'] for r in selected}==set(prior['observed_body_IDs']) and len(selected)==83
    for p,h in prior['evidence'].items():assert digest(p)==h
    sheets=prior['review_sheets']+pixel['review_sheets']+[transition['runs'][0]['review_sheet']]
    assert len(sheets)==24
    for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
    final=deepcopy(prior)
    final.update(frames=63284,initialized_runs=4,
        runs=prior['runs']+[dict(choice='corrected-wine-context',frames=10721,physical_body_candidates=3,pages=3,run_plan=str(runpath))],
        current_final_reconstruction=str(newpath),current_final_reconstruction_sha256=digest(newpath),
        selected_current_pages=selected,exact_compatible_actual_body_reuses=reused,fresh_corrected_context_pages=fresh,
        distinct_source_body_objects=83,distinct_body_pages=83,selected_current_body_pages=83,
        complete_body_planes=184,complete_header_planes=128,
        historical_executed_plane_counts_include_superseded_old_reply=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        corrected_wine_question_andanswer_with_both16_frame_A_transitions_observed=True,
        all83_current_pages_five_captions_andfour_host_transitions_directly_viewed=True,
        current_final_reply_verified=True,changed_current_reply_not_approved_by_old_actual_page=False,
        current_prose_orall_fifth_gates_not_approved_here=True,full_current_batch_gameplay_approval=True,
        fresh_wine_context_source_whole_exchange='B152R5/R8/R12',
        body_plane_reuse_is_record_specific_not_whole_ROM_equivalence=True,
        name_headers=sorted(prior['name_headers']+[
            h for h in pixel['headers'] if (h['source_selector'],h['expected_actor_ID'],h['text']) not in
                {(v['source_selector'],v['expected_actor_ID'],v['text']) for v in prior['name_headers']}],key=lambda h:(h['source_selector'],h['expected_actor_ID'],h['text'])),
        review_sheets=[dict(s,directly_viewed=True) for s in sheets],registered_integration_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in evidence})
    save(out,final)
    print('Current gameplay complete:80 exact body reuses+3 fresh contextual pages;83 unique bodies,5 captions andfour ordinary sailing returns.')


if __name__=='__main__':main()
