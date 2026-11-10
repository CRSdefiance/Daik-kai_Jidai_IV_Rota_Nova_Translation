"""Cold boot complete B215 Japanese content with ordinary input and read-only observation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read

if __name__=='__main__':
    fp=Path('work/analysis/lil_B215_source_fixture_v6748/complete_B215_source_B22_fixture.json')
    fixture=read(fp);selected=fixture['fixtures'][0]
    assert selected['case']=='clean_Japanese' and selected['source_block']==215
    source=Path('scripts/run_lil_opening_trace_v1706.py')
    changes={
        'from scripts import observe_script_sources_v733 as original':'from scripts import observe_lil_B180_v4810 as original',
        'from scripts.prepare_lil_opening_research_v1704 import ROM':"ROM=Path(SELECTED['research_ROM'])",
        "ROOT=Path('work/analysis/lil_opening_trace_v1706')":"ROOT=Path('work/analysis/lil_B215_source_run_v6749')",
        "CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')":"CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B215_source_v6749')",
        "receipt=read('work/analysis/lil_opening_research_v1704/research_image_receipt.json')":'receipt=SELECTED',
        "inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json')":"base_inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json');inputs=ROOT/'inputs.json'",
        "assert sha(inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'":"assert sha(base_inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'",
        "ROOT.mkdir(parents=True);(ROOT/'source_contract.json')":"ROOT.mkdir(parents=True);save(inputs,read(base_inputs)+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,15501,240)]);(ROOT/'source_contract.json')",
        'no_save_savestate_or_gameplay_fixtures':'no_save_or_savestate_or_RAM_fixtures',
        "'only_ROM_ROOT_globals_rebound_for_current_source':True":"'only_observer_ROM_ROOT_globals_rebound':True,'explicit_B22_entry_ROM_fixture':True,'source_event215_not_naturally_selected':True,'displayed_original_source_block':215,'all17_source_commands_retained':True,'fixture_manifest':str(FIXTUREPATH),'fixture_manifest_sha256':sha(FIXTUREPATH.read_bytes())",
        "'--frames','100000'":"'--frames','16001'",
        "'--capture-at','4000','6000','--pause-at','6000'":"'--capture-at',*map(str,range(2350,16001,60))",
        "'--dump-capture-ram','--dump-pause-ram','--dump-ram'":"'--dump-ram'",
        'no_gameplay_fixture_save_or_ROM_runtime_edit':'no_savestate_or_emulated_RAM_runtime_fixture',
    }
    text=checked_text(source.read_text(encoding='utf-8'),changes)
    exec(compile(text,str(source)+'::B215-complete-source-fixture','exec'),dict(
        __name__='__main__',__file__=__file__,SELECTED=selected,FIXTUREPATH=fp))
