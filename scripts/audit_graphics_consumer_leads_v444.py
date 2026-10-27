"""Reconcile unresolved open-call leads with exact current code and native traces."""

import json
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/legacy_review_v444')
ROM = Path('out/all_routes_combined_v443_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = current.read_file('/__arm9__.bin')
    main = bytes(MainCodeFile(arm, 0x02000000).sections[0].data)
    source = bytes(MainCodeFile(clean.read_file('/__arm9__.bin'), 0x02000000).sections[0].data)
    ranges = [(0x28B74, 0x28BAC), (0xB7158, 0xB7294), (0xD0398, 0xD0518),
              (0xFDED0, 0xFDF00), (0x100310, 0x100390)]
    assert all(main[lo:hi] == source[lo:hi] for lo, hi in ranges)
    disassembler = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    contexts = []
    for address in (0x020B7178, 0x020D0474, 0x02100348):
        contexts.append({'open_call': address, 'instructions': [
            {'address': i.address, 'assembly': i.mnemonic + ' ' + i.op_str}
            for i in disassembler.disasm(main[address - 0x02000000 - 24:address - 0x02000000 + 4], address - 24)]})
    dynamic_path = Path('work/analysis/image_registry_v385/dynamic_loader_proof.json')
    dynamic = read(dynamic_path)
    assert len(dynamic['dynamic_event_and_town_files']) == 300
    assert all(row['all_header_palette_pixels_exact'] and
               sha(current.read_file(row['path'])) == row['whole_PXL_sha256']
               for row in dynamic['dynamic_event_and_town_files'])
    stream_path = Path('work/analysis/fls_stream_v310/proof.json')
    stream = read(stream_path)
    previous = NdsImage.open(stream['candidate'])
    assert sha(Path(stream['candidate']).read_bytes()) == stream['candidate_sha256']
    assert arm[0xFD178:0x10044C] == previous.read_file('/__arm9__.bin')[0xFD178:0x10044C]
    assert len(stream['cases']) == 15
    for case in stream['cases']:
        assert case['native_constructor_and_full_stream_parser_return_pass']
        assert {0x020FDED0, 0x02100310, 0x02100348} <= set(case['executed_native_addresses'])
        assert current.read_file(case['path']) == previous.read_file(case['path'])
    callers = []
    for offset in range(0, len(main) - 3, 4):
        word = struct.unpack_from('<I', main, offset)[0]
        if word & 0x0F000000 != 0x0B000000:
            continue
        displacement = word & 0xFFFFFF
        if displacement & 0x800000:
            displacement -= 0x1000000
        if 0x02000000 + offset + 8 + displacement * 4 == 0x020D0398:
            callers.append(0x02000000 + offset)
    assert len(callers) == 11
    proof = {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'all_selected_code_ranges_exact_clean': ranges,
        'SDK_open_call_argument_contexts': contexts,
        'lead_classifications': [
            {'call': 0x020B7178, 'entry': 0x020B7158, 'classification': 'PXL event/town staging loader',
             'argument': 'entry r1 preserved in r4, then passed as SDK r1',
             'actual_native_proof': str(dynamic_path), 'proof_sha256': sha(dynamic_path.read_bytes()),
             'all300_current_files_exact_to_native_load_evidence': True,
             'direct_parents': [0x02028B9C, 0x020B7284]},
            {'call': 0x020D0474, 'entry': 0x020D0398, 'classification': 'general file wrapper, disk mode0',
             'argument': 'entry r1 preserved in r4, then passed as SDK r1',
             'all11_aligned_main_code_direct_callers': callers,
             'not_a_separate_raw_graphics_viewer': True,
             'deeper_filename_and_consumer_tracing_remains_open': True},
            {'call': 0x02100348, 'entry': 0x02100310, 'classification': 'FLS stream file opener',
             'argument': 'FDED0 forwards caller r1;100310 preserves it in r4 before SDK open',
             'actual_native_proof': str(stream_path), 'proof_sha256': sha(stream_path.read_bytes()),
             'all15_original_stream_traces_include_this_exact_call': True,
             'all15_current_FLS_files_and_stream_code_exact_to_native_evidence': True},
        ],
        'raw_frame6_brown_marks': {
            'source_extraction': str(ROOT / 'frame6_source.png'),
            'source_extraction_sha256': sha((ROOT / 'frame6_source.png').read_bytes()),
            'visual_review': 'Magnified source pixels resemble handwritten marks; exact reading is unconfirmed. Retain source pixels; do not invent English.',
            'translation_or_identity_gate_cleared': False,
        },
        'scope': 'Reuses explicitly bounded native evidence only after current code/resource byte equality. No new playback or raw-comic display is claimed; generic and indirect consumers remain open.',
        'ROM_changed': False, 'all18_plaques_incomplete': True, 'full_goal_complete': False,
    }
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'consumer_leads_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Three file-open leads classified;300 PXL and15 FLS evidence bindings match V443. Raw/indirect consumers remain open.')


if __name__ == '__main__':
    main()
