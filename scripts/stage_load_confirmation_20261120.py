"""Review and verify the original Load confirmation on both menu paths."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import unpack_from
import sys
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_tavern_round_digits_20261120 as parent
from scripts import replay_damaged_save_digits_20261120 as boot
from scripts import stage_save_dialogue_followup_20261119 as modal
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_save_location_labels_20261119 import HEADING, exact_mask


base, batch = parent.base, parent.batch
ROOT = Path('work/load_confirmation_20261120')
ROM, PROOF = ROOT / 'Load_Confirmation_RESEARCH_ONLY.nds', ROOT / 'staged.json'
NATIVE_SHEET, GAMEPLAY_SHEET = ROOT / 'native_load_confirmation.png', ROOT / 'gameplay_comparison.png'
GAME = ROOT / 'gameplay_proof.json'
HISTORY = Path('work/retail_exit_scope_20261119/quit/capture/capture_report.json')
SOURCE = Path('translations/common_submenus_arm9_v1.json')
OFFSET, POINTER, SELECTOR = 0x169F2C, 0xEE674, 0xEE078
BEFORE, AFTER = b'Load this data?', b'Load this save?'
SPAN = len(BEFORE) + 1
FRAMES = (2200, 2600, 3000, 3400, 3800, 4200, 4600, 5000, 5400, 5800, 6200, 6600, 7000)
HOLDS = {2600: 'Continue / before No', 3400: 'Continue / before Yes',
         5800: 'In-game Load / before No', 6600: 'In-game Load / before Yes'}


def patch(arm, clean):
    for lo, hi in ((SELECTOR, 0xEE090), (0x546F8, 0x54798), (POINTER, POINTER + 4)):
        assert arm[lo:hi] == clean[lo:hi]
    assert unpack_from('<I', arm, POINTER) == (modal.BASE + OFFSET,)
    assert arm[OFFSET:OFFSET + SPAN] == BEFORE + b'\0' and len(AFTER) + 1 == SPAN
    assert b'%' not in BEFORE + AFTER
    return arm[:OFFSET] + AFTER + b'\0' + arm[OFFSET + SPAN:]


def stage():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    image, clean = (base.NdsImage.open(p) for p in (parent.ROM, CLEAN))
    assert base.digest(CLEAN) == release['clean_input_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    arm, source_arm = runtime.arm, clean.read_file(ARM)
    changed = patch(arm, source_arm)
    row, = [r for r in base.load(SOURCE)['records'] if r['id'] == 'DK4_LOAD_CONFIRM']
    source_text = bytes.fromhex(row['source_hex'])
    assert OFFSET == row['offset'] and source_arm[OFFSET:OFFSET + len(source_text)] == source_text
    live = bytearray(runtime.raw)
    assert live[OFFSET:OFFSET + SPAN] == BEFORE + b'\0'
    live[OFFSET:OFFSET + SPAN] = AFTER + b'\0'
    target = with_components(runtime, changed, runtime.common)
    target.raw = bytes(live)
    raster, _, _ = modal.font_tools(image)
    font = GameAsciiFont.from_arm9(arm)
    assert font == GameAsciiFont.from_arm9(changed)
    sheet = Image.new('RGB', (936, 128), '#283744')
    draw = ImageDraw.Draw(sheet)
    displays = []
    # Unlike the composed save messages, the original load caller passes a
    # fixed pointer directly into the same native modal formatter.
    probe_source = checked_text(getsource(modal.probe), {
        'assert STACK - 0x88 < pointer < STACK': 'assert pointer == BASE + offset'})
    helpers = vars(modal).copy()
    exec(compile(probe_source, __file__ + '::direct-load-confirmation', 'exec'), helpers)
    for i, (context, code, literal) in enumerate(((runtime, arm, BEFORE), (target, changed, AFTER))):
        body = helpers['probe'](context, SELECTOR, 0, 1, OFFSET, literal)
        pixels, lines, origins, glyphs = modal.render(raster, font, code, body)
        assert lines == [literal.decode('ascii')] and origins == [0]
        assert [glyphs[0]['code'], glyphs[-1]['code']] == [literal[0], literal[-1]]
        displays.append(dict(display_hex=body.hex(), lines=lines, width=6 * len(lines[0]),
                             native_ink_sha256=modal.digest(pixels), one_page=True))
        cell = Image.frombytes('L', (modal.WIDTH, modal.HEIGHT), bytes(255 * (not p) for p in pixels))
        x = i * 468
        draw.text((x + 8, 5), 'Previous' if i == 0 else 'Revised', fill='white')
        sheet.paste(cell.resize((456, 96), Image.Resampling.NEAREST), (x + 8, 24))

    image.replace_file(ARM, changed)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    patch_file, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    make_xdelta(CLEAN, ROM, patch_file)
    apply_xdelta(CLEAN, patch_file, rebuilt)
    assert rebuilt.read_bytes() == candidate
    sheet.save(NATIVE_SHEET)
    reference = dict(offset=OFFSET, pointer_field=modal.BASE + POINTER, selector=modal.BASE + SELECTOR,
                     runtime_pointer=modal.BASE + OFFSET, allocation=SPAN)
    record = dict(id=row['id'], file_path=ARM, speaker='System', decision='revision',
                  english=AFTER.decode('ascii'), previous_English=BEFORE.decode('ascii'),
                  source_Japanese=source_text.split(b'\0', 1)[0].decode('cp932'),
                  source_meaning='Asks the player to confirm loading the selected saved game.',
                  context='The player has chosen an occupied slot in Continue or in-game Load. No returns to the list and Yes loads the selected game.',
                  localization_note='Save names what the player just selected and matches the instruction above the list. Keep it as one direct question.',
                  source_reference=reference | dict(ARM9_sha256=modal.digest(source_arm), allocation=len(source_text)),
                  current_reference=reference | dict(ARM9_sha256=modal.digest(arm)),
                  source_hex=source_text.hex(), current_hex=(BEFORE + b'\0').hex(), staged_hex=(AFTER + b'\0').hex(),
                  runtime_substitutions=[], review=dict.fromkeys(batch.GATES, True), native_displays=displays)
    base.save(PROOF, dict(candidate_sha256=modal.digest(candidate), parent_sha256=release['candidate_sha256'],
        target_ARM9_sha256=modal.digest(changed), target_COMMON_sha256=release['target_COMMON_sha256'],
        clean_input_sha256=release['clean_input_sha256'], whole_parent_inverse=True,
        clean_input_patch_byte_exact=True, clean_input_patch_sha256=base.digest(patch_file),
        changed_call=reference, records=[record], native_sheet_sha256=base.digest(NATIVE_SHEET)))


def replay(side):
    assert side in ('before', 'after', 'startup')
    stage_context = FunctionType(boot.replay.__code__, vars(boot) | {'stage': sys.modules[__name__]})
    release = base.load(parent.RELEASE)
    proof = base.load(PROOF)
    if side == 'startup':
        history = base.load(parent.STARTUP_CAPTURE)
        rom = ROM
        source = history['battery_save_preloaded']
    else:
        history = base.load(HISTORY)
        rom = parent.stage.ROOT / 'clean_rebuilt.nds' if side == 'before' else ROM
        source = history['battery_save_preloaded']
        # Continue: open prompt and decline, reopen and accept. In town: System > Load,
        # select the occupied slot, cancel and reopen, then accept.
        prefix = history['scripted_input_schedule'][:3]
        keys = ((2801, 'B'), (3201, 'A'), (3601, 'A'), (4201, 'X'),
                (5001, 'A'), (5201, 'DOWN'), (5401, 'A'), (5601, 'A'),
                (6001, 'B'), (6401, 'A'), (6801, 'A'))
        inputs = [*prefix, *(dict(start=n, duration=8, buttons=[key]) for n, key in keys),
                  dict(start=4601, duration=8, buttons=[], touch=[146, 93])]
        history = history | dict(scripted_input_schedule=sorted(inputs, key=lambda row: row['start']),
                                 exact_requested_capture_frames=list(FRAMES), frames=7200)
    assert base.digest(rom) == (release['candidate_sha256'] if side == 'before' else proof['candidate_sha256'])
    assert base.digest(source['source']) == source['source_sha256']
    stage_context(rom, history, source['source'], side)
    assert base.digest(source['source']) == source['source_sha256']


def check():
    assert not GAME.exists() and not GAMEPLAY_SHEET.exists()
    proof = base.load(PROOF)
    paths = [ROOT / p / 'capture/capture_report.json' for p in ('before', 'after')]
    reports = [base.load(path) for path in paths]
    for report, sha in zip(reports, (proof['parent_sha256'], proof['candidate_sha256']), strict=True):
        assert report['ROM_sha256'] == sha and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert report['frames'] == 7200 and report['exact_requested_capture_frames'] == list(FRAMES)
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot']
        assert base.digest(donor['source']) == base.digest(donor['destination']) == donor['source_sha256']
    assert all(reports[0][k] == reports[1][k] for k in ('scripted_input_schedule', 'core_options'))
    font = GameAsciiFont.from_arm9(base.NdsImage.open(ROM).read_file(ARM))
    old, new = map(shots, reports)
    results = []
    evidence = {str(p): base.digest(p) for p in paths}
    sheet = Image.new('RGB', (1024, 420), '#283744')
    draw = ImageDraw.Draw(sheet)
    for n in FRAMES:
        previous, revised = (captured(table[n]) for table in (old, new))
        evidence.update({t[n]['path']: t[n]['PNG_sha256'] for t in (old, new)})
        difference = ImageChops.difference(previous, revised).getbbox()
        if n not in HOLDS:
            assert difference is None
            if n in (3000, 6200):
                exact_mask(revised, font, 'Select a save to load.', HEADING)
            continue
        assert difference and 76 <= difference[0] < difference[2] <= 106 and 296 <= difference[1] < difference[3] <= 308
        masks = [font_mask(img, font, text.decode('ascii'), 16, 297, (10, 290, 245, 350), (0, 8, 0))
                 for img, text in ((previous, BEFORE), (revised, AFTER))]
        results.append(dict(frame=n, sequence=HOLDS[n], complete_ink_pixels=masks, diff_bounds=list(difference),
                            before=old[n], after=new[n]))
        y = (len(results) - 1) * 104
        for i, (image, label) in enumerate(((previous, 'Previous'), (revised, 'Revised'))):
            x = i * 512
            draw.text((x + 6, y + 3), f'{HOLDS[n]} / {label}', fill='white')
            sheet.paste(image.crop((0, 285, 256, 325)).resize((512, 80), Image.Resampling.NEAREST), (x, y + 20))
    assert new[3800]['framebuffer_sha256'] == new[7000]['framebuffer_sha256']
    sheet.save(GAMEPLAY_SHEET)
    base.save(GAME, dict(candidate_sha256=proof['candidate_sha256'], parent_sha256=proof['parent_sha256'],
        ordinary_controls=True, hardware=False, holds=results, cancelled_to_slot_list=[3000, 6200],
        accepted_to_same_Lisbon_screen=[3800, 7000], matching_control_frames=[f for f in FRAMES if f not in HOLDS],
        selected_save_preserved=True, evidence=evidence,
        sheets={str(p): base.digest(p) for p in (NATIVE_SHEET, GAMEPLAY_SHEET)}))
    print('Four complete paired confirmations, both cancellations and both loads passed.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'before', 'after', 'startup', 'check'))
    action = parser.parse_args().action
    if action in ('stage', 'check'):
        globals()[action]()
    else:
        replay(action)
