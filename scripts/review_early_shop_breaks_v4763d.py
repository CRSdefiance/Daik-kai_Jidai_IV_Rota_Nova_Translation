"""Source-bound, offline investigation of the user's two shop screenshots.

No ROM, registry, historical compiler, editorial credit or gameplay claim changes.
"""
from dataclasses import asdict, replace
from pathlib import Path
import json
import struct

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.common_portrait_reflow import compile_paragraph
from dk4tool.patch.shop_657_reflow import compile_657
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.layout import format_markup
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shop_business_editorial import PROFILE, compile_paragraph as historical_compile
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/early_shop_breaks_v4763d')
CURRENT = Path('out/all_routes_combined_font_and_square_fixed_20261027.nds')
CURRENT_SHA = '89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077'
EDITORIAL = Path('out/all_routes_combined_v4749_candidate.nds')
EDITORIAL_SHA = '2d118f5a7ce4a0d1af6b5f97ffcd6e6813b7ff6cb78736943215898fc1b809d9'


def reference(row):
    return dict(message_ID=row.message_id, block=row.block, offset=row.block_offset,
                copy_end=row.copy_end, bytes=len(row.text), record_index=row.record_index,
                table_offset=row.table_offset, start_in_record=row.start)


def expected_plane(arm, lines, y_offset):
    """Independent fixed-cell plane, including every blank pixel and row."""
    font = GameAsciiFont.from_arm9(arm)
    expected = bytearray(228 * 64)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            glyph = font.decode(char)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        px, py = 6 + col * 6 + x, row * 16 + y_offset + y
                        assert 0 <= px < 228 and 0 <= py < 64
                        expected[py * 228 + px] = 1
    return bytes(expected)


if __name__ == '__main__':
    assert not ROOT.exists()
    assert sha(CURRENT.read_bytes()) == CURRENT_SHA
    assert sha(EDITORIAL.read_bytes()) == EDITORIAL_SHA
    assert sha(Path('work/clean.nds').read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(CURRENT)
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    arm, common = current.read_file('/__arm9__.bin'), current.read_file('/COMMON/MESFILE.DK4')
    directory = sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    entries = owned_entries(common, arm, directory)
    historical = read('translations/square_contextual_final_review_v1.json')
    reviewed = {r['message_id']: r for r in historical['records']}
    records = []
    for n in (657, 689):
        row, jp, review = entries[n], source[n], reviewed[n]
        assert row.text.hex() == review['integrated_hex']
        assert jp.text.hex() == review['source_hex']
        records.append(dict(message_ID=n, source_reference=reference(jp), source_hex=jp.text.hex(),
            clean_Japanese=jp.text.decode('cp932'), current_reference=reference(row),
            current_hex=row.text.hex(), current_text=row.text.decode('ascii'),
            historical_justified_wording_retention=review['fresh_retained_wording_justification'],
            historical_formatting_approval_preserved=True,
            current_status='formatting-quality-reopened' if n == 657 else 'comparison-control-no-revision',
            source_meaning='A polite question recognizing a sailor, followed by a recommendation to use the trade house for bulk business.' if n == 657 else 'The Netherlands became independent from Spain only recently, after a long independence war.',
            wording_decision='retain-wording',
            current_reason='The conversational tag question and practical trade-house recommendation faithfully convey the Japanese. The defect is the generated placement of breaks.' if n == 657 else 'The complete, neutral historical explanation preserves recent independence, Spain and the long war; its paragraph uses native wrapping. No change justified by this layout finding.'))
    paragraph = ' '.join(entries[657].text.decode('ascii').split())
    legacy, old_lines = historical_compile(paragraph)
    prototype, prototype_lines = compile_paragraph(paragraph)
    proposed, generated_lines = compile_657(paragraph)
    new_lines = ["You're a sailor, aren't you? For", 'bulk trade, try the trade house.']
    assert legacy == entries[657].text and new_lines[0] == "You're a sailor, aren't you? For"
    candidates = []
    for width in range(PROFILE.window_width_px, 143, -6):
        lines = format_markup(paragraph, replace(PROFILE, window_width_px=width)).split('{LB}')
        candidates.append(dict(width_px=width, lines=lines,
            weak_endings=[s.split()[-1] for s in lines[:-1] if s.split()[-1].strip('.,!?;:').lower() in {'a','an','as','at','for','from','in','of','the','to','with'}]))
    cohort = []
    for row in entries:
        raw = row.text.rstrip(b' ')
        if b'\n  ' not in raw or not raw.isascii():
            continue
        text = b' '.join(raw.split()).decode('ascii')
        try:
            old, before_lines = historical_compile(text)
        except ValueError:
            continue
        if old != raw:
            continue
        after, after_lines = compile_paragraph(text)
        assert len(after_lines) <= len(before_lines)
        assert b' '.join(after.split()) == b' '.join(raw.split())
        cohort.append(dict(current_reference=reference(row), current_hex=row.text.hex(), paragraph=text,
            old_lines=before_lines, candidate_lines=after_lines, candidate_hex=after.hex(),
            changed=raw != after, fewer_rows=len(after_lines) < len(before_lines),
            disposition='offline-layout-lead-only-consumer-and-context-not-newly-approved'))
    assert len(cohort) == 58
    ROOT.mkdir(parents=True)
    cases = []
    tiles = []
    for path, digest, offset in ((EDITORIAL, EDITORIAL_SHA, 0), (CURRENT, CURRENT_SHA, 1)):
        image = NdsImage.open(path)
        a = image.read_file('/__arm9__.bin')
        cpu = machine(a)
        cpu.mem_write(0x02387A20, bytes(MainCodeFile(a, BASE).sections[3].data[:-48]))
        cpu.mem_write(STACK + 0x27C, struct.pack('<I', 0x02118480))
        raster, _, meta = font_tools(image)
        for label, n, raw in [('657-current', 657, legacy), ('657-proposal', 657, proposed), ('689-control', 689, entries[689].text)]:
            formatted, lines = native_layout(cpu, raw, n, (), 0x02054014)
            if label == '657-proposal':
                assert lines == generated_lines
                assert b' '.join(formatted.split()).decode('ascii') == paragraph
            events = []
            plane = raster(a, formatted, 0x01FFCE40 - BASE, size=(228,64),
                           instruction_limit=2000000, glyph_events=events)
            assert [e['code'] for e in events if e['code'] != 32] == glyph_codes(formatted)
            assert all(0 <= e['x'] and e['x'] + 6 <= 228 and 0 <= e['y'] and e['y'] + 12 <= 64 for e in events)
            assert plane == expected_plane(a, lines, offset), (path, label, lines)
            output = ROOT / f'{path.stem}_{label}.png'
            Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in plane)).save(output)
            cases.append(dict(ROM=str(path), ROM_sha256=digest, label=label, message_ID=n,
                compiled_hex=raw.hex(), native_formatted_hex=formatted.hex(), lines=lines,
                glyph_events=events, plane_sha256=sha(plane), preview=str(output),
                preview_sha256=sha(output.read_bytes()), native_parent=0x02054014,
                native_table=0x02118480, source_wrapper_canaries_and_ordered_substitutions=True,
                unchanged_logical_geometry='228x48 / 6x12 / four rows',
                physical_oracle_geometry='228x64 / row pitch16',
                glyph_y_offset=offset, independent_full_plane_equal=True,
                complete_first_internal_last_characters_bounds_and_single_page=True))
            tiles.append((f'{path.stem} / {label}', output))
    sheet = Image.new('RGB',(936,170*3),'#263238')
    draw = ImageDraw.Draw(sheet)
    for index,(label,path) in enumerate(tiles):
        x,y = index//3*468,index%3*170
        draw.text((x+6,y+5),label,fill='white')
        with Image.open(path) as preview:
            sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+6,y+30))
    sheet_path = ROOT/'native_layout_comparison.png'
    sheet.save(sheet_path)
    dependencies = ['dk4tool/dialogue/common_portrait_reflow.py','dk4tool/patch/shop_657_reflow.py','dk4tool/patch/shop_business_editorial.py',
                    'scripts/primary_town_native_font_v2102.py','scripts/prepare_product_pitches_v747.py',
                    'translations/square_contextual_final_review_v1.json']
    save(ROOT/'source_current_findings_and_native_proposal.json',dict(
        format='dk4-user-early-shop-break-review-v1', current_ROM=str(CURRENT), current_ROM_sha256=CURRENT_SHA,
        current_COMMON_sha256=sha(common), current_ARM9_sha256=sha(arm), directory_sha256=directory,
        records=records, legacy_657_candidates=candidates, proposed_657_lines=new_lines,
        proposed_657_hex=proposed.hex(), prototype_657_lines=prototype_lines, prototype_657_hex=prototype.hex(), exact_legacy_compiler_cohort=cohort,
        cohort_count=len(cohort), proposed_changed_count=sum(r['changed'] for r in cohort),
        proposed_fewer_row_count=sum(r['fewer_rows'] for r in cohort),
        finding='The historical outer loop narrows the entire candidate width to avoid a weak ending. It rejects the two-row full-width solution ending For, then accepts three short rows at192px, splitting the tag question. The successor explores all legal boundaries at the original full capacity instead.',
        two_rows_without_a_weak_ending_impossible_at_existing_budgets=True,
        selected_host_generated_full_width_layout=True, native657_dynamic_wrapper_not_enabled=True, no_prose_shortening_or_viewport_widening=True,
        weak_ending_disposition='The host formatter generates a complete-word soft wrap after For, just as the separately eligible native paragraph wrapper for comparison689 ends its second row with a. Message657 is not in that dynamic wrapper scope; its generated bytes retain its existing consumer. These are ordinary soft wraps within one sentence, not authored dramatic pauses or new lexical fragments. Two complete rows preserve the tag question and use the full existing native capacity. The historical generated-break compiler and its weak-ending rules remain unchanged.',
        native_cases=cases, sheet=str(sheet_path), sheet_sha256=sha(sheet_path.read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in dependencies},
        producer_sha256=sha(Path(__file__).read_bytes()), actual_new_gameplay_frames=0,
        new_editorial_credit=0, candidate_ROM_created=False, release_registry_changed=False,
        historical_compilers_and_approvals_unchanged=True, all_roms_preserved=True,
        status='offline-proposal-native-passed-actual-and-registered-integration-pending', full_goal_complete=False))
    print(dict(cohort=len(cohort),changed=sum(r['changed'] for r in cohort),
               fewer_rows=sum(r['fewer_rows'] for r in cohort),native_cases=len(cases),
               proposed_657=new_lines, actual_new_frames=0, release_changed=False))
