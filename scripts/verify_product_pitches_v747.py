"""Verify registered ancestry, exact scoped components and complete native copies."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.product_pitches_editorial import IDS, compile_template, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/product_pitches_v747')
ROM = Path('out/all_routes_combined_v747_candidate.nds')


def reject(action):
    try:
        action()
    except (ValueError, AssertionError):
        return True
    raise AssertionError('Malformed pitch input accepted')


def main():
    old, new = NdsImage.open('out/all_routes_combined_v746_candidate.nds'), NdsImage.open(ROM)
    manifest = read(ROM.with_suffix('.manifest.json'))
    registry = read('translations/release_stack.json')
    before_registry = read(ROOT / 'release_stack_before_V747.json')
    assert manifest['profile'] == 'all-routes-unified-v747'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == []
    assert all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers']) == 114
    assert registry['accepted_layers'] == before_registry['accepted_layers']
    assert registry['canonical_baseline'] == before_registry['canonical_baseline']
    changed = [p for _, p, raw in old.iter_files() if new.read_file(p) != raw]
    assert changed == ['/COMMON/MESFILE.DK4']
    assert old.rom.arm7 == new.rom.arm7 and old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    assert common == (ROOT / 'research_COMMON.bin').read_bytes()
    assert arm == (ROOT / 'research_ARM9.bin').read_bytes()
    source_common, source_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    before = common_message_entries(source_common, source_arm, clean=False)
    after = common_message_entries(common, arm, clean=False)
    assert [a.message_id for a, b in zip(before, after, strict=True) if a.text.rstrip() != b.text.rstrip()] == list(IDS)
    selected = [e for e in after if e.block == 8]
    ids = [selected[0].message_id - 1, *(e.message_id for e in selected), selected[-1].message_id + 1]
    copies = []
    factory = loader.machine_for
    loader.machine_for = arm946_machine
    try:
        for i in ids:
            for cold in (False, True):
                result = loader.warm_copy(arm, common, i, after[i].text, cold_cache=cold)
                copies.append({'message_id': i, 'cold_cache': cold, 'complete_copy_verified': True,
                               'copy_bytes': result['copied_bytes']})
    finally:
        loader.machine_for = factory
    doc = read('translations/product_pitches_editorial_manuscript_v1.json')
    legacy = deepcopy(doc)
    legacy['translation_policy'] = 'natural-dialogue-v1'
    stale = deepcopy(doc)
    stale['records'][0]['source_hex'] = '41'
    missing = deepcopy(doc)
    missing['records'] = missing['records'][1:]
    controls = {
        'legacy_policy': reject(lambda: transform(source_common, source_arm, legacy)),
        'stale_Japanese_source': reject(lambda: transform(source_common, source_arm, stale)),
        'missing_packed_product_intro': reject(lambda: transform(source_common, source_arm, missing)),
        'authored_break': reject(lambda: compile_template('Two\nlines.{PAD}', 676)),
        'lost_substitution': reject(lambda: compile_template('No product.{PAD}', 675)),
        'extra_substitution': reject(lambda: compile_template('%s %s{PAD}', 675)),
        'unsafe_macro': reject(lambda: compile_template('FIRE{PAD}', 676)),
    }
    native = read(ROOT / 'native_review.json')
    assert native['complete_native_printf_wrap_cases'] == 11289
    assert len(native['complete_native_font_planes']) == 11
    assert sha((ROOT / 'native_layout_matrix.json').read_bytes()) == native['matrix_sha256']
    save(ROOT / 'registered_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'all470_batches114_accepted_layers_and_final_guards_pass': True,
        'only_COMMON_and_ARM9_message_offsets_and32_owned_dispatch_bytes_change': True,
        'all675_graphics_and_other_internal_files_and_prior14_prose_revisions_exact_V746': True,
        'all3668_native_IDs_and_owner_order_preserved': True,
        'native_copies': copies, 'complete_native_copy_count': len(copies),
        'native_IO_bridged_to_exact_bytes_not_gameplay_claim': True,
        'meaningful_rejection_controls': controls, 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'live_gameplay_pending': True, 'full_goal_complete': False})
    clean, patch, result = Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'patch_reconstruction_RESEARCH_ONLY.nds'
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, result)
    assert result.read_bytes() == ROM.read_bytes()
    save(ROOT / 'patch_proof.json', {
        'clean_source_sha256': sha(clean.read_bytes()), 'candidate_sha256': sha(ROM.read_bytes()),
        'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
        'complete_reconstruction_sha256': sha(result.read_bytes()), 'whole_ROM_byte_exact': True})
    print('V747 registered checks,122 native copies,7 rejection controls and exact clean patch pass.', flush=True)


if __name__ == '__main__':
    main()
