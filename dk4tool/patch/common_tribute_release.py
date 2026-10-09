"""Source-locked tribute text repack and reviewed resident runtime component."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records

SOURCE_COMMON = '8dd709b8c8e8e35d61b9999191b326e91601029325884fc8289123f3d945147c'
SOURCE_ARM9 = '863776d944118cc12418a91ed32e24cac1755aeac70ace682fdfa0897818b7eb'
BASE = 0x02000000


def runtime_component(arm9, component):
    if sha(arm9) != SOURCE_ARM9 or component.get('source_arm9_sha256') != SOURCE_ARM9:
        raise ValueError('Tribute runtime requires exact complete V142 ARM9')
    code = MainCodeFile(arm9, BASE)
    before = [bytes(section.data) for section in code.sections]
    resident = code.sections[1]
    if resident.ramAddress != 0x01FF8000 or len(resident.data) != 6944 or resident.bssSize:
        raise ValueError('Tribute runtime resident extent differs')
    payload = bytes.fromhex(component['payload_hex'])
    if len(payload) != 652 or sha(payload) != component['payload_sha256']:
        raise ValueError('Complete reviewed tribute runtime payload differs')
    resident.data.extend(payload)
    end = resident.ramAddress + len(resident.data)
    low = (end + 31) & ~31
    if end > 0x01FFA000 or component['reserved_arena_low'] != low:
        raise ValueError('Tribute runtime reservation or overlay bound differs')
    if {row['offset'] for row in component['static_patches']} != {0xB2590, 0x54798, 0x54160, 0xE45E4}:
        raise ValueError('Tribute runtime requires all three hooks and arena reservation')
    expected = bytearray(before[0])
    for row in component['static_patches']:
        at = row['offset']
        old, new = bytes.fromhex(row['source_hex']), bytes.fromhex(row['replacement_hex'])
        if len(old) != 4 or len(new) != 4 or before[0][at:at + 4] != old:
            raise ValueError('Tribute runtime hook source differs')
        code.sections[0].data[at:at + 4] = new
        expected[at:at + 4] = new
    if struct.unpack_from('<I', expected, 0xE45E4)[0] != low:
        raise ValueError('Tribute runtime fails to reserve complete helper extent')
    for at in (code.codeSettingsOffs, code.codeSettingsOffs + 4):
        struct.pack_into('<I', expected, at, struct.unpack_from('<I', before[0], at)[0] + len(payload))
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    if (bytes(loaded.sections[0].data) != expected or bytes(loaded.sections[1].data) != before[1] + payload
            or bytes(loaded.sections[2].data) != before[2] or sha(saved) != component['target_arm9_sha256']):
        raise ValueError('Tribute runtime changes unrelated bytes or reviewed output')
    return saved


def transform(common, arm9, document, component):
    if sha(common) != SOURCE_COMMON:
        raise ValueError('Tribute repack requires exact complete V142 COMMON')
    runtime = runtime_component(arm9, component)
    clean = NdsImage.open('work/clean.nds')
    if sha(Path('work/clean.nds').read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean tribute source differs')
    clean_common = clean.read_file('/COMMON/MESFILE.DK4')
    source = common_message_entries(clean_common, clean.read_file('/__arm9__.bin'))
    rows = document['records']
    if len(rows) != 8 or {row['message_id'] for row in rows} != set(range(76, 84)):
        raise ValueError('All eight complete tribute selections are required')
    encoded = {}
    for row in rows:
        i = row['message_id']
        if bytes.fromhex(row['source_hex']) != source[i].text or (row['block'], row['record']) != (source[i].block, source[i].record_index):
            raise ValueError('Tribute source or native owner differs')
        text = row['english'].removesuffix('{PAD}')
        if '\n' in text or text.count('%s') != (2 if i == 83 else 1):
            raise ValueError('Tribute requires complete unbroken prose and original substitutions')
        encoded[i] = text.encode('cp932')
    blocks = IlnkContainer.parse(clean_common).blocks
    owners = {(source[i].block, source[i].record_index) for i in encoded}
    prefixes = {}
    for owner in owners:
        first = next(e for e in source if (e.block, e.record_index) == owner)
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    return repack_native_records(common, runtime, encoded, prefixes)


def apply_release(common, arm9, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-common-tribute-release-v1' or config.get('status') != 'reviewed-experimental':
        raise ValueError('Tribute release review is incomplete')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Tribute review dependency changed')
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    if (review.get('status') != 'reviewed-native-layout-gameplay-pending'
            or review.get('final_common_sha256') != config['target_common_sha256']
            or review.get('final_arm9_sha256') != config['target_arm9_sha256']):
        raise ValueError('Tribute native layout review differs from final output')
    component = json.loads(Path(config['runtime_component']).read_text(encoding='utf-8'))
    result = transform(common, arm9, document, component)
    if sha(result.common) != config['target_common_sha256'] or sha(result.arm9) != config['target_arm9_sha256']:
        raise ValueError('Tribute complete reviewed output differs')
    return result.common, result.arm9, {'status': 'pass-tribute-repair-gameplay-pending',
        'authored_ids': list(range(76, 84)), 'changed_records': sorted(result.changed_records),
        'changed_offsets': sorted(result.changed_offsets), 'all_native_entries_compared': len(result.entries),
        'expected_common_sha256': sha(result.common), 'expected_arm9_sha256': sha(result.arm9),
        'runtime_verified': False}
