"""Extend transcription equivalence and prove ownership of its existing code tail."""
from pathlib import Path
import struct

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census
from scripts.probe_duel_thumb_equivalence_v1124 import runner, PROPOSAL, original, START, END, BASE
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_renderer_ownership_v1125')


def main():
    assert not ROOT.exists()
    plan = read(PROPOSAL / 'assembly_proposal.json')
    paired_path = Path('work/analysis/duel_thumb_equivalence_v1124/original_vs_thumb_equivalence.json')
    paired = read(paired_path)
    assert len(paired['cases']) == 159 and paired['all159_original_vs_research_context_widget_macro_scope_and_timing_pairs_pass']
    rom = NdsImage.open(original.ROM)
    arm = rom.read_file('/__arm9__.bin')
    proposed = (PROPOSAL / 'proposed_ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == plan['source_ARM9_sha256'] and sha(proposed) == plan['research_ARM9_sha256']
    replacement = proposed[START - BASE:END - BASE]
    font_return = paired['new_Thumb_font_return']
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    actor = catalog['names'][0]
    texts = [b'Alpha.', b'Alpha.\nBeta.', b'Alpha.\nBeta.\nGamma.',
             b'Alpha.\nBeta.\nGamma.\nDelta.', b'\nAlpha.', b'Alpha.\n', b'',
             b'  Alpha.  Beta.', b'\x82\x65ernando', b'\x82\x65ernando\nNext row.',
             b'X' * 51, b'Alpha.\n\nGamma.']
    cases = []
    ROOT.mkdir(parents=True)
    for timing, delay, key in (('timed60', 60, 0), ('wait61_no_key', 0, 0), ('wait_key_first', 0, 1)):
        source_call, source_observations = runner(arm, raw, replacement, False, delay, key, BASE + 0xDAC4)
        target_call, target_observations = runner(arm, raw, replacement, True, delay, key, font_return)
        for text in texts:
            args = (arm, raw, actor['object'], bytes.fromhex(actor['name_hex']),
                    'direct_negative', 0, 1939, text)
            a = source_call(*args, direct=True)
            b = target_call(*args, direct=True)
            left, right = source_observations[-1], target_observations[-1]
            assert left['native_contexts'] == right['native_contexts'], (timing, text)
            assert left['engine_calls'] == right['engine_calls']
            assert a['expanded_hex'] == b['expanded_hex']
            assert not a['selected_by_proposed_scope'] and not b['selected_by_proposed_scope']
            assert bytes(left['cpu'].mem_read(0x02460214, 0x200)) == bytes(right['cpu'].mem_read(0x02460214, 0x200))
            context = bytes.fromhex(left['native_contexts'][0]['complete_native_context_hex'])
            y = struct.unpack_from('<i', context, 40)[0]
            if text == b'Alpha.':
                assert y == 12
            elif text in (b'Alpha.\nBeta.', b'Alpha.\nBeta.\nGamma.'):
                assert y == 0
            cases.append({'timing': timing, 'input_hex': text.hex(), 'native_Y': y,
                          'complete76byte_context_widget_macro_wait_and_callee_saved_ABI_exact': True})
            left.pop('cpu'); right.pop('cpu')
    assert len(cases) == 36
    spans = [[START, END]]
    refs_before = census(rom, spans, spans)
    after_rom = NdsImage.open(original.ROM)
    after_rom.rom.arm9 = proposed
    refs_after = census(after_rom, spans, spans)
    external = [row for row in refs_before if not row[-1]]
    assert external == [['ARM_branch', 'section0', BASE + 0xD4B8, START, False],
                        ['ARM_branch', 'section0', BASE + 0xD524, START, False]]
    assert external == [row for row in refs_after if not row[-1]]
    assert not rom.rom.arm7OverlayTable
    old, new = MainCodeFile(arm, BASE), MainCodeFile(proposed, BASE)
    shape = lambda code: [(section.ramAddress, len(section.data), section.bssSize) for section in code.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(proposed)
    assert all(old.sections[index].data == new.sections[index].data for index in (1, 2, 3, 4))
    assert len(new.sections[3].data) - 48 == 123040
    restored = bytearray(proposed)
    restored[START - BASE:END - BASE] = arm[START - BASE:END - BASE]
    assert bytes(restored) == arm
    code_end = START + plan['transcription_bytes'] - 12
    instructions = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(proposed[START - BASE + 8:code_end - BASE], START + 8))
    assert sum(instruction.size for instruction in instructions) == code_end - START - 8
    assert all(instruction.size == 2 or instruction.mnemonic == 'blx' for instruction in instructions)
    assert all(instruction.bytes != b'\x00\xbf' for instruction in instructions)
    assert instructions[-1].mnemonic == 'pop' and 'pc' in instructions[-1].op_str
    tail = [START + plan['transcription_bytes'], END]
    assert tail == [0x0200DAF0, 0x0200DB5C]
    assert proposed[tail[0] - BASE:tail[1] - BASE] == bytes(108)
    assert not any(tail[0] <= row[3] < tail[1] for row in refs_after)
    proof_path = ROOT / 'owned_function_transcription_and_tail.json'
    save(proof_path, {
        'source_proposal': str(PROPOSAL / 'assembly_proposal.json'),
        'source_ARM9_sha256': sha(arm), 'research_ARM9_sha256': sha(proposed),
        'original159_pairs': str(paired_path), 'additional36_empty_multiline_CP932_spacing_and_width_controls': cases,
        'all195_context_widget_macro_timing_and_callee_saved_pairs_pass': True,
        'source_and_research_incoming_reference_census': [refs_before, refs_after],
        'only_two_external_calls_preserved_both_target_original_ARM_entry': external,
        'all_main_autoload_staged_code_overlays_and_ARM7_scanned_ARM7_has_no_overlays': True,
        'original_function_owned_span': spans[0], 'private_tail_for_future_formatter': tail,
        'tail_ownership_derives_from_transcribed_function_not_zero_byte_search': True,
        'all_tail_references_absent_and_preceding_return_and_literal_pool_bounded': True,
        'ARM_entry_8bytes_Thumb1_or_ARMv5_BLX_only': [[instruction.address, instruction.bytes.hex(), instruction.mnemonic, instruction.op_str]
                                                   for instruction in instructions],
        'shape_before_after': [shape(old), shape(new)],
        'all_sections_BSS_cache_and_entire123040byte_staged_payload_exact': True,
        'restoring_only_original308byte_function_recovers_every_ARM9_byte': True,
        'models': ['message loader', 'SDK clear', 'UI registration', 'font boundary', 'engine yield/event/key/sound'],
        'still_research_transcription_not_formatter_or_playable_ROM_or_actual_gameplay': True,
        'no_new_completed_entries': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    path = Path('translations/editorial_review_current_v1.json')
    ledger = read(path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(research_renderer_transcription=str(PROPOSAL / 'assembly_proposal.json'),
        renderer_equivalence_and_owned_tail=str(proof_path),
        renderer_owned_tail108_bytes_with_original_stack_footprint=True,
        formatting_status='source-name-fonts-and-research-transcription-pass;formatter-implementation-integration-and-actual-open')
    save(path, ledger)
    print('195 paired renderer checks pass;108 owned function-tail bytes verified;staged memory and playable ROM unchanged.')


if __name__ == '__main__':
    main()
