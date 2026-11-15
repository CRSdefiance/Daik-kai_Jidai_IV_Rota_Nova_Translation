"""Review the full oasis, mirage, bog and preliminary-find report families."""

from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_price_info_wraps_20261115 as parent
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case, portrait_sheets, render_portrait
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.verify_release_baseline import files


base = parent.base
ARM, COMMON, CLEAN, GATES = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN, parent.stage.GATES
ROOT = Path('work/expedition_report_wraps_20261115_v2')
ROM = ROOT / 'Expedition_Report_Wraps_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/expedition_report_wraps_context_20261115_v2.json')
CONTEXT = MANUSCRIPT.with_name('oasis_and_whale_reports_context_v1.json')
NUMBERS = range(2288, 2322 + 1)
PHRASES = {
    2288: ('found an oasis!',), 2289: ('found an oasis!',), 2291: ('found an oasis!',),
    2292: ('found an oasis!', 'Shall we go now?'), 2293: ('found an oasis!',),
    2302: ('Admiral, I think it was a mirage.',),
    2303: ('It was just a mirage...',), 2304: ('What a shame.', 'It was a mirage.'),
    2306: ('Seems it was a mirage, Admiral.',), 2307: ('What a letdown.',),
    2311: ('I hear the expedition is', 'stuck in a bottomless bog!'),
    2315: ('found something!',), 2316: ('found something!',), 2318: ('found something!',),
    2319: ('found something!',), 2320: ('turned up something!',), 2322: ('has found something!',),
}
PROSE = {
    2289: ("It appears the expedition found an oasis! Let's hurry!",
           'The officer qualifies the sighting before urging haste. “It appears” keeps the measured register.'),
    2292: ('It seems our party found an oasis! Shall we go now?',
           'The older speaker qualifies the report and invites the admiral to go immediately. The question keeps that cadence.'),
    2294: ("An oasis here... It's heaven-sent.",
           'Keep the unexpected find and the reference to heaven. The original painter stranded “heaven” on a second row.'),
    2298: ('An oasis here! Lucky us, Admiral!',
           'Keep the rough voice’s delight and direct address. The original painter stranded “lucky” on a second row.'),
    2302: ('Ah, the oasis... Admiral, I think it was a mirage.',
           'The speaker hesitates, then addresses the admiral and offers a tentative explanation.'),
    2306: ('The oasis vanished... Seems it was a mirage, Admiral.',
           'Keep the abrupt disappearance, the older voice’s pause and the qualified conclusion.'),
    2316: ('It appears the expedition found something!',
           'Keep the formal uncertainty and the unspecified find before the outcome is shown.'),
}


def bind_groups(original, clean, arm):
    groups = {}
    for group in original['native_context'][:5]:
        table = group['table'] - 0x02000000
        assert len(group['slots']) == 8
        assert unpack_from('<8i', clean, table) == unpack_from('<8i', arm, table) == tuple(group['slots'])
        caller, = group['native_callers']
        start, end = caller['load_PC'] - 0x02000000, caller['call_PC'] - 0x02000000 + 4
        assert clean[start:end] == arm[start:end] == bytes.fromhex(caller['clean_and_current_hex'])
        pointer = caller['literal_address'] - 0x02000000
        assert unpack_from('<I', clean, pointer) == unpack_from('<I', arm, pointer) == (group['table'],)
        for n in range(group['first_ID'], group['last_ID'] + 1):
            groups[n] = group | {'consumer': caller['consumer']}
    assert set(groups) == set(NUMBERS)
    return groups


def owned_deployment(common, arm, old, edited):
    original = IlnkContainer.parse(common).blocks
    blocks, slots = list(original), {}
    for n, body in edited.items():
        record = old[n]
        block, lo, hi = record.block, record.block_offset, record.copy_end
        raw = original[block][lo:hi]
        assert raw.rstrip(b'\0') == record.text and raw.endswith(b'\0')
        assert len(body) < len(raw), (n, len(body), len(raw))
        replacement = (body + b'\0').ljust(len(raw), b'\0')
        blocks[block] = blocks[block][:lo] + replacement + blocks[block][hi:]
        slots[n] = dict(block=block, start=lo, end=hi, before=raw.hex(), after=replacement.hex(),
                        new_null_fields=len(record.text) - len(body))
    deployed = IlnkContainer(blocks).to_bytes()
    rebound = owned_entries(deployed, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    for a, b in zip(old, rebound, strict=True):
        shifts = sum(slot['new_null_fields'] for slot in slots.values()
                     if slot['block'] == a.block and slot['end'] <= a.block_offset)
        text = edited.get(a.message_id, a.text)
        assert replace(a, record_index=a.record_index + shifts, text=text, end=a.start + len(text)) == b
    inverse = list(blocks)
    for slot in slots.values():
        i, lo, hi = slot['block'], slot['start'], slot['end']
        inverse[i] = inverse[i][:lo] + bytes.fromhex(slot['before']) + inverse[i][hi:]
    assert IlnkContainer(inverse).to_bytes() == common
    return deployed, rebound, slots


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    historic = base.load(CONTEXT)
    assert historic['source_ROM_sha256'] == release['clean_input_sha256']
    historical = {row['message_ID']: row for row in historic['records']}
    groups = bind_groups(historic, clean_arm, runtime.arm)
    arm, common = runtime.arm, runtime.common
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256'] and sha256(common).hexdigest() == release['target_COMMON_sha256']
    old = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    logical = {n: ' '.join(old[n].text.decode('ascii').split()) for n in NUMBERS}
    wrap = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | dict(PHRASES=PHRASES))
    edited = wrap({n: dict(english=PROSE[n][0] if n in PROSE else logical[n]) for n in sorted(PHRASES.keys() | PROSE.keys())})
    assert all(body != old[n].text for n, body in edited.items())
    deployed, rebound, slots = owned_deployment(common, arm, old, edited)

    cpu_context = with_components(runtime, arm, deployed)
    render, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    rows, preview = [], []
    for n in NUMBERS:
        before, after = old[n], rebound[n]
        original = historical[n]
        assert original['id'] in credited and original['source_hex'] == source[n].text.hex()
        assert original['original_substitution_count'] == 0 and b'%' not in after.text
        speaker = next(actor for actor, _, message in groups[n]['original_voice_choices'] if message == n)
        case = portrait_case(cpu_context, original, groups[n], after.text, speaker)
        display = case.pop('display')
        if b'\n' in after.text:
            assert display == after.text, (n, display, after.text)
        else:
            assert b' '.join(display.split()) == after.text, n
            assert b'\n' not in display, (n, display)
        pixels, glyphs = render_portrait(render, arm, kanji, display)
        assert [g['code'] for g in glyphs] == glyph_codes(display)
        if n in edited:
            preview.append((n, pixels))
        reason = PROSE[n][1] if n in PROSE else (
            'Keep the existing voice and meaning. Group ' + ' / '.join(PHRASES[n]) + ' within the generated rows.'
            if n in PHRASES else original['localization_note'])
        rows.append(dict(id=original['id'], message_ID=n, file_path=COMMON, speaker=original['speaker'],
            context=original['context'], source_meaning=original['source_meaning'], localization_note=reason,
            english=' '.join(after.text.decode('ascii').split()), previous_English=before.text.decode('ascii'),
            decision='revision' if n in PROSE else 'wrap revision' if n in edited else 'retention',
            clean_Japanese=source[n].text.decode('cp932'), source_reference=reference(source[n]),
            current_reference=reference(before), staged_reference=reference(after), source_hex=source[n].text.hex(),
            current_hex=before.text.hex(), staged_hex=after.text.hex(), native=case,
            visible_lines=[line.strip() for line in display.decode('ascii').splitlines()],
            native_ink_sha256=sha256(pixels).hexdigest(), glyph_count=len(glyphs), inherited_credit=True,
            review=dict.fromkeys(GATES, True) | {'formatting': False}))
    image = base.NdsImage.open(parent.ROM)
    original_files = files(image)
    image.replace_file(COMMON, deployed)
    target_files = files(image)
    assert original_files.keys() == target_files.keys() and {p for p in original_files if original_files[p] != target_files[p]} == {COMMON}
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheets = portrait_sheets(ROOT, preview)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), candidate_sha256=base.digest(ROM),
        previous_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        complete_reviewed_families=[group for group in historic['native_context'][:5]], historical_context=str(CONTEXT),
        historical_context_sha256=base.digest(CONTEXT), records=rows))
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_COMMON_sha256=sha256(deployed).hexdigest(), target_ARM9_sha256=sha256(arm).hexdigest(),
        allocations=slots, whole_parent_inverse=True, preserved_entries=len(rebound) - len(slots),
        sheets=sheets, font=font, native_checked_records=len(rows), changed_records=len(edited),
        manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'{len(rows)} original report paths and {len(edited)} revised native pages verified.')


if __name__ == '__main__':
    main()
