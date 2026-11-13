"""Source-reviewed promotion prose with bounded post-substitution wrapping."""

from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.verify_village_wrap_v608 import read

IDS = tuple(range(675, 682))
HOOK, STUB = 0x01FFCF50, 0x01FFC664
OLD_STUB = bytes.fromhex('623e83e2060d53e3b73f059a6a0e73e33f02000aac3f05ea00f020e3')


def compile_template(english, message_id):
    text = english.removesuffix('{PAD}')
    slots = 1 if message_id == 675 else 2 if message_id == 681 else 0
    if (not text.isascii() or text != ' '.join(text.split()) or any(c in text for c in '{}')
            or text.count('%s') != slots or '%' in text.replace('%s', '')
            or any(token in text for token in ('FI', 'FA', 'FO', 'FU', 'IC'))):
        raise ValueError('One reviewed paragraph and the exact source product/location substitutions are required')
    if len(text) >= 200:
        raise ValueError('Template exceeds bounded existing runtime scratch')
    return b' ' + text.encode('ascii')


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(row['message_id'] for row in manuscript['records']) == IDS
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    authored, prefixes = {}, {}
    for row in manuscript['records']:
        i = row['message_id']
        assert bytes.fromhex(row['source_hex']) == source[i].text
        assert bytes.fromhex(row['canonical_source_hex']) == accepted[i].text
        assert bytes.fromhex(row['current_text_hex']) == before[i].text
        assert source[i].text.count(b'%s') == (1 if i == 675 else 2 if i == 681 else 0)
        authored[i] = compile_template(row['english'], i)
        owner = before[i].block, before[i].record_index
        first = next(e for e in before if (e.block, e.record_index) == owner)
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    repack = repack_native_records(common, arm, authored, prefixes, generated_linebreaks=True)
    for a, b in zip(before, repack.entries, strict=True):
        assert (a.message_id, a.block, a.record_index) == (b.message_id, b.block, b.record_index)
        assert b.text.rstrip(b' ') == authored.get(a.message_id, a.text).rstrip(b' ')
    original = MainCodeFile(arm, 0x02000000)
    code = MainCodeFile(repack.arm9, 0x02000000)
    section = code.sections[4]
    assert section.ramAddress == 0x01FFC000 and len(section.data) == 4096
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old_hook = bytes(ks.asm('b 0x01ffcbd8', HOOK)[0])
    assert bytes(section.data)[0xF50:0xF54] == old_hook
    assert bytes(section.data)[0x664:0x680] == OLD_STUB
    hook = bytes(ks.asm(f'b {STUB}', HOOK)[0])
    stub = bytes(ks.asm('sub ip,r3,#672; sub ip,ip,#3; cmp ip,#6; bls 0x01ffcf78; b 0x01ffcbd8; nop; nop', STUB)[0])
    assert len(stub) == 28
    section.data[0xF50:0xF54] = hook
    section.data[0x664:0x680] = stub
    result_arm = bytes(code.save())
    after = MainCodeFile(result_arm, 0x02000000)
    # Native offset metadata is already independently constrained by the repacker.
    assert all(bytes(after.sections[i].data) == bytes(MainCodeFile(repack.arm9, 0x02000000).sections[i].data) for i in range(4))
    restored = bytearray(after.sections[4].data)
    restored[0xF50:0xF54], restored[0x664:0x680] = old_hook, OLD_STUB
    assert restored == original.sections[4].data
    assert all(a == b for i, (a, b) in enumerate(zip(blocks, IlnkContainer.parse(repack.common).blocks, strict=True)) if i != 8)
    return repack.common, result_arm, {
        'changed_records': [f'COMMON_MESSAGE_{i}' for i in IDS],
        'changed_native_offset_fields': sorted(repack.changed_offsets),
        'direct_portrait_parent': 0x02054014, 'newly_wrapped_numeric_IDs': list(IDS),
        'all_other_question_and_queued_parents_unchanged': True,
        'owned_hook_and_now_unreferenced_historical_table_stub': [HOOK, STUB, 28],
        'no_section_pool_cache_or_startup_growth': True, 'all_other_message_meaning_preserved': True,
        'original_macro_printf_and_bounded_wrap_helpers_unchanged': True, 'experimental': True}


def apply_release(common, arm, config_path):
    config = read(config_path)
    assert config['format'] == 'dk4-product-pitches-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    common, arm, report = transform(common, arm, read(manuscript))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, report
