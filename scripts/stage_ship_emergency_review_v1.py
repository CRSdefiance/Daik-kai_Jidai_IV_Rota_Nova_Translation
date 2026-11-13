"""Verify stored emergency reports and their native name and supply expansions."""

from hashlib import sha256
import inspect
from itertools import product
from pathlib import Path
from types import FunctionType

from dk4tool.patch.ship_emergency_wrap_v1 import DYNAMIC, HOOK, LITERAL_COPY, LITERAL_PARAGRAPH, PRIOR, STATIC, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_ship_emergency_review_v1 import ARM, BASE, COMMON, OUTPUT, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.probe_button_prompt_native import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case, portrait_sheets, render_portrait
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT = Path('out/ship_emergency_20261111_v1')
ROM = ROOT / 'ship_emergency_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_ship_emergency_verification.json'
SHIP_NAMES = ('Latina', 'Santa Maria', 'ABCDEFGHIJKLMNOPQR', 'FIFOFOFU', '長崎丸長崎丸長崎丸')
PHRASES = {
    573: ("Admiral, we're taking on water!", "It looks like the bottom", "of the flagship's hull is damaged."),
    574: ("Admiral, we've sprung a leak!", "The bottom of the flagship's hull", 'is damaged.'),
    575: ("We're taking on water!", "Think there's damage", 'to the bottom of the hull?'),
    576: ("We're in trouble!", "This ship's taking on water!", "the bottom of the hull's damaged."),
    577: ('Admiral, trouble!', "The flagship's taking on water.", "The bottom of the hull's damaged!"),
    578: ("Water's coming in", 'through the bottom of the ship!'),
    579: ("Admiral, we've got a leak!", "The bottom of the flagship's hull", 'appears to be damaged.'),
    609: ("Ugh... My head's spinning...", "I'm so hungry...", "I can't go on..."),
}


def with_arguments():
    source = checked_text(inspect.getsource(portrait_case), {
        'def portrait_case(ctx, row, group, stored, actor_id):':
            'def portrait_case(ctx, row, group, stored, actor_id, arguments):',
        '    assert actor != 0\n':
            '    assert actor != 0\n'
            '    pointers = []\n'
            '    for i, argument in enumerate(arguments):\n'
            '        assert b"\\0" not in argument and 0 < len(argument) < 48\n'
            '        pointer = ARGUMENT_MEMORY + i * 64\n'
            '        cpu.mem_write(pointer, argument + b"\\0")\n'
            '        pointers.append(pointer)\n'
            '    pointers.extend([0] * (2 - len(pointers)))\n'
            '    expanded = stored % tuple(arguments) if arguments else stored\n',
        "len(stored) + 1)) == stored + b'\\0'": "len(expanded) + 1)) == expanded + b'\\0'",
        '(*args, 0, 0)': '(*args, *pointers)',
    })
    env = {**portrait_case.__globals__, 'ARGUMENT_MEMORY': 0x02470000}
    exec(compile(source, __file__ + '::native-portrait-with-arguments', 'exec'), env)
    return env['portrait_case']


def verify_scope(arm):
    cpu = machine(arm)
    source = checked_text(inspect.getsource(dispatch), {'count=128': 'count=1024'})
    env = dict(dispatch.__globals__)
    exec(compile(source, __file__ + '::selector-dispatch', 'exec'), env)
    run = env['dispatch']
    scope = DYNAMIC | STATIC
    offsets = (0x274, 0x27C)
    parents = {parent for parent, _ in scope} | {0x02053C14, 0x02053EF4}
    keys = {k + delta for values in scope.values() for k in values for delta in (-4, -1, 0, 1, 4)}
    keys |= {0x021185A0, 0x021185E0, 0x02118640, 0x02118760, 516}
    compiled = (b' Exact break\n  Second row', b'W' * 36 + b'\n  Second row')
    texts = (*compiled, b'Plain name argument', b' Unprotected\nRow', b'W' * 37 + b'\n  Second row')
    choices = {PRIOR: 0, LITERAL_COPY: 0, LITERAL_PARAGRAPH: 0}
    for parent, offset, key, text in product(sorted(parents), offsets, sorted(keys), texts):
        cpu.mem_write(ARGS[1], text + b'\0')
        stack = {0x264: parent, **dict.fromkeys(offsets, 0), offset: key}
        if key in DYNAMIC.get((parent, offset), ()):
            expected = LITERAL_PARAGRAPH
        elif key in STATIC.get((parent, offset), ()) and text in compiled:
            expected = LITERAL_COPY
        else:
            expected = PRIOR
        target, registers = run(cpu, HOOK, stack, tuple(choices))
        assert target == expected and registers == ARGS
        choices[target] += 1
    return dict(tested=sum(choices.values()), preserved_previous=choices[PRIOR],
        compiled_literal=choices[LITERAL_COPY], dynamic_paragraph=choices[LITERAL_PARAGRAPH],
        original_stack_registers_and_return_preserved=True)


def main():
    assert not ROOT.exists()
    review, release = load(OUTPUT), load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert review['registered_input'] == runtime.receipt()
    assert all(digest(path) == expected for path, expected in review['evidence'].items())
    rows = {row['message_ID']: row for row in review['records']}
    static = FunctionType(compile_layouts.__code__, {**compile_layouts.__globals__, 'PHRASES': PHRASES})
    storage = static({n: row for n, row in rows.items() if not row['original_substitutions']})
    storage.update({n: row['english'].encode('ascii') for n, row in rows.items() if row['original_substitutions']})
    patched, selector = transform(runtime.arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(runtime.common, patched, rows, storage)
    scope = verify_scope(arm)
    assert packing['all_41_blocks_fit_8KiB']
    staged = with_components(runtime, arm, common)
    render, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    supplies = [row['English'] for row in review['arguments']['supplies']]
    both, activity = [row['English'] for row in review['arguments']['automatic_travel_literals']]
    groups = {n: group for group in review['exact_native_groups']
              for n in range(group['first_ID'], group['last_ID'] + 1)}
    native = with_arguments()
    results, pages, lookups, images = [], [], [], {}
    for n, row in rows.items():
        looked_up = current_copy(staged, row | {'current_hex': storage[n].hex()}, BASE + 0x5528C)
        staged.calls.clear()
        lookups.append(dict(message_ID=n, source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=reference(rebound[n]),
            staged_hex=storage[n].hex(), original_stored_lookup=looked_up))
        group = groups.get(n)
        actor_id = next(i for i, _, msg in group['original_voice_choices'] if msg == n) if group else None
        if group and group['arguments'] == ['named ship']:
            args = [(name,) for name in SHIP_NAMES]
        elif 601 <= n <= 608:
            args = [(supply,) for supply in supplies]
        elif 610 <= n <= 613:
            args = [(supply, activity) for supply in (*supplies, both)]
        else:
            args = [()]
        for variant, names in enumerate(args):
            arguments = tuple(value.encode('cp932') for value in names)
            native_case = native(staged, row, group, storage[n], actor_id, arguments)
            display = native_case.pop('display')
            expected = row['english'].encode('ascii') % arguments if arguments else row['english'].encode('ascii')
            assert b' '.join(display.split()) == expected, (n, names, display, expected)
            if b'\n' in storage[n]:
                assert display == storage[n], (n, display)
            if group and group['arguments'] == ['named ship']:
                assert any(arguments[0] in line for line in display.split(b'\n')), (n, names, display)
            if display not in images:
                pixels, glyphs = render_portrait(render, arm, kanji, display)
                assert glyphs[0]['code'] == expected[0] and glyphs[-1]['code'] == expected[-1]
                images[display] = (sha256(pixels).hexdigest(), len(glyphs))
                label = f'{n} / variant {variant + 1}' if names else str(n)
                pages.append((label, pixels))
            ink, count = images[display]
            results.append(native_case | dict(message_ID=n, arguments=names, display_hex=display.hex(),
                visible_lines=[line.strip() for line in display.decode('cp932').split('\n')],
                native_ink_sha256=ink, complete_glyphs=count, protected_phrases=PHRASES.get(n, ())))
    assert len(lookups) == 41 and len(results) == 109
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release['candidate_sha256']
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    assert NdsImage.open(ROM).read_file(ARM) == arm and NdsImage.open(ROM).read_file(COMMON) == common
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        stored=lookups, storage=packing, selector=selector, selector_scope=scope, native_cases=results,
        rendered_unique_pages=len(pages), contact_sheets=portrait_sheets(ROOT, pages), font=font,
        complete_serialized_ROM_parent_inverse=True, actual_gameplay=False, new_credit=0,
        evidence={str(path): digest(path) for path in (OUTPUT, Path(__file__))}))
    print(f'41 stored templates, 109 native expansions and {len(pages)} distinct ink planes pass.')


if __name__ == '__main__':
    main()
