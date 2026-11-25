"""Stage the Auto Move warnings and check all stored and rendered dialogue."""

from hashlib import sha256
import inspect
from itertools import product
from pathlib import Path
from types import FunctionType

from dk4tool.patch.navigation_prerequisite_wrap_v1 import HOOK, LITERAL_COPY, PRIOR, SCOPE, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_navigation_prerequisite_review_v1 import ARM, BASE, COMMON, OUTPUT, RELEASE
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


ROOT = Path('out/navigation_prerequisites_20261111_v1')
ROM = ROOT / 'navigation_prerequisites_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_navigation_prerequisites_verification.json'
PHRASES = {
    640: ('a route to that port.',),
    645: ("from the Captain's Cabin.",),
    646: ("from the Captain's Cabin.",),
    647: ("from the Captain's Cabin.", 'give the order'),
    648: ("from the Captain's Cabin, okay?",),
    649: ("from the Captain's Cabin, will you?",),
    650: ("from the Captain's Cabin?", 'give the order'),
    651: ("from the Captain's Cabin, please!",),
    652: ("the order from the Captain's Cabin.",),
}


def compile_storage(rows):
    compiler = FunctionType(compile_layouts.__code__, {**compile_layouts.__globals__, 'PHRASES': PHRASES})
    return compiler(rows)


def verify_scope(arm):
    cpu = machine(arm)
    source = checked_text(inspect.getsource(dispatch), {'count=128': 'count=1024'})
    env = dict(dispatch.__globals__)
    exec(compile(source, __file__ + '::selector-dispatch', 'exec'), env)
    run = env['dispatch']
    parent, selector_offset = next(iter(SCOPE))
    keys = set(SCOPE[(parent, selector_offset)])
    accepted = (b' Exact break\n  Second row', b'W' * 36 + b'\n  Second row')
    rejected = (b'Plain warning', b'No leading\n  Row', b' Unguarded\nRow',
                b'W' * 35 + b'\n  Second row', b'W' * 37 + b'\n  Second row', b'W' * 36 + b'\nSecond row')
    control_keys = {key + delta for key in keys for delta in (-4, -1, 1, 4)}
    control_keys |= {0x02118520, 0x02118580, 0x02118620, 609, 629, 637, 645}
    matched = fallback = 0
    for caller, offset, key, text in product((parent, 0x02053F40, 0x02053DB4),
            (0x270, 0x274, selector_offset), sorted(keys | control_keys), accepted + rejected):
        stack = {0x264: caller, 0x270: 0, 0x274: 0, 0x27C: 0, offset: key}
        cpu.mem_write(ARGS[1], text + b'\0')
        active = caller == parent and offset == selector_offset and key in keys and text in accepted
        expected = LITERAL_COPY if active else PRIOR
        target, registers = run(cpu, HOOK, stack, (PRIOR, LITERAL_COPY))
        assert (target, registers) == (expected, ARGS)
        matched += active
        fallback += not active
    assert matched == len(keys) * len(accepted)
    return dict(tested=matched + fallback, compiled_literal=matched, returned_to_prior_selector=fallback,
                original_stack_registers_and_return_preserved=True)


def rebuild_components(arm, common, rows, storage):
    patched, selector = transform(arm)
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    target_common, target_arm, rebound, packing = repack(common, patched, rows, storage)
    assert packing['all_41_blocks_fit_8KiB']
    return target_arm, target_common, rebound, packing, selector


def main():
    assert not ROOT.exists()
    review, release = load(OUTPUT), load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert review['registered_input'] == runtime.receipt()
    assert all(digest(path) == expected for path, expected in review['evidence'].items())
    rows = {row['message_ID']: row for row in review['records']}
    storage = compile_storage(rows)
    arm, common, rebound, packing, selector = rebuild_components(runtime.arm, runtime.common, rows, storage)
    scope = verify_scope(arm)
    staged = with_components(runtime, arm, common)
    render, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    groups = {n: group for group in review['exact_native_groups']
              for n in range(group['first_ID'], group['last_ID'] + 1)}
    results, lookups, pages = [], [], []
    for n, row in rows.items():
        native_bytes = storage[n]
        looked_up = current_copy(staged, row | {'current_hex': native_bytes.hex()}, BASE + 0x5528C)
        staged.calls.clear()
        lookups.append(dict(message_ID=n, source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=reference(rebound[n]),
            staged_hex=native_bytes.hex(), original_stored_lookup=looked_up))
        group = groups[n]
        actor = next(i for i, _, message in group['original_voice_choices'] if message == n)
        result = portrait_case(staged, row, group, native_bytes, actor)
        display = result.pop('display')
        expected = row['english'].encode('ascii')
        assert b' '.join(display.split()) == expected
        if b'\n' in native_bytes:
            assert display == native_bytes
        pixels, glyphs = render_portrait(render, arm, kanji, display)
        assert glyphs[0]['code'] == expected[0] and glyphs[-1]['code'] == expected[-1]
        lines = [line.strip() for line in display.decode('ascii').split('\n')]
        assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(n, ()))
        assert all(lines) and len(lines) <= 4
        pages.append((n, pixels))
        results.append(result | dict(message_ID=n, display_hex=display.hex(), visible_lines=lines,
            native_ink_sha256=sha256(pixels).hexdigest(), complete_glyphs=len(glyphs),
            protected_phrases=PHRASES.get(n, ())))
    assert len(lookups) == len(results) == len(pages) == 24
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
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
    print('24 stored warnings, 24 native portrait pages, and the full registered parent inverse pass.')


if __name__ == '__main__':
    main()
