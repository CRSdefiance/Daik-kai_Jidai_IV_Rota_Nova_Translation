"""Check the revised shark proposal in its original full exchange and choice flow."""

import sys
from inspect import getsource
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageDraw
from scripts import replay_sailing_help_20261120 as startup
from scripts import replay_shark_encounter_v4 as earlier
from scripts import stage_final_early_wrap_leads_20261121 as stage
from scripts import verify_shark_encounter_v1 as old_verifier
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
OUT = stage.ROOT / 'shark'
PROOF, SHEET = OUT / 'verified.json', OUT / 'shark_proposal_and_choice.png'


def replay():
    first = earlier.replay_base
    code = checked_text(getsource(first.replay), {
        'out = stage.ROOT / choice': 'out = OUT / choice\n    out.parent.mkdir(exist_ok=True)',
    })
    scope = vars(first) | dict(stage=stage, OUT=OUT, FINAL=earlier.FINAL,
                              fixture_controller=earlier.initialized.fixture_controller,
                              commands=lambda choice: earlier.commands())
    exec(compile(code, __file__ + '::shark-proposal-replay', 'exec'), scope)
    scope['replay']('raise')
    verify()


def verify():
    cap = OUT / 'raise/capture'
    report_path = cap / 'capture_report.json'
    journal_path = cap / 'navigation_command_journal.json'
    candidate = base.digest(stage.ROM)
    report, final = checked_report(report_path, candidate, earlier.FINAL)
    history_path = earlier.OUT / 'raise/capture/capture_report.json'
    history = base.load(history_path)
    assert report['scripted_input_schedule'] == history['scripted_input_schedule']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    assert report['battery_save_preloaded']['source_sha256'] == history['battery_save_preloaded']['source_sha256']
    assert [r['mode'] for r in report['synthetic_condition_fixtures']] == [
        'initialize', 'restore-entry', 'restore-return-and-roster']
    journal = base.load(journal_path)['commands_received']
    assert all(r['validation_passed'] for r in journal)
    assert [r['command'] for r in journal] == earlier.commands()
    frames = {r['frame']: r for r in report['frames_captured'] if r['path'].endswith('_navigation.png')}
    saved = {r['frame']: r for r in report['read_only_pause_RAM_snapshots']}

    from pathlib import Path

    def snapshot(frame):
        row = saved[frame]
        assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    rows = {r['message_ID']: r for r in base.load(stage.PROOF)['records']}
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = image.read_file(stage.ARM), image.read_file('/GRP/KANJI.FNT')
    raster, _, _ = stage.portrait.font_tools(image)
    addresses = [unpack_from('<I', arm, at)[0] - stage.nav.BASE for at in (0x5444C, 0x54450)]
    cases = []
    sheet = Image.new('RGB', (768, 432), '#263238')
    label = ImageDraw.Draw(sheet)
    sequence = dict(zip(old_verifier.COMMON_IDS, old_verifier.COMMON_HOLDS, strict=True))
    panels = [(n, sequence[n]) for n in (2448, 2449, 2450)] + [(None, old_verifier.MENU), (None, 13627), (None, earlier.FINAL)]
    for i, (number, frame) in enumerate(panels):
        shot = old_verifier.captured(frames[frame])
        x, y = i % 3 * 256, i // 3 * 216
        label.text((x + 4, y + 4), str(number) if number else ('Choice / Baby Shark / Sailing'.split(' / ')[i - 3]), fill='white')
        sheet.paste(shot.crop((0, 192, 256, 384)), (x, y + 22))
        if number:
            raw = snapshot(frame)
            plain, formatted = [raw[at:at + 256].split(b'\0', 1)[0] for at in addresses]
            row = rows[number]
            assert plain.hex() == row['staged_hex'] and formatted.hex() == row['display_hex']
            ink, glyphs = stage.portrait.render_portrait(raster, arm, kanji, formatted)
            assert stage.sha256(ink).hexdigest() == row['ink_sha256']
            assert bytes(bool(v) for v in ink) == old_verifier.portrait_ink(frames[frame]['path'], old_verifier.PAPER)
            cases.append(dict(message_ID=number, frame=frame, exact_visible_glyphs=True, glyph_count=len(glyphs), capture=frames[frame]))
    fixture = report['synthetic_condition_fixtures'][0]
    entry, next_word = earlier.initialized.ENTRY, earlier.initialized.CONTINUE + 4
    assert final[entry:next_word] == arm[entry:next_word]
    assert all(final[address-stage.nav.BASE] == snapshot(earlier.replay_base.PAUSE)[address-stage.nav.BASE]
               for address in fixture['actor_membership_fields'].values())
    _, get = get_machine(arm, final)
    item = get(0xCB190) + 4 + 4 * 20
    assert get(0x4A368, item) == 2 and get(0x4A224, item) == 4
    assert frames[earlier.FINAL]['framebuffer_sha256'] != frames[13627]['framebuffer_sha256']
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=candidate, actual_emulator=True, hardware=False,
                          original_exchange_before_choice=cases, original_raise_choice_and_item=True,
                          original_roster_and_code_restored=True, sailing_return=True, natural_shark_battle=False,
                          sheet={'path': str(SHEET), 'sha256': base.digest(SHEET)},
                          evidence={str(p): base.digest(p) for p in (report_path, journal_path, history_path, SHEET)}))
    print('Verified Samwell’s complete proposal, Al’s objection, the Baby Shark reward and the return to sailing.')


if __name__ == '__main__':
    if sys.argv[1:] == ['startup']:
        FunctionType(startup.startup.__code__, startup.env | {'parent': stage.parent, 'stage': stage})()
    elif sys.argv[1:] == ['verify']:
        verify()
    else:
        assert sys.argv[1:] == ['shark']
        replay()

