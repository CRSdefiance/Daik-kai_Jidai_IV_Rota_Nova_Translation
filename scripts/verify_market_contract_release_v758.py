"""Registered stack, complete native copies, source branches and exact patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_contract_editorial import compile_text, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_market_contract_v758 import CONFIG, MANUSCRIPT
from scripts.review_market_contract_v758 import CURRENT, ROOT
from scripts.prepare_product_pitches_v747 import wrapper_dispatch
from scripts.review_market_stock_v755 import fragments
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v758_candidate.nds')


def reject(action):
    try:
        action()
    except (AssertionError, ValueError):
        return True
    raise AssertionError('Invalid Market prose input accepted')


def main():
    old, new = NdsImage.open(CURRENT), NdsImage.open(ROM)
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    old_common, old_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    manifest, registry = read(ROM.with_suffix('.manifest.json')), read('translations/release_stack.json')
    previous = read(ROOT / 'release_stack_before_V758.json')
    assert manifest['profile'] == 'all-routes-unified-v758' and manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == [] and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert registry['accepted_layers'] == previous['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert registry['canonical_baseline'] == previous['canonical_baseline']
    assert [p for _, p, raw in old.iter_files() if raw != new.read_file(p)] == ['/COMMON/MESFILE.DK4']
    assert old.rom.arm7 == new.rom.arm7 and old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    assert common == (ROOT / 'research_COMMON.bin').read_bytes() and arm == (ROOT / 'research_ARM9.bin').read_bytes()
    doc = read(MANUSCRIPT)
    a, b, repack = transform(old_common, old_arm, doc)
    assert (a, b) == (common, arm)
    before, after = common_message_entries(old_common, old_arm, clean=False), common_message_entries(common, arm, clean=False)
    assert [a.message_id for a, b in zip(before, after, strict=True) if a.text != b.text] == list(range(754, 762))
    copies = []
    for block in range(41):
        p = ROOT / f'native_copies_block_{block:02d}.json'
        report = read(p)
        assert report['COMMON_sha256'] == sha(common) and report['ARM9_sha256'] == sha(arm)
        assert report['verifier_sha256'] == sha(Path('scripts/verify_contract_native_copies_v758.py').read_bytes())
        assert {(r['message_id'], r['cold_cache']) for r in report['cases']} == {
            (e.message_id, cold) for e in after if e.block == block for cold in (False, True)}
        copies.extend(report['cases'])
    assert len(copies) == 7336
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    context = fragments(clean_arm)
    assert fragments(arm) == context and len(context) == 36
    selected_a, selected_b = wrapper_dispatch(old_arm), wrapper_dispatch(arm)
    assert [i for i, (a, b) in enumerate(zip(selected_a, selected_b, strict=True)) if a != b] == [761]
    stale, unreviewed, legacy = deepcopy(doc), deepcopy(doc), deepcopy(doc)
    stale['records'][0]['source_hex'] = '41'
    unreviewed['records'][0]['review']['formatting'] = False
    legacy['translation_policy'] = 'natural-dialogue-v1'
    row = doc['records'][0]
    rejects = {
        'stale_source': reject(lambda: transform(old_common, old_arm, stale)),
        'unreviewed_formatting': reject(lambda: transform(old_common, old_arm, unreviewed)),
        'legacy_policy': reject(lambda: transform(old_common, old_arm, legacy)),
        'authored_indent': reject(lambda: compile_text({**row, 'english': '  Offset %s and %s.{PAD}'})),
        'authored_break': reject(lambda: compile_text({**row, 'english': 'Two %s\nlines %s.{PAD}'})),
        'missing_argument': reject(lambda: compile_text({**row, 'english': 'Missing %s.{PAD}'})),
        'extra_argument': reject(lambda: compile_text({**row, 'english': 'Extra %s %s %s.{PAD}'})),
        'unsafe_command': reject(lambda: compile_text({**row, 'english': 'FIRE %s and %s.{PAD}'})),
    }
    config = read(CONFIG)
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    for p, digest in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == digest, p
    save(ROOT / 'registered_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'all470_batches114_layers_final_guards_and675_graphics_preserved': True,
        'all3660_unselected_visible_texts_and27_other_blocks_exact': True,
        'all7336_guarded_warm_cold_native_copy_contracts_pass': True,
        'all36_original_source_selection_fragments_each_clean_and_candidate': context,
        'all18340_dispatch_cases_differ_only_in761': True, 'rejections': rejects,
        'repack': repack, 'producer_sha256': sha(Path(__file__).read_bytes()),
        'actual_gameplay_pending': True, 'full_goal_complete': False})
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch, reconstructed = ROM.with_suffix('.xdelta'), ROOT / 'patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    save(ROOT / 'patch_proof.json', {'clean_source_sha256': sha(clean.read_bytes()),
        'candidate_sha256': sha(ROM.read_bytes()), 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
        'whole_ROM_byte_exact': True})
    print('Registered V758,7336 native copies,36 source fragments and exact clean-input patch pass.', flush=True)


if __name__ == '__main__':
    main()
