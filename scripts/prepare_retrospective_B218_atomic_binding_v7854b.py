"""Strengthen trace/panel consistency before challenges;preserve the first positive producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
TRACE='''        require(sha(Path(fixtures[case]['research_ROM']).read_bytes())==group['research_ROM_sha256'],'actual fixture bytes')
        fixture_image=NdsImage.open(fixtures[case]['research_ROM'])
        fixture_blocks=IlnkContainer.parse(fixture_image.read_file(PATHS[0])).blocks
        fixture_hashes={n:sha(v) for n,v in enumerate(fixture_blocks)}
        trace_pairs=[]
        for tr in trace['rows']:
            location=tr['source']
            require(tr['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] and location['classification']=='original_SC_cache'
                and location['route']==2 and location['whole_resident_payload_exact_ROM']
                and location['actual_sha256']==fixture_hashes[location['block']],'original resident trace source')
            if tr['kind']!='after_command' or location['block']!=22:continue
            entry=trace['rows'][tr['entry_row']]
            trace_pairs.append(dict(fixture_offset=entry['source']['instruction_offset'],word=entry['source']['first_word'],
                start=entry['frame'],returned=tr['frame'],duration=tr['frame']-entry['frame'],
                native_result=tr['result_words'],decoded_length=tr['decoded_length'],
                before_RNG=entry['original_RNG_seed'],after_RNG=tr['original_RNG_seed'],UI_after=tr['native_UI_request_words']))
        require(trace_pairs==group['command_pairs'],'actual measurements equal original trace')
        for measured,command in zip(group['command_pairs'],fixtures[case]['all24_stored_fixture_commands'],strict=True):'''
PANELS='''        text_refs={r['id']:r for r in fixtures[case]['original_text_records']}
        captures={r['frame']:r for r in report['frames_captured']}
        historical_planes={r['id']:r['complete_pages']['pages'][0] for r in p['original_stored']['records']}
        for panel in group['panels']:
            ident=panel['id'];fixture_text=text_refs[ident]
            interval=next(r for r in group['command_pairs'] if r['fixture_offset']==fixture_text['fixture_command_offset'])
            require(panel['interval']==interval and panel['source_selector']==fixture_text['source_selector'],'actual interval/source association')
            expected_plane=stored['changed_stored_pages']['pages'][0] if case=='proposed_English' and ident==TARGET else historical_planes[ident]
            require(panel['native_stored_plane']==expected_plane['native_plane']
                and panel['native_stored_plane_sha256']==expected_plane['native_plane_sha256']
                and checked_plane(expected_plane)==Path(panel['native_stored_plane']).read_bytes(),'actual final stored plane association')
            holds=panel['complete_body_andheader_holds']
            require(all(interval['start']+20<h['frame']<interval['returned']-4
                and h['capture']==captures[h['frame']]['path'] and h['sha256']==captures[h['frame']]['PNG_sha256'] for h in holds),'actual complete hold/report association')'''
COMPARE='''    for c,previous,proposed in zip(actual['command_comparisons'],groups['previous_English']['command_pairs'],groups['proposed_English']['command_pairs'],strict=True):
        require(c['previous']==previous and c['proposed']==proposed
            and c['differing_fields']==[k for k in previous if previous[k]!=proposed[k]],'complete command comparison association')
    require(sum(c['previous']['duration']!=c['proposed']['duration'] for c in actual['command_comparisons'])==actual['duration_difference_rows']
        and sum(bool(c['differing_fields']) for c in actual['command_comparisons'])==actual['command_difference_rows'],'computed timing/offset counts')
    require(all(c['previous']['native_result']==c['proposed']['native_result'] and c['previous']['UI_after']==c['proposed']['UI_after']
        for c in actual['command_comparisons']),'measured original result/UI equality')
    panels={r['id']:r for r in groups['proposed_English']['panels']}'''
if __name__=='__main__':
    root=Path('work/analysis/retrospective_B218_atomic_binding_v7854b');assert not root.exists()
    changes={
        "        for measured,command in zip(group['command_pairs'],fixtures[case]['all24_stored_fixture_commands'],strict=True):":TRACE,
        "        for panel in group['panels']:\n            holds=panel['complete_body_andheader_holds']":PANELS,
        "    panels={r['id']:r for r in groups['proposed_English']['panels']}":COMPARE,
    }
    checked_text(Path('dk4tool/patch/lil_B218_retrospective_v1.py').read_text(encoding='utf-8'),changes)
    producer_changes={
        'lil_B218_retrospective_v1':'lil_B218_retrospective_v2',
        'work/analysis/retrospective_B218_atomic_v7854':'work/analysis/retrospective_B218_atomic_v7854b',
    }
    checked_text(Path('scripts/validate_retrospective_B218_atomic_v7854.py').read_text(encoding='utf-8'),producer_changes)
    module=derive('dk4tool/patch/lil_B218_retrospective_v1.py','dk4tool/patch/lil_B218_retrospective_v2.py',changes)
    producer=derive('scripts/validate_retrospective_B218_atomic_v7854.py','scripts/validate_retrospective_B218_atomic_v7854b.py',producer_changes)
    root.mkdir(parents=True);save(root/'provenance.json',dict(module=module,producer=producer,
        all_original_native_high_constants_andone_final_commit_guards_preserved=True,
        exact_trace_panel_interval_report_plane_andcomparison_associations_added=True,
        prior_module_positive_producer_andproof_preserved=True,full_goal_complete=False))
