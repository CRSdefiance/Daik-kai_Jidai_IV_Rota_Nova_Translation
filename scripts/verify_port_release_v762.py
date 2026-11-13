"""Final component/preservation gates and exact clean-input V762 patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import port_services_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_port_release_v762 import CONFIG, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v762_candidate.nds')


def reject(action):
    try: action()
    except (ValueError, AssertionError): return True
    raise AssertionError('Malformed service manuscript was accepted')


def main():
    old, new = [NdsImage.open(p) for p in ('out/all_routes_combined_v760_candidate.nds', ROM)]
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    oc, oa = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    manifest, registry, before = read(ROM.with_suffix('.manifest.json')), read('translations/release_stack.json'), read(ROOT / 'release_stack_before_v762.json')
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes()) and manifest['profile'] == 'all-routes-unified-v762'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and len(manifest['batches']) == 470 and not manifest['required_batches']
    assert registry['accepted_layers'] == before['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert registry['canonical_baseline'] == before['canonical_baseline']
    assert [p for _, p, data in old.iter_files() if data != new.read_file(p)] == ['/COMMON/MESFILE.DK4']
    assert old.rom.arm7 == new.rom.arm7 and old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    assert owned.apply_release(oc, oa, CONFIG)[:2] == (common, arm)
    assert common == (ROOT / 'research_COMMON.bin').read_bytes() and arm == (ROOT / 'research_combined_ARM9.bin').read_bytes()
    tables = common_message_entries(common, arm, clean=False); doc = read(MANUSCRIPT)
    assert all(tables[r['message_id']].text == owned.compile_text(r) for r in doc['records'])
    copies = [read(ROOT / f'native_copies_block_{k:02d}.json') for k in range(41)]
    assert all(r['COMMON_sha256'] == sha(common) and r['ARM9_sha256'] == sha(arm) for r in copies)
    assert {(r['message_id'], r['cold_cache']) for report in copies for r in report['cases']} == {(i, cold) for i in range(3668) for cold in (False, True)}
    stale = deepcopy(doc); stale['records'][0]['source_hex'] = '41'
    wrong_current = deepcopy(doc); wrong_current['records'][0]['current_text_hex'] = '41'
    unreviewed = deepcopy(doc); unreviewed['records'][0]['review']['formatting'] = False
    wrong_args = deepcopy(doc); wrong_args['records'][-1]['runtime_argument_contract'] = ['literal_admiral_short_name']
    legacy = deepcopy(doc); legacy['translation_policy'] = 'natural-dialogue-v1'
    row = next(r for r in doc['records'] if r['message_id'] == 808)
    negatives = {'stale_source': reject(lambda: owned.transform(oc, oa, stale)),
        'stale_current': reject(lambda: owned.transform(oc, oa, wrong_current)),
        'formatting_gate_false': reject(lambda: owned.transform(oc, oa, unreviewed)),
        'wrong_argument_role': reject(lambda: owned.transform(oc, oa, wrong_args)),
        'legacy_policy': reject(lambda: owned.transform(oc, oa, legacy)),
        'authored_indent': reject(lambda: owned.compile_text({**row, 'english': '  Hello, %s.{PAD}'})),
        'authored_break': reject(lambda: owned.compile_text({**row, 'english': 'Hello,\n%s.{PAD}'})),
        'dropped_argument': reject(lambda: owned.compile_text({**row, 'english': 'Hello.{PAD}'})),
        'extra_argument': reject(lambda: owned.compile_text({**row, 'english': 'Hello, %s %s.{PAD}'})),
        'source_command_pair_in_prose': reject(lambda: owned.compile_text({**row, 'english': 'FIRE %s.{PAD}'})),
        'nonprintable': reject(lambda: owned.compile_text({**row, 'english': 'Hello\x7f %s.{PAD}'})),
        'overlong_paragraph': reject(lambda: owned.compile_text({**row, 'english': 'Hello ' * 40 + '%s.{PAD}'})),
        'modal_overflow': reject(lambda: owned.compile_text({'message_id': 267, 'english': 'An excessive system line beyond the original display bounds.{PAD}'}))}
    save(ROOT / 'registered_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm), 'profile': manifest['profile'],
        'all470_batches114_layers_and_prior_graphics_preserved': True,
        'only_COMMON_ARM9_changed_from_V760': True, 'all7336_distinct_warm_cold_copies_and18_final_messages_exact': True,
        'rejections': negatives, 'producer_sha256': sha(Path(__file__).read_bytes()),
        'actual_gameplay_pending': True, 'full_goal_complete': False})
    clean = Path('work/clean.nds'); assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch, rebuilt = ROM.with_suffix('.xdelta'), ROOT / 'patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean, ROM, patch); apply_xdelta(clean, patch, rebuilt)
    assert ROM.read_bytes() == rebuilt.read_bytes()
    save(ROOT / 'patch_proof.json', {'clean_source_sha256': sha(clean.read_bytes()), 'candidate_sha256': sha(ROM.read_bytes()),
        'patch_sha256': sha(patch.read_bytes()), 'byte_exact_reconstruction': True})
    print('Registered V762 preserves all preceding layers/art;7336 copies,18 final messages and13 negative gates pass;clean patch exact. Actual scenes pending.', flush=True)


if __name__ == '__main__': main()
