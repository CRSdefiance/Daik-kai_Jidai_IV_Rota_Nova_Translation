"""Reuse exact native parent cases; reload changed archive offsets and changed blocks."""
import argparse
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    rebuild_path = Path('work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json')
    prior_path = Path('work/analysis/Hodram_B54_B60_loaders_v8813/325_loads14fresh636reused_parent_modes.json')
    rebuilt, prior = load(rebuild_path), load(prior_path)
    modes_path = Path(prior['parent_mode_proof'])
    assert sha(modes_path.read_bytes()) == prior['parent_mode_sha256']
    old_modes = load(modes_path)
    image = NdsImage.open(rebuilt['research_ROM'])
    assert sha(Path(rebuilt['research_ROM']).read_bytes()) == rebuilt['research_ROM_sha256']
    arm = image.read_file('/__arm9__.bin')
    sections = MainCodeFile(arm, BASE).sections
    spans = [(s.ramAddress, bytes(s.data)) for s in sections]
    spans.append((POOL, bytes(sections[3].data[:-48])))
    for row in old_modes['executed_source_words']:
        expected = bytes.fromhex(row['hex'])
        matches = [data[row['PC'] - base:row['PC'] - base + len(expected)]
                   for base, data in spans if base <= row['PC'] and row['PC'] + len(expected) <= base + len(data)]
        assert matches and all(value == expected for value in matches)
    blocks = IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    cases = {n: [c for c in old_modes['native_handoff_and_first_read_cases']
                  if c['route'] == 1 and c['block'] == n] for n in range(len(blocks))}
    changed = set()
    for number, block in enumerate(blocks):
        assert len(cases[number]) == 2 and {c['mode'] for c in cases[number]} == {0, 1}
        if any(c['source_block_sha256'] != sha(block) for c in cases[number]):
            changed.add(number)
    assert changed == set(range(61, 71))
    env = {**loader.__dict__, 'EXPECTED_ACTIONS': 326}
    exec(compile(prior['source_owned_loader_adapter'], __file__ + '::current-archive-loads', 'exec'), env)
    penv = {**parent.__dict__, 'CHANGED_BLOCKS': changed, 'REUSED_PARENT_CASES': cases}
    exec(compile(prior['source_owned_parent_adapter'], __file__ + '::changed-parent-cases', 'exec'), penv)
    args.out.mkdir(parents=True)
    loaded = env['run'](image, 'pending-Hodram-research')
    load_path = args.out / 'native_loads.json'
    save(load_path, loaded)
    modes = penv['run'](image, 'pending-Hodram-research', loaded)
    mode_path = args.out / 'native_parent_modes.json'
    save(mode_path, modes)
    fresh = [c for c in modes['native_handoff_and_first_read_cases'] if c['block'] in changed]
    reused = [c for c in modes['native_handoff_and_first_read_cases'] if c['block'] not in changed]
    assert len(fresh) == 20 and len(reused) == 630
    assert all(c in cases[c['block']] for c in reused)
    assert len(loaded['routes'][0]['actions']) == 326
    save(args.out / 'verification.json', dict(reconstruction=str(rebuild_path), reconstruction_sha256=sha(rebuild_path.read_bytes()),
        research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
        prior=str(prior_path), prior_sha256=sha(prior_path.read_bytes()),
        prior_executed_parent_instructions_match_current_runtime=True,
        fresh_whole_archive_loads_andcache_hits=325, fresh_parent_cases=20,
        exact_reused_parent_cases=630, original_EV1_action_count=326,
        loads=str(load_path), loads_sha256=sha(load_path.read_bytes()),
        modes=str(mode_path), modes_sha256=sha(mode_path.read_bytes()),
        controlled_native_route_inputs_not_optional_event_activation=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('325 whole native loads/cache hits;20 fresh and630 exact reused parent cases pass.')


if __name__ == '__main__':
    main()
