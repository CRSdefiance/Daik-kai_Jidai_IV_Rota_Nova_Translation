"""Repack eleven source-reviewed reports in COMMON4/23;preserve all other copies."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.hot_spring_notice_editorial import current_entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries, DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import search_reports_runtime_v1659 as runtime
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/search_reports_payload_v1661')
MANUSCRIPT = Path('translations/search_reports_editorial_manuscript_v1.json')
IDS = (312, *range(2217, 2222), *range(2229, 2234))
PROFILE = 'Search-role1-role7-postmacro-and-original-loss-modal-v1'
SOURCE_COMMON = 'f159d3e6ab03d7bf61262e674d009e5661fc6dc1ffba2f357f4af437704a0147'
SOURCE_ARM = runtime.SOURCE


def compiled(row):
    n, text = row['message_id'], row['english']
    if n not in IDS or not text or not text.isascii() or text != ' '.join(text.split()):
        raise ValueError('One unwrapped natural ASCII paragraph required')
    if any(ord(c) < 32 or ord(c) > 126 or c in '{}' for c in text):
        raise ValueError('No authored controls or layout markup')
    count = 1 if n == 312 else 2 if n >= 2229 else 0
    if row['native_argument_count'] != count or text.count('%s') != count or '%' in text.replace('%s', '') or row['source_native_macros']:
        raise ValueError('Preserve the exact original numeric argument count and no added macros')
    role, table = ((None, None) if n == 312 else (7, 0x02116E80) if n >= 2229 else (1, 0x02116EC0))
    if (row['source_role'], row['source_table']) != (role, table):
        raise ValueError('Preserve original role/table or distinct speakerless modal')
    if n == 312 and len(text.replace('%s', '')) + 20 > 35:
        raise ValueError('The loss notice must fit one native35-cell line including a full ten-digit CP932 amount')
    if len(text) >= 160:
        raise ValueError('Longer paragraphs need a separately reviewed native contract')
    return text.encode('ascii')


def plan(common, arm, doc):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    clean, canonical = NdsImage.open('work/clean.nds'), NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path('work/clean.nds').read_bytes()) == doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    before, source = current_entries(common, arm), IlnkContainer.parse(common)
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert row['source_hex'] == jp[n].text.hex() and row['canonical_source_hex'] == base[n].text.hex()
        assert row['current_text_hex'] == before[n].text.hex()
        assert all(row['review'][g] for g in ['source', 'context', 'localization', 'naturalness'])
        authored[n] = compiled(row)
    blocks = {before[n].block for n in IDS}
    assert blocks == {4, 23}
    changed = [n for n in IDS if authored[n] != before[n].text]
    assert changed == list(IDS)
    target, runtime_plan = runtime.apply(arm)
    target, rebuilt, metadata = bytearray(target), list(source.blocks), []
    sizes = {}
    def put(at, value):
        target[at:at+len(value)] = value
        metadata.append({'address': 0x02000000+at, 'source_hex': arm[at:at+len(value)].hex(), 'target_hex': value.hex()})
    for block in sorted(blocks):
        numbers = [r.message_id for r in before if r.block == block]
        assert numbers == list(range(numbers[0], numbers[-1]+1))
        body = bytearray()
        for n in numbers:
            row = before[n]
            payload = source.blocks[block][row.block_offset:row.copy_end]
            assert 0 < len(payload) < 512 and payload.startswith(row.text+b'\0')
            if n in changed:
                assert not set(payload[len(row.text)+1:])-{0, 32}
                payload = authored[n]+b'\0'
            put(TABLE_OFFSET+n*2, struct.pack('<H', len(body)))
            body.extend(payload)
        assert 0 < len(body) <= 8192
        rebuilt[block] = bytes(body)
        put(DIRECTORY_OFFSET+block*4, struct.pack('<HH', numbers[0], len(body)))
        sizes[str(block)] = [len(source.blocks[block]), len(body)]
    a, c = bytes(target), IlnkContainer(rebuilt).to_bytes()
    directory = sha(a[DIRECTORY_OFFSET:TABLE_OFFSET])
    after = owned_entries(c, a, directory)
    assert len(before) == len(after) == 3668
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    assert all(rebuilt[b] == source.blocks[b] for b in range(41) if b not in blocks)
    for n, row in enumerate(before):
        if n not in changed:
            new = after[n]
            assert source.blocks[row.block][row.block_offset:row.copy_end] == rebuilt[new.block][new.block_offset:new.copy_end]
    patches = runtime_plan['patches'] + metadata
    restored = bytearray(a)
    for p in patches:
        at, value = p['address']-0x02000000, bytes.fromhex(p['source_hex'])
        restored[at:at+len(value)] = value
    assert bytes(restored) == arm
    old, new = [MainCodeFile(value, 0x02000000) for value in [arm, a]]
    shape = lambda obj: [(s.ramAddress, len(s.data), s.bssSize) for s in obj.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(a)
    assert all(old.sections[i].data == new.sections[i].data for i in [1, 2, 3, 4])
    assert len(new.sections[3].data)-48 == 123040
    return c, a, {'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
                   'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'directory_sha256': directory,
                   'changed_records': [f'COMMON_MESSAGE_{n}' for n in changed], 'native_IDs': list(IDS),
                   'actual_changed_message_IDs': changed, 'patches': patches, 'runtime_plan': runtime_plan,
                   'all3657_unselected_texts_and_native_copy_spans_preserved': True,
                   'all39_other_blocks_and_opaque_duel_prefix_exact': True,
                   'only_COMMON4_23_metadata_and_existing188_172_runtime_banks_changed': True,
                   'shared_balance_literal_status_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact': True,
                   'old_new_block_bytes': sizes, 'all_ARM9_patches_restore_source_exact': True,
                   'consumer_layout_profile': PROFILE}


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    common, arm, proof = plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    ROOT.mkdir(parents=True)
    cp, ap = ROOT/'COMMON_RESEARCH_ONLY.DK4', ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(common)
    ap.write_bytes(arm)
    save(ROOT/'native_payload_plan.json', {**proof, 'target_COMMON': str(cp), 'target_ARM9': str(ap),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'no_ROM_registry_or_completion_change': True, 'full_goal_complete': False})
    print('Eleven reports repacked in COMMON4/23;3657 other complete copies and39 other blocks exact;186/188 selector,168/172 gate and123040 staged bytes fixed.')
