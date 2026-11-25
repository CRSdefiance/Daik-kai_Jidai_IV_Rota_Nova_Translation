"""Prove all native selections before registering the late Refit stage."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_editorial import CONFIG, plan
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from scripts import probe_remaining_common_layout as loader
from scripts.prepare_refit_editorial_v830 import MANUSCRIPT, ROM
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_editorial_v831')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not Path(CONFIG).exists()
    registry_path = Path('translations/release_stack.json')
    save(ROOT / 'registry_before.json', read(registry_path))
    old = NdsImage.open(ROM)
    source_common, source_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    common, arm, proof = plan(source_common, source_arm, read(MANUSCRIPT))
    (ROOT / 'target_COMMON.bin').write_bytes(common)
    (ROOT / 'target_ARM9.bin').write_bytes(arm)
    save(ROOT / 'repack_plan.json', proof)
    print('Source-locked block plan:', proof['repacked_block_range'], 'native IDs:', len(proof['repacked_native_IDs']), flush=True)
    expected = {e.message_id: e.text for e in current_entries(source_common, source_arm)}
    expected.update({r['message_id']: bytes.fromhex(r['compiled_hex'])[:-1] for r in proof['records']})
    previous_factory = loader.machine_for
    loader.machine_for = arm946_machine
    cases = []
    try:
        for message_id in range(3668):
            reports = [loader.warm_copy(arm, common, message_id, expected[message_id], cold_cache=cold) for cold in (False, True)]
            cases.append({'message_id': message_id, 'text_sha256': sha(expected[message_id]),
                          'complete_native_warm_and_cold_guards_and_return_pass': True,
                          'warm_copy_bytes': reports[0]['copied_bytes'],
                          'cold_host_file_contract_reads': reports[1]['host_file_contract_reads']})
            if message_id % 500 == 0:
                print('Native complete warm/cold:', message_id, '/3668', flush=True)
    finally:
        loader.machine_for = previous_factory
    copy_path = ROOT / 'native_copy_proof.json'
    save(copy_path, {'target_common_sha256': sha(common), 'target_arm9_sha256': sha(arm),
                     'all3668_native_IDs_warm_and_cold7336_complete_copies': cases,
                     'native_loader_cache_and_aligned_copy_execute': True,
                     'source_ILNK_reader_host_bridge_not_gameplay_or_hardware': True,
                     'producer_sha256': sha(Path(__file__).read_bytes())})
    font_path = Path('work/analysis/refit_editorial_v830/native_font_verification.json')
    config = {'format': 'dk4-refit-help-editorial-v1',
              'source_common_sha256': sha(source_common), 'source_arm9_sha256': sha(source_arm),
              'target_common_sha256': sha(common), 'target_arm9_sha256': sha(arm),
              'directory_sha256': proof['directory_sha256'],
              'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
              'native_copy_proof': str(copy_path), 'native_font_proof': str(font_path),
              'dependencies': {str(p): sha(Path(p).read_bytes()) for p in (
                  'dk4tool/patch/refit_help_editorial.py', 'dk4tool/dialogue/refit_help.py',
                  'scripts/prepare_item_common_v788.py', 'scripts/prepare_recruitment_common_v772.py',
                  str(copy_path), str(font_path))}}
    save(CONFIG, config)
    registry = read(registry_path)
    assert registry == read(ROOT / 'registry_before.json')
    assert 'all-routes-unified-v831' not in registry['profiles']
    profile = deepcopy(registry['profiles']['all-routes-unified-v829'])
    profile.update(refit_help_editorial=CONFIG, status='experimental',
                   description='Complete V829 stack plus31 freshly reviewed Refit help entries:18 revisions,13 retained;original renderer and memory bounds preserved.',
                   note='Late source-locked COMMON stage after frozen ceremony/levelup/cliff transforms. Actual revised help-panel and startup verification pending.')
    registry['profiles']['all-routes-unified-v831'] = profile
    save(registry_path, registry)
    print('All7336 native copies pass; V831 full profile registered. ROM build and actual panels pending.', flush=True)


if __name__ == '__main__':
    main()
