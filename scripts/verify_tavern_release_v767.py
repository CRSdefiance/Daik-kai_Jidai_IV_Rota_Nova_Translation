"""Registered Tavern candidate preservation,negative gates and exact clean patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import tavern_conversations_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_tavern_release_v767 import CONFIG, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v767_candidate.nds')


def reject(action):
    try: action()
    except (ValueError, AssertionError): return True
    raise AssertionError('Malformed Tavern input accepted')


def main():
    old, new = [NdsImage.open(path) for path in ('out/all_routes_combined_v762_candidate.nds', ROM)]
    c, a = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    oc, oa = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    manifest = read(ROM.with_suffix('.manifest.json'))
    registry, before = read('translations/release_stack.json'), read(ROOT / 'release_stack_before_v767.json')
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes()) and manifest['profile'] == 'all-routes-unified-v767'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and len(manifest['batches']) == 470 and not manifest['required_batches']
    assert registry['accepted_layers'] == before['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert registry['canonical_baseline'] == before['canonical_baseline']
    assert [path for _, path, data in old.iter_files() if data != new.read_file(path)] == ['/COMMON/MESFILE.DK4']
    assert old.rom.arm7 == new.rom.arm7 and old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    assert owned.apply_release(oc, oa, CONFIG)[:2] == (c, a)
    assert c == (ROOT / 'research_COMMON.bin').read_bytes() and a == (ROOT / 'research_combined_ARM9.bin').read_bytes()
    entries = common_message_entries(c, a, clean=False); doc = read(MANUSCRIPT)
    assert all(entries[r['message_id']].text == owned.compile_text(r) for r in doc['records'])
    old_entries = common_message_entries(oc, oa, clean=False)
    assert all(x.text == y.text for x, y in zip(old_entries, entries, strict=True) if x.message_id not in owned.IDS)
    copies = [read(ROOT / f'native_copies_block_{k:02d}.json') for k in range(41)]
    assert {(r['message_id'], r['cold_cache']) for report in copies for r in report['cases']} == {(n, cold) for n in range(3668) for cold in (False, True)}
    assert all(report['COMMON_sha256'] == sha(c) and report['ARM9_sha256'] == sha(a) for report in copies)
    stale = deepcopy(doc); stale['records'][0]['source_hex'] = '41'
    wrong_current = deepcopy(doc); wrong_current['records'][0]['current_text_hex'] = '41'
    unreviewed = deepcopy(doc); unreviewed['records'][0]['review']['formatting'] = False
    wrong_args = deepcopy(doc); wrong_args['records'][0]['runtime_argument_contract'] = ['native_person_name']
    legacy = deepcopy(doc); legacy['translation_policy'] = 'natural-dialogue-v1'
    row = next(r for r in doc['records'] if r['message_id'] == 822)
    tests = {'stale_source': reject(lambda: owned.transform(oc, oa, stale)),
        'stale_current': reject(lambda: owned.transform(oc, oa, wrong_current)),
        'unapproved_formatting': reject(lambda: owned.transform(oc, oa, unreviewed)),
        'wrong_native_roles': reject(lambda: owned.transform(oc, oa, wrong_args)),
        'legacy_policy': reject(lambda: owned.transform(oc, oa, legacy)),
        'authored_indent': reject(lambda: owned.compile_text({**row, 'english': '  Hello, %s.{PAD}'})),
        'internal_padding': reject(lambda: owned.compile_text({**row, 'english': 'Hello,   %s.{PAD}'})),
        'authored_break': reject(lambda: owned.compile_text({**row, 'english': 'Hello,\n%s.{PAD}'})),
        'lost_argument': reject(lambda: owned.compile_text({**row, 'english': 'Hello.{PAD}'})),
        'extra_argument': reject(lambda: owned.compile_text({**row, 'english': 'Hello, %s %s.{PAD}'})),
        'nonprintable': reject(lambda: owned.compile_text({**row, 'english': 'Hello\x7f %s.{PAD}'})),
        'overlong': reject(lambda: owned.compile_text({**row, 'english': 'Hello ' * 40 + '%s.{PAD}'})),
        'literal_coordinate_pattern': reject(lambda: owned.compile_text({'message_id': 842, 'english': 'Near N 3 and %s.{PAD}'}))}
    assert old_entries[676].text == entries[676].text and old_entries[677].text == entries[677].text
    save(ROOT / 'registered_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'COMMON_sha256': sha(c), 'ARM9_sha256': sha(a), 'all470_batches114_layers_and_prior_graphics_preserved': True,
        'only_COMMON_ARM9_changed_from_V762': True, 'all3637_other_strings_and_repaired676_677_exact': True,
        'all7336_whole_native_copy_spans_pass': True, 'negative_gates': tests,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'actual_gameplay_pending': True, 'full_goal_complete': False})
    clean = Path('work/clean.nds'); assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch, rebuilt = ROM.with_suffix('.xdelta'), ROOT / 'patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean, ROM, patch); apply_xdelta(clean, patch, rebuilt)
    assert ROM.read_bytes() == rebuilt.read_bytes()
    save(ROOT / 'patch_proof.json', {'clean_source_sha256': sha(clean.read_bytes()), 'candidate_sha256': sha(ROM.read_bytes()),
        'patch_sha256': sha(patch.read_bytes()), 'byte_exact_reconstruction': True})
    print('V767 all470/114 layers,3637 other strings,7336 whole copies,13 negative gates and exact clean patch pass.', flush=True)


if __name__ == '__main__': main()
