"""Controlled portrait-dialogue pagination research; never a playable release."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO, helper
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, wrapper
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link
from scripts.revalidate_name_migration_v276 import ARM9, DIGEST, ROM, name_fields
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path('work/analysis/dialogue_pagination_v288')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == DIGEST
    image = NdsImage.open(ROM)
    source = image.read_file('/__arm9__.bin')
    assert sha(source) == ARM9
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    named, names = name_fields(source, clean)
    code = MainCodeFile(named, BASE)
    original = [bytes(s.data) for s in code.sections]
    payload = bytearray(original[3][:-48])
    key = IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks[44].split(b'\0')[179]
    assert key[0] == 6
    manuscript = json.loads(Path('translations/confirmed_name_editorial_v287.json').read_text(encoding='utf-8'))
    paragraph = next(r for r in manuscript['records'] if r['id'] == 'DK4_MES_B298_R0046')
    target = bytes.fromhex(paragraph['compiled_target_hex'])
    assert target[0] == 8 and target.count(b'\n') == 4
    target = b'\x06' + target[1:]
    entries = []

    def store(raw):
        payload.extend(bytes(-len(payload) % 4))
        pointer = POOL + len(payload)
        payload.extend(raw + b'\0')
        return pointer

    for before, after in [(key, target), (key[1:], target[1:])]:
        entries.append((store(before), store(after), len(before) + 1))
    payload.extend(bytes(-len(payload) % 4))
    table = POOL + len(payload)
    for entry in entries:
        payload.extend(struct.pack('<3I', *entry))
    entry = POOL + len(payload)
    payload.extend(helper(entry, table, len(entries)))
    for field in CALLS:
        assert struct.unpack_from('<I', source, field)[0] == branch_link(BASE + field, MACRO)
        struct.pack_into('<I', code.sections[0].data, field, branch_link(BASE + field, entry))
    payload.extend(bytes(-len(payload) % 32))
    size = len(payload) + 64
    assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
    payload.extend(wrapper(STAGE + len(payload), STAGE + size, size, named))
    code.sections[3].data = payload + original[3][-48:-4] + struct.pack('<I', size)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    initialized(saved)
    parsed = MainCodeFile(saved, BASE)
    restore = bytearray(parsed.sections[0].data)
    for field in (*CALLS, 0x8E4, 0xE45DC):
        restore[field:field + 4] = original[0][field:field + 4]
    at = code.codeSettingsOffs
    restore[at:at + 12] = original[0][at:at + 12]
    assert restore == original[0]
    assert all(bytes(parsed.sections[i].data) == original[i] for i in (1, 2))
    assert bytes(parsed.sections[3].data[:len(original[3]) - 48]) == original[3][:-48]
    image.replace_file('/__arm9__.bin', saved)
    fixture = ROOT / 'five_line_portrait_research_only.nds'
    image.save(fixture)
    schedule = json.loads(Path('work/emulation_v193/name_editorial_v280_rafael/capture_report.json').read_text(encoding='utf-8'))['scripted_input_schedule']
    schedule = [r for r in schedule if r['start'] < 4000]
    (ROOT / 'opening_inputs.json').write_text(json.dumps(schedule, indent=2) + '\n', encoding='utf-8')
    manifest = {'format': 'dk4-controlled-portrait-pagination-research-v288',
                'research_ROM': str(fixture), 'research_ROM_sha256': sha(fixture.read_bytes()),
                'source_ROM': str(ROM), 'source_ROM_sha256': DIGEST,
                'controlled_prompt': '/data/SC0.DK4 B44R179',
                'original_prompt_key_hex': key.hex(), 'complete_target_hex': target.hex(),
                'source_paragraph': '/data/SC0.DK4 B298R0046',
                'original_scene_not_a_legitimate_shadow_puzzle_context': True,
                'original_Julio_actor6_retained': True, 'name_fields': names,
                'all_other_files_graphics_routes_and_native_macro_renderer_preserved': True,
                'native_startup_pool_cache_and_preservation_pass': True,
                'actual_five_line_display_and_input_pending': True,
                'not_for_playable_handoff': True, 'full_goal_complete': False}
    (ROOT / 'fixture_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Controlled five-line portrait fixture prepared; original actor, graphics and renderer retained.')


if __name__ == '__main__':
    main()
