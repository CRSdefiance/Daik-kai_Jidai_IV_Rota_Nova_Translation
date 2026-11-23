"""Verify and replay the Search sailor-loss count without changing the crew outcome."""

import sys
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import check_departure_numerals_native_20261119 as prior
from scripts import replay_sailing_help_20261120 as startup_runner
from scripts import replay_shore_phrase_wraps_20261121 as history
from scripts import stage_shore_loss_digits_20261121 as stage
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.plan_literal_static_layout_v1 import render
from scripts.primary_town_native_font_v2102 import font_tools
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


base = stage.base
ROOT = stage.ROOT / 'replay'
CAPTURE, LIVE = ROOT / 'capture', ROOT / 'gameplay.json'
NATIVE = stage.ROOT / 'native.json'
NATIVE_SHEET, GAME_SHEET = stage.ROOT / 'native_counts.png', ROOT / 'loss_notice_comparison.png'
AMOUNTS = (0, 1, 5, 9, 10, 11, 20, 99, 100, 999, 65535, 2147483647)
TEMPLATE = b'Sailors lost: %s.'


def offline():
    earlier = base.load(stage.parent.RELEASE)
    ctx = RegisteredRuntime(stage.parent.RELEASE, earlier['own_registered_startup'], captain=3)
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    clean = base.NdsImage.open(stage.CLEAN)
    assert (arm, base.load(stage.PROOF)['call']) == stage.patch(ctx.arm, clean.read_file(stage.ARM))
    raw = bytearray(ctx.raw)
    offset = stage.CALL - stage.BASE
    assert raw[offset:offset + 4] == ctx.arm[offset:offset + 4]
    raw[offset:offset + 4] = arm[offset:offset + 4]
    old, _, _ = prior.provider.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    new, _, provider = prior.provider.machine(arm, ctx.common, bytes(raw), ctx.plan)
    check_numbers = FunctionType(prior.verify_numbers.__code__, prior.verify_numbers.__globals__ |
                                 {'CASES': {stage.CALL: AMOUNTS}})
    cases = check_numbers(old, new)
    assert len(cases) == 32 * len(AMOUNTS)
    assert all(bytes.fromhex(row['current_hex']).decode() == str(row['number']) for row in cases)
    raster, _, font_contract = font_tools(image)
    font = GameAsciiFont.from_arm9(arm)
    buffers = unpack_from('<2I', arm, 0x54890)
    renders = []
    sheet = Image.new('RGB', (936, 6 * 76), '#273034')
    labels = ImageDraw.Draw(sheet)
    for i, amount in enumerate(AMOUNTS):
        argument = str(amount).encode('ascii')
        assert prior.prepare_notice(new, stage.MESSAGE, TEMPLATE, (argument,), buffers) == TEMPLATE % argument
        expected = TEMPLATE % argument
        pixels, lines, origins, glyphs = render(raster, font, arm, expected)
        assert lines == [expected.decode()] and origins == [0]
        assert glyphs[0]['code'] == ord('S') and glyphs[-1]['code'] == ord('.')
        assert all(g['code'] < 128 and 0 <= g['x'] < 216 and g['y'] == 0 for g in glyphs)
        renders.append(dict(number=amount, visible_lines=lines, formatted_hex=expected.hex(),
                            complete_font_bounds_and_buffer_guards=True, pages=1, ink_sha256=stage.batch.digest(pixels)))
        x, y = (i % 2) * 468, (i // 2) * 76
        labels.text((x + 4, y + 3), f'COMMON 312  count {amount}', fill='white')
        img = Image.frombytes('L', (228, 48), bytes(25 if v else 245 for v in pixels)).crop((0, 0, 228, 24))
        sheet.paste(img.resize((456, 48), Image.Resampling.NEAREST), (x + 4, y + 20))
    assert provider.reads
    sheet.save(NATIVE_SHEET)
    lead = base.load(stage.LEAD)
    clean_source = stage.parent.stage.portrait.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))
    original = clean_source[stage.MESSAGE]
    assert original.text.hex() == lead['source_hex'] and original.text.count(b'%s') == 1
    assert lead['current_hex'] == TEMPLATE.hex()
    old_review = base.load(Path('translations/search_reports_editorial_manuscript_v3.json'))
    older, = [r for r in old_review['records'] if r.get('message_id', r.get('message_ID')) == stage.MESSAGE]
    row = dict(id=older['id'], file_path=stage.COMMON, message_ID=stage.MESSAGE, speaker='System',
               context='After Search finds that the expedition was attacked or otherwise lost sailors, the original effect removes sailors and gives the count before sailing resumes.',
               source_meaning='The system reports how many people were lost.',
               english=TEMPLATE.decode(), decision='retention',
               localization_note='The short notice clearly states the actual loss and works for singular or plural counts. Use regular-width digits in its existing substitution.',
               clean_Japanese=original.text.decode('cp932'), source_hex=lead['source_hex'], current_hex=lead['current_hex'],
               source_reference=lead['source_reference'], current_reference=lead['current_reference'],
               original_substitution_count=1, render_cases=renders, review=dict.fromkeys(REQUIRED_REVIEW_GATES, True))
    proof = dict(candidate_sha256=base.digest(stage.ROM), parent_sha256=earlier['candidate_sha256'],
                 translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                 review_gates=sorted(REQUIRED_REVIEW_GATES), records=[row], numeric_ring_checks=cases, font=font_contract,
                 sheet=dict(path=str(NATIVE_SHEET), sha256=base.digest(NATIVE_SHEET)), test_stress_values_only=True)
    validate_natural_dialogue_batch(proof)
    base.save(NATIVE, proof)
    print(f'Checked {len(cases)} number allocations and {len(renders)} complete modal layouts.', flush=True)


def verify_replay():
    prior_rom = stage.parent.ROM
    after, before = map(base.NdsImage.open, (stage.ROM, prior_rom))
    new_arm, arm = (i.read_file(stage.ARM) for i in (after, before))
    digest = base.digest(stage.ROM)
    prev, live = history.CAPTURE / 'capture_report.json', CAPTURE / 'capture_report.json'
    previous, end_previous = checked_report(prev, base.digest(prior_rom), history.RETURN)
    current, end_current = checked_report(live, digest, history.RETURN)
    old_commands = history.CAPTURE / 'navigation_command_journal.json'
    commands = CAPTURE / 'navigation_command_journal.json'
    assert base.load(commands)['commands_received'] == base.load(old_commands)['commands_received']
    for key in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'):
        assert current[key] == previous[key]
    for field in ('source', 'source_sha256', 'copied_byte_exact_before_cold_boot'):
        assert current['battery_save_preloaded'][field] == previous['battery_save_preloaded'][field]
    fixture_key = 'synthetic_battle_recovery_proximity_fixtures'
    assert not any(v for k, v in current.items() if k.startswith('synthetic_') and k != fixture_key)
    before_choices, after_choices = [[(c['frame'], c['changes'], c.get('test_shore_message')) for c in s[fixture_key]]
                                    for s in (previous, current)]
    assert before_choices == after_choices and before_choices[-1][0] == history.PAGE
    assert end_previous[history.TABLE:history.TABLE + 32] == end_current[history.TABLE:history.TABLE + 32]
    assert end_current[history.TABLE:history.TABLE + 32] == new_arm[history.TABLE:history.TABLE + 32]

    reports = [{r['frame']: r for r in s['frames_captured'] if r['path'].endswith('_navigation.png')}
               for s in (previous, current)]
    original, installed = reports
    assert original.keys() == installed.keys()
    assert all(original[n]['PNG_sha256'] == installed[n]['PNG_sha256'] for n in original if n != history.LOSS)

    def snapshot(data, frame):
        row, = (r for r in data['read_only_pause_RAM_snapshots'] if r['frame'] == frame)
        assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    at = unpack_from('<I', new_arm, 0x54894)[0] - stage.BASE
    old, new = (snapshot(r, history.LOSS)[at:at + 64].split(b'\0')[0] for r in (previous, current))
    assert old.hex() == base.load(stage.LEAD)['expanded_hex'] and new == TEMPLATE % b'11'
    state = history.previous_check.fleet_state
    assert state(arm, end_previous) == state(new_arm, end_current)
    first, last = [state(new_arm, snapshot(current, n)) for n in (history.PAGE, history.RETURN)]
    assert sum(first['crew']) - sum(last['crew']) == 11
    raster, _, _ = font_tools(after)
    pixels, rows, _, _ = render(raster, GameAsciiFont.from_arm9(new_arm), new_arm, new)
    old_screen, new_screen = [history.previous_check.city.captured(r[history.LOSS]) for r in reports]
    left, top, right, _ = history.previous_check.city.PAPER
    crop = (left, top, right, top + 48)
    assert bytes(c == (0, 8, 0) for c in new_screen.crop(crop).get_flattened_data()) == pixels
    delta = ImageChops.difference(old_screen, new_screen).getbbox()
    assert delta is not None and left <= delta[0] < delta[2] <= right and top <= delta[1] < delta[3] <= top + 16
    assert not history.previous_check.visible_paper(installed[history.RETURN]['path'])
    sheet = Image.new('RGB', (768, 216), '#263238')
    labels = ImageDraw.Draw(sheet)
    returned = history.previous_check.city.captured(installed[history.RETURN])
    for i, (label, screen) in enumerate((('Prior wide digits', old_screen), ('Regular digits', new_screen), ('Return to sailing', returned))):
        labels.text((i * 256 + 4, 4), label, fill='white')
        sheet.paste(screen.crop((0, 192, 256, 384)), (i * 256, 22))
    sheet.save(GAME_SHEET)
    base.save(LIVE, dict(candidate_sha256=digest, parent_sha256=base.digest(prior_rom),
                         actual_emulator=True, hardware=False, original_loss=11, notice_rows=rows,
                         expected_complete_native_ink=True, unchanged_other_screen_captures=len(original)-1,
                         fixture_scope='The same copied Search save, shoreline fixture and restored report variant as the before capture.',
                         unchanged_effect_and_return=True, sheet=dict(path=str(GAME_SHEET), sha256=base.digest(GAME_SHEET)),
                         evidence={str(p): base.digest(p) for p in (prev, live, commands, old_commands, GAME_SHEET)}))
    print('Verified the complete regular-width notice, identical crew loss and unchanged sailing return.', flush=True)


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'offline':
        offline()
    elif action == 'startup':
        FunctionType(startup_runner.startup.__code__, startup_runner.env | {'parent': stage.parent, 'stage': stage})()
    elif action == 'verify':
        verify_replay()
    else:
        assert action == 'play'
        FunctionType(history.replay.__code__, vars(history) | {'stage': stage, 'ROOT': ROOT, 'CAPTURE': CAPTURE, 'verify': verify_replay})()

