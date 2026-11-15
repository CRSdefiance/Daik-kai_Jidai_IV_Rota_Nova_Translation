"""Verify stored mutiny dialogue and the original three-choice caption renderer."""

from dataclasses import replace
from hashlib import sha256
import inspect
from itertools import product
from pathlib import Path
import struct
from types import FunctionType

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.layout import format_markup
from dk4tool.patch.mutiny_choice_labels_v1 import TABLE
from dk4tool.patch.mutiny_static_wrap_v1 import HOOK, LITERAL_COPY, MAXIMUM_TEMPLATE, PRIOR, SCOPE, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import native_menu_backing_surface_v4080 as backing
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_ship_command_native_menu_v1 import provider
from scripts.checkpoint_mutiny_review_v1 import ARM, BASE, COMMON, OUTPUT, PRONOUN_IDS, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import PROFILE
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT = Path('out/mutiny_20261111_v1')
ROM = ROOT / 'mutiny_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_mutiny_verification.json'
PARENTS = {0x53D44: (0x02053DB8, 0x27C), 0x53F0C: (0x02053F40, 0x274),
           0x53BD8: (0x02053C14, 0x270), 0x53FE4: (0x02054014, 0x274)}
PHRASES = {
    508: ("I'm going out of my mind", 'staring at the sea', 'day after day!', 'I want to get back on land!'),
    509: ('growing restless.', 'It might be wise', 'put into port soon.'),
    510: ('more and more upset.', 'put into port for a while...'),
    511: ("the crew's worn out.", "Don't you think", 'we put into port?'),
    512: ('the whole crew', 'looks worn out.', 'put into port soon?'),
    513: ('go stir-crazy', 'if we keep this up.', 'put into port', 'for a while.'),
    514: ('growing restless.', "We'd best", 'make a stop in port.'),
    515: ('all grumpy.', "Let's go into port.", "I'm scared!"),
    516: ("I can't take this anymore!", "I'll force you to head for port!"),
    517: ("The crew's about to boil over,", 'Admiral. What should we do?'),
    518: ('ready to use force...', 'What should we do, Admiral?'),
    519: ("The crew's about to lose it.", 'What do we do, Admiral?'),
    520: ("we've got trouble!", "The crew's", 'to use force!', 'What should we do?'),
    522: ('fit to burst, Admiral.', 'What do you think we ought to do?'),
    523: ("The crew's really mad!", 'we have to', 'go to port!', 'What do we do?'),
    524: ('at the end of its patience.', 'How shall we handle this?'),
    525: ('If you defy the admiral,', "you'll answer to me!"),
    526: ('Defy the admiral', "you'll have me to deal with!"),
    527: ('Listen to the admiral!', "If you won't obey,", "you'll have to face me!"),
    528: ('If you defy the admiral,', "you'll have to deal with me!"),
    529: ('You wanna defy the admiral?', 'You deal with me!'),
    530: ('Do as the admiral says!', "Anyone who won't", 'answer to me!'),
    531: ('Settle down!', "If you won't,", "you'll have to deal with me!"),
    533: ("We're out of trouble for now,", "we'd better put into port", 'as soon as we can.'),
    534: ("...Admiral, let's put into port", "There's no telling", 'what will happen next.'),
    535: ("we've got to", 'find a port.', 'I feel kind of sorry'),
    536: ("...Admiral, let's make a port call.", 'I hate seeing the crew like this.'),
    537: ('We got through it this time...', "Let's find a port, quick.", 'I hate doing this', 'to our own crew.'),
    538: ('Things seem to have settled down.', "Still, we'd best find a port soon."),
    539: ("everyone's still on edge.", "we'd better put into port soon."),
    540: ("They've calmed down this time,", "there's no telling", 'what will happen next.', "We'd best put into port soon."),
    541: ("can't restrain the crew", 'without a Boarding Leader!'),
    542: ('without a Boarding Leader,', "we can't put down the mutiny."),
    543: ('put down a mutiny', 'without a Boarding Leader!'),
    544: ('put down', 'a Boarding Leader', 'would be reckless!'),
    545: ('Without a Boarding Leader,', 'force the crew', 'back down!'),
    546: ("can't subdue the crew", 'by force', 'without a Boarding Leader.'),
    547: ('Without a Boarding Leader,', 'get the crew to listen!'),
    548: ("I'm sorry, everyone.", "Let's forget the formalities", 'share a special meal.', "It's my way", 'making it up to you.'),
    549: ('...Bear with me a little longer.', 'No formalities today.', 'treat you all to a special meal!'),
    550: ('a little longer, okay?', "Let's all sit down", 'to a good meal today.', 'That ought to lift your spirits!'),
    551: ('Please bear with me a little longer.', 'To make it up to you,', "I'll treat", 'everyone to a special meal today.'),
    553: ('Drag the admiral out!', "Let's give them a beating!"),
    560: ("You've already hit the admiral.", "Haven't you had enough?"),
    561: ('You went too far', 'laid hands on the admiral!'),
    562: ('You laid hands on the admiral.', 'Still not satisfied?'),
    563: ('Leave the poor admiral alone!',),
    564: ("You must've had enough by now!",),
    570: ("If it's food you need,", 'leave it to me!'),
}


def compile_layouts(rows):
    profile = replace(PROFILE, window_width_px=216, max_lines=4, guard_linebreaks=True)
    storage = {}
    for n, row in rows.items():
        text = row['english']
        assert text.isascii() and '%' not in text and not any(token in text for token in ('FI', 'FA', 'FO', 'FU', 'IC'))
        if len(text) <= 36:
            assert n not in PHRASES
            storage[n] = text.encode('ascii')
            continue
        phrases = PHRASES.get(n, ())
        marked = text
        assert '_' not in marked and all(text.count(phrase) == 1 for phrase in phrases)
        for phrase in phrases:
            marked = marked.replace(phrase, phrase.replace(' ', '_'))
        lines = format_markup(marked, profile).replace('_', ' ').split('{LB}')
        assert 2 <= len(lines) <= 4 and all(0 < len(line) <= (35 if i else 36)
                                           for i, line in enumerate(lines)), (n, lines)
        assert ' '.join(lines) == text and all(any(phrase in line for line in lines) for phrase in phrases), n
        prefix = '' if len(lines[0]) == 36 else ' '
        stored = (prefix + '\n  '.join(lines)).encode('ascii')
        assert len(stored) < MAXIMUM_TEMPLATE
        storage[n] = stored
    return storage


def verify_scope(arm):
    cpu = machine(arm)
    source = checked_text(inspect.getsource(dispatch), {'count=128': 'count=1024'})
    env = dict(dispatch.__globals__)
    exec(compile(source, __file__ + '::scope-dispatch', 'exec'), env)
    run = env['dispatch']
    offsets = (0x270, 0x274, 0x27C)
    parents = {parent for parent, _ in SCOPE} | {0x02053C5C, 0x02053D24, 0x02053EF4}
    keys = {key + delta for values in SCOPE.values() for key in values for delta in (-1, 0, 1)}
    keys |= {532, 552, 572, 0x02116820, 0x02118760, 0x02118800, 0x02116730}
    accepted = (b' Exact break\n  Second row', b'W' * 36 + b'\n  Second row')
    texts = (*accepted, b'Ordinary body', b'No leading\n  Row', b' Unprotected\nRow',
             b'W' * 35 + b'\n  Second row', b'W' * 37 + b'\n  Second row', b'W' * 36 + b'\nSecond row')
    positive = total = 0
    for parent, offset, key, text in product(sorted(parents), offsets, sorted(keys), texts):
        cpu.mem_write(ARGS[1], text + b'\0')
        stack = {0x264: parent, **dict.fromkeys(offsets, 0), offset: key}
        active = key in SCOPE.get((parent, offset), ()) and text in accepted
        target, registers = run(cpu, HOOK, stack, (PRIOR, LITERAL_COPY))
        assert target == (LITERAL_COPY if active else PRIOR) and registers == ARGS, (parent, offset, key, text)
        total += 1
        positive += active
    assert positive == len(accepted) * sum(len(keys) for keys in SCOPE.values())
    return dict(tested=total, selected=positive, original_stack_registers_and_return_preserved=True,
        all_other_callers_rejoin_previous_selector=True)


def portrait_case(ctx, row, group, stored, actor_id):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    if group is None:
        entry = 0x53FE4
        key = row['message_ID']
        fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
        actor = get(0x36778, fleet)
    else:
        entry = group['consumer'] - BASE
        key = group['table']
        actor = ctx.actor_root + (0x19E4 if actor_id == 3 else 4 + 32 * actor_id)
    assert actor != 0
    args = {0x53D44: (group and group['original_role_argument'], key),
            0x53F0C: (actor, key), 0x53BD8: (key, 0), 0x53FE4: (actor, key)}[entry]
    seen = {}

    def hook(u, pc, size, unused):
        if pc == 0x02053D70 or pc == 0x02053C7C:
            u.reg_write(UC_ARM_REG_R0, actor_id)
        elif pc == 0x0205408C:
            u.reg_write(UC_ARM_REG_PC, 0x02054144)
        elif pc == 0x01FFCF3C:
            parent, offset = PARENTS[entry]
            sp = u.reg_read(UC_ARM_REG_SP)
            assert struct.unpack('<I', u.mem_read(sp + 0x264, 4))[0] == parent
            assert struct.unpack('<I', u.mem_read(sp + offset, 4))[0] == key
            assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), len(stored) + 1)) == stored + b'\0'
            speaker = u.reg_read(UC_ARM_REG_R2)
            assert speaker == (ctx.actor_root + 0x19E4 if entry == 0x53BD8 else actor)
            seen.update(output=u.reg_read(UC_ARM_REG_R0), speaker_pointer=speaker, parent=parent)
        elif pc == 0x02054164:
            seen['display'] = bytes(u.mem_read(seen['output'], 256)).split(b'\0', 1)[0]
            u.emu_stop()

    hooks = [0x0205408C, 0x01FFCF3C, 0x02054164]
    if entry == 0x53D44:
        hooks.append(0x02053D70)
    if entry == 0x53BD8 and actor_id != 3:
        hooks.append(0x02053C7C)
    for pc in hooks:
        cpu.hook_add(UC_HOOK_CODE, hook, begin=pc, end=pc)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (*args, 0, 0), strict=True):
        cpu.reg_write(register, value)
    cpu.emu_start(BASE + entry, STOP, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x02054164
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return seen | dict(original_entry=BASE + entry, original_table=key if group else None,
        supplied_offline_actor_ID=actor_id, original_file_reads=provider.reads)


def render_portrait(raster, arm, kanji, text):
    renderer = checked_text(inspect.getsource(render), {'1 <= len(lines) <= 3': '1 <= len(lines) <= 4'})
    env = {**render.__globals__, 'HEIGHT': 64}
    exec(compile(renderer, __file__ + '::four-row-portrait', 'exec'), env)
    return env['render'](raster, arm, kanji, text)


def portrait_sheets(root, pages):
    results = []
    for first in range(0, len(pages), 20):
        batch = pages[first:first + 20]
        sheet = Image.new('RGB', (936, 154 * ((len(batch) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (number, pixels) in enumerate(batch):
            x, y = (i % 2) * 468, (i // 2) * 154
            draw.text((x + 4, y + 3), f'ID {number}', fill='white')
            page = Image.frombytes('L', (228, 64), bytes(36 if ink else 246 for ink in pixels))
            sheet.paste(page.resize((456, 128), Image.Resampling.NEAREST), (x + 4, y + 19))
        path = root / f'portrait_sheet_{first // 20 + 1:02d}.png'
        sheet.save(path)
        results.append(dict(path=str(path), sha256=digest(path), messages=[n for n, _ in batch]))
    return results


def check_menu(parent, arm, labels, allocation):
    source = checked_text(inspect.getsource(provider), {
        '(BASE+TABLE, 2, 0, 0)': '(BASE+TABLE, 3, 0, LAST_OPTION_DEFAULT)',
        'BASE+TABLE, 2, 0, 0)': 'BASE+TABLE, 3, 0, 2)',
        'cpu.reg_read(UC_ARM_REG_R0) == 2': 'cpu.reg_read(UC_ARM_REG_R0) == 3',
        '        if index == 1:\n            assert pointer == expected_pointer':
            '        assert pointer == expected_pointer[index]',
    })
    env = {**provider.__globals__, 'TABLE': TABLE, 'LAST_OPTION_DEFAULT': 0xFFFFFFFF}
    exec(compile(source, __file__ + '::three-choice-provider', 'exec'), env)
    get_menu = env['provider']
    before = get_menu(parent, [r['original_pointer'] for r in allocation['changes']])
    after = get_menu(arm, [r['target_pointer'] for r in allocation['changes']])
    assert [r['text'] for r in before['options']] == [row['source_Japanese'] for row in labels]
    assert [r['text'] for r in after['options']] == [row['english'] for row in labels]
    assert before['descriptor_hex'] == after['descriptor_hex']
    assert before['modal_rectangle'][1::2] == after['modal_rectangle'][1::2]

    painter = checked_text(inspect.getsource(backing.paint), {
        "'expected[(y+yy)*backing_width+x+index*6+xx]'": "'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
    })
    painter_env = dict(vars(backing))
    exec(compile(painter, __file__ + '::choice-pixel-plane', 'exec'), painter_env)
    width = after['minimum_width_units'] * 6
    sheet = Image.new('RGB', (420, 333), '#263238')
    draw = ImageDraw.Draw(sheet)
    variants = []
    for option in after['options']:
        assert option['width_units'] == len(option['text'])
        for style in (1, 15):
            pixels, proof = painter_env['paint'](arm, option['text'].encode('ascii'), style,
                                                  width, (0, option['index'] * 12))
            assert proof['independent_complete_native_pixels_match'] and proof['visible_cell_center_twice'] == width
            assert proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
            color = (244, 235, 205) if style == 1 else (0, 165, 170)
            tile = Image.new('RGB', (width, 12))
            tile.putdata([(0, 8, 0) if value else color for value in pixels])
            pos = len(variants) * 55
            draw.text((5, pos + 3), f"{option['text']}  /  native style {style}", fill='white')
            sheet.paste(tile.resize((width * 3, 36), Image.Resampling.NEAREST), (5, pos + 17))
            assert proof['style'] == style
            variants.append(dict(option=option['index'], plane_sha256=sha256(pixels).hexdigest(), **proof))
    return dict(parent=before, research=after, captions=variants, native_UI_loop_return_is_offline_boundary=True), sheet


def main():
    assert not ROOT.exists()
    manuscript, release = load(OUTPUT), load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert manuscript['registered_input'] == runtime.receipt()
    assert all(digest(path) == expected for path, expected in manuscript['evidence'].items())
    rows = {row['message_ID']: row for row in manuscript['records']}
    labels = manuscript['original_choice_menu']['records']
    storage = compile_layouts(rows)
    modified, allocation, selector = transform(runtime.arm, labels)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(runtime.common, modified, rows, storage)
    assert packing['all_41_blocks_fit_8KiB']
    selector_scope = verify_scope(arm)
    staged = with_components(runtime, arm, common)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    groups = {n: group for group in manuscript['exact_native_crew_groups']
              for n in range(group['first_ID'], group['last_ID'] + 1)}
    cases, pages, exact_lookups = [], [], []
    for n, row in rows.items():
        lookup = current_copy(staged, row | {'current_hex': storage[n].hex()}, BASE + 0x5528C)
        staged.calls.clear()
        exact_lookups.append(dict(message_ID=n, source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=reference(rebound[n]),
            staged_hex=storage[n].hex(), original_stored_lookup=lookup))
        group = groups.get(n)
        if group is None:
            actors = [None]
        elif group['consumer'] == 0x02053BD8:
            actors = [group['table_slots'].index(n)]
        else:
            candidates = [i for i, _, selected in group['original_voice_choices'] if selected == n]
            actors = candidates if n in PRONOUN_IDS else candidates[:1]
        assert actors
        displays = []
        for actor_id in actors:
            native = portrait_case(staged, row, group, storage[n], actor_id)
            displays.append(native.pop('display'))
            assert b' '.join(displays[-1].split()) == row['english'].encode('ascii'), (n, displays[-1])
            if b'\n' in storage[n]:
                assert displays[-1] == storage[n], (n, displays[-1])
            cases.append(dict(message_ID=n, display_hex=displays[-1].hex(), **native))
        assert len(set(displays)) == 1
        pixels, glyphs = render_portrait(raster, arm, kanji, displays[0])
        assert glyphs[0]['code'] == ord(row['english'][0]) and glyphs[-1]['code'] == ord(row['english'][-1])
        pages.append((n, pixels))
        for case in cases[-len(actors):]:
            case.update(visible_lines=[line.strip() for line in displays[0].decode('ascii').split('\n')],
                native_ink_sha256=sha256(pixels).hexdigest(), complete_glyphs=len(glyphs),
                protected_phrases=PHRASES.get(n, ()))
    assert len(exact_lookups) == len(pages) == 65 and len(cases) == 77
    menu, menu_sheet = check_menu(runtime.arm, arm, labels, allocation)
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
    menu_path = ROOT / 'mutiny_choice_sheet.png'
    menu_sheet.save(menu_path)
    menu['sheet'] = dict(path=str(menu_path), sha256=digest(menu_path))
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        storage=packing, menu_allocation=allocation, wrap_selector=selector, selector_scope=selector_scope,
        complete_serialized_ROM_parent_inverse=True, stored=exact_lookups,
        native_portrait_cases=cases, contact_sheets=portrait_sheets(ROOT, pages), native_menu=menu, font=font,
        actual_gameplay=False, new_credit=0, evidence={str(path): digest(path) for path in (OUTPUT, Path(__file__))}))
    print('65 stored dialogues, 77 native portrait expansions and six native menu caption planes pass.')


if __name__ == '__main__':
    main()
