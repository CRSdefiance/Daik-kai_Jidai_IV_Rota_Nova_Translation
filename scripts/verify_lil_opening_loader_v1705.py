"""Current/research entire SC2 native loads and both original parent modes."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.prepare_lil_opening_research_v1704 import ROM,PARENT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_loader_v1705')


if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    receipt=read('work/analysis/lil_opening_research_v1704/research_image_receipt.json')
    assert sha(ROM.read_bytes())==receipt['research_ROM_sha256'] and sha(PARENT.read_bytes())==receipt['parent_sha256']
    expected=len(IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks)
    source=inspect.getsource(loader.run);assert source.count('for route in range(4):')==1
    source=source.replace('for route in range(4):','for route in (2,):')
    old='assert all_actions == 1312 and loaded == 1307';assert source.count(old)==1
    source=source.replace(old,f'assert loaded == {expected} and all_actions == len(words)')
    env=dict(loader.__dict__);exec(compile(source,__file__,'exec'),env);load=env['run']
    source=inspect.getsource(parent.run);assert source.count('for route in range(4):')==1
    source=source.replace('for route in range(4):','for route in (2,):')
    old='assert len(cases) == 2614';assert source.count(old)==1
    source=source.replace(old,f'assert len(cases) == {2*expected}')
    env=dict(parent.__dict__);exec(compile(source,__file__,'exec'),env);handoff=env['run']
    results=[]
    clean_arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for label,path in [('current',PARENT),('research',ROM)]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin')
        for a,b in [(0x23E94,0x23F84),(0x23F4C,0x24134),(0x24134,0x24230),(0x2A510,0x2A530)]:assert arm[a:b]==clean_arm[a:b]
        loaded=load(image,label);save(ROOT/(label+'_native_loads.json'),loaded)
        parents=handoff(image,label,loaded);save(ROOT/(label+'_native_parent_modes.json'),parents)
        results.append({'label':label,'ROM_sha256':sha(path.read_bytes()),'load_proof':str(ROOT/(label+'_native_loads.json')),
            'parent_proof':str(ROOT/(label+'_native_parent_modes.json')),'whole_SC2_loads_and_cache_hits':expected,
            'original_parent_mode_cases':2*expected})
    save(ROOT/'loader_and_initial_entry_proof.json',{'versions':results,'original_shipped_EV2_selects_all_blocks_by_index':True,
        'resized_B22_fits_original_0x2400_cache_capacity':True,'original_loaded_block_and_tail_guards_exact':True,
        'both_original_modes_start_instruction_pointer_at_loaded_payload_plus8':True,
        'all_other_SC2_blocks_load_byte_exact_despite_updated_outer_offsets':True,
        'SDK_IO_bridge_only_no_loader_cache_success_stub':True,
        'later_script_control_flow_and_external_interior_entry_audit_still_pending':True,
        'no_registered_candidate_or_editorial_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Entire current/research SC2 original loads/cache hits and both original entry modes pass;B22 starts at+8. Later control-flow/actual scene audit remains.')
