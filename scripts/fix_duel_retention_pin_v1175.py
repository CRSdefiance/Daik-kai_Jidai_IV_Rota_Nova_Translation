"""Bind the active ROM pin to its physical E-drive inventory path."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save


def main():
    path = Path('translations/rom_retention_pins.json')
    old_hash = sha(path.read_bytes())
    pins = read(path)
    lexical = Path('out/all_routes_combined_v1166_candidate.nds').absolute()
    physical = Path('E:/Rota Nova translations/Generated/out/all_routes_combined_v1166_candidate.nds')
    digest = sha(physical.read_bytes())
    assert digest == sha(lexical.read_bytes()) == '19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26'
    matches = [row for row in pins if Path(row['path']) == lexical]
    assert len(matches) == 1
    matches[0]['path'] = str(physical)
    save(path, pins)
    receipt = Path('work/analysis/duel_static_completion_v1174/physical_retention_pin_correction.json')
    assert not receipt.exists()
    result = {'reason': 'Retention inventory accepts only physical E-drive paths; the C out path is a junction alias.',
        'before_pins_sha256': old_hash, 'current_pins_sha256': sha(path.read_bytes()),
        'same_ROM_lexical_alias': str(lexical), 'physical_inventory_pin': str(physical), 'ROM_sha256': digest,
        'no_ROM_or_frozen_archive_bytes_changed': True, 'no_cleanup_deletion_applied': True,
        'producer_sha256': sha(Path(__file__).read_bytes())}
    save(receipt, result)
    archive = Path('E:/Rota Nova translations/Editorial review/V1174 Combined V1166 and static duel completion')
    save(archive/'post_checkpoint_physical_retention_pin_correction.json', result)
    print('V1166 pin now names the physical E inventory path; ROM hash unchanged; no deletion.')


if __name__ == '__main__':
    main()
