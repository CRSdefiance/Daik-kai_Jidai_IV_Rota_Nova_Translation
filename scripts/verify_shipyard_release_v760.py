"""Full registered Yard component, native gates, preservation and clean patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_common import compile_text
from dk4tool.patch.shipyard_editorial_release import apply_release, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_shipyard_release_v760 import CONFIG, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v760_candidate.nds')


def reject(action):
    try:
        action()
    except (ValueError, AssertionError):
        return True
    raise AssertionError('Malformed Yard release input was accepted')


def main():
    old, new = [NdsImage.open(p) for p in ('out/all_routes_combined_v758_candidate.nds', ROM)]
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    old_common, old_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    manifest, registry, before_registry = read(ROM.with_suffix('.manifest.json')), read('translations/release_stack.json'), read(ROOT / 'release_stack_before_V760.json')
    assert manifest['profile'] == 'all-routes-unified-v760' and manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == [] and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert registry['accepted_layers'] == before_registry['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert registry['canonical_baseline'] == before_registry['canonical_baseline']
    assert [p for _, p, data in old.iter_files() if data != new.read_file(p)] == ['/COMMON/MESFILE.DK4']
    assert old.rom.arm7 == new.rom.arm7 and old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    c, a, proof = apply_release(old_common, old_arm, CONFIG)
    assert (c, a) == (common, arm)
    assert common == (ROOT / 'research_COMMON.bin').read_bytes()
    assert arm == (ROOT / 'research_combined_ARM9.bin').read_bytes()
    copies = [read(ROOT / f'native_copies_block_{k:02d}.json') for k in range(41)]
    assert sum(len(r['cases']) for r in copies) == 7336
    assert all(r['COMMON_sha256'] == sha(common) and r['ARM9_sha256'] == sha(arm) for r in copies)
    entries = common_message_entries(common, arm, clean=False)
    doc = read(MANUSCRIPT)
    assert all(entries[r['message_id']].text == compile_text(r) for r in doc['records'])
    stale = deepcopy(doc); stale['records'][0]['source_hex'] = '41'
    unreviewed = deepcopy(doc); unreviewed['records'][0]['review']['formatting'] = False
    legacy = deepcopy(doc); legacy['translation_policy'] = 'natural-dialogue-v1'
    swapped = deepcopy(doc); swapped['records'][-2]['runtime_argument_contract'] = ['typed_gold_currency', 'literal_ship_name', 'typed_preparation_duration']
    row = doc['records'][-2]
    rejections = {
        'stale_clean_source': reject(lambda: transform(old_common, old_arm, stale)),
        'unreviewed_formatting': reject(lambda: transform(old_common, old_arm, unreviewed)),
        'legacy_policy': reject(lambda: transform(old_common, old_arm, legacy)),
        'typed_argument_order': reject(lambda: transform(old_common, old_arm, swapped)),
        'authored_indent': reject(lambda: compile_text({**row, 'english': '  %s %s %s{PAD}'})),
        'authored_break': reject(lambda: compile_text({**row, 'english': '%s\n%s %s{PAD}'})),
        'dropped_argument': reject(lambda: compile_text({**row, 'english': '%s %s{PAD}'})),
        'extra_argument': reject(lambda: compile_text({**row, 'english': '%s %s %s %s{PAD}'})),
        'native_command_in_authored_prose': reject(lambda: compile_text({**row, 'english': 'FIRE %s %s %s{PAD}'})),
    }
    save(ROOT / 'registered_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'source_canonical_base': registry['canonical_baseline'],
        'all470_batches114_layers_final_guards_and675_graphics_preserved': True,
        'only_COMMON_and_ARM9_changed_from_V758': True, 'full_registered_transform_matches_research_components': True,
        'all7336_warm_cold_copy_contracts_pass': True, 'all21_final_native_messages_exact': True,
        'rejections': rejections, 'proof': proof, 'actual_gameplay_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch, restored = ROM.with_suffix('.xdelta'), ROOT / 'patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, restored)
    assert ROM.read_bytes() == restored.read_bytes()
    save(ROOT / 'patch_proof.json', {'clean_source_sha256': sha(clean.read_bytes()),
        'candidate_sha256': sha(ROM.read_bytes()), 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
        'byte_exact_reconstruction': True})
    print('Registered V760 preserves all prior layers/graphics; all native copies and9 negative gates pass; exact clean-input patch reconstructs every ROM byte. Actual gameplay pending.', flush=True)


if __name__ == '__main__':
    main()
