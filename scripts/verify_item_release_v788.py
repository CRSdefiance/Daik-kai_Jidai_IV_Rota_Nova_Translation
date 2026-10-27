"""Registered inheritance, exact paragraph contracts and clean-input patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import item_diplomacy_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.register_item_release_v788 import CONFIG, CURRENT, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v788_candidate.nds')


def reject(action):
    try: action()
    except (ValueError, AssertionError): return True
    raise AssertionError('Invalid editorial contract accepted')


def main():
    old, new = [NdsImage.open(p) for p in (CURRENT, ROM)]
    oc, oa = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    c, a = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    manifest = read(ROM.with_suffix('.manifest.json'))
    registry = read('translations/release_stack.json')
    before_registry = read(ROOT/'release_stack_before_v788.json')
    assert manifest['profile'] == 'all-routes-unified-v788' and manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and len(manifest['batches']) == 470 and not manifest['required_batches']
    assert registry['canonical_baseline'] == before_registry['canonical_baseline']
    assert registry['accepted_layers'] == before_registry['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert {k: v for k, v in registry['profiles']['all-routes-unified-v788'].items() if k not in ('item_diplomacy_editorial', 'description')} == {
        k: v for k, v in registry['profiles']['all-routes-unified-v783'].items() if k != 'description'}
    for name, h in read(ROOT/'frozen_prior_dependencies.json').items(): assert sha(Path(name).read_bytes()) == h, name
    assert all(registry['profiles'][k] == v for k, v in before_registry['profiles'].items())
    files = [{p: v for _, p, v in r.iter_files()} for r in (old, new)]
    components = [dict(r.iter_components()) for r in (old, new)]
    assert files[0].keys() == files[1].keys() and components[0].keys() == components[1].keys()
    assert {p for p in files[0] if files[0][p] != files[1][p]} == {'/COMMON/MESFILE.DK4'}
    assert {p for p in components[0] if components[0][p] != components[1][p]} == {'/__arm9__.bin'}
    assert old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    assert owned.apply_release(oc, oa, CONFIG)[:2] == (c, a)
    assert c == (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a == (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    prior, entries = common_message_entries(oc, oa, clean=False), owned.current_entries(c, a)
    doc = read(MANUSCRIPT)
    assert all(entries[r['message_id']].text == owned.compile_text(r) for r in doc['records'])
    assert all(x.text == y.text for x, y in zip(prior, entries, strict=True) if x.message_id not in owned.IDS)
    assert doc['remaining_gates'] and not doc['whole_batch_completion_credit']
    negative = {}
    for name in ('source', 'current', 'formatting', 'legacy', 'unreviewed_prose'):
        d = deepcopy(doc)
        if name == 'source': d['records'][0]['source_hex'] = '41'
        elif name == 'current': d['records'][0]['current_text_hex'] = '41'
        elif name == 'formatting': d['records'][0]['review']['formatting'] = False
        elif name == 'legacy': d['translation_policy'] = 'natural-dialogue-v1'
        else: d['records'][0]['english'] = 'Different wording.{PAD}'
        negative[name] = reject(lambda d=d: owned.transform(oc, oa, d))
    row = next(r for r in doc['records'] if r['message_id'] == 1113)
    for name, text in (('indent', '  Send %s this %s?{PAD}'), ('padding', 'Send  %s this %s?{PAD}'),
                       ('break', 'Send %s\nthis %s?{PAD}'), ('lost_arg', 'Send %s?{PAD}'),
                       ('extra_arg', 'Send %s this %s %s?{PAD}'), ('macro', 'Send %s this %s {FI}?{PAD}')):
        negative[name] = reject(lambda text=text: owned.compile_text({**row, 'english': text}))
    negative['reversed_arguments'] = reject(lambda: owned.compile_text({**row, 'English_argument_source_indices': [1, 0]}))
    watch = read('work/analysis/dialogue_formatting_user_recheck_v782/COMMON676_677.json')
    cpu = machine(a)
    from ndspy.code import MainCodeFile
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(a, 0x02000000).sections[3].data[:-48]))
    cases = []
    for r in watch['entries']:
        formatted, lines = native_layout(cpu, entries[r['id']].text, r['id'], ())
        assert formatted.hex() == r['native_formatted_hex'] and lines == r['lines']
        cases.append({'id': r['id'], 'lines': lines, 'native_formatted_hex': formatted.hex()})
    save(ROOT/'user676_677_preserved.json', {'candidate_sha256': sha(ROM.read_bytes()), 'cases': cases,
        'old_actual_capture': watch['earlier_actual_capture'], 'no_fresh_shop_activation_claim': True,
        'formatting_watchlist_remains_ongoing': True})
    save(ROOT/'registered_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'COMMON_sha256': sha(c), 'ARM9_sha256': sha(a), 'all470_batches114_accepted_layers_and_graphics_retained': True,
        'only_COMMON_and_ARM9_change_from_V783': True, 'all3592_other_strings_exact': True,
        'all7336_complete_native_copies': True, 'all2774_native_layouts_and76_fonts': True,
        'all_frozen_parser_producers_dependencies_and_prior_profiles_preserved': True,
        'negative_gates': negative, 'actual_scenes_and_eligibility_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch = ROM.with_suffix('.xdelta')
    rebuilt = ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    save(ROOT/'patch_proof.json', {'clean_source_sha256': sha(clean.read_bytes()), 'candidate_sha256': sha(ROM.read_bytes()),
        'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'byte_exact_reconstruction': True,
        'canonical_base_sha256': registry['canonical_baseline']['sha256']})
    print('V788 exact registered inheritance, 7336 copies, 2774 layouts, 12 negative gates and clean-input patch pass. Actual scenes pending.', flush=True)


if __name__ == '__main__':
    main()
