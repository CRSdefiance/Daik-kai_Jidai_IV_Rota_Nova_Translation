"""Verify all stored shark portraits and both original choice captions."""

from hashlib import sha256
import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.patch.shark_encounter_wrap_v1 import HOOK, LITERAL_COPY, MAXIMUM_TEMPLATE, PRIOR, SCOPE, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import stage_mutiny_review_v1 as portrait
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.register_faction_and_epilogue_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.review_shark_encounter_v1 import ARM, BASE, COMMON, MENU, OUTPUT
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate


ROOT = Path('out/shark_encounter_staged_20261111_v1')
ROM = ROOT / 'shark_encounter_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PHRASES = {
    2431: ('A shark may be a monster,', 'but killing one this small...', "I don't know."),
    2432: ('Shark or no shark,', "I don't like the idea", 'of killing anything this small.'),
    2433: ('Look how small this shark is.', "It'd be cruel to kill it..."),
    2434: ('It may be a shark,', "but I can't bear to take the life", 'of something so small.'),
    2435: ("So you're going to let it go?!", "You've got to be kidding!", 'Think what could happen', "once it's grown!"),
    2437: ('what happens.',),
    2439: ('turn out, though...',),
    2441: ("what happens later...", '(Grumble, grumble.)'),
    2442: ("It's for the best in the long run.", "There's no room for pity."),
    2448: ("I've got a hunch", 'you can eat shark.', 'It could even be a new trade good.'),
    2449: ('raise this one', 'and see?'),
    2450: ('What are you talking about?', "You don't know how dangerous", 'sharks are!'),
    2451: ('You catch a shark, you kill it.', "Admiral, don't listen to him.", "Let's kill it and be done with it!"),
    2452: ("That's more like it!", 'Oh, this is going to be fun.', "I can't wait!"),
    2453: ('Aw, there goes a good meal...', 'What a waste.'),
}
AMENDMENTS = {
    2448: dict(english="I've got a hunch you can eat shark. It could even be a new trade good.",
               localization_note='Preserve the two tentative ideas. Samwell is excited at the prospect of a new trade good.'),
}


def reviewer(name, replacements, **values):
    helper = getattr(portrait, name)
    source = inspect.getsource(helper)
    if replacements:
        source = checked_text(source, replacements)
    env = {**vars(portrait), **globals(), **values}
    exec(compile(source, __file__ + '::' + name, 'exec'), env)
    return env[name]


def check_menu(before, after, labels, allocation):
    menu = reviewer('check_menu', {
        "    source = checked_text(inspect.getsource(provider), {\n"
        "        '(BASE+TABLE, 2, 0, 0)': '(BASE+TABLE, 3, 0, LAST_OPTION_DEFAULT)',\n"
        "        'BASE+TABLE, 2, 0, 0)': 'BASE+TABLE, 3, 0, 2)',\n"
        "        'cpu.reg_read(UC_ARM_REG_R0) == 2': 'cpu.reg_read(UC_ARM_REG_R0) == 3',":
            "    source = checked_text(inspect.getsource(provider), {\n"
            "        '(BASE+TABLE, 2, 0, 0)': '(BASE+TABLE, 2, 0, LAST_OPTION_DEFAULT)',\n"
            "        'BASE+TABLE, 2, 0, 0)': 'BASE+TABLE, 2, 0, 1)',",
    }, TABLE=MENU)
    proof, sheet = menu(before, after, labels, allocation)
    sheet = sheet.crop((0, 0, sheet.width, 220))
    assert len(proof['captions']) == 4
    return proof, sheet


def active_rows(source):
    return {row['message_ID']: row | AMENDMENTS.get(row['message_ID'], {}) for row in source['records']}


def main():
    assert not ROOT.exists()
    manuscript, release = map(load, (OUTPUT, RELEASE))
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert manuscript['registered_input'] == runtime.receipt()
    assert all(digest(path) == expected for path, expected in manuscript['evidence'].items())
    rows = active_rows(manuscript)
    labels = manuscript['original_choice_menu']['records']
    storage = reviewer('compile_layouts', None)(rows)
    modified, allocation, selector = transform(runtime.arm, labels)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, packing = repack(runtime.common, modified, rows, storage)
    assert packing['all_41_blocks_fit_8KiB']
    assert arm[:DIRECTORY_OFFSET] == modified[:DIRECTORY_OFFSET] and arm[TABLE_END:] == modified[TABLE_END:]
    selector_proof = reviewer('verify_scope', None)(arm)
    staged = with_components(runtime, arm, common)
    raster, _, font = portrait.font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    groups = {n: group | {'original_role_argument': None} for group in manuscript['captain_tables']
              for n in group['table_slots']}
    cases, pages, lookups = [], [], []
    for n, row in rows.items():
        raw = storage[n]
        lookup = current_copy(staged, row | {'current_hex': raw.hex()}, BASE + 0x5528C)
        staged.calls.clear()
        lookups.append(dict(message_ID=n, source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=reference(rebound[n]),
            staged_hex=raw.hex(), original_stored_lookup=lookup))
        actor = row.get('captain_index', row.get('original_actor_ID'))
        group = groups.get(n)
        assert group is None or group['table_slots'][actor] == n
        direct = dict(consumer=0x02053FE4, table=n, original_role_argument=None)
        native = portrait.portrait_case(staged, row, group or direct, raw, actor)
        if group is None:
            assert native.pop('original_table') == n
            native['original_direct_message_ID'] = n
        display = native.pop('display')
        assert b' '.join(display.split()) == row['english'].encode('ascii'), (n, display)
        if b'\n' in raw:
            assert display == raw, (n, display)
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, display)
        assert glyphs[0]['code'] == ord(row['english'][0]) and glyphs[-1]['code'] == ord(row['english'][-1])
        visible = [line.strip() for line in display.decode('ascii').split('\n')]
        assert all(any(phrase in line for line in visible) for phrase in PHRASES.get(n, ()))
        cases.append(dict(message_ID=n, display_hex=display.hex(), **native, visible_lines=visible,
            native_ink_sha256=sha256(bytes(pixel == 1 for pixel in pixels)).hexdigest(), complete_glyphs=len(glyphs),
            protected_phrases=PHRASES.get(n, ())))
        pages.append((n, pixels))
    assert len(lookups) == len(pages) == len(cases) == 29
    menu, menu_sheet = check_menu(runtime.arm, arm, labels, allocation)
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(release['candidate']).read_bytes()

    ROOT.mkdir()
    ROM.write_bytes(target)
    assert NdsImage.open(ROM).read_file(ARM) == arm and NdsImage.open(ROM).read_file(COMMON) == common
    menu_path = ROOT / 'shark_choice_sheet.png'
    menu_sheet.save(menu_path)
    menu['sheet'] = dict(path=str(menu_path), sha256=digest(menu_path))
    sheets = reviewer('portrait_sheets', {
        'range(0, len(pages), 20)': 'range(0, len(pages), 10)',
        'pages[first:first + 20]': 'pages[first:first + 10]',
        'first // 20 + 1': 'first // 10 + 1',
    })
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        storage=packing, menu_allocation=allocation, wrap_selector=selector, selector_scope=selector_proof,
        complete_serialized_ROM_parent_inverse=True, stored=lookups, editorial_amendments=AMENDMENTS,
        native_portrait_cases=cases, contact_sheets=sheets(ROOT, pages), native_menu=menu, font=font,
        actual_gameplay=False, new_credit=0, evidence={str(path): digest(path) for path in (OUTPUT, RELEASE, Path(__file__))}))
    print('29 stored portraits and four original choice caption planes passed.')


if __name__ == '__main__':
    main()
