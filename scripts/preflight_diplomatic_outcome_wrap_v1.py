"""Exercise the exact original modal wrappers with the scoped formatter in memory."""

from itertools import product
from pathlib import Path
from types import SimpleNamespace

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.diplomatic_outcome_wrap_v1 import (
    BASE, EXISTING_SELECTOR, HOOK, NOTICE_IDS, NOTICE_PARENT,
    PARAGRAPH_ENTRY, YES_NO_IDS, YES_NO_PARENT, transform,
)
from dk4tool.patch.main_pool_cache_visibility import POOL
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_diplomatic_outcomes_v1 import OUTPUT, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_literal_notice_formatting_v1 import run_case
from scripts.preflight_shared_dynamic_notice_wrap_v1 import eligible_model, font_tools, render
from scripts.probe_button_prompt_native import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.verify_shared_crew_selector_v1 import dispatch


ROOT = Path('work/SharedText_20261110_v1/diplomatic_outcomes_wrap_v1')
PROOF = ROOT / 'native_wrap_preflight.json'
PARENTS = {NOTICE_PARENT: set(NOTICE_IDS), YES_NO_PARENT: set(YES_NO_IDS)}


def verify_dispatch(before, after):
    original, candidate = machine(before), machine(after)
    targets = EXISTING_SELECTOR, PARAGRAPH_ENTRY
    scopes = [
        (parent, number, number in selected)
        for parent, selected in PARENTS.items() for number in range(3668)
    ]
    scopes.extend((parent, number, False) for parent, number in product(
        (0x02054698, 0x020546A0, 0x02054720, 0x02054764),
        sorted(set(NOTICE_IDS) | set(YES_NO_IDS))))
    for parent, number, eligible in scopes:
        stack = {0xC4: parent, 0xD0: number}
        old, new = (dispatch(cpu, HOOK, stack, targets) for cpu in (original, candidate))
        assert old[0] == EXISTING_SELECTOR
        assert new[0] == (PARAGRAPH_ENTRY if eligible else EXISTING_SELECTOR), (parent, number)
        assert old[1][:3] == new[1][:3]
    return dict(pairs_tested=len(scopes), selected=sum(active for _, _, active in scopes),
        fallback_entry_unchanged=True, original_argument_registers_preserved=True)


def preview_sheets(cases, pages):
    per_sheet = 24
    sheets = []
    for start in range(0, len(cases), per_sheet):
        stop = min(start + per_sheet, len(cases))
        sheet = Image.new('RGB', (936, 122 * ((stop - start + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i in range(start, stop):
            x, y = ((i - start) % 2) * 468, ((i - start) // 2) * 122
            case = cases[i]
            label = f"{i + 1}. ID {case['message_ID']}  " + ' / '.join(case['arguments'])
            draw.text((x + 4, y + 3), label, fill='white')
            page = Image.frombytes('L', (228, 48), pages[i])
            page = page.point(lambda ink: 36 if ink else 246)
            sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x + 4, y + 19))
        path = ROOT / f'sheet_{start // per_sheet + 1:02d}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=digest(path), pages=stop - start))
    return sheets


def main():
    assert not ROOT.exists()
    manuscript, release = load(OUTPUT), load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert runtime.receipt() == manuscript['registered_input']
    selected = set(manuscript['legacy_wrapper_overwidth_IDs'])
    assert selected == set(NOTICE_IDS) | set(YES_NO_IDS)
    original = runtime.arm
    runtime.arm, owned = transform(original)
    scope = verify_dispatch(original, runtime.arm)
    assert scope['selected'] == len(selected)
    sections = MainCodeFile(runtime.arm, BASE).sections
    runtime.sections = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    cases, pages = [], []
    for row in manuscript['records']:
        for previous in row['native_current_wrapper_expansions']:
            result = run_case(runtime, row, previous['arguments'])
            runtime.calls.clear()
            assert result['expanded_hex'] == previous['expanded_hex']
            raw = bytes.fromhex(result['native_wrapper_output_hex'])
            expanded = bytes.fromhex(result['expanded_hex']).decode('ascii')
            assert 1 <= len(result['native_wrapper_lines']) <= 3
            assert [line.strip() for line in result['native_wrapper_lines']] == eligible_model(expanded, True)
            pixels, glyphs = render(raster, runtime.arm, kanji, raw)
            assert glyphs[0]['code'] == ord(expanded[0])
            assert glyphs[-1]['code'] == ord(expanded[-1])
            cases.append(result | dict(full_independent_glyph_plane_match=True,
                first_and_last_characters_match=True, glyph_count=len(glyphs)))
            pages.append(pixels)
    assert len(cases) == manuscript['complete_native_expansion_cases']
    ROOT.mkdir(parents=True, exist_ok=False)
    sheets = preview_sheets(cases, pages)
    save(PROOF, dict(manuscript=str(OUTPUT), manuscript_sha256=digest(OUTPUT),
        registered_input=manuscript['registered_input'], research_ARM9=owned, scope=scope, font=font,
        complete_cases=len(cases), contact_sheets=sheets, cases=cases,
        stored_text_unmodified=True, actual_gameplay=False, final_formatting_gate_pending=True))
    print(f"{len(cases)} native glyph planes pass across {len(sheets)} contact sheets. "
          f"{scope['pairs_tested']} dispatch pairs checked.")


if __name__ == '__main__':
    main()
