"""Reversible B194 paragraph relocation with every source command and four native skips."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B194_relocation_v5506')
DOC = Path('translations/lil_B194_editorial_manuscript_v3.json')
OWNER, STREAM, RESULT, LENGTH = 0x02650000, 0x02660000, 0x02668000, 0x02668100


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(DOC)
    assert all(doc['review_gates'].values()) and len(doc['records']) == 11
    image = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    arm = image.read_file('/__arm9__.bin')
    assert sha(arm) == doc['required_runtime_ARM9_sha256']
    container = IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    for key in ['source_context', 'branch_proof', 'native_font_proof']:
        assert sha(Path(doc[key]).read_bytes()) == doc[key + '_sha256']
    context, branches, font = [read(doc[k]) for k in ['source_context', 'branch_proof', 'native_font_proof']]
    assert len(context['blocks']) == 1
    spec = context['blocks'][0]
    assert spec['block'] == 194
    source = container.blocks[194]
    assert sha(source) == spec['current_block_sha256']
    old_end = 8 + struct.unpack_from('<H', source, 4)[0]
    assert len(source) == old_end == 540
    commands = spec['all_current_native_commands']
    assert len(commands) == 21 and sum(c['word'] == 0x4000 for c in commands) == 11
    assert [c['offset'] for c in commands if c['word'] == 0x8000] == [312]
    assert [c['offset'] for c in commands if c['word'] == 0xC200] == [494, 534]
    assert [c['offset'] for c in commands if c['word'] == 0x632A] == [406]
    fonts = {r['id']: r for r in font['cases']}
    patches, texts = [], []
    for row in doc['records']:
        assert row['block'] == 194
        at = row['current_reference']['offset']
        old = bytes.fromhex(row['current_hex'])
        value = bytes.fromhex(fonts[row['id']]['encoded_hex'])
        assert source[at:at + len(old)] == old
        pad = len(value) % 2 != len(old) % 2
        if pad:
            value += b' '
        assert b'\0' not in value and value[:1] == old[:1]
        assert len(value) % 2 == len(old) % 2
        assert value.count(b'FI') == old.count(b'FI')
        assert not any(m in value for m in [b'FA', b'FO'])
        patches.append(dict(start=at, end=at + len(old), value=value, old=old))
        texts.append(dict(id=row['id'], record_index=row['current_record_index'], old_offset=at,
                          old_length=len(old), new_length=len(value), parity_space_added=pad,
                          target_hex=value.hex()))
    patches.sort(key=lambda p: p['start'])
    assert all(a['end'] <= b['start'] for a, b in zip(patches, patches[1:]))

    def mapped(offset):
        delta = 0
        for p in patches:
            if offset < p['start']:
                break
            if p['start'] < offset < p['end']:
                raise ValueError('Interior reference into replaced text: ' + str(offset))
            if offset == p['start']:
                return offset + delta
            delta += len(p['value']) - len(p['old'])
        return offset + delta

    parts, last = [], 0
    for p in patches:
        parts.extend([source[last:p['start']], p['value']])
        last = p['end']
    parts.append(source[last:old_end])
    logical = bytearray(b''.join(parts))
    assert len(logical) == mapped(old_end) and len(logical) < 0x2400
    fixups = []
    for edge in branches['operands_requiring_adjustment_when_resizing']:
        assert edge['block'] == 194
        start, end = mapped(edge['offset']), mapped(edge['matched_skip_target'])
        span = end - start - 4
        assert 0 <= span <= 0xFFFF and span % 2 == 0
        assert struct.unpack_from('<H', logical, start)[0] == edge['word']
        old_span = struct.unpack_from('<H', source, edge['span_field_offset'])[0]
        struct.pack_into('<H', logical, start + 2, span)
        fixups.append({**edge, 'new_offset': start, 'new_unmatched_next': start + 4,
                       'new_matched_skip_target': end, 'source_span': old_span, 'target_span': span})
    assert len(fixups) == 4
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    target = bytes(logical) + b'\0' * (-len(logical) % 4)
    assert source[6:16] == target[6:16]
    inventory, walker, inventory_source = scoped_inventory()
    target_commands, target_speeches = inventory(arm, target)
    assert len(target_commands) == 21 and len(target_speeches) == 11
    by_offset = {r['offset']: r for r in target_commands}
    boundaries = set(by_offset) | {len(logical)}
    command_map = []
    for old in commands:
        new = by_offset[mapped(old['offset'])]
        assert new['word'] == old['word']
        assert new['ancestor_0100_offsets'] == [mapped(a) for a in old['ancestor_0100_offsets']]
        if old['word'] not in [0x100, 0x200, 0x300, 0x4000]:
            assert source[old['offset']:old['offset'] + old['native_extent']] == target[new['offset']:new['offset'] + new['native_extent']]
        command_map.append(dict(word=old['word'], old_offset=old['offset'], new_offset=new['offset'],
                                old_extent=old['native_extent'], new_extent=new['native_extent']))
    cpu = machine(arm)
    cpu.mem_write(STREAM - 16, b'\xa5' * (len(target) + 32))
    cpu.mem_write(STREAM, target)
    main_before = bytes(cpu.mem_read(0x02000000, 0x400000))
    cases = []
    for edge in fixups:
        assert edge['new_unmatched_next'] in boundaries and edge['new_matched_skip_target'] in boundaries
        for prior in [0, 1, 2, 3, 0xFFFFFFFF]:
            cpu.mem_write(OWNER - 16, b'\xa5' * 64)
            cpu.mem_write(OWNER, struct.pack('<4I', 0, STREAM + edge['new_offset'], 0, 0))
            owner_before = bytes(cpu.mem_read(OWNER - 16, 64))
            cpu.mem_write(RESULT - 16, b'\xa5' * 64)
            cpu.mem_write(RESULT, bytes(24))
            cpu.mem_write(LENGTH - 16, b'\xa5' * 36)
            cpu.mem_write(LENGTH, bytes(4))
            call(cpu, 0x2A510, (RESULT, OWNER, LENGTH, prior))
            extent = struct.unpack('<I', cpu.mem_read(LENGTH, 4))[0]
            take = edge['word'] == 0x100 or (edge['word'] == 0x200 and prior == 0) or (edge['word'] == 0x300 and prior == 1)
            assert edge['new_offset'] + extent == (edge['new_matched_skip_target'] if take else edge['new_unmatched_next'])
            assert struct.unpack('<6I', cpu.mem_read(RESULT, 24)) == (3, 0, 0, 0, 0, 0)
            assert bytes(cpu.mem_read(OWNER - 16, 64)) == owner_before
            assert bytes(cpu.mem_read(STREAM, len(target))) == target
            assert bytes(cpu.mem_read(0x02000000, 0x400000)) == main_before
            for p in [STREAM - 16, STREAM + len(target), RESULT - 16, RESULT + 24, LENGTH - 16, LENGTH + 4]:
                assert bytes(cpu.mem_read(p, 16)) == b'\xa5' * 16
            cases.append(dict(new_offset=edge['new_offset'], last_result=prior, native_extent=extent,
                              source_target_preserved_at_mapped_native_boundary=True,
                              ABI_all4MiB_owner_stream_result_length_and_guards_exact=True))
    for row in texts:
        at = row['new_offset'] = mapped(row['old_offset'])
        row['new_record_index'] = target[:at].count(b'\0')
        assert target[at - 5:at] == source[row['old_offset'] - 5:row['old_offset']] == b'\0\x40\xff\xff\0'
        assert target[at:at + row['new_length']].hex() == row['target_hex']
        assert target[at + row['new_length']] == 0
    end_maps = [dict(source_offset=536, target_offset=mapped(536), extent=4, source_four_zero_bytes_exact=True)]
    assert target[mapped(536):mapped(536) + 4] == bytes(4) and mapped(536) + 4 == len(logical)
    restored = bytearray(target[:len(logical)])
    struct.pack_into('<H', restored, 4, old_end - 8)
    for edge in fixups:
        struct.pack_into('<H', restored, edge['new_offset'] + 2, edge['source_span'])
    for p in reversed(patches):
        at = mapped(p['start'])
        restored[at:at + len(p['value'])] = p['old']
    assert bytes(restored) == source
    ROOT.mkdir(parents=True)
    (ROOT / 'explicit_unmatched_native_walk.py.txt').write_text(walker, encoding='utf-8')
    file = ROOT / 'SC2_block194_RESEARCH_ONLY.bin'
    file.write_bytes(target)
    block = dict(block=194, source_block_sha256=sha(source), research_block_sha256=sha(target),
                 source_bytes=len(source), research_bytes=len(target), source_logical_end=old_end,
                 research_logical_end=len(logical), unowned_appended_copy=None,
                 original2000_pause_and_resume_maps=[], original_declared_end_word_maps=end_maps,
                 text_records=texts, actor_style_commands=[], choice_commands=[], relative_skip_fixups=fixups,
                 target_native_skip_cases=cases, command_map=command_map,
                 all_nested_original_command_types_ancestors_and_opaque_bytes_preserved=True,
                 inverse_restoration_recovers_every_original_logical_byte=True,
                 inverse_recovers_entire_source_without_source_tailzeros=True, research_block=str(file),
                 external_entry_and_actual_revised_paths_approval_pending=True)
    target_blocks = list(container.blocks)
    target_blocks[194] = target
    assert len(target_blocks) == 336
    assert all(a == b for i, (a, b) in enumerate(zip(container.blocks, target_blocks, strict=True)) if i != 194)
    prospective = IlnkContainer(target_blocks).to_bytes()
    target_file = ROOT / 'SC2_RESEARCH_ONLY.DK4'
    target_file.write_bytes(prospective)
    save(ROOT / 'nested_source_relocation_research.json', dict(
        candidate=doc['current_ROM'], candidate_sha256=doc['current_ROM_sha256'], manuscript=str(DOC),
        manuscript_sha256=sha(DOC.read_bytes()), choices=None, choices_sha256=None,
        no_source2100_or4100_objects=True, source_context=doc['source_context'], source_branch_proof=doc['branch_proof'],
        target_SC2=str(target_file), target_SC2_sha256=sha(prospective), source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        blocks=[block], all11_speeches_and6_nonrelative_leaves_preserved=True,
        all4_source_relative_sites_and20_native_skip_cases_preserved=True, all335_other_SC2_blocks_exact=True,
        one_original_FI_preserved=True, predicate_alignment_recheck_pending=True,
        explicit_unmatched_native_walk=walker, unchanged_inventory_function=inventory_source,
        predicates_typed_dispatch_final_parity_fonts_external_references_and_sampling_pending=True,
        no_source2000_pause_commands=True, source_FE_system_objects=1, no_source_dynamic_speaker_objects=True,
        single_declared_tail_endword_exact=True, external_references_complete=False,
        not_a_release_relocation_map=True, no_ROM_registry_or_completion_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(dict(source_bytes=len(source), target_stored_bytes=len(target), target_logical_bytes=len(logical),
               commands=21, speeches=11, relative_sites=4, native_skip_cases=len(cases),
               target_predicate=mapped(312), target_predicate_operand_alignment=(mapped(312) + 4) % 4,
               target_resource42=mapped(406), target_C200=[mapped(494), mapped(534)], target_end=mapped(536), credit=0))
