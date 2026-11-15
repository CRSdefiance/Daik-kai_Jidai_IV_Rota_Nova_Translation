"""Run the original complete archive loader and parent handoff for current SC3."""
import inspect
from pathlib import Path
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/Maria_B0_B32_clean_20261109')
OUT = ROOT/'loaders_v1'
REBUILT = ROOT/'stored_reconstruction_v1/reconstruction.json'


def main():
    assert not OUT.exists()
    rebuilt = load(REBUILT)
    assert len(rebuilt['changed_blocks']) == 32 and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert digest(rebuilt['research_ROM']) == rebuilt['research_ROM_sha256']
    image = NdsImage.open(rebuilt['research_ROM'])
    loader_source = checked_text(inspect.getsource(loader.run), {
        'for route in range(4):': 'for route in [3]:',
        'assert all_actions == 1312 and loaded == 1307': 'assert all_actions == 304 and loaded == 303',
    })
    parent_source = checked_text(inspect.getsource(parent.run), {
        'for route in range(4):': 'for route in [3]:',
        'assert len(cases) == 2614': 'assert len(cases) == 606',
        'all_blocks_bound_to_V727_complete_native_loader_payloads':
            'all_blocks_bound_to_fresh_complete_native_loader_payloads',
    })
    env, penv = dict(vars(loader)), dict(vars(parent))
    exec(compile(loader_source, __file__+'::same-native-loader-explicit-SC3-only', 'exec'), env)
    exec(compile(parent_source, __file__+'::same-native-parent-explicit-SC3-only', 'exec'), penv)
    OUT.mkdir()
    loaded = env['run'](image, 'Maria301-stored-research')
    load_path = OUT/'native_loads.json'
    save(load_path, loaded)
    modes = penv['run'](image, 'Maria301-stored-research', loaded)
    modes_path = OUT/'native_parent_modes.json'
    save(modes_path, modes)
    save(OUT/'verification.json', dict(
        reconstruction=str(REBUILT), reconstruction_sha256=digest(REBUILT),
        research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
        route=3, fresh_whole_archive_loads_andcache_hits=303, original_EV3_action_count=304,
        fresh_parent_cases=606, exact_reused_parent_cases=0,
        loads=str(load_path), loads_sha256=digest(load_path),
        modes=str(modes_path), modes_sha256=digest(modes_path),
        source_owned_loader_adapter=loader_source, source_owned_parent_adapter=parent_source,
        all_native_executed_instructions_current_ROM_exact=True,
        all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact=True,
        controlled_native_route_inputs_not_optional_event_activation=True,
        unchanged_other_routes_not_replayed=True, actual_gameplay=False, new_credit=0,
        evidence={str(p): digest(p) for p in [REBUILT, Path(loader.__file__), Path(parent.__file__), Path(__file__)]}))
    print('303 whole SC3 loads/cache hits and606 native parent handoffs pass; other routes unchanged/not replayed.')


if __name__ == '__main__':
    main()
