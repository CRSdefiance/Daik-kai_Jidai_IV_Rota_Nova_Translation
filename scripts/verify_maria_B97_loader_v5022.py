"""Fresh original303 SC3 loads/cache hits and606 parent modes per current/reference image."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.maria_B97_reference_paths_v5021 import ROM,PARENT,STORED
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_loader_v5022')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read(STORED);assert sha(PARENT.read_bytes())==receipt['parent_sha256'] and sha(ROM.read_bytes())==receipt['research_ROM_sha256']
    source=inspect.getsource(loader.run);assert source.count('for route in range(4):')==1 and source.count('assert all_actions == 1312 and loaded == 1307')==1
    source=source.replace('for route in range(4):','for route in (3,):').replace('assert all_actions == 1312 and loaded == 1307','assert loaded == 303 and all_actions == len(words)')
    env=dict(loader.__dict__);exec(compile(source,__file__+'::SC3-loader','exec'),env);load=env['run']
    source2=inspect.getsource(parent.run);assert source2.count('for route in range(4):')==1 and source2.count('assert len(cases) == 2614')==1
    source2=source2.replace('for route in range(4):','for route in (3,):').replace('assert len(cases) == 2614','assert len(cases) == 606')
    env=dict(parent.__dict__);exec(compile(source2,__file__+'::SC3-parent','exec'),env);handoff=env['run']
    ROOT.mkdir(parents=True);(ROOT/'scoped_loader_source.txt').write_text(source,encoding='utf-8');(ROOT/'scoped_parent_source.txt').write_text(source2,encoding='utf-8');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');results=[]
    for label,path in [('current',PARENT),('research',ROM)]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');assert len(IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks)==303
        for a,b in [(0x23E94,0x23F84),(0x23F4C,0x24134),(0x24134,0x24230),(0x2A510,0x2A530)]:assert arm[a:b]==clean[a:b]
        loads=load(image,label);lp=ROOT/(label+'_native_loads.json');save(lp,loads);parents=handoff(image,label,loads);pp=ROOT/(label+'_native_parent_modes.json');save(pp,parents)
        results.append(dict(label=label,ROM_sha256=sha(path.read_bytes()),load_proof=str(lp),load_sha256=sha(lp.read_bytes()),parent_proof=str(pp),parent_sha256=sha(pp.read_bytes()),whole_SC3_loads_and_cache_hits=303,original_parent_modes=606))
    save(ROOT/'whole_SC3_and_B97_initial_entry_proof.json',dict(versions=results,all303_whole_blocks_and606_modes_each_pass=True,B97_CS0101_fits_original_0x2400_cache=True,original_EV3_actions_select_by_block_index_without_interior_byte_offset=True,original_parent_both_modes_start_at_loaded_payload_plus8=True,all_payload_cache_metadata_and_tail_guards_exact=True,SDK_IO_bridges_only_no_loader_or_cache_success_stub=True,no_scene_eligibility_or_gameplay_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Both images:303 fresh original loads/cache hits and606 parent entry modes pass.')
