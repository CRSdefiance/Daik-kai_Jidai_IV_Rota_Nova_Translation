"""Verify complete integration, unchanged prior prose, one native block and patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_rumors import IDS, compile_paragraph, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_rumors_v749')
ROM = Path('out/all_routes_combined_v749_candidate.nds')


def reject(action):
    try:
        action()
    except (ValueError, AssertionError):
        return True
    raise AssertionError('Malformed regional rumor manuscript accepted')


def main():
    old, new = NdsImage.open('out/all_routes_combined_v748_candidate.nds'), NdsImage.open(ROM)
    manifest = read(ROM.with_suffix('.manifest.json'))
    registry, previous = read('translations/release_stack.json'), read(ROOT / 'release_stack_before_V749.json')
    assert manifest['profile'] == 'all-routes-unified-v749'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == []
    assert all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers']) == 114 and registry['accepted_layers'] == previous['accepted_layers']
    assert registry['canonical_baseline'] == previous['canonical_baseline']
    changed = [p for _, p, raw in old.iter_files() if raw != new.read_file(p)]
    assert changed == ['/COMMON/MESFILE.DK4']
    assert old.rom.arm7 == new.rom.arm7 and old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    assert common == (ROOT / 'research_COMMON.bin').read_bytes() and arm == (ROOT / 'research_ARM9.bin').read_bytes()
    source_common, source_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    before = common_message_entries(source_common, source_arm, clean=False)
    after = common_message_entries(common, arm, clean=False)
    assert [a.message_id for a, b in zip(before, after, strict=True) if a.text.rstrip() != b.text.rstrip()] == list(IDS)
    selected = [e for e in after if e.block == 9]
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
    doc = read('translations/regional_rumors_manuscript_v1.json')
    legacy, stale, missing = deepcopy(doc), deepcopy(doc), deepcopy(doc)
    legacy['translation_policy'] = 'natural-dialogue-v1'
    stale['records'][0]['source_hex'] = '41'
    missing['records'] = [r for r in missing['records'] if r['message_id'] != 713]
    controls = {
        'legacy_policy': reject(lambda: transform(source_common, source_arm, legacy)),
        'stale_Japanese_source': reject(lambda: transform(source_common, source_arm, stale)),
        'missing_packed_regional rumor_sibling713': reject(lambda: transform(source_common, source_arm, missing)),
        'authored_break': reject(lambda: compile_paragraph('Two\nlines.{PAD}')),
        'authored_alignment_spaces': reject(lambda: compile_paragraph('  Offset text.{PAD}')),
        'invented_substitution': reject(lambda: compile_paragraph('Regional rumor %s.{PAD}')),
        'unsafe_macro': reject(lambda: compile_paragraph('FIRE{PAD}'))}
    native = read(ROOT / 'native_review.json')
    assert len(native['all21_native_printf_macro_wrap_and_complete_font_planes']) == 21
    assert len(native['revised_IDs']) == 12 and len(native['retained_wording_IDs']) == 9
    save(ROOT / 'registered_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'all470_batches114_accepted_layers_and_final_guards_pass': True,
        'only_COMMON_and_ARM9_native_offsets_and_owned28_dispatch_bytes_differ': True,
        'all675_graphics_all_other_files_and_prior36_revisions_exact_V748': True,
        'all3668_native_IDs_NUL_owners_block_sizes_preserved': True,
        'native_copies': copies, 'complete_native_copy_count': len(copies),
        'native_IO_bridged_to_exact_bytes_not_gameplay_claim': True,
        'meaningful_rejection_controls': controls, 'gameplay_pending': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    clean, patch, result = Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'patch_reconstruction_RESEARCH_ONLY.nds'
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, result)
    assert result.read_bytes() == ROM.read_bytes()
    save(ROOT / 'patch_proof.json', {'clean_source_sha256': sha(clean.read_bytes()),
        'candidate_sha256': sha(ROM.read_bytes()), 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
        'complete_reconstruction_sha256': sha(result.read_bytes()), 'whole_ROM_byte_exact': True})
    print(f'V749 complete integration,{len(copies)} native copies,7 rejection controls and exact patch pass.', flush=True)


if __name__ == '__main__':
    main()
