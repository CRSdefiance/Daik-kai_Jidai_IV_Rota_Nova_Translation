"""Source-bound whole-message repack; research only, without parser mutation."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.context_item_diplomacy_v784 import CURRENT
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.review_item_diplomacy_v784 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/item_diplomacy_integration_v788')
RUNTIME = Path('work/analysis/scheme_name_width_v787/WIDTH_RESEARCH_ONLY.bin')
IDS = tuple(range(1070, 1146))


def repack(common, arm, authored):
    entries = parser.common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    low, high = min(entries[n].block for n in authored), max(entries[n].block for n in authored)
    attempts = []
    for count in range(high-low+1, len(blocks)+1):
        for first in range(max(0, high-count+1), min(low, len(blocks)-count)+1):
            last = first+count-1
            selected = [e for e in entries if first <= e.block <= last]
            if any(set(blocks[b][:next(e.block_offset for e in selected if e.block == b)])-{0, 32}
                   for b in range(first, last+1)):
                continue
            opaque, groups, group, body = {}, [], [], bytearray()
            for e in selected:
                payload = authored.get(e.message_id, e.text)+b'\0'
                tail = blocks[e.block][e.block_offset+len(e.text)+1:e.copy_end]
                if set(tail)-{0, 32}:
                    assert e.message_id not in authored
                    payload = blocks[e.block][e.block_offset:e.copy_end]
                    opaque[e.message_id] = payload
                assert len(payload) <= 4096
                if len(body)+len(payload) > 4096:
                    groups.append((group, bytes(body)))
                    group, body = [], bytearray()
                group.append((e.message_id, len(body), payload))
                body.extend(payload)
            groups.append((group, bytes(body)))
            attempts.append({'first': first, 'last': last, 'available_blocks': count,
                             'needed_blocks': len(groups), 'payload_bytes': sum(len(b) for _, b in groups)})
            if len(groups) == count:
                return entries, blocks, first, last, selected, opaque, groups, attempts
    raise AssertionError('Complete reviewed prose does not fit the existing 41-block allocation')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    manuscript = read(MANUSCRIPT)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    assert all(all(r['review'][g] for g in ('source', 'context', 'localization', 'naturalness'))
               and not r['review']['formatting'] for r in manuscript['records'])
    rom = NdsImage.open(CURRENT)
    common, original_arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    arm = RUNTIME.read_bytes()
    width = read(RUNTIME.parent/'native_width_verification.json')
    assert sha(arm) == width['target_ARM9_sha256'] == '23fb7c8ffb3055b71c1d41b41756ad1b0b0903c25e3854ca27306cdfe218d6f7'
    assert sha(original_arm) == 'daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02'
    old = parser.common_message_entries(common, original_arm, clean=False)
    assert old == parser.common_message_entries(common, arm, clean=False)
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    source = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert source[n].text.hex() == row['source_hex'] and accepted[n].text.hex() == row['canonical_source_hex']
        assert old[n].text.hex() == row['current_text_hex']
        text = row['english'].removesuffix('{PAD}')
        assert text == ' '.join(text.split()) and text.isascii() and all(32 <= ord(c) < 127 for c in text)
        assert not any(c in text for c in '{}')
        argc = len(row['source_native_arguments'])
        assert source[n].text.count(b'%s') == text.count('%s') == argc
        assert row['English_argument_source_indices'] == list(range(argc))
        assert '%' not in text.replace('%s', '')
        authored[n] = b' '+text.encode('ascii')
    before, blocks, first, last, selected, opaque, groups, attempts = repack(common, arm, authored)
    target, rebuilt, fields, mapping = bytearray(arm), list(blocks), [], []
    for block, (group, body) in zip(range(first, last+1), groups, strict=True):
        rebuilt[block] = body
        at = parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = parser.TABLE_OFFSET+n*2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
            mapping.append({'id': n, 'block': block, 'offset': offset,
                'text_hex': authored.get(n, before[n].text).hex(), 'complete_payload_hex': payload.hex()})
    c, a = IlnkContainer(rebuilt).to_bytes(), bytes(target)
    directory = sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after = local_entries(directory)(c, a, clean=False)
    assert len(after) == len(before) == 3668
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    assert all(blocks[i] == rebuilt[i] for i in range(41) if not first <= i <= last)
    for n, payload in opaque.items():
        e = after[n]
        assert rebuilt[e.block][e.block_offset:e.copy_end] == payload
    assert all(before[n].text == after[n].text for n in (676, 677))
    restored = bytearray(a)
    for at, size in fields:
        restored[at:at+size] = arm[at:at+size]
    assert bytes(restored) == arm and cache_plan(a) == cache_plan(original_arm)
    code = [MainCodeFile(v, 0x02000000) for v in (original_arm, arm, a)]
    shape = lambda v: [(s.ramAddress, len(s.data), s.bssSize) for s in v.sections]
    assert shape(code[0]) == shape(code[1]) == shape(code[2]) and bytes(code[2].save()) == a
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c)
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(a)
    save(ROOT/'prospective_common_repack.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_COMMON_sha256': sha(common),
        'source_ARM9_sha256': sha(original_arm), 'runtime_research_ARM9_sha256': sha(arm),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'directory_sha256': directory,
        'smallest_fitting_contiguous_existing_block_range': [first, last],
        'attempts_in_ascending_block_count': attempts, 'metadata_fields': fields,
        'complete_selection_map': mapping, 'selected76': list(IDS),
        'all3592_other_strings_and_unselected_blocks_exact': True,
        'opaque_payload_IDs': sorted(opaque), 'opaque_payloads_and_user676_677_exact': True,
        'sections_BSS_cache_and_staged_payload_unchanged': True,
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'runtime_input': str(RUNTIME),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'production_parser_registry_ROM_and_completion_unchanged': True})
    print(f'76 complete paragraphs fit existing blocks {first}-{last}; 3592 other strings, opaque spans and repaired 676/677 preserved. Research only.', flush=True)


if __name__ == '__main__':
    main()
