"""Research-only COMMON executable prefix,33 prose drafts and scoped draw front.

The opaque component precedes the first mapped entry in its existing8KiB block.
Every mapped selection retains its own less-than512byte copy allocation.
No playable ROM or manuscript formatting approval is produced here.
"""
from pathlib import Path
import struct

from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import entries, SINGLE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.sighting_grammar_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.duel_cache_front_v1142 import assemble as front_assemble, ADDRESS as FRONT, END
from scripts.duel_renderer_thumb_v1124 import assemble as renderer_assemble
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_cache_payload_v1144')
ROM = Path('out/all_routes_combined_v1105_candidate.nds')
BASE = 0x02000000


def main():
    assert not ROOT.exists()
    compiler_path = Path('work/analysis/duel_layout_native_v1141b/compiler_provenance.json')
    compiler = read(compiler_path)
    component = Path(compiler['binary']).read_bytes()
    positions = read('work/analysis/duel_PIC_positions_v1143/PIC_native_position_matrix.json')
    assert positions['all14100_positioned_native_cases_pass'] and positions['binary_sha256'] == sha(component)
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '64b1da09fe0f75007af73b0f44a39ce9d2d3c6dedbb70cf6c0ca20223a7f1c29'
    before = current_entries(common, arm)
    source = IlnkContainer.parse(common)
    manuscript_path = Path('translations/duel_editorial_manuscript_v3.json')
    manuscript = read(manuscript_path)
    authored = {}
    for row in manuscript['records']:
        assert all(row['review'][gate] for gate in ('source', 'context', 'localization', 'naturalness'))
        assert not row['review']['formatting']
        text = row['english'].encode('ascii')
        assert text and b'\0' not in text and b'\n' not in text and b'\r' not in text
        assert text.count(b'%s') == row['native_argument_count']
        authored[row['message_id']] = text
    assert set(authored) == set(range(1931, 1957)) | set(range(1973, 1980))
    assert min(row.message_id for row in before if row.block == 20) == 1756
    assert min(row.message_id for row in before if row.block == 22) == 1977
    assert max(row.message_id for row in before if row.block == 22) == 2099
    prefix = component + b'\0' * 4
    assert len(component) == 1480 and len(prefix) == 1484
    groups = {20: list(range(1756, 1931)), 21: list(range(1931, 1977)), 22: list(range(1977, 2100))}
    rebuilt = list(source.blocks)
    target = bytearray(arm)
    fields, opaque = [], {}
    for block, ids in groups.items():
        body = bytearray(prefix if block == 21 else b'')
        for number in ids:
            old = before[number]
            raw_tail = source.blocks[old.block][old.block_offset + len(old.text) + 1:old.copy_end]
            if set(raw_tail) - {0, 32}:
                assert number not in authored
                payload = source.blocks[old.block][old.block_offset:old.copy_end]
                opaque[number] = payload
            else:
                payload = authored.get(number, old.text) + b'\0'
            assert 0 < len(payload) < 512
            at = TABLE_OFFSET + number * 2
            struct.pack_into('<H', target, at, len(body))
            fields.append([at, 2])
            body.extend(payload)
        assert 0 < len(body) <= 8192
        rebuilt[block] = bytes(body)
        at = DIRECTORY_OFFSET + block * 4
        struct.pack_into('<HH', target, at, ids[0], len(body))
        fields.append([at, 4])
    new_common = IlnkContainer(rebuilt).to_bytes()
    directory = sha(target[DIRECTORY_OFFSET:TABLE_OFFSET])
    after = entries(new_common, bytes(target), directory)
    assert len(after) == len(before) == 3668
    assert all(new.text == authored.get(old.message_id, old.text) for old, new in zip(before, after, strict=True))
    assert after[1931].block == 21 and after[1931].block_offset == len(prefix)
    assert all(0 < entry.copy_end - entry.block_offset < 512 for entry in after)
    assert rebuilt[21][:len(component)] == component
    assert all(rebuilt[b] == source.blocks[b] for b in range(41) if b not in groups)
    # Install only the already measured original-function transcription and its
    # own108byte tail. Original cache allocation/getter and native cache ops stay.
    start, end = 0xDA28, 0xDB5C
    transcription = renderer_assemble(arm)
    assert len(transcription) == 200
    front, assembly = front_assemble(len(component))
    assert len(front) == 104
    target[start:end] = transcription + bytes(end - start - len(transcription))
    target[FRONT - BASE:END - BASE] = front + bytes(END - FRONT - len(front))
    original_font_call = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm('blx 0x020d5404', BASE + 0xDA96)[0])
    assert target[0xDA96:0xDA9A] == original_font_call
    target[0xDA96:0xDA9A] = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(f'bl {FRONT}', BASE + 0xDA96)[0])
    assert target[0x535E0:0x535E8] == SINGLE
    assert struct.unpack_from('<I', arm, 0x552A0)[0] == 0x0228E6DC
    assert after[1931].text == authored[1931]
    final = bytes(target)
    assert entries(new_common, final, directory) == after
    restored = bytearray(final)
    for at, size in fields:
        restored[at:at + size] = arm[at:at + size]
    restored[start:end] = arm[start:end]
    assert bytes(restored) == arm
    old_code, new_code = MainCodeFile(arm, BASE), MainCodeFile(final, BASE)
    shape = lambda code: [(section.ramAddress, len(section.data), section.bssSize) for section in code.sections]
    assert shape(old_code) == shape(new_code) and cache_plan(arm) == cache_plan(final)
    assert all(old_code.sections[index].data == new_code.sections[index].data for index in (1, 2, 3, 4))
    assert len(new_code.sections[3].data) - 48 == 123040
    ROOT.mkdir(parents=True)
    common_path, arm_path = ROOT / 'COMMON_RESEARCH_ONLY.DK4', ROOT / 'ARM9_RESEARCH_ONLY.bin'
    common_path.write_bytes(new_common)
    arm_path.write_bytes(final)
    save(ROOT / 'cache_prefix_research_plan.json', {
        'source_ROM': str(ROM), 'source_ROM_sha256': sha(ROM.read_bytes()),
        'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
        'target_COMMON': str(common_path), 'target_COMMON_sha256': sha(new_common),
        'target_ARM9': str(arm_path), 'target_ARM9_sha256': sha(final),
        'directory_sha256': directory, 'metadata_fields': fields,
        'research_manuscript': str(manuscript_path), 'research_manuscript_sha256': sha(manuscript_path.read_bytes()),
        'all33_prose_formatting_gates_remain_false_not_a_release_batch': True,
        'new_code_prefix': {'block': 21, 'carrier_message_ID': 1931,
            'prefix_bytes': len(prefix), 'component_bytes': len(component), 'component_sha256': sha(component),
            'existing_COMMON_owner': 0x0228E6DC, 'existing_single_cache_base': 0x0228E70C,
            'entry': 'duel_draw', 'opaque_executable_data_never_selected_as_a_message': True},
        'block_groups': {str(block): [ids[0], ids[-1], len(rebuilt[block])] for block, ids in groups.items()},
        'all3635_unselected_texts_exact_and_all3668_IDs_copy_spans_valid': True,
        'all_unselected38_blocks_and_all_opaque_tail_payloads_preserved': True,
        'owned_runtime_span': [BASE + start, BASE + end], 'front_bytes': len(front), 'front_assembly': assembly,
        'all_OTHER_ARM9_bytes_and_entire_boot_prefix_exact': True,
        'all_sections_BSS_cache_allocations_arenas_and123040_staged_bytes_exact': True,
        'native_cache_warm_cold_copy_lifetime_CPU_scope_and_MCR_range_proofs_pending': True,
        'not_a_registered_or_playable_ROM': True, 'no_completed_entry_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Research payload prepared:33 drafts plus1484byte opaque prefix in existing block21;104byte exact-scope front;no allocation growth or playable ROM.')


if __name__ == '__main__':
    main()
