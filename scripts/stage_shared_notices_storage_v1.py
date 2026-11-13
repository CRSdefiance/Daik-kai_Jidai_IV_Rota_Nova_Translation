"""Bind reviewed shared-notice layouts to exact COMMON storage in a research ROM."""

import inspect
import struct
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import CAPACITY
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.shared_notice_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.compare_shared_text_source_v1 import DIRECTORY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_literal_notice_formatting_v1 import OUTPUT, run_case
from scripts.preflight_shared_dynamic_notice_wrap_v1 import ROOT as DYNAMIC, manuscript
from scripts.refine_literal_notice_layout_v2 import ROOT as STATIC
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import WRAPPERS, current_copy
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_ship_command_release_v1 import ARM, RELEASE, STARTUP


ROOT = DYNAMIC.with_name('literal_notice_storage_v1')
COMMON = '/COMMON/MESFILE.DK4'


def copy_span(blocks, row):
    return blocks[row.block][row.block_offset:row.copy_end]


def relocate(common, arm, source_rows, storage):
    archive = IlnkContainer.parse(common)
    assert archive.to_bytes() == common
    source = owned_entries(common, arm, DIRECTORY)
    groups = defaultdict(list)
    touched = {source[n].block for n in storage}
    for entry in source:
        if entry.block in touched:
            groups[entry.block].append(entry)
    blocks, target, original_fields = list(archive.blocks), bytearray(arm), {}

    def update_field(offset, value):
        original_fields[offset] = arm[offset:offset + 2]
        struct.pack_into('<H', target, offset, value)

    for block, group in groups.items():
        previous = archive.blocks[block]
        body = bytearray(previous[:group[0].block_offset])
        for entry in group:
            n = entry.message_id
            original = copy_span(archive.blocks, entry)
            payload = original
            if n in storage and storage[n] != entry.text:
                reviewed = source_rows[n]
                assert reference(entry) == reviewed['current_reference']
                assert entry.text.hex() == reviewed['current_hex']
                assert storage[n].count(b'%s') == bytes.fromhex(reviewed['source_hex']).count(b'%s')
                assert b'\0' not in storage[n] and storage[n].isascii()
                payload = storage[n] + b'\0'
                # Preserve the phase of every following record without changing visible text.
                payload += bytes((len(original) - len(payload)) % 2)
            assert len(body) % 2 == entry.block_offset % 2
            assert 0 < len(payload) < 512
            update_field(entry.table_offset, len(body))
            body.extend(payload)
        assert 0 < len(body) <= CAPACITY
        blocks[block] = bytes(body)
        update_field(DIRECTORY_OFFSET + block * 4 + 2, len(body))

    target_arm = bytes(target)
    target_common = IlnkContainer(blocks).to_bytes()
    new_directory = sha256(target_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    rebound = owned_entries(target_common, target_arm, new_directory)
    for old, new in zip(source, rebound, strict=True):
        assert new.message_id == old.message_id and new.block == old.block
        assert new.text == storage.get(old.message_id, old.text)
        if new.text == old.text:
            assert copy_span(blocks, new) == copy_span(archive.blocks, old), old.message_id
    restored = list(blocks)
    for block, group in groups.items():
        restored[block] = blocks[block][:group[0].block_offset] + b''.join(
            copy_span(archive.blocks, entry) if entry.text != rebound[entry.message_id].text
            else copy_span(blocks, rebound[entry.message_id]) for entry in group)
    assert IlnkContainer(restored).to_bytes() == common
    for at, old in original_fields.items():
        target[at:at + 2] = old
    assert bytes(target) == arm
    return target_common, target_arm, rebound, dict(touched_blocks=sorted(touched),
        source_block_lengths={block: len(archive.blocks[block]) for block in groups},
        target_block_lengths={block: len(blocks[block]) for block in groups},
        changed_visible_templates=[n for n in storage if source[n].text != rebound[n].text],
        complete_COMMON_and_ARM9_table_inverse=True, all_unselected_native_copy_spans_exact=True,
        new_directory_sha256=new_directory, native_message_count=len(rebound), native_block_count=len(blocks),
        all_41_blocks_fit_8KiB=all(len(block) <= CAPACITY for block in blocks))


def main():
    assert not ROOT.exists()
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    binding = ctx.receipt()
    static_path, dynamic_path = STATIC / 'layout.json', DYNAMIC / 'native_preflight.json'
    static, dynamic = load(static_path), load(dynamic_path)
    assert dynamic['registered_input'] == binding
    assert static['runtime']['COMMON_sha256'] == binding['COMMON_sha256']
    original, common = ctx.arm, ctx.common
    wrapped, wrapper = transform(original)
    assert wrapper == dynamic['research_transform']
    source_rows = {row['message_ID']: row for row in load(OUTPUT)['records']}
    assert len(source_rows) == 30
    dynamic_rows, decisions = manuscript()
    static_rows = {row['message_ID']: row for row in static['records']}
    assert set(static_rows).isdisjoint(dynamic_rows) and len(static_rows) == 19
    markup = {n: row['provisional_storage_markup'] for n, row in static_rows.items()}
    markup.update({n: row['english'] for n, row in dynamic_rows.items()})
    storage = {n: value.replace('{LB}', '\n').encode('ascii') for n, value in markup.items()}
    ctx.common, ctx.arm, rebound, storage_proof = relocate(common, wrapped, source_rows, storage)
    table = slice(DIRECTORY_OFFSET, TABLE_END)
    assert ctx.raw[table] == original[table]
    raw = bytearray(ctx.raw)
    raw[table] = ctx.arm[table]
    ctx.raw = bytes(raw)
    sections = MainCodeFile(ctx.arm, BASE).sections
    ctx.sections = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]

    # Execute the existing preflight with the loader's actual template pointer intact.
    source = checked_text(inspect.getsource(run_case), {
        '        u.reg_write(UC_ARM_REG_R1, test)':
            '        assert bytes(u.mem_read(ptr, len(template) + 1)) == template + b"\\0"',
        'original_storage_unmodified=True': 'actual_stored_template_pointer_used=True',
        'scratch_template_test_before_widget_creation=True': 'stopped_before_widget_creation=True',
    })
    namespace = dict(run_case.__globals__)
    exec(compile(source, __file__ + '::original-stored-template-pointer', 'exec'), namespace)
    check_case = namespace['run_case']
    cases = [(n, (), row['native_display_hex']) for n, row in static_rows.items()]
    cases.extend((row['message_ID'], row['arguments'], row['native_wrapper_output_hex']) for row in dynamic['records'])
    stored = []
    for n, arguments, expected in cases:
        row = {**source_rows[n], 'english': markup[n], 'current_hex': storage[n].hex()}
        case = check_case(ctx, row, arguments)
        ctx.calls.clear()
        assert case['native_wrapper_output_hex'] == expected, (n, arguments)
        stored.append(case)
    direct = []
    for n, row in source_rows.items():
        for target in sorted({call['target'] for call in row['native_callers']} - set(WRAPPERS)):
            direct.append(current_copy(ctx, {**row, 'current_hex': storage[n].hex()}, target))
            ctx.calls.clear()
    assert len(stored) == 59 and len(direct) == 1
    rom = NdsImage.open(ctx.rompath)
    rom.replace_file(ARM, ctx.arm)
    rom.replace_file(COMMON, ctx.common)
    serialized = bytes(rom.rom.save())
    rom.replace_file(ARM, original)
    rom.replace_file(COMMON, common)
    assert bytes(rom.rom.save()) == ctx.rompath.read_bytes()
    ROOT.mkdir()
    research = ROOT / 'shared_notices_RESEARCH_ONLY.nds'
    research.write_bytes(serialized)
    assert NdsImage.open(research).read_file(COMMON) == ctx.common
    assert NdsImage.open(research).read_file(ARM) == ctx.arm
    references = [dict(message_ID=n, source=source_rows[n]['source_reference'],
        previous=source_rows[n]['current_reference'], target=reference(rebound[n]),
        target_hex=storage[n].hex()) for n in sorted(source_rows)]
    save(ROOT / 'stored_verification.json', dict(registered_input=binding, target=str(research),
        target_sha256=digest(research), storage=storage_proof, runtime_wrapper=wrapper,
        complete_serialized_ROM_parent_inverse=True, stored_cases=stored, direct_lookup_cases=direct,
        exact_record_references=references, final_editorial_amendments=decisions,
        offline_snapshot_changes_limited_to_relocated_catalogue_tables=True,
        no_gameplay_or_release_credit=True, pending_original_gameplay=True,
        evidence={str(p): digest(p) for p in (static_path, dynamic_path, OUTPUT, Path(__file__))}))
    print(f'30 shared notices, {len(stored)} stored formatter cases, {len(direct)} direct lookup. Research ROM only.')


if __name__ == '__main__':
    main()
