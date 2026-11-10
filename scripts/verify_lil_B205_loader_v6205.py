"""Fresh whole-SC2 load/cache and two parent modes for V6160 and the resized reference."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prepare_lil_B205_references_v6200 import ROM,PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_loader_v6205')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read('work/analysis/lil_B205_research_v6203/research_image_receipt.json')
    assert sha(ROM.read_bytes())==receipt['research_ROM_sha256'] and sha(PARENT.read_bytes())==receipt['parent_sha256']
    count=len(IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks);assert count==336
    a=checked_text(inspect.getsource(loader.run),{'for route in range(4):':'for route in (2,):','assert all_actions == 1312 and loaded == 1307':'assert loaded == 336 and all_actions == len(words)'})
    b=checked_text(inspect.getsource(parent.run),{'for route in range(4):':'for route in (2,):','assert len(cases) == 2614':'assert len(cases) == 672'})
    env=dict(loader.__dict__);exec(compile(a,__file__+'::whole-SC2-loader','exec'),env);load=env['run']
    env=dict(parent.__dict__);exec(compile(b,__file__+'::two-parent-modes','exec'),env);handoff=env['run']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');ROOT.mkdir(parents=True);(ROOT/'scoped_loader_source.txt').write_text(a,encoding='utf-8');(ROOT/'scoped_parent_source.txt').write_text(b,encoding='utf-8');versions=[]
    for label,path in [('current',PARENT),('research',ROM)]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin')
        for start,end in [(0x23E94,0x23F84),(0x23F4C,0x24134),(0x24134,0x24230),(0x2A510,0x2A530)]:assert arm[start:end]==clean[start:end]
        loaded=load(image,label);lp=ROOT/(label+'_native_loads.json');save(lp,loaded)
        modes=handoff(image,label,loaded);mp=ROOT/(label+'_native_parent_modes.json');save(mp,modes)
        versions.append(dict(label=label,ROM_sha256=sha(path.read_bytes()),load_proof=str(lp),load_sha256=sha(lp.read_bytes()),parent_proof=str(mp),parent_sha256=sha(mp.read_bytes()),whole_SC2_loads_and_cache_hits=336,original_parent_modes=672))
    save(ROOT/'whole_SC2_and_B205_initial_entry_proof.json',dict(versions=versions,fresh_current_whole_SC2_loads=336,fresh_research_whole_SC2_loads=336,fresh_current_parent_modes=672,fresh_research_parent_modes=672,all336_whole_blocks_and672_modes_each_pass=True,B205_fits_original_0x2400_cache=True,original_EV2_actions_select_by_block_index_without_interior_byte_offset=True,original_parent_both_modes_start_at_loaded_payload_plus8=True,all_payload_cache_metadata_and_tail_guards_exact=True,SDK_IO_bridges_only_no_loader_or_cache_success_stub=True,later_control_flow_and_actual_revised_paths_reference_approval_pending=True,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Fresh V6160/reference:672 whole loads/cache hits and1344 original parent modes pass. No reuse of an old whole-ROM guard.')
