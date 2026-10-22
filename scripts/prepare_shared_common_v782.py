"""Research-only full paragraphs in the smallest fitting existing block window."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import shared_dialogue_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.context_shared_dialogue_v781 import CURRENT, ROOT as SOURCE
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.review_shared_dialogue_v781 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_integration_v782')


def main():
    doc = read(MANUSCRIPT)
    assert len(doc['records']) == 50 and all(all(r['review'][g] for g in ('source', 'context', 'localization', 'naturalness'))
                                           and not r['review']['formatting'] for r in doc['records'])
    filters = read(ROOT/'caller_filters.json')
    assert len(filters['all150_complete_original_village_selector_cases']) == 150
    assert read(ROOT/'scope_proof.json')['cases'] == 34343
    assert read(ROOT/'consumer_routing.json')['source_callers_select_nonnull_portrait_core_for_these_families']
    rom = NdsImage.open(CURRENT)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    assert sha(arm) == runtime.SOURCE
    old = parser.common_message_entries(common, arm, clean=False)
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    source = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert source[n].text.hex() == row['source_hex'] and accepted[n].text.hex() == row['canonical_source_hex']
        assert old[n].text.hex() == row['current_text_hex']
        text = row['english'].removesuffix('{PAD}')
        assert text == ' '.join(text.split()) and text.isascii() and all(32 <= ord(c) < 127 for c in text)
        assert not any(c in text for c in '{}')
        argc = int(1028 <= n <= 1048)
        assert len(row['source_native_arguments']) == source[n].text.count(b'%s') == text.count('%s') == argc
        assert row['English_argument_source_indices'] == list(range(argc)) and '%' not in text.replace('%s', '')
        authored[n] = b' '+text.encode('ascii')
    assert sorted(authored) == list(range(1020, 1070))
    container = IlnkContainer.parse(common)
    blocks = container.blocks
    low, high = min(old[n].block for n in authored), max(old[n].block for n in authored)
    attempts, chosen = [], None
    for count in range(high-low+1, len(blocks)+1):
        for first in range(max(0, high-count+1), min(low, len(blocks)-count)+1):
            last = first+count-1
            selected = [e for e in old if first <= e.block <= last]
            opaque, valid = {}, True
            for block in range(first, last+1):
                first_entry = next(e for e in selected if e.block == block)
                if set(blocks[block][:first_entry.block_offset]) - {0, 32}:
                    valid = False
                    break
            if not valid:
                continue
            groups, group, body = [], [], bytearray()
            for e in selected:
                tail = blocks[e.block][e.block_offset+len(e.text)+1:e.copy_end]
                payload = authored.get(e.message_id, e.text)+b'\0'
                if set(tail)-{0, 32}:
                    assert e.message_id not in authored, e.message_id
                    payload = blocks[e.block][e.block_offset:e.copy_end]
                    opaque[e.message_id] = payload
                assert len(payload) <= 4096
                if len(body)+len(payload) > 4096:
                    groups.append((group, bytes(body)))
                    group, body = [], bytearray()
                group.append((e.message_id, len(body), payload))
                body.extend(payload)
            groups.append((group, bytes(body)))
            attempts.append({'first': first, 'last': last, 'available_blocks': count, 'needed_blocks': len(groups),
                             'payload_bytes': sum(len(b) for _, b in groups)})
            if len(groups) == count:
                chosen = first, last, selected, opaque, groups
                break
        if chosen is not None:
            break
    assert chosen is not None
    first, last, selected, opaque, groups = chosen
    target = bytearray(arm)
    for at, payload in runtime.code().items():
        offset = at-0x02000000
        target[offset:offset+len(payload)] = payload
    runtime_only = bytes(target)
    rebuilt, fields, mapping = list(blocks), [], []
    for block, (group, body) in zip(range(first, last+1), groups, strict=True):
        rebuilt[block] = body
        at = parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = parser.TABLE_OFFSET+n*2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
            mapping.append({'id': n, 'block': block, 'offset': offset, 'text_hex': authored.get(n, old[n].text).hex(),
                            'complete_payload_hex': payload.hex()})
    target = bytes(target)
    c = IlnkContainer(rebuilt).to_bytes()
    digest = sha(target[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after = local_entries(digest)(c, target, clean=False)
    assert len(after) == len(old) == 3668
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(old, after, strict=True))
    new_blocks = IlnkContainer.parse(c).blocks
    assert all(x == y for i, (x, y) in enumerate(zip(blocks, new_blocks, strict=True)) if not first <= i <= last)
    for n, payload in opaque.items():
        e = after[n]
        assert new_blocks[e.block][e.block_offset:e.copy_end] == payload
    assert all(old[n].text == after[n].text for n in (676, 677))
    restored = bytearray(target)
    for at, size in fields:
        restored[at:at+size] = runtime_only[at:at+size]
    assert bytes(restored) == runtime_only and cache_plan(target) == cache_plan(arm)
    before, final = [MainCodeFile(a, 0x02000000) for a in (arm, target)]
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in final.sections]
    assert bytes(final.save()) == target
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c)
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'prospective_common_repack.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(target), 'directory_sha256': digest,
        'smallest_fitting_contiguous_existing_block_range': [first, last], 'attempts_in_ascending_block_count': attempts,
        'metadata_fields': fields, 'complete_selection_map': mapping, 'selected50': sorted(authored),
        'all3618_other_strings_and_unselected_blocks_exact': True,
        'opaque_payload_IDs': sorted(opaque), 'opaque_payloads_and_user676_677_exact': True,
        'sections_BSS_cache_and_staged_payload_unchanged': True,
        'manuscript_sha256': sha(Path(MANUSCRIPT).read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'production_parser_registry_ROM_and_completion_unchanged': True})
    print(f'50 full paragraphs fit original blocks{first}-{last};3618 other strings,opaque payloads and repaired676/677 exact. Research only.', flush=True)


if __name__ == '__main__':
    main()
