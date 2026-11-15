"""Rebind the crew notices to the registered build and exercise stored native rendering."""

import inspect
import struct
from hashlib import sha256
from pathlib import Path
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.crew_loss_portrait_wrap_v1 import SCOPE, transform
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import STARTUP as STARTUP_REPORT, checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_literal_notice_formatting_v1 import run_case
from scripts.preflight_shared_dynamic_notice_wrap_v1 import HEIGHT, WIDTH, font_tools, render
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.register_shared_notices_v1 import RELEASE, REGISTRY
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_ship_loss_context_v1 import OUTPUT, SOURCE
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import ARM, COMMON, relocate
from scripts.stage_ship_command_release_v1 import CLEAN


OUT = Path('work/SharedCrewLoss_20261110_v4')
SHIP_CAP = Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
NAMES = ('Latina', 'ABCDEFGHIJKLMNOPQR', 'Santa Maria', 'FIFOFOFU', '長崎丸長崎丸長崎丸')


def bind_startup(folder):
    """Adapt the existing exact-candidate cold-boot receipt to the runtime reader."""
    release = load(RELEASE)
    assert digest(REGISTRY) == release['registry_sha256']
    receipt = Path(release['own_registered_startup'])
    assert digest(receipt) == release['own_registered_startup_sha256']
    startup = load(receipt)['startup']
    assert len(startup['original_protected_name_getters']) == 24
    assert digest(STARTUP_REPORT) == startup['evidence'][str(STARTUP_REPORT)]
    report, raw = checked_report(STARTUP_REPORT, release['candidate_sha256'], startup['frames'])
    path = folder / 'registered_parent_startup.json'
    save(path, dict(candidate_sha256=report['ROM_sha256'], cold_boot=True, savestate=False,
        actual_captain_getter=3, read_only_snapshot=report['read_only_RAM_snapshot'],
        startup_report=str(STARTUP_REPORT), startup_report_sha256=digest(STARTUP_REPORT),
        original_review_receipt=str(receipt), original_review_receipt_sha256=digest(receipt)))
    ctx = RegisteredRuntime(RELEASE, path, captain=3)
    assert ctx.raw == raw and digest(ctx.rompath) == release['candidate_sha256']
    return ctx


def bind_voices(ctx):
    clean = NdsImage.open(CLEAN).read_file(ARM)
    assert ctx.arm[0x2C1E0:0x2C65C] == clean[0x2C1E0:0x2C65C]
    for lo, hi in ((0x53EC0, 0x53F9C), (0x54058, 0x54144), (0x54164, 0x54240)):
        assert ctx.arm[lo:hi] == clean[lo:hi]
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    tables = load(SOURCE)['native_personality_tables']
    result, actors = [], {}
    for table in tables:
        pointer = table['pointer']
        assert ctx.arm[pointer - BASE:pointer - BASE + 32].hex() == table['table_hex']
        members = table['slots']
        fallback = next(n for n in members if n != -1)
        for index in range(207):
            actor = ctx.actor_root + (0x19E4 if index == 3 else 4 + index * 32)
            voice = get(0x7E988, actor)
            number = get(0x53F4C, actor, pointer)
            assert number == (fallback if members[voice] == -1 else members[voice])
            if members[voice] != -1:
                actors.setdefault(number, (index, actor, pointer))
            result.append(dict(table=pointer, actor_ID=index, original_voice=voice, message_ID=number,
                native_fallback_used=members[voice] == -1))
        assert get(0x53F4C, 0, pointer) == fallback
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return actors, result


def with_components(ctx, arm, common):
    clone = RegisteredRuntime.__new__(RegisteredRuntime)
    clone.__dict__.update(ctx.__dict__)
    clone.arm, clone.common = arm, common
    field = slice(DIRECTORY_OFFSET, TABLE_END)
    assert ctx.raw[field] == ctx.arm[field]
    clone.raw = ctx.raw[:field.start] + arm[field] + ctx.raw[field.stop:]
    sections = MainCodeFile(arm, BASE).sections
    clone.sections = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]
    clone.calls = []
    return clone


def portrait_case(ctx, row, choice, name):
    code = checked_text(inspect.getsource(consumer), {
        '0x53F0C:0x02053F40,': '0x53F0C:0x02053F40,CONFIRMATION_ENTRY:CONFIRMATION_PARENT,',
    })
    env = {**consumer.__globals__, 'portrait_machine': ctx.machine,
        'CONFIRMATION_ENTRY': 0x53EC0, 'CONFIRMATION_PARENT': 0x02053EF4}
    exec(compile(code, __file__ + '::original-portrait', 'exec'), env)
    _, actor, table = choice
    entry = 0x53EC0 if row['group'] == 'abandon-confirmation-personality' else 0x53F0C
    body = env['consumer'](ctx.arm, ctx.common, ctx.raw, ctx.plan, entry, actor, table, name)
    ctx.calls.clear()
    return body


def modal_case(ctx, row, name, compiled):
    code = checked_text(inspect.getsource(run_case), {
        '        u.reg_write(UC_ARM_REG_R1, test)': '        assert original == template',
    })
    env = dict(run_case.__globals__)
    exec(compile(code, __file__ + '::original-modal', 'exec'), env)
    body = env['run_case'](ctx, {**row, 'current_hex': compiled.hex(),
        'current_copies': [{'wrapper': BASE + 0x546B8}]}, (name,))
    ctx.calls.clear()
    return body


def sheets(folder, cases):
    items = []
    for at in range(0, len(cases), 12):
        batch = cases[at:at + 12]
        sheet = Image.new('RGB', (936, 154 * ((len(batch) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(batch):
            x, y = i % 2 * 468, i // 2 * 154
            draw.text((x + 4, y + 3), f"{at + i + 1}. {row['message_ID']} · {row['variant']}", fill='white')
            with Image.open(row['preview']) as page:
                sheet.paste(page.resize((456, page.height * 2), Image.Resampling.NEAREST), (x + 4, y + 18))
        path = folder / f'crew_notices_{at // 12 + 1:02d}.png'
        sheet.save(path)
        items.append(dict(path=str(path), sha256=digest(path), pages=len(batch)))
    return items


def main():
    assert not OUT.exists()
    OUT.mkdir()
    ctx = bind_startup(OUT)
    packet = load(OUTPUT)
    assert packet['counts'] == {'retention': 14, 'revision': 8}
    bound = load(SHIP_CAP)
    assert bound['max_name_bytes_excluding_NUL'] == 18
    assert all(1 <= len(n.encode('cp932')) <= 18 for n in NAMES)
    actors, choices = bind_voices(ctx)
    rows = {row['message_ID']: row for row in packet['records']}
    assert set(rows) == set(actors) | {338, 339}
    assert digest(ctx.rompath) == ctx.release['candidate_sha256']
    assert ctx.receipt()['ARM9_sha256'] == ctx.release['target_ARM9_sha256']
    directory = sha256(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    previous = owned_entries(ctx.common, ctx.arm, directory)
    for number, row in rows.items():
        assert reference(previous[number]) == row['current_reference']
        assert previous[number].text.hex() == row['current_hex']
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    arm, runtime = transform(ctx.arm)
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(ctx.common, arm, rows, storage)
    proposed = with_components(ctx, arm, common)
    baseline = with_components(ctx, ctx.arm, ctx.common)
    raster, _, _ = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    portrait_render = FunctionType(render.__code__, {**render.__globals__, 'HEIGHT': 64})
    cases, findings = [], []
    for number, row in rows.items():
        for variant, name in enumerate(NAMES):
            name_bytes = name.encode('cp932')
            expected = storage[number].replace(b'%s', name_bytes)
            if number in actors:
                body = portrait_case(proposed, row, actors[number], name_bytes)
                assert body['input_hex'] == expected.hex()
                assert body['selector'] in SCOPE[body['parent']]
                raw = bytes.fromhex(body['formatted_hex'])
                if variant == 1:
                    old = portrait_case(baseline, row, actors[number], name_bytes)
                    assert old['parent'] == body['parent'] and old['selector'] == body['selector']
                    findings.append(dict(message_ID=number, prior_max_name_output_hex=old['formatted_hex'],
                        revised_max_name_output_hex=raw.hex()))
                pixels, glyphs = portrait_render(raster, arm, kanji, raw)
                height = 64
            else:
                body = modal_case(proposed, row, name, storage[number])
                raw = bytes.fromhex(body['native_wrapper_output_hex'])
                pixels, glyphs = render(raster, arm, kanji, raw)
                height = HEIGHT
            assert b' '.join(raw.split()) == expected
            assert len(raw.split(b'\n')) <= 3
            path = OUT / f'ID{number}_{variant}.png' if variant in (0, 1, 4) else None
            if path:
                tone = {0: 255, 1: 0, 15: 180}
                Image.frombytes('L', (WIDTH, height), bytes(tone[p] for p in pixels)).save(path)
            cases.append(dict(message_ID=number, variant=variant, name=name, native=body, ordered_glyphs=glyphs,
                output_hex=raw.hex(), exact_complete_pixels=True, preview=str(path) if path else None,
                preview_sha256=digest(path) if path else None))
    image = NdsImage.open(ctx.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    rom = OUT / 'crew_notices_RESEARCH_ONLY.nds'
    rom.write_bytes(bytes(image.rom.save()))
    image.replace_file(ARM, ctx.arm)
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == ctx.rompath.read_bytes()
    previews = [row for row in cases if row['preview']]
    save(OUT / 'native_preflight.json', dict(runtime=ctx.receipt(), selector=runtime, storage=packing,
        source_choices=choices, cases=cases, earlier_and_proposed_comparison=findings,
        exact_record_references=[dict(message_ID=n, source=rows[n]['source_reference'],
            prior=rows[n]['current_reference'], proposed=reference(rebound[n])) for n in rows],
        research_ROM=str(rom), research_ROM_sha256=digest(rom), complete_serialized_parent_inverse=True,
        visual_review_pending=True, sheets=sheets(OUT, previews),
        candidate_offline_only=True, representative_gameplay_and_registration_pending=True,
        evidence={str(p):digest(p) for p in (OUTPUT, SOURCE, SHIP_CAP, Path(__file__))}, new_credit=0))
    print(f'{len(cases)} stored native cases, {len(choices)} original voice selections and {len(previews)} preview pages.')


if __name__ == '__main__':
    main()
