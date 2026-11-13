"""Review COMMON742 with every original product-to-item prerequisite pair.

Research-only preparation. No playable release or gameplay completion is claimed.
"""

import struct
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.specialty_question_editorial import wrap_question
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_product_pitches_v747 import native_layout, wrapper_dispatch
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_town_responses_context_v751 import specialty
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/specialty_question_v752')
MANUSCRIPT = Path('translations/specialty_question_manuscript_v1.json')
RAM = Path('E:/Rota Nova translations/Generated/work/emulation_v193/giveaway_v746_new/frame_003200_arm9_ram.bin')
ENGLISH = 'Hey! Could I have your %s? I think we could make %s a local specialty here.'


def catalog(arm):
    raw = RAM.read_bytes()
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    code = MainCodeFile(arm, BASE)

    def source_bytes(address, size):
        # The staged read-only pool is copied from section3 with a48-byte trailer.
        if 0x02387A20 <= address < 0x02387A20 + len(code.sections[3].data) - 48:
            at = address - 0x02387A20
            return bytes(code.sections[3].data[at:at + size])
        for section in code.sections:
            if section.ramAddress <= address and address + size <= section.ramAddress + len(section.data):
                at = address - section.ramAddress
                return bytes(section.data[at:at + size])
        raise AssertionError(('Unmapped source bytes', hex(address), size))

    def checked_call(offset, args):
        executed = call(cpu, offset, args)
        assert all(bytes(cpu.mem_read(pc, 4)) == source_bytes(pc, 4) for pc in executed)
        return cpu.reg_read(UC_ARM_REG_R0)

    result = {}
    # All original product prerequisites reference only static items0..19.
    # Generated/downloaded item names are mutable buffers and irrelevant here.
    for kind, getter, count, stride in (('items', 0xCB190, 20, 20), ('products', 0xCB124, 124, 16)):
        start = checked_call(getter, ()) + 4
        rows = []
        for index in range(count):
            ob = start + index * stride
            vt = struct.unpack('<I', cpu.mem_read(ob, 4))[0]
            fn = struct.unpack('<I', cpu.mem_read(vt + 8, 4))[0]
            pointer = checked_call(fn - BASE, (ob,))
            encoded = bytes(cpu.mem_read(pointer, 80)).split(b'\0')[0]
            assert encoded and encoded.isascii() and len(encoded) < 40
            assert source_bytes(pointer, len(encoded) + 1) == encoded + b'\0'
            row = {'index': index, 'object': ob, 'name_getter': fn, 'name_pointer': pointer, 'name': encoded.decode('ascii')}
            if kind == 'products':
                row['prerequisite_item'] = cpu.mem_read(ob + 13, 1)[0]
                # Native source metadata and existing runtime object must agree.
                assert arm[0x15EF18 + index * 12 + 7] == row['prerequisite_item']
            rows.append(row)
        result[kind] = rows
    result.update({'RAM_source': str(RAM), 'RAM_sha256': sha(raw),
        'all_executed_getter_instructions_and_complete_names_bound_to_current_ROM': True})
    return result


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom_path = Path('out/all_routes_combined_v751_candidate.nds')
    rom = NdsImage.open(rom_path)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds')
    source_arm = clean.read_file('/__arm9__.bin')
    assert source_arm[0xBAB64:0xBADC8] == arm[0xBAB64:0xBADC8]
    assert specialty(source_arm) == specialty(arm)
    target, ownership = wrap_question(arm)
    old_dispatch, new_dispatch = wrapper_dispatch(arm), wrapper_dispatch(target)
    changed = [i for i, (a, b) in enumerate(zip(old_dispatch, new_dispatch, strict=True)) if a != b]
    assert changed == [3668 + 742]
    names = catalog(arm)
    assert all(p['prerequisite_item'] < 20 or p['prerequisite_item'] >= 218 for p in names['products'])
    pairs = [(p, names['items'][p['prerequisite_item']]) for p in names['products'] if p['prerequisite_item'] < 20]
    assert len(pairs) == 25 and {i['index'] for _, i in pairs} == set(range(20))
    # Exact source instructions require product+13 == item index before collecting
    # any candidate. Other inventory/stock/technology tests can only reduce this
    # product/item matrix. They are not claimed earned or fully exercised here.
    assert source_arm[0xBAC1C:0xBAC28].hex() == '0d00d0e5000055e11000001a'
    row = deepcopy(next(r for r in read('translations/town_events_editorial_manuscript_v1.json')['records'] if r['message_id'] == 742))
    before = common_message_entries(common, arm, clean=False)
    row.update({'english': ENGLISH + '{PAD}', 'current_text_hex': before[742].text.hex(),
        'current_English': before[742].text.decode('cp932'), 'decision': 'revise',
        'speaker': 'Local specialty requester, original town actor getter B2CD8',
        'context': 'OriginalBAB64 first filters218 inventory objects against five town stock slots, comparing product+13 with the item index atBAC1C. BAD0C supplies the item name then product name to original Yes/No parent53FCC, message742; acceptance743 and refusal744 follow. Tests bind all25 prerequisite pairs but do not claim earned eligibility or actual inventory transfer.',
        'localization_note': 'Keep the attention call, request for the specific owned item, its role in creating the named local specialty, and the tentative prediction. I think we could preserves the speculation. The Japanese repeats its request with a final dou dai; natural English combines both appeals into Could I have your ...? rather than repeating the question. Your works with singular, plural and mass names; no it/them agreement is guessed. Here retains the town context. One logical paragraph; wrap only after both native substitutions.',
        'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
        'status': 'source-prose-reviewed-native-formatting-in-progress-not-integrated'})
    doc = {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'file_path': '/COMMON/MESFILE.DK4', 'source_clean_COMMON_sha256': sha(clean.read_file('/COMMON/MESFILE.DK4')),
        'source_canonical_COMMON_sha256': read('translations/town_events_editorial_manuscript_v1.json')['source_canonical_COMMON_sha256'],
        'current_ROM_sha256': sha(rom_path.read_bytes()), 'records': [row], 'status': 'research-not-a-playable-candidate'}
    checks = []
    font = GameAsciiFont.from_arm9(target)
    cpu = machine(target)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(target, BASE).sections[3].data[:-48]))
    for product, item in pairs:
        values = (item['name'], product['name'])
        formatted, lines = native_layout(cpu, b' ' + ENGLISH.encode('ascii'), 742, values, parent=0x02053FCC)
        assert len(lines) == 1 or len(lines[-1]) > 8, values
        pixels = raster(target, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        expected = bytearray(228 * 64)
        for line_no, line in enumerate(lines):
            for column, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[(16 * line_no + y) * 228 + 6 + column * 6 + x] = 1
        assert pixels == bytes(expected)
        path = ROOT / f"native_item_{item['index']}_product_{product['index']}.png"
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).resize((684,192),Image.Resampling.NEAREST).save(path)
        checks.append({'item': item, 'product': product, 'lines': lines, 'formatted_hex': formatted.hex(),
            'every_glyph_blank_cell_and_complete_substitution_exact': True, 'preview': str(path), 'preview_sha256': sha(path.read_bytes())})
    row['review']['formatting'] = True
    row['status'] = 'source-context-all25-prerequisite-pairs-native-font-reviewed-gameplay-and-integration-pending'
    validate_natural_dialogue_batch(doc)
    save(MANUSCRIPT, doc)
    save(ROOT / 'runtime_names.json', names)
    save(ROOT / 'native_review.json', {'current_ROM': str(rom_path), 'current_ROM_sha256': sha(rom_path.read_bytes()),
        'source_ROM_sha256': sha(clean.source.read_bytes()), 'research_ARM9_sha256': sha(target),
        'ownership': ownership, 'all18340_dispatch_pairs_only_original_question742_newly_wrapped': True,
        'changed_dispatch_index': changed, 'all25_original_prerequisite_pairs': checks,
        'source_eligibility_span': [0xBAB64,0xBAD0C], 'source_eligibility_sha256': sha(source_arm[0xBAB64:0xBAD0C]),
        'product_item_comparison_exact_instruction_hex': source_arm[0xBAC1C:0xBAC28].hex(),
        'source_response_fragments': specialty(arm), 'not_whole_event_eligibility_transfer_or_gameplay_verification': True,
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    (ROOT / 'research_ARM9.bin').write_bytes(target)
    print('COMMON742: all25 prerequisite pairs and18340 parent/ID dispatches pass; gameplay/integration pending.', flush=True)


if __name__ == '__main__':
    main()
