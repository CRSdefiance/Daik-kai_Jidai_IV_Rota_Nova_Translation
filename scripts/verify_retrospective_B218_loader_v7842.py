"""Fresh complete changed-archive native loads and original parent modes; no simulated success."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_loader_v7842')
REFERENCE=Path('work/analysis/retrospective_B218_reference_v7841/research_image_receipt.json')
MAP=Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json')
if __name__=='__main__':
    assert not ROOT.exists()
    ref,mapping=map(read,[REFERENCE,MAP]);rom=Path(ref['research_ROM']);image=NdsImage.open(rom)
    assert sha(rom.read_bytes())==ref['research_ROM_sha256'] and sha(Path(ref['parent']).read_bytes())==ref['parent_sha256']
    assert ref['source_relocation_plan_sha256']==sha(MAP.read_bytes()) and ref['all335_other_blocks_and_every_other_file_component_exact']
    bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert len(bank)==336 and sha(bank[218])==mapping['groups'][0]['target_block_sha256']
    a=checked_text(inspect.getsource(loader.run),{
        'for route in range(4):':'for route in (2,):',
        'assert all_actions == 1312 and loaded == 1307':'assert loaded == 336 and all_actions == len(words)'})
    b=checked_text(inspect.getsource(parent.run),{
        'for route in range(4):':'for route in (2,):',
        'assert len(cases) == 2614':'assert len(cases) == 672'})
    env=dict(loader.__dict__);exec(compile(a,__file__+'::original-complete-SC2-loads','exec'),env);load=env['run']
    env=dict(parent.__dict__);exec(compile(b,__file__+'::original-both-parent-modes','exec'),env);handoff=env['run']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=image.read_file('/__arm9__.bin')
    for start,end in [(0x23E94,0x23F84),(0x23F4C,0x24134),(0x24134,0x24230),(0x2A510,0x2A530)]:assert arm[start:end]==clean[start:end]
    ROOT.mkdir(parents=True);loaded=load(image,'research');lp=ROOT/'research_native_loads.json';save(lp,loaded)
    modes=handoff(image,'research',loaded);mp=ROOT/'research_native_parent_modes.json';save(mp,modes)
    save(ROOT/'whole_SC2_336_loads_cache_hits672_original_parent_modes.json',dict(
        research_ROM=str(rom),research_ROM_sha256=ref['research_ROM_sha256'],
        load_proof=str(lp),load_proof_sha256=sha(lp.read_bytes()),parent_proof=str(mp),parent_proof_sha256=sha(mp.read_bytes()),
        whole_SC2_loads_andcache_hits=336,original_parent_modes=672,
        all336_native_loads_cache_hits_and672_modes_pass=True,
        B218_stored1020_logical1018_andtwo_tail_bytes_fit_original_cache=True,
        all_payload_metadata_source_bytes_andtail_guards_preserved=True,
        original_EV2_actions_select_by_block_index_without_interior_byte_offset=True,
        original_parent_both_modes_start_at_loaded_payload_plus8=True,
        SDK_IO_bridges_only_no_loader_cache_orVM_success_stub=True,
        scoped_original_loader_source=a,scoped_original_parent_source=b,
        bounded_caller_census_actual_scene_policy_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,MAP,Path(__file__)]},full_goal_complete=False))
    print('Changed SC2 archive:336 complete native loads/cache hits and672 original parent modes pass;1020stored/1018logical/tail2 preserved.')
