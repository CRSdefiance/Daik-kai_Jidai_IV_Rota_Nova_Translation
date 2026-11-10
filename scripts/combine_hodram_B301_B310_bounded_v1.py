"""Join disjoint source-complete QA runs without conflating their frame timelines."""
from pathlib import Path
from copy import deepcopy
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B301_B310_clean_20261107')
OUT=ROOT/'bounded_combined_v1'
FIXTURE=OUT/'fixture_set.json';LIVE=OUT/'focused_actual_pixels.json';MENU=OUT/'menu_actual_pixels.json'

def main():
    assert not OUT.exists()
    created=load(ROOT/'focused_fixtures_bounded_v1/fixtures.json')['fixtures'];assert len(created)==2
    master=load(ROOT/'focused_fixtures_v1/hodram_desert_temple_wolf_and_offer_fixture.json')
    native=load(ROOT/'storage_inputs_v6/native_pages.json')
    byid={r['id']:r for r in native['records']};fixtures=[];actual=[];menus=[];evidence={};transitions=[]
    def bind(path):
        path=Path(path);h=digest(path)
        assert str(path) not in evidence or evidence[str(path)]==h
        evidence[str(path)]=h
    for index,entry in enumerate(created,1):
        fpath=Path(entry['fixture']);f=load(fpath);assert digest(fpath)==entry['fixture_sha256']
        apath=ROOT/f'bounded_pixels_{index}_v1/focused_actual_pixels.json'
        mpath=ROOT/f'bounded_menus_{index}_v1/menu_actual_pixels.json'
        tpath=ROOT/f'bounded_run_{index}_v1/terminal.json'
        console=ROOT/f'bounded_run_{index}_console_v1.log'
        a,m,t=map(load,[apath,mpath,tpath]);text=console.read_text(encoding='utf-8-sig')
        assert 'Undefined instruction' not in text and 'Saved cold-boot frame evidence:' in text
        assert (a['frames'],a['selected_utterances'],a['selected_pages'])==(f['frames'],len(f['selected_records']),f['expected_pages'])
        assert a['all_selected_pages_observed_in_exact_fixture_order'] and a['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert a['evidence'][str(fpath)]==digest(fpath) and a['evidence'][str(tpath)]==digest(tpath)
        assert m['fixture_sha256']==digest(fpath) and m['terminal_sha256']==digest(tpath)
        assert m['ordered_body_receipt_sha256']==digest(apath)
        assert m['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert m['byte_identical_menu_occurrences_bound_by_exact_source_keys_andordered_surrounding_calls']
        assert f['QA_block_inside_original_stack_buffer'] and f['padded_QA_block_bytes']<=f['source_bound_QA_block_limit']==9216
        assert f['original_initializers']==master['original_initializers']
        assert f['clean_andregistered_host_exit_commands_identical'] and f['source_bound_QA_host_exit_hex']=='00c200000000'
        assert a['following_nonfixture_modal_frame']<a['frames']
        observer=Path(t['observer']);assert digest(observer)==t['observer_sha256']
        obs=load(observer);assert not obs['errors'] and not obs['mismatches'] and obs['all_host_slots_restored_and_core_file_exact']
        following=[r for r in obs['rows'] if r['kind']=='modal_paint' and r['frame']>=a['following_nonfixture_modal_frame']]
        assert following and 'supplies' in following[-1]['text_CP932']
        report=load(t['report']);assert digest(t['report'])==t['report_sha256']
        final=report['frames_captured'][-1];assert final['frame']==f['frames'] and digest(final['path'])==final['PNG_sha256']
        transitions.append(dict(fixture_index=index,fixture=str(fpath),frames=f['frames'],following_native_dialogue=following[-1],final_capture=final,
            console=str(console),console_sha256=digest(console),no_undefined_instruction_in_native_output=True))
        fixtures.append(f);actual.append(a);menus.append(m)
        for p in [fpath,apath,mpath,tpath,console,observer,Path(t['report'])]:bind(p)
        for p,h in a['evidence'].items():
            assert digest(p)==h
            bind(p)
    def no_offset(r):return {k:v for k,v in r.items() if k!='fixture_offset'}
    for key in ['selected_records','copied_commands','menus']:
        assert [no_offset(r) for f in fixtures for r in f[key]]==[no_offset(r) for r in master[key]]
    selected=[{**r,'fixture_index':i,'fixture':created[i-1]['fixture']} for i,f in enumerate(fixtures,1) for r in f['selected_records']]
    assert len(selected)==96 and len({r['id'] for r in selected})==96
    pages=[]
    for row in selected:
        r=byid[row['id']];display=r['complete_native_English_display']
        count=1 if r['kind']=='system-FE' else len(display['pages'])
        pages.extend((row['id'],p) for p in range(1,count+1))
    ordered=[{**r,'fixture_index':i,'fixture':created[i-1]['fixture']} for i,a in enumerate(actual,1) for r in a['ordered_selected_source_calls']]
    assert [(r['id'],r['page']) for r in ordered]==pages and len(pages)==97
    header_expectations={}
    for f in fixtures:
        for k,v in f['expected_header_actor_ID_by_selector'].items():
            assert k not in header_expectations or header_expectations[k]==v
            header_expectations[k]=v
    assert len(header_expectations)==14
    total_frames=sum(f['frames'] for f in fixtures);assert total_frames==34162
    OUT.mkdir()
    save(FIXTURE,dict(format='dk4-disclosed-native-dialogue-fixture-set-v1',fixtures=created,frames=total_frames,initialized_runs=2,
        selected_records=selected,expected_pages=97,expected_header_actor_ID_by_selector=header_expectations,
        source_selectors_with_header=sorted(map(int,header_expectations)),frame_numbers_are_run_local=True,
        complete_original_scene_including_transitions_andbranches_retained=False,
        no_original_conditional_menu_outcome_orstat_claim=True,all100_source_command_copies_and96_bindings_exact=True,
        all_QA_blocks_inside_original_stack_buffer=True,native_capacity_proof=str(ROOT/'native_QA_capacity_v1.json'),new_credit=0))
    bind(FIXTURE)
    live=deepcopy(actual[0]);live.pop('following_nonfixture_modal_frame')
    live.update(frames=total_frames,initialized_fixture_runs=2,selected_utterances=96,selected_pages=97,
        complete_body_planes=sum(a['complete_body_planes'] for a in actual),complete_header_planes=sum(a['complete_header_planes'] for a in actual),
        body_pages=[{**r,'fixture_index':i,'fixture':created[i-1]['fixture']} for i,a in enumerate(actual,1) for r in a['body_pages']],
        headers=[{**r,'fixture_index':i} for i,a in enumerate(actual,1) for r in a['headers']],
        ordered_selected_source_calls=ordered,observed_source_selectors=sorted(map(int,header_expectations)),
        review_sheets=[s for a in actual for s in a['review_sheets']],unvisited_utterances=129,
        fixture_set=str(FIXTURE),fixture_set_sha256=digest(FIXTURE),frame_numbers_are_run_local=True,
        source_order_preserved_across_independent_initialized_fixtures=True,following_native_dialogue_per_run=transitions,
        direct_visual_review_pending=True,evidence=evidence)
    assert live['complete_body_planes']==210 and live['complete_header_planes']==194 and len(live['review_sheets'])==17
    save(LIVE,live)
    # The combined sheet contains the unchanged complete per-run menu crops.
    images=[]
    for m in menus:
        s=m['review_sheet'];assert digest(s['path'])==s['sha256']
        images.append(Image.open(s['path']).convert('RGB'))
    width=max(im.width for im in images);height=sum(im.height for im in images)
    sheet=Image.new('RGB',(width,height),'#eee');y=0
    for im in images:sheet.paste(im,(0,y));y+=im.height
    png=OUT/'menus_QA.png';sheet.save(png)
    menu=deepcopy(menus[0])
    for key in ['fixture','fixture_sha256','terminal','terminal_sha256']:menu.pop(key)
    menu.update(fixture_set=str(FIXTURE),fixture_set_sha256=digest(FIXTURE),frames=total_frames,initialized_fixture_runs=2,
        menus=[{**r,'fixture_index':i,'fixture':created[i-1]['fixture']} for i,m in enumerate(menus,1) for r in m['menus']],
        menu_samples=[{**r,'fixture_index':i} for i,m in enumerate(menus,1) for r in m['menu_samples']],
        complete_live_caption_samples=sum(m['complete_live_caption_samples'] for m in menus),
        ordered_body_receipt=str(LIVE),ordered_body_receipt_sha256=digest(LIVE),
        review_sheet=dict(path=str(png),sha256=digest(png)),per_fixture_review_sheets=[m['review_sheet'] for m in menus],
        frame_numbers_are_run_local=True,evidence=evidence)
    assert {(m['block'],m['source_command_offset'],tuple(m['observed_selected_options'])) for m in menu['menus']}=={(302,1226,(0,)),(302,2272,(0,)),(304,576,(0,)),(309,738,(0,))}
    save(MENU,menu)
    save(OUT/'bounded_return_checks.json',dict(qualified_runs=2,qualified_frames=34162,utterances=96,pages=97,menus=4,
        complete_body_planes=210,complete_header_planes=194,all100_source_command_copies_exact=True,
        following_native_dialogue_per_run=transitions,all_native_output_logs_free_of_undefined_instructions=True,
        actual_dialogue_andmenu_visual_review_pending=True,new_credit=0,
        evidence={**evidence,**{str(p):digest(p) for p in [LIVE,MENU,Path(__file__),ROOT/'native_QA_capacity_v1.json',ROOT/'capacity_guard_rejection_v2.json']}}))
    print('Joined two bounded runs/34,162 frames:96 utterances97 pages4 menus,210 exact bodies194 headers, both following-dialogue returns pass. Visual approval pending.')

if __name__=='__main__':main()
