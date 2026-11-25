"""Bind held emulator frames to the exact stored B128 commands and native masks."""

from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from scripts import check_rafael_voyage_ceuta_20261119 as previous
from scripts import replay_rafael_sail_controls_20261119 as replay
from scripts import verify_rafael_sail_controls_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = replay.base, replay.native, replay.stage
deck = previous.deck
ROOT = replay.ROOT
PROOF = ROOT / 'live_display.json'


def sheet(views):
    target = ROOT / 'lesson_display.png'
    output = Image.new('RGB', (1024, 284 * ((len(views) + 1) // 2)), '#263238')
    draw = ImageDraw.Draw(output)
    for i, (name, frame) in enumerate(views):
        x, y = 512 * (i % 2), 284 * (i // 2)
        draw.text((x + 5, y + 4), name, fill='white')
        image = frame.crop((0, 252, 256, 384)).resize((512, 264), Image.Resampling.NEAREST)
        output.paste(image, (x, y + 18))
    output.save(target)
    return dict(path=str(target), sha256=base.digest(target))


def main():
    assert not PROOF.exists()
    inputs = [stage.PROOF, replay.MANIFEST, offline.PROOF, ROOT / 'capture/capture_report.json',
              ROOT / 'observer/commands.json']
    staged, fixture, layouts, report, trace = map(base.load, inputs)
    assert staged['candidate_sha256'] == fixture['stage_sha256'] == layouts['candidate_sha256']
    assert report['ROM_sha256'] == fixture['fixture_sha256'] == base.digest(replay.FIXTURE)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    group, = staged['groups']
    assert group['after'] == fixture['original_block_128_sha256']
    observed = previous.tavern.observed_commands(trace, 44, fixture['block_44_sha256'])
    delta = fixture['offset_delta']
    commands = {r['stored_offset'] + delta: r for r in group['commands']}
    stored = {r['id']: r for r in layouts['revisions']}
    arm, font_path = native.ARM, '/GRP/KANJI.FNT'
    rom = base.NdsImage.open(stage.ROM)
    fonts = (rom.read_file(arm), rom.read_file(font_path))
    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release['own_registered_startup'], captain=3)
    assert ctx.arm == fonts[0] and ctx.image.read_file(font_path) == fonts[1]
    _, painter = offline.display.early.prior.precedent.planners(ctx.arm)
    converters = (*fonts, painter, offline.display.stage.system.native_painter(ctx))
    font = deck.GameAsciiFont.from_arm9(ctx.arm)
    images = deck.shots(report)
    expected = checked_text(previous.getsource(previous.expected_page), {
        "if ident == 'DK4_MES_B42_R0080':\n        assert body.startswith(b'FI,') and body.count(b'FI') == 1":
        "if b'FI' in body:\n        assert body.count(b'FI') == 1",
    })
    scope = vars(previous) | dict(stage=SimpleNamespace(NAMES=stage.NAMES, workflow=stage.workflow))
    exec(compile(expected, __file__ + '::native-progressive-and-FE', 'exec'), scope)
    match = FunctionType(previous.hold_with_mask.__code__, scope)
    evidence = {str(p): base.digest(p) for p in inputs}
    panels, views, executed = [], {}, []
    for entered, returned in observed:
        at = entered['source']['instruction_offset']
        if at not in commands:
            continue
        command = commands[at]
        assert command['word'] == entered['source']['first_word']
        executed.append(dict(original_command_offset=command['stored_offset'], word=command['word'],
            entered=entered['frame'], returned=returned['frame'], results=returned['result_words']))
        if command['word'] != 0x4000:
            continue
        ident, = command['record_ids']
        raw = bytes.fromhex(command['stored'])
        selector, plane, mask = scope['expected_page'](converters, raw, ident)
        hold, screen = match(entered, returned, images, font, selector, mask)
        if ident in stored:
            cases = stored[ident]['layouts']
            reference = next((p for p in cases if p['scope'] == 'Rafael default'), cases[0])
            assert plane.hex() == reference['pages'][0]['native_plane_hex']
        panels.append(dict(id=ident, hold=hold, full_body_and_nameplate_match=True, selector=selector,
                           revision=ident in stored))
        evidence[hold['capture']] = hold['sha256']
        index = int(ident[-4:])
        if index in (12, 56, 89, 128, 180, 210):
            views[index] = (ident, screen)

    assert panels and len({p['id'] for p in panels}) == len(panels)
    assert executed[-1]['word'] == 0 and any(p['selector'] == 254 for p in panels)
    assert {'DK4_MES_B128_R0012', 'DK4_MES_B128_R0128'}.issubset(p['id'] for p in panels)
    unvisited = sorted({r for c in commands.values() for r in c['record_ids']} - {p['id'] for p in panels})
    sample = sheet([views[index] for index in sorted(views)])
    assert all(base.digest(p) == digest for p, digest in evidence.items())
    base.save(PROOF, dict(candidate_sha256=staged['candidate_sha256'], predecessor_sha256=staged['predecessor_sha256'],
        initialized_gameplay=True, natural_activation=False, hardware=False, panels=panels, unvisited=unvisited,
        original_end_command_executed=True, commands=executed, sheets=[sample], evidence=evidence))
    print(f'Verified {len(panels)} live bodies and nameplates, including {sum(p["revision"] for p in panels)} revisions. '
          f'{len(unvisited)} conditional bodies remained offline.')


if __name__ == '__main__':
    main()
