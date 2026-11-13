"""Strict help/menu title sharing, releasing two former title slots for UI prose."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_help_release import sha
from dk4tool.patch.grand_race_help_release import validate_release_batch as validate_help
from dk4tool.patch.grand_race_menu_release import validate_release_batch as validate_menu

HELP = 'translations/grand_race_help_arm9_v2.json'
MENU = 'translations/grand_race_menu_arm9_v2.json'
SHARED = ((0x1152CC, 0x137AA8, 16, 'GRAND_RACE_UI_ABOUT', 0x137AB8),
          (0x1152DC, 0x1379CC, 12, 'GRAND_RACE_UI_BASIC_RULES', 0x1379D8))


def compile_records(source):
    help_batch = json.loads(Path(HELP).read_text(encoding='utf-8'))
    menu_batch = json.loads(Path(MENU).read_text(encoding='utf-8'))
    validate_help(help_batch, source)
    validate_menu(menu_batch, source)
    menu = {row['id']: row for row in menu_batch['records']}
    released = {old for _, old, _, _, _ in SHARED}
    records = [dict(row) for row in help_batch['records'] if row['offset'] not in released]
    for descriptor, old, size, menu_id, target in SHARED:
        titles = [row for row in help_batch['records'] if row['offset'] == old]
        if len(titles) != 1 or len(bytes.fromhex(titles[0]['source_hex'])) != size:
            raise ValueError('Exact previous help title ownership differs')
        if menu[menu_id]['offset'] != target or menu[menu_id]['english'] != titles[0]['english']:
            raise ValueError('Shared menu/help title is not identical complete English')
        original = source[descriptor:descriptor + 4]
        if original != struct.pack('<I', 0x02000000 + old):
            raise ValueError('Original help title descriptor differs')
        records.append({'id': menu_id + '_SHARED_HELP_TITLE_POINTER', 'offset': descriptor,
                        'source_hex': original.hex().upper(),
                        'replacement_hex': struct.pack('<I', 0x02000000 + target).hex().upper()})
    if len(records) != 18:
        raise ValueError('Shared title variant must retain every complete help page')
    return records


def validate_release_batch(batch, source):
    policy = batch['native_shared_help_titles']
    for key, expected in (('help_batch', HELP), ('menu_batch', MENU)):
        if policy.get(key) != expected or policy.get(key + '_sha256') != sha(Path(expected).read_bytes()):
            raise ValueError('Shared help/title dependency is missing or stale')
    if batch['records'] != compile_records(source):
        raise ValueError('Shared help title records differ from complete reviewed dependencies')
