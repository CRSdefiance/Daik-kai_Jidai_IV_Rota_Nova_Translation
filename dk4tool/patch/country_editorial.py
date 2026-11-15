"""Complete country prose in unchanged native blocks and portrait allocations."""

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

IDS = tuple(range(688, 709))
STUB = 0x01FFC664
OLD = 'sub ip,r3,#672; sub ip,ip,#3; cmp ip,#6; bls 0x01ffcf78; b 0x01ffcbd8; nop; nop'
NEW = 'sub ip,r3,#688; cmp ip,#20; bls 0x01ffcf78; add ip,ip,#13; cmp ip,#6; bls 0x01ffcf78; b 0x01ffcbd8'


def compile_paragraph(english):
    text = english.removesuffix('{PAD}')
    if (not text or not text.isascii() or text != ' '.join(text.split())
            or any(c in text for c in '{}%') or len(text) >= 200
            or any(token in text for token in ('FI', 'FA', 'FO', 'FU', 'IC'))):
        raise ValueError('Country prose requires one safe ASCII paragraph without authored layout or substitutions')
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
        assert b'%' not in source[i].text
        authored[i] = compile_paragraph(row['english'])
        owner = before[i].block, before[i].record_index
        first = next(e for e in before if (e.block, e.record_index) == owner)
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    result = repack_native_records(common, arm, authored, prefixes)
    code = MainCodeFile(result.arm9, 0x02000000)
    snapshot = [bytes(s.data) for s in code.sections]
    assert code.sections[4].ramAddress == 0x01FFC000 and len(snapshot[4]) == 4096
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old, new = (bytes(ks.asm(s, STUB)[0]) for s in (OLD, NEW))
    assert len(old) == len(new) == 28 and snapshot[4][0x664:0x680] == old
    code.sections[4].data[0x664:0x680] = new
    target_arm = bytes(code.save())
    after_code = MainCodeFile(target_arm, 0x02000000)
    assert all(bytes(after_code.sections[i].data) == snapshot[i] for i in range(4))
    restored = bytearray(after_code.sections[4].data)
    restored[0x664:0x680] = old
    assert restored == snapshot[4]
    after = common_message_entries(result.common, target_arm, clean=False)
    for a, b in zip(before, after, strict=True):
        assert (a.message_id, a.block, a.record_index) == (b.message_id, b.block, b.record_index)
        assert b.text.rstrip(b' ') == authored.get(a.message_id, a.text).rstrip(b' ')
    assert all(a == b for i, (a, b) in enumerate(zip(blocks, IlnkContainer.parse(result.common).blocks, strict=True)) if i not in (8, 9))
    assert len(common) == len(result.common) and len(arm) == len(target_arm)
    return result.common, target_arm, {
        'changed_records': [f'COMMON_MESSAGE_{i}' for i in IDS],
        'changed_native_offset_fields': sorted(result.changed_offsets),
        'newly_wrapped_direct_portrait_IDs': list(IDS), 'retained_promotion_scope': [675, 681],
        'owned28_byte_existing_dispatch_stub': STUB,
        'all3668_IDs_NUL_owners_block_sizes_and39_other_blocks_preserved': True,
        'all_other_visible_prose_and_prior21_revisions_preserved': True,
        'all_startup_sections_fonts_pool_allocator_and_helper_extents_preserved': True,
        'experimental': True}


def apply_release(common, arm, config_path):
    config = read(config_path)
    assert config['format'] == 'dk4-country-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    common, arm, report = transform(common, arm, read(manuscript))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, report
