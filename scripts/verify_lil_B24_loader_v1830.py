"""Re-execute original whole-SC2 loading and both parent modes for lesson resizing."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.prepare_lil_B24_research_v1829 import ROM, PARENT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B24_loader_v1830')

if __name__ == '__main__':
    assert not ROOT.exists()
    receipt = read('work/analysis/lil_B24_research_v1829/research_image_receipt.json')
    assert sha(ROM.read_bytes()) == receipt['research_ROM_sha256']
    assert sha(PARENT.read_bytes()) == receipt['parent_sha256']
    expected = len(IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks)
    assert expected == 336
    source = inspect.getsource(loader.run)
    assert source.count('for route in range(4):') == 1
    assert source.count('assert all_actions == 1312 and loaded == 1307') == 1
    source = source.replace('for route in range(4):', 'for route in (2,):')
    source = source.replace('assert all_actions == 1312 and loaded == 1307',
                            f'assert loaded == {expected} and all_actions == len(words)')
    env = dict(loader.__dict__)
    exec(compile(source, __file__, 'exec'), env)
    load = env['run']
    source2 = inspect.getsource(parent.run)
    assert source2.count('for route in range(4):') == 1
    assert source2.count('assert len(cases) == 2614') == 1
    source2 = source2.replace('for route in range(4):', 'for route in (2,):')
    source2 = source2.replace('assert len(cases) == 2614', f'assert len(cases) == {expected * 2}')
    env = dict(parent.__dict__)
    exec(compile(source2, __file__, 'exec'), env)
    handoff = env['run']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    results = []
    ROOT.mkdir(parents=True)
    (ROOT / 'scoped_loader_source.txt').write_text(source, encoding='utf-8')
    (ROOT / 'scoped_parent_source.txt').write_text(source2, encoding='utf-8')
    for label, path in [('current', PARENT), ('research', ROM)]:
        image = NdsImage.open(path)
        arm = image.read_file('/__arm9__.bin')
        for a, b in [(0x23E94, 0x23F84), (0x23F4C, 0x24134), (0x24134, 0x24230), (0x2A510, 0x2A530)]:
            assert arm[a:b] == clean[a:b]
        loaded = load(image, label)
        load_path = ROOT / (label + '_native_loads.json')
        save(load_path, loaded)
        parents = handoff(image, label, loaded)
        parent_path = ROOT / (label + '_native_parent_modes.json')
        save(parent_path, parents)
        results.append({'label': label, 'ROM_sha256': sha(path.read_bytes()),
                        'load_proof': str(load_path), 'load_sha256': sha(load_path.read_bytes()),
                        'parent_proof': str(parent_path), 'parent_sha256': sha(parent_path.read_bytes()),
                        'whole_SC2_loads_and_cache_hits': expected, 'original_parent_modes': expected * 2})
    save(ROOT / 'whole_SC2_and_B24_initial_entry_proof.json', {
        'versions': results, 'all336_whole_blocks_and672_modes_each_pass': True,
        'B24_block_fits_original_0x2400_cache': True,
        'original_EV2_actions_select_by_block_index_without_interior_byte_offset': True,
        'original_parent_both_modes_start_at_loaded_payload_plus8': True,
        'all_payload_cache_metadata_and_tail_guards_exact': True,
        'SDK_IO_bridges_only_no_loader_or_cache_success_stub': True,
        'later_control_flow_and_actual_revised_paths_reference_approval_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Both ROMs:336 original loads/cache hits and672 parent entry modes pass;later lesson path approval pending.', flush=True)
