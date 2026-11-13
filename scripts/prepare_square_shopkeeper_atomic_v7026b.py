"""Keep the positive v1 compiler; add individual actual-page/source-reference guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/square_shopkeeper_atomic_tools_v7026b')
if __name__=='__main__':
    assert not ROOT.exists()
    anchor="    for scene in ['static','staged']:\n"
    extra='''    fixtures=load(actual['fixtures']);bycase={f['case']:f for f in fixtures['fixtures']};target_last_pages=[]
    for version in actual['versions']:
        fixture=bycase[version['case']];records={r['id']:r for r in fixture['original_text_records']}
        expected_names={r['actor_ID']:r['text'] for v in names['versions'] if v['case']==version['version'] for r in v['name_getters']['rows'] if r['consumer']=='progressive-nameplate'}
        require(len(version['panels'])==(17 if version['scene']=='static' else 13),'complete individual speeches')
        require(len({p['id'] for p in version['panels']})==len(version['panels']),'unique actual speech references')
        for panel in version['panels']:
            record=records[panel['id']];require(panel['actor_ID']==record['source_selector'],'actual source selector')
            pair=next(p for p in version['command_pairs'] if p['offset']==record['fixture_command_offset'])
            require(pair['word']==0x4000 and (pair['start'],pair['returned'])==(panel['start'],panel['returned']),'complete speech interval')
            require(len(panel['complete_page_holds'])==panel['native_pages'] and all(panel['complete_page_holds']),'every actual native page')
            require(panel['name']==(None if panel['actor_ID']==254 else expected_names[panel['actor_ID']]),'actual native name binding')
            require(bool(panel['complete_name_holds'])==(panel['name'] is not None),'every actual named header')
            if version['version']=='target':
                for number,holds in enumerate(panel['complete_page_holds'],1):target_last_pages.append((panel['id'],number,holds[-1]['capture'],holds[-1]['sha256']))
        require(sum(p['native_pages'] for p in version['panels'])==version['actual_complete_page_observations']==(17 if version['scene']=='static' else 15),'actual page count')
        require(sum(sum(map(len,p['complete_page_holds'])) for p in version['panels'])==version['actual_complete_body_holds'],'individual body holds')
        require(sum(len(p['complete_name_holds']) for p in version['panels'])==version['actual_complete_name_holds'],'individual name holds')
    require(sum(p['actor_ID'] in [82,85] for v in actual['versions'] if v['version']=='target' for p in v['panels'])==9,'nine changed nameplate observations')
    require(len(view['all32_whole_frame_panes_pixel_equal'])==32 and all(p['whole_pane_pixel_equal'] for p in view['all32_whole_frame_panes_pixel_equal']),'complete viewed panes')
    require(sorted(target_last_pages)==sorted((p['id'],p['page'],p['capture'],p['sha256']) for p in view['all32_whole_frame_panes_pixel_equal']),'viewed exact actual pages')
'''
    end="        require(a['command_pairs'][-1]['result']==b['command_pairs'][-1]['result']==[0,0],'original normal returns')\n"
    measured='''        measured=next(c for c in actual['comparisons'] if c['scene']==scene);computed=[]
        for x,y in zip(a['command_pairs'],b['command_pairs'],strict=True):
            fields=[k for k in x if x[k]!=y[k]]
            if fields:computed.append(dict(offset=x['offset'],word=x['word'],different_fields=fields,before=x,after=y))
        require(measured['command_differences']==computed and measured['normal_exit_frames']==[a['exit_frame'],b['exit_frame']],'all measured command/RNG/timing differences retained')
        require(measured['no_full_RAM_final_components_future_or_complete_causal_equivalence_claim'],'later-world scope')
    require([sum(not d['all_differences_within_nameplate_strip'] for d in c['RGB_differences']) for c in actual['comparisons']]==[82,0],'all outside-nameplate RGB differences retained')
'''
    rows=[derive('dk4tool/patch/square_shopkeeper_label_release_v1.py','dk4tool/patch/square_shopkeeper_label_release_v2.py',{
        "CONFIG='translations/square_shopkeeper_label_release_v1.json'":"CONFIG='translations/square_shopkeeper_label_release_v2.json'",
        'dk4-ten-square-shopkeeper-label-release-v1':'dk4-ten-square-shopkeeper-label-release-v2',anchor:extra+anchor,end:end+measured})]
    rows.append(derive('scripts/validate_square_shopkeeper_atomic_v7026.py','scripts/validate_square_shopkeeper_atomic_v7026b.py',{
        'square_shopkeeper_label_release_v1':'square_shopkeeper_label_release_v2','atomic_v7026':'atomic_v7026b'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_compiler_successor.json',dict(tools=rows,
        v1_positive_one_write_proof_preserved=True,no_native_address_runtime_format_data_span_or_wording_change=True,
        additional_individual_source_intervals_pages_captions_view_references_and_measured_difference_guards=True,new_review_credit=0,full_goal_complete=False))
