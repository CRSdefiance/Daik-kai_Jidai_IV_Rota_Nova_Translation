"""Stage the phrase refinement and verify the actual stored native formatting."""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from types import FunctionType

from dk4tool.patch import diplomatic_outcome_wrap_v1 as v1, diplomatic_outcome_wrap_v2 as v2
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_diplomatic_outcomes_v1 import OUTPUT, RELEASE, TOWN_ARGUMENTS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_diplomatic_outcome_wrap_v1 import PROOF, preview_sheets
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import eligible_model, font_tools, render
from scripts.probe_button_prompt_native import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.stage_diplomatic_outcomes_storage_v1 import RECEIPT, stored_case_runner
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shared_crew_selector_v1 import dispatch


ROOT = Path('out/diplomatic_outcomes_20261110_v2')
ROM = ROOT / 'diplomatic_outcomes_phrase_RESEARCH_ONLY.nds'
EVIDENCE = ROOT / 'stored_phrase_verification.json'


def proposed_lines(text, phrase):
    assert '\x01' not in text
    if phrase:
        assert text.endswith(phrase) and text[-len(phrase) - 1] == ' '
        text = text[:-len(phrase)] + phrase.replace(' ', '\x01')
    return [line.replace('\x01', ' ') for line in eligible_model(text, True)]


def new_sample_cases(manuscript, records):
    counts = Counter()
    result = set()
    for number, phrase in v2.PHRASES.items():
        row = records[number]
        domains = [manuscript['town_names'] if i in TOWN_ARGUMENTS.get(number, ())
                   else manuscript['company_test_names'] for i in range(row['native_substitution_count'])]
        shapes = {}
        for args in product(*domains):
            text = row['english'] % args
            before, after = eligible_model(text, True), proposed_lines(text, phrase)
            counts['catalog_cases'] += 1
            assert len(after) == len(before) and after[-1].endswith(phrase)
            if before != after:
                counts['improved_catalog_cases'] += 1
                key = len(after), tuple(len(line) % 2 for line in after)
                rank = len(text), args
                if key not in shapes or rank > shapes[key][0]:
                    shapes[key] = rank, args
        result.update((number, args) for _, args in shapes.values())
    return result, counts


def main():
    assert not ROOT.exists()
    manuscript, old, staged = load(OUTPUT), load(PROOF), load(RECEIPT)
    assert digest(OUTPUT) == old['manuscript_sha256'] and digest(staged['research_ROM']) == staged['research_ROM_sha256']
    release = load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert runtime.receipt() == manuscript['registered_input'] == staged['registered_input']
    rows = {row['message_ID']: row for row in manuscript['records']}
    original_wrapped, _ = v1.transform(runtime.arm)
    wrapped, layout = v2.transform(runtime.arm)
    assert old['scope']['pairs_tested'] == 7444 and old['scope']['selected'] == 27
    original_cpu, candidate_cpu = machine(original_wrapped), machine(wrapped)
    scoped = {v1.NOTICE_PARENT: set(v1.NOTICE_IDS), v1.YES_NO_PARENT: set(v1.YES_NO_IDS)}
    sample_ids = [93, 125, 338, 339, *range(348, 384)]
    for parent, number in product((*scoped, 0x020546A0, 0x02054720), sample_ids):
        stack = {0xC4: parent, 0xD0: number}
        active = number in scoped.get(parent, ())
        old_dispatch = dispatch(original_cpu, v1.HOOK, stack, (v1.PARAGRAPH_ENTRY, v1.EXISTING_SELECTOR))
        new_dispatch = dispatch(candidate_cpu, v1.HOOK, stack, (v2.ENTRY, v1.EXISTING_SELECTOR))
        assert old_dispatch[0] == (v1.PARAGRAPH_ENTRY if active else v1.EXISTING_SELECTOR)
        assert new_dispatch[0] == (v2.ENTRY if active else v1.EXISTING_SELECTOR)
        assert old_dispatch[1][:3] == new_dispatch[1][:3]

    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    common, arm, entries, packing = repack(runtime.common, wrapped, rows, storage)
    assert common == NdsImage.open(staged['research_ROM']).read_file(COMMON)
    assert json.loads(json.dumps(packing)) == staged['storage']
    native = with_components(runtime, arm, common)
    baseline = with_components(runtime, NdsImage.open(staged['research_ROM']).read_file(ARM), common)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    old_cases = {(case['message_ID'], tuple(case['arguments'])): case for case in old['cases']}
    extra, catalog = new_sample_cases(manuscript, rows)
    run_stored = stored_case_runner()
    changed_pages, changed_cases, checks = [], [], []
    for n, args in sorted(set(old_cases) | extra):
        row = rows[n] | {'current_hex': storage[n].hex()}
        previous = old_cases.get((n, args))
        if previous is None:
            previous = run_stored(baseline, row, args)
            baseline.calls.clear()
        fresh = run_stored(native, row, args)
        native.calls.clear()
        assert fresh['expanded_hex'] == previous['expanded_hex']
        text = bytes.fromhex(fresh['expanded_hex']).decode('ascii')
        expected = proposed_lines(text, v2.PHRASES.get(n))
        assert [line.strip() for line in fresh['native_wrapper_lines']] == expected, (
            n, args, fresh['native_wrapper_lines'], expected)
        raw = bytes.fromhex(fresh['native_wrapper_output_hex'])
        assert b'\x1f' not in raw
        changed = fresh['native_wrapper_output_hex'] != previous['native_wrapper_output_hex']
        if changed or (n, args) not in old_cases:
            pixels, glyphs = render(raster, arm, kanji, raw)
            assert glyphs[0]['code'] == ord(text[0]) and glyphs[-1]['code'] == ord(text[-1])
            changed_pages.append(pixels)
            changed_cases.append(fresh)
        checks.append(dict(message_ID=n, arguments=args, expanded_hex=fresh['expanded_hex'],
            prior_display_hex=previous['native_wrapper_output_hex'], display_hex=raw.hex(),
            changed_layout=changed, reused_viewed_pixels=not changed and (n, args) in old_cases))

    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    ROOT.mkdir(parents=True)
    with ROM.open('xb') as stream:
        stream.write(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release['candidate_sha256']
    rebound = NdsImage.open(ROM)
    assert rebound.read_file(ARM) == arm and rebound.read_file(COMMON) == common
    sheets = FunctionType(preview_sheets.__code__, {**preview_sheets.__globals__, 'ROOT': ROOT})
    sheet_proof = sheets(changed_cases, changed_pages)
    save(EVIDENCE, dict(registered_input=runtime.receipt(), research_ROM=str(ROM),
        research_ROM_sha256=digest(ROM), target_ARM9_sha256=sha256(arm).hexdigest(),
        target_COMMON_sha256=sha256(common).hexdigest(), storage=packing, wrapper=layout,
        layout_model=catalog, fresh_dispatch_pairs=len(sample_ids) * 4,
        previous_complete_dispatch_scope_proof_preserved=True,
        complete_serialized_ROM_parent_inverse=True, no_prose_or_substitution_change=True,
        records=[dict(message_ID=n, source=row['source_reference'], previous=row['current_reference'],
                      staged=reference(entries[n]), staged_hex=storage[n].hex()) for n, row in rows.items()],
        cases=checks, contact_sheets=sheet_proof, font=font, actual_gameplay=False,
        evidence={str(path): digest(path) for path in (OUTPUT, PROOF, RECEIPT, Path(__file__))}))
    print(f"{len(checks)} stored cases, {len(changed_pages)} fresh pages across {len(sheet_proof)} sheets.")


if __name__ == '__main__':
    main()
