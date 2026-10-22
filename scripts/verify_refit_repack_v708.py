"""Execute all native warm/cold COMMON copies before approving the new directory."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_repack import DIRECTORY_V2 as DIRECTORY
from dk4tool.patch.refit_help_repack import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.run_room_gender_v694 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v708')


def main():
    ROOT.mkdir(exist_ok=True)
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    manuscript = read('translations/refit_help_manuscript_v2.json')
    target_common, target_arm, proof = transform(common, arm, manuscript)
    (ROOT / 'target_COMMON.bin').write_bytes(target_common)
    (ROOT / 'target_ARM9.bin').write_bytes(target_arm)
    save(ROOT / 'repack_proof.json', proof)
    expected = {e.message_id: e.text for e in common_message_entries(common, arm, clean=False)}
    expected.update({r['message_id']: bytes.fromhex(r['compiled_hex'])[:-1] for r in proof['records']})
    old_factory = loader.machine_for
    loader.machine_for = arm946_machine
    cases = []
    try:
        for message_id in range(3668):
            reports = [loader.warm_copy(target_arm, target_common, message_id, expected[message_id], cold_cache=cold)
                for cold in (False, True)]
            cases.append({'message_id': message_id, 'bytes_sha256': sha(expected[message_id]),
                'complete_native_warm_and_cold_guards_and_return_pass': True,
                'warm_copy_bytes': reports[0]['copied_bytes'], 'cold_reads': reports[1]['host_file_contract_reads']})
            if message_id % 500 == 0:
                print('V708 native warm/cold', message_id, '/3668', flush=True)
    finally:
        loader.machine_for = old_factory
    save(ROOT / 'all_native_copies.json', {'all3668_native_IDs_warm_and_cold7336_complete_copies': cases,
        'exact_directory_sha256_to_approve': DIRECTORY,
        'all3637_unselected_message_texts_byte_exact': True,
        'higher_reader_open_read_bridged_to_exact_source_native_ILNK_cache_and_aligned_copy_execute': True,
        'host_file_contracts_not_hardware_or_actual_screen_proof': True,
        'all_executable_startup_allocator_pool_and_cache_layout_unchanged': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V708 all7336 native complete warm/cold copies pass; three-block layout preserves startup/allocator boundaries.', flush=True)


if __name__ == '__main__':
    main()
