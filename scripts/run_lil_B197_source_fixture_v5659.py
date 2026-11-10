"""Cold boot complete book-source fixtures; select menus through ordinary gamepad input."""
import argparse,inspect
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=['clean_Japanese'],required=True)
    p.add_argument('--path',choices=['buy','no_buy','delegate'],required=True);args=p.parse_args()
    fp=Path('work/analysis/lil_B197_source_fixture_v5658/complete_B197_source_B22_fixture.json');fixture=read(fp)
    selected=next(r for r in fixture['fixtures'] if r['case']==args.case)
    source=Path('scripts/run_lil_opening_trace_v1706.py');text=source.read_text(encoding='utf-8')
    root=f'work/analysis/lil_B197_source_run_v5659_{args.path}_{args.case}'
    cap=f'E:/Rota Nova translations/Generated/work/emulation_v193/lil_B197_source_v5659_{args.path}_{args.case}'
    mapping={r['fixture_offset']:r['source_offset'] for r in selected['selected_original_objects'] if r['source_word']==0x2200}
    choices={at:['buy','no_buy','delegate'].index(args.path) for at in mapping}
    def install_controller(harness,observers,folder):
        old=harness.main;events=[];seen=set()
        def ordinary_input(frontend,frame,buttons):
            for observer in observers:
                pending=[observer.rows[i] for i in observer.pending.values()]
                for row in pending:
                    s=row['source']
                    if s.get('block')!=22 or s.get('first_word')!=0x2200:continue
                    at=s['instruction_offset'];assert at in choices
                    age=frame-row['frame'];option=choices[at]
                    frontend.pressed.discard(buttons['A']);frontend.pressed.discard(buttons['DOWN'])
                    names=[]
                    if option>=1 and 30<=age<35:names=['DOWN']
                    if option==2 and 60<=age<65:names=['DOWN']
                    if 120<=age<125:names=['A']
                    frontend.pressed.update(buttons[n] for n in names)
                    if names:events.append(dict(frame=frame,buttons=names,fixture_menu_offset=at,source_menu_offset=mapping[at],requested_option=option))
                    if at not in seen:
                        seen.add(at);save(folder/'live_menu_inputs.json',dict(path=args.path,seen_source_menus=sorted(mapping[a] for a in seen),events=events,ordinary_gamepad_only=True))
        body=inspect.getsource(old);needle='            core.retro_run()'
        assert body.count(needle)==1
        body=body.replace(needle,'            B197_ORDINARY_INPUT(frontend,frame,buttons)\n'+needle)
        compile(body,'<B197-ordinary-gamepad-main>','exec')
        (folder/'frontend_main_with_ordinary_menu_input.py').write_text(body,encoding='utf-8')
        env={**harness.__dict__,'B197_ORDINARY_INPUT':ordinary_input};exec(compile(body,'<B197-ordinary-gamepad-main>','exec'),env)
        harness.main=env['main']
        return old,events
    changes=[
        ('from scripts import observe_script_sources_v733 as original','from scripts import observe_lil_B180_v4810 as original'),
        ('from scripts.prepare_lil_opening_research_v1704 import ROM',"ROM=Path(SELECTED['research_ROM'])"),
        ("ROOT=Path('work/analysis/lil_opening_trace_v1706')",'ROOT=Path('+repr(root)+')'),
        ("CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')",'CAP=Path('+repr(cap)+')'),
        ("receipt=read('work/analysis/lil_opening_research_v1704/research_image_receipt.json')",'receipt=SELECTED'),
        ("inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json')","base_inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json');inputs=ROOT/'inputs.json'"),
        ("assert sha(inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'","assert sha(base_inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'"),
        ("ROOT.mkdir(parents=True);(ROOT/'source_contract.json')","ROOT.mkdir(parents=True);save(inputs,read(base_inputs)+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,12501,240)]);(ROOT/'source_contract.json')"),
        ('no_save_savestate_or_gameplay_fixtures','no_save_or_savestate_or_RAM_fixtures'),
        ("'only_ROM_ROOT_globals_rebound_for_current_source':True","'only_observer_ROM_ROOT_globals_rebound':True,'explicit_B22_entry_ROM_fixture':True,'source_event197_not_selected':True,'displayed_original_source_block':197,'all_source39_commands_retained':True,'requested_book_path':REQUESTED_PATH,'frontend_ordinary_menu_controller':True,'fixture_manifest':str(FIXTUREPATH),'fixture_manifest_sha256':sha(FIXTUREPATH.read_bytes())"),
        ("'--frames','100000'","'--frames','13001'"),
        ("'--capture-at','4000','6000','--pause-at','6000'","'--capture-at',*map(str,range(2350,13001,60))"),
        ("'--dump-capture-ram','--dump-pause-ram','--dump-ram'","'--dump-ram'"),
        ('no_gameplay_fixture_save_or_ROM_runtime_edit','no_savestate_or_emulated_RAM_runtime_fixture'),
        ('    try:harness.main()',"    old_main,ordinary_events=INSTALL_CONTROLLER(harness,observers,ROOT)\n    try:harness.main()"),
        ('        sys.stdin=old_stdin;harness.ct=old_ct;stream.close()',"        harness.main=old_main\n        save(ROOT/'ordinary_menu_inputs.json',dict(events=ordinary_events,ordinary_gamepad_only=True,no_game_RAM_or_predicate_or_seed_write=True))\n        sys.stdin=old_stdin;harness.ct=old_ct;stream.close()")]
    for a,b in changes:assert a in text,a;text=text.replace(a,b)
    exec(compile(text,str(source)+'::B197-complete-choice-fixture','exec'),dict(__name__='__main__',__file__=__file__,SELECTED=selected,FIXTUREPATH=fp,REQUESTED_PATH=args.path,INSTALL_CONTROLLER=install_controller))
