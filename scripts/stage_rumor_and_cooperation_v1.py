"""Verify the 44 stored rumor and cooperation portraits after native substitution."""

import inspect
import struct
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.rumor_and_cooperation_wrap_v1 import DYNAMIC, HOOK, PARAGRAPH, PRIOR, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import stage_mutiny_review_v1 as portrait
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_machine_scoped_v764 import machine
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.preflight_shipyard_fleet_setup_v1 import name_samples
from scripts.register_shark_encounter_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.review_rumor_and_cooperation_v1 import ARM, BASE, COMMON, IDS, OUTPUT
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT = Path('out/rumor_and_cooperation_staged_20261111_v1')
ROM = ROOT / 'rumor_and_cooperation_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
ARG_BUFFER = 0x02470000
AMENDMENTS = {
    2812: dict(english="Seems %s is trying to spread nasty rumors in %s. Don't worry, Admiral. The town's on your side!",
               localization_note='Use the young voice’s short opening and reassurance. “The town’s on your side” expresses the townspeople’s support and keeps the original names and address.'),
}


def active_rows(manuscript):
    return {row['message_ID']: row | AMENDMENTS.get(row['message_ID'], {}) for row in manuscript['records']}


def renderer():
    source = checked_text(inspect.getsource(portrait.portrait_case), {
        'def portrait_case(ctx, row, group, stored, actor_id):':
            'def portrait_case(ctx, row, group, stored, actor_id, substitutions):',
        '    seen = {}':
            "    inputs = [ARG_BUFFER + 128 * i for i in range(len(substitutions))]\n"
            "    for address, text in zip(inputs, substitutions, strict=True):\n"
            "        assert len(text) < 128 and b'\\0' not in text\n"
            "        cpu.mem_write(address, text + b'\\0')\n"
            "    values = (*args, *inputs, *([0] * (2 - len(inputs))))\n"
            "    expanded = stored % tuple(substitutions)\n"
            "    seen = {}",
        "len(stored) + 1)) == stored + b'\\0'":
            "len(expanded) + 1)) == expanded + b'\\0'",
        '(*args, 0, 0), strict=True)': 'values, strict=True)',
    })
    env = portrait.portrait_case.__globals__ | {'ARG_BUFFER': ARG_BUFFER}
    exec(compile(source, __file__ + '::actual-native-portrait-and-expansion', 'exec'), env)
    return env['portrait_case']


def catalogue(runtime):
    towns, _ = name_samples(runtime)
    town_names = [row['text'] for row in towns]
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)

    def word(at):
        return struct.unpack('<I', cpu.mem_read(at, 4))[0]

    def text(ptr):
        return bytes(cpu.mem_read(ptr, 96)).split(b'\0', 1)[0].decode('cp932')

    companies = get(0xCB160) + 4
    factions = []
    for n in range(20):
        obj = companies + 76 * n
        factions.append(text(get(word(word(obj) + 8) - BASE, obj)))
    city = get(0xCB178) + 4 + 108 * town_names.index('Lisbon')
    talkers = {
        'Local patron': get(0xB2C58, city, 12),
        'Town representative': get(0xB2B60, city),
        'Trader': get(0xB2CD8, city, 1),
    }
    actors = {role: get(0x7EE08, pointer) for role, pointer in talkers.items()}
    assert len(set(actors.values())) == len(actors)
    for role, pointer in talkers.items():
        assert pointer == runtime.actor_root + 4 + 32 * actors[role]
    number_values = {value: text(get(0xABF50, value)) for value in (1, 1000, 30000, 2147483647)}
    assert all(value == int(native) and not native.isascii() for value, native in number_values.items())
    runtime.calls.clear()
    return dict(town_names=town_names, faction_names=factions, numeric_strings=number_values,
                original_Lisbon_talkers=actors)


def samples(row, catalog):
    n, args = row['message_ID'], row['original_substitutions']
    longest_town = max(catalog['town_names'], key=lambda text: len(text.encode('cp932')))
    longest_faction = max(catalog['faction_names'], key=lambda text: len(text.encode('cp932')))
    number = catalog['numeric_strings']
    if args == ['town']:
        return [(longest_town,)]
    if args == ['faction']:
        return [(longest_faction,), ('Clifford',)] if n in (2796, 2798, 2800) else [(longest_faction,)]
    if args == ['faction', 'town']:
        return [(longest_faction, longest_town), ('Clifford', 'Lisbon')]
    if args == ['gold amount', 'faction']:
        return [(number[1000], 'Clifford'), (number[30000], longest_faction), (number[2147483647], longest_faction)]
    if args == ['gold amount']:
        return [(number[value],) for value in (1, 30000, 2147483647)]
    assert not args
    return [()]


def check_selector(arm):
    cpu = machine(arm)
    cases = [(parent, offset, key, PARAGRAPH)
             for (parent, offset), keys in DYNAMIC.items() for key in keys]
    cases.extend((parent, offset, key, PRIOR) for parent, offset, key in (
        (0x02054014, 0x274, 2795), (0x02054014, 0x274, 2806), (0x02054014, 0x274, 2425),
        (0x02053C14, 0x274, 0x02117200), (0x02053F40, 0x274, 0x02117204),
        (0x02053F40, 0x274, 2801), (0x02054014, 0x274, 0x02117200),
    ))
    results = []
    for parent, offset, key, expected in cases:
        chosen, registers = dispatch(cpu, HOOK, {0x264: parent, offset: key}, (PRIOR, PARAGRAPH))
        assert chosen == expected and registers[:3] == ARGS[:3]
        results.append(dict(parent=parent, stack_offset=offset, selector=key, continuation=chosen))
    return results


def main():
    assert not ROOT.exists()
    manuscript, release = map(load, (OUTPUT, RELEASE))
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert manuscript['registered_input'] == runtime.receipt()
    assert all(digest(path) == value for path, value in manuscript['evidence'].items())
    rows = active_rows(manuscript)
    assert tuple(rows) == IDS
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    wrapped, ownership = transform(runtime.arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    pack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, allocation = pack(runtime.common, wrapped, rows, storage)
    assert allocation['all_41_blocks_fit_8KiB']
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    checks = check_selector(arm)
    staged = with_components(runtime, arm, common)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    native = renderer()
    catalog = catalogue(runtime)
    cases, lookups, pages = [], [], []
    for n, row in rows.items():
        raw = storage[n]
        lookup = current_copy(staged, row | {'current_hex': raw.hex()}, BASE + 0x5528C)
        staged.calls.clear()
        lookups.append(dict(message_ID=n, source=row['source_reference'], previous=row['current_reference'],
                            stored=reference(rebound[n]), stored_hex=raw.hex(), original_lookup=lookup))
        actor = row.get('representative_actor_ID')
        if actor is None:
            actor = catalog['original_Lisbon_talkers'][row['speaker']]
        group = dict(consumer=row['original_consumer'], table=row.get('original_table', n), original_role_argument=None)
        for arguments in samples(row, catalog):
            encoded = tuple(value.encode('cp932') for value in arguments)
            result = native(staged, row, group, raw, actor, encoded)
            display = result.pop('display')
            assert b' '.join(display.split()) == raw % encoded, (n, display)
            try:
                plane, glyphs = portrait.render_portrait(raster, arm, kanji, display)
            except AssertionError as exc:
                raise ValueError((n, arguments, display.decode('cp932').split('\n'))) from exc
            logical = (raw % encoded).decode('cp932')
            assert chr(glyphs[0]['code']) == logical[0] and chr(glyphs[-1]['code']) == logical[-1]
            lines = [line.strip() for line in display.decode('cp932').split('\n')]
            cases.append(dict(message_ID=n, arguments=arguments, exact_display_hex=display.hex(), lines=lines,
                native_ink_sha256=sha256(bytes(p == 1 for p in plane)).hexdigest(), native_glyphs=len(glyphs), **result))
            label = f"{n}  {' / '.join(arguments)}" if arguments else str(n)
            pages.append((label, plane))
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    output = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(release['candidate']).read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(output)
    assert NdsImage.open(ROM).read_file(ARM) == arm and NdsImage.open(ROM).read_file(COMMON) == common
    source = checked_text(inspect.getsource(portrait.portrait_sheets), {
        'range(0, len(pages), 20)': 'range(0, len(pages), 10)',
        'pages[first:first + 20]': 'pages[first:first + 10]',
        'first // 20 + 1': 'first // 10 + 1',
    })
    env = portrait.portrait_sheets.__globals__.copy()
    exec(compile(source, __file__ + '::readable-contact-sheets', 'exec'), env)
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        parent_inverse_exact=True, records=lookups, native_portrait_cases=cases, ownership=ownership,
        storage=allocation, selector_cases=checks, catalogue=catalog, font_contract=font, editorial_amendments=AMENDMENTS,
        sheets=env['portrait_sheets'](ROOT, pages), gameplay_and_release_pending=True, new_credit=0,
        evidence={str(path): digest(path) for path in (OUTPUT, RELEASE, Path(__file__))}))
    print(f'44 stored portraits and {len(cases)} native portrait displays passed.')


if __name__ == '__main__':
    main()
