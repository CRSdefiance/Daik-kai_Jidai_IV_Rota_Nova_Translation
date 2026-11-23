"""Review the swimmer encounter, ship leaks and Square business replies."""

from hashlib import sha256
import json
from pathlib import Path
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import stage_fleet_encounter_dialogue_20261119 as fleet
from scripts import stage_ship_emergency_review_v1 as emergency
from scripts import stage_square_country_briefings_20261115 as square
from scripts.checkpoint_ship_emergency_review_v1 import bind_runtime
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case, portrait_sheets, render_portrait
from scripts.verify_release_baseline import files


RELEASES = Path('releases')
PARENT = RELEASES / 'all_routes_editorial_20261120_amsterdam_tavern_candidate/verification/registered_release_verification.json'
ROOT = Path('work/swimmer_leak_square_dialogue_20261120_v2')
ROM = ROOT / 'candidate.nds'
CLEAN = Path('work/clean.nds')
ARM, COMMON = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
GATES = ['source', 'context', 'localization', 'naturalness', 'formatting']
SWIMMER, LEAK, SQUARE = range(441, 457), range(573, 585), range(682, 688)
PRIOR = (
    'all_routes_editorial_20261119_fleet_encounter_dialogue_candidate',
    'all_routes_editorial_20261111_ship_emergency_candidate',
    'all_routes_editorial_20261119_square_shop_followup_candidate',
)
EDITS = {
    445: ("What the...? S-somebody's swimming out there!", ("S-somebody's swimming out there!",),
          "Keep the stammer and the rough voice. The complete report follows the sudden reaction."),
    456: ("Could that be the fabled mermaid?", (),
          "The full question keeps the deliberate voice and its uncertain identification. Fabled preserves the legendary figure."),
    573: ("Admiral, we're taking on water! Looks like the flagship's hull is damaged at the bottom.",
          ("Admiral, we're taking on water!", "Looks like the flagship's hull", "is damaged at the bottom."),
          "Keep the alarm, the tentative diagnosis and its exact location. The flagship stays next to its hull."),
    575: ("We're taking on water! Is the hull damaged underneath?",
          ("We're taking on water!", "Is the hull damaged underneath?"),
          "The brisk young voice follows the alarm with one complete question. The diagnosis remains uncertain."),
    576: ("We're in trouble! This ship's taking on water! The hull looks damaged underneath.",
          ("We're in trouble!", "This ship's taking on water!", "The hull looks damaged underneath."),
          "The gruff voice still leads with the alarm. Its tentative explanation fits as one complete thought."),
    578: ("Admiral! The ship's leaking! Water's coming in from below!",
          ("Admiral! The ship's leaking!", "Water's coming in from below!"),
          "Short exclamations keep the frightened voice and make the direction of the water a complete second beat."),
    682: ("Business? I've got bigger worries. I just hope peace returns soon.",
          ("Business? I've got bigger worries.", "I just hope peace returns soon."),
          "The dismissive answer and the hope for peace work as complete sentences. The pause separates the shopkeeper's concerns."),
    687: ("Business? Our regular ship sank. Now everyone's in a bind.",
          ("Business? Our regular ship sank.", "Now everyone's in a bind."),
          "The shopkeeper mentions the town's regular service in plain terms and gives its loss and consequences separate beats."),
}

RETENTIONS = {
    441: 'Keep the short notice of movement and the stammered identification of a swimmer.',
    442: 'The uncertain first look leads to a more specific guess that someone is swimming.',
    443: 'The first question and hesitant report convey the double take.',
    444: 'The soft surprise and the question leave the swimmer unidentified.',
    446: 'The measured opening and a separate, stammered report preserve both beats.',
    447: 'The short, youthful exclamation stops at seeing a swimmer.',
    448: 'The deliberate question gives way to genuine surprise at someone swimming.',
    449: 'The courteous voice compares the swimmer to a mermaid from legend and remains unsure.',
    450: 'The quick exclamation carries both the excitement and the reference to legend.',
    451: 'The casual stories and excited question fit this sailor’s register.',
    452: 'The quiet surprise and might preserve the speaker’s cautious recognition.',
    453: 'Really preserves the rough voice’s surprise, and the complete legend comparison stays on its own row.',
    454: 'The broken question leaves room for recognition and introduces no reference to legends.',
    455: 'The stammer carries the young voice’s hesitation without adding a new emotion.',
    574: 'The shipwright reports a definite diagnosis. The complete noun phrase stays together despite the short predicate.',
    577: 'The warning and both factual statements preserve the older voice and the location of the damage.',
    579: 'The measured diction preserves the speaker’s tentative diagnosis and the complete hull reference.',
    580: 'The named ship is explicit. The separate observation preserves uncertainty about its hull.',
    581: 'They say and the following question preserve two different kinds of uncertainty.',
    582: 'Word is fits the rough voice and separates the secondhand report from the speaker’s inference.',
    583: 'The direct report and Looks like preserve the older voice and qualify the cause.',
    584: 'They say and I think keep the young voice’s report separate from its diagnosis.',
    683: 'The short rebuke preserves the shopkeeper’s anger and the ongoing epidemic.',
    684: 'The blunt appeal to survival is natural and the two statements each fit a row.',
    685: 'The invitation to look around and the smile fit the unusually good business.',
    686: 'The exasperated question leaves the bad conditions unstated, as in the source.',
}


def digest(data):
    return sha256(data).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    assert not ROOT.exists()
    release = load(PARENT)
    runtime = RegisteredRuntime(PARENT, release['own_registered_startup'], captain=3)
    assert digest(CLEAN.read_bytes()) == release['clean_input_sha256']
    clean = NdsImage.open(CLEAN)
    original_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), original_arm)
    arm, common = runtime.arm, runtime.common
    assert digest(arm) == release['target_ARM9_sha256'] and digest(common) == release['target_COMMON_sha256']
    directory = digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    previous = owned_entries(common, arm, directory)
    historical = {}
    prior_refs = {}
    for directory_name, scope in zip(PRIOR, (SWIMMER, LEAK, SQUARE), strict=True):
        path = RELEASES / directory_name / 'verification/registered_review.json'
        rows = {row['message_ID']: row for row in load(path)['records'] if row['message_ID'] in scope}
        assert rows.keys() == set(scope)
        historical.update(rows)
        prior_refs[path.as_posix()] = digest(path.read_bytes())
    assert historical.keys() == EDITS.keys() | RETENTIONS.keys()
    assert not EDITS.keys() & RETENTIONS.keys()
    assert square.selectors(arm) == square.selectors(original_arm)
    groups = fleet.source_groups(original_arm, arm)
    original_groups, _ = bind_runtime(runtime, original_arm)
    leak_groups = {number: group for group in original_groups if group['first_ID'] in (573, 580)
                   for number in range(group['first_ID'], group['last_ID'] + 1)}
    assert leak_groups.keys() == set(LEAK)

    rows = {}
    for number, prior in historical.items():
        ja, old = source[number], previous[number]
        past_hex = prior['registered_reference'].get('exact_stored_hex', prior.get('staged_hex'))
        assert prior['source_hex'] == ja.text.hex() and past_hex == old.text.hex(), number
        old_english = ' '.join(old.text.decode('ascii').split())
        assert old_english == prior['english'], number
        english, phrases, note = EDITS.get(number, (old_english, (), RETENTIONS.get(number)))
        rows[number] = dict(id=prior['id'], message_ID=number, file_path=COMMON,
                            speaker=prior['speaker'], context=prior['context'],
                            source_meaning=prior['source_meaning'], localization_note=note,
                            clean_Japanese=ja.text.decode('cp932'), english=english, previous_English=old_english,
                            source_reference=reference(ja), current_reference=reference(old),
                            source_hex=ja.text.hex(), current_hex=old.text.hex(), protected_phrases=phrases,
                            decision='retention' if number not in EDITS else 'wrap revision' if old_english == english else 'revision',
                            review=dict.fromkeys(GATES, True) | {'formatting': False})
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ |
                            {'PHRASES': {n: EDITS[n][1] for n in EDITS if EDITS[n][1]}})
    edited = compiler({n: rows[n] for n in EDITS})
    edited[456] = b' ' + edited[456]
    new_common, entries, slots = owned_deployment(common, arm, previous, edited)
    assert all(previous[n].text != entries[n].text for n in EDITS)
    ctx = with_components(runtime, arm, new_common)
    cpu, get, provider = ctx.machine(arm, new_common, ctx.raw, ctx.plan)
    painter, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    ship_case = emergency.with_arguments()
    pages = []
    for number, row in rows.items():
        stored = entries[number].text
        pointer = get(0x5528C, number)
        assert bytes(cpu.mem_read(pointer, len(stored) + 1)) == stored + b'\0'
        row.update(staged_reference=reference(entries[number]), staged_hex=stored.hex(), native_displays=[])
        if number in SWIMMER:
            group, choices = groups[number]
            actor = next(actor for actor, _, message in choices if message == number)
            cases = [portrait_case(ctx, row, group, stored, actor)]
        elif number in LEAK:
            group = leak_groups[number]
            actor = next(actor for actor, _, message in group['original_voice_choices'] if message == number)
            arguments = [()] if number <= 579 else [(name.encode('cp932'),) for name in emergency.SHIP_NAMES]
            cases = [ship_case(ctx, row, group, stored, actor, args) | {'arguments': args} for args in arguments]
        else:
            display, _ = square.native_layout(cpu, stored, number, ())
            cases = [dict(display=display, formatter_parent=0x02054014)]
        for case in cases:
            display = case.pop('display')
            args = case.pop('arguments', ())
            expected = row['english'].encode('ascii')
            if args:
                expected = expected % args
                assert all(any(arg in line for line in display.splitlines()) for arg in args)
            assert b' '.join(display.split()) == expected
            lines = [line.strip() for line in display.decode('cp932').splitlines()]
            assert all(any(phrase in line for line in lines) for phrase in row['protected_phrases']), (number, lines)
            ink, glyphs = render_portrait(painter, arm, kanji, display)
            assert [g['code'] for g in glyphs] == glyph_codes(display)
            assert glyphs[0]['code'] == expected[0] and glyphs[-1]['code'] == expected[-1]
            row['native_displays'].append(case | dict(display_hex=display.hex(), visible_lines=lines,
                named_arguments=[arg.decode('cp932') for arg in args], glyph_count=len(glyphs),
                complete_ink_sha256=digest(ink), pages=1))
            if number in EDITS:
                pages.append((number, ink))
    assert provider.reads

    image = NdsImage.open(runtime.rompath)
    before = files(image)
    image.replace_file(COMMON, new_common)
    after = files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {COMMON}
    candidate = bytes(image.rom.save())
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == runtime.rompath.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    sheets = portrait_sheets(ROOT, pages)
    write(ROOT / 'staging.json', dict(candidate_sha256=digest(candidate), parent_sha256=release['candidate_sha256'],
          clean_input_sha256=release['clean_input_sha256'], target_COMMON_sha256=digest(new_common),
          target_ARM9_sha256=digest(arm), complete_inverse=True, allocations=slots, verified_entries=len(entries),
          source_proofs=prior_refs, font=font, contact_sheets=sheets,
          translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
          review_gates=GATES, records=list(rows.values()), native_offline_only=True, new_credit=0))
    print(f'{len(rows)} reviews, {len(edited)} revisions, {sum(len(r["native_displays"]) for r in rows.values())} native cases.')


if __name__ == '__main__':
    main()
