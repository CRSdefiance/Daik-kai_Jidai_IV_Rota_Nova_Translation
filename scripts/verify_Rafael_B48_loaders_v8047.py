"""Run every native load/cache path andboth parent modes in the resized Rafael SC0 archive."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.create_Rafael_B48_reference_v8046 import ROM,PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_loaders_v8047')
RECEIPT=Path('work/analysis/Rafael_B48_reference_v8046/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read(RECEIPT);assert sha(ROM.read_bytes())==receipt['research_ROM_sha256'] and sha(PARENT.read_bytes())==receipt['parent_sha256']
    image=NdsImage.open(ROM);counts={r:len(IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks) for r in [0]};assert counts=={0:343}
    expected=0
    for route in [0]:
        ev=image.read_file(f'/data/EV{route}.DK4');begin,end=struct.unpack_from('<2I',ev,0x4C);assert (end-begin)%2==0;expected+=(end-begin)//2
    a=checked_text(inspect.getsource(loader.run),{'for route in range(4):':'for route in (0,):','assert all_actions == 1312 and loaded == 1307':'assert all_actions == EXPECTED_ACTIONS and loaded == 343'})
    b=checked_text(inspect.getsource(parent.run),{'for route in range(4):':'for route in (0,):','assert len(cases) == 2614':'assert len(cases) == 686'})
    env={**loader.__dict__,'EXPECTED_ACTIONS':expected};exec(compile(a,__file__+'::one-resized-original-loader','exec'),env);load=env['run']
    env=dict(parent.__dict__);exec(compile(b,__file__+'::original-two-parent-modes','exec'),env);handoff=env['run']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=image.read_file('/__arm9__.bin')
    for start,end in [(0x23E94,0x23F84),(0x23F4C,0x24134),(0x24134,0x24230),(0x2A510,0x2A530)]:assert arm[start:end]==clean[start:end]
    ROOT.mkdir(parents=True);loaded=load(image,'research');lp=ROOT/'whole_SC0_native_loads.json';save(lp,loaded)
    modes=handoff(image,'research',loaded);mp=ROOT/'whole_SC0_native_parent_modes.json';save(mp,modes)
    save(ROOT/'343_whole_native_loads_cache_hits686_initial_parent_modes.json',dict(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=receipt['parent_sha256'],archive_block_counts=counts,original_action_count=expected,fresh_native_whole_loads_andcache_hits=343,fresh_initial_parent_modes=686,load_proof=str(lp),load_sha256=sha(lp.read_bytes()),parent_mode_proof=str(mp),parent_mode_sha256=sha(mp.read_bytes()),exact_B48_header_andall_mapped_targets_fit_original_0x2400_cache=True,all_original_EV0_actions_select_block_indices_not_interior_offsets=True,both_original_parent_modes_begin_payload_plus8=True,all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact=True,original_executed_instructions_exact_only_SDK_IO_bridges=True,source_owned_loader_adapter=a,source_owned_parent_adapter=b,controlled_native_route_global_inputs_not_ordinary_event_activation=True,caller_census_relocated_controls_actual_andregistered_release_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [RECEIPT,Path(loader.__file__),Path(parent.__file__),Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('Resized SC0:343 complete native loads/cache hits and686 original initial parent modes pass. No source eligibility,optional activation oractual UI claim.')
