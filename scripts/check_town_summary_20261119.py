"""Verify Town Summary headings, exact reconstruction, and candidate startup."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_inn_numerals_20261119 as verification
from scripts import stage_town_summary_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots

base, inn = stage.base, verification.inn
STARTUP = stage.ROOT / 'own_startup'
STARTUP_PROOF = stage.ROOT / 'own_startup_verification.json'
PLAYBACK = stage.ROOT / 'verified_town_summary_v3.json'
SHEET = stage.ROOT / 'town_summary_comparison.png'
SCREEN_INSET_X = 8
STATUS_REGION = (76, 48, 112, 60)
INK = (197, 198, 197)


def mask(image, font, word, rectangle):
    left, top, right, bottom = rectangle
    expected = {(left + 6*i + x, top + 1 + y)
                for i, char in enumerate(word) for x in range(6) for y in range(11)
                if font.decode(char).getpixel((x, y))}
    assert all(left <= x < right and top <= y < bottom for x, y in expected)
    actual = {(x, y) for x in range(left, right) for y in range(top, bottom) if image.getpixel((x, y)) == INK}
    assert actual == expected, (word, rectangle, len(expected-actual), len(actual-expected))
    return dict(text=word, complete_ink_pixels=len(actual), rectangle=rectangle)


def verify():
    assert not PLAYBACK.exists()
    staged = base.load(stage.PROOF)
    runs = [stage.observe.ROOT / case for case in ('baseline_v2', 'corrected')]
    reports = [folder / 'capture/capture_report.json' for folder in runs]
    traces = [folder / 'requests.json' for folder in runs]
    old, new = map(base.load, reports)
    assert (old['ROM_sha256'], new['ROM_sha256']) == (staged['parent_sha256'], staged['candidate_sha256'])
    assert new['ROM_sha256'] == base.digest(stage.ROM)
    assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and old['core_options'] == new['core_options']
    assert old['core_DLL_sha256'] == new['core_DLL_sha256']
    for report in (old, new):
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']

    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    a, b = (base.load(p) for p in traces)
    for trace in (a, b):
        assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        assert len(trace['rows']) == 1
    prior, correct = a['rows'][0], b['rows'][0]
    assert prior['frame'] == correct['frame'] and prior['cursor'] == correct['cursor'] == [84, 60]
    assert prior['clip_rect'] == correct['clip_rect'] == [0, 0, 228, 72]
    assert bytes.fromhex(correct['text_hex']) == arm[stage.TEXT:stage.TEXT+24]
    assert bytes.fromhex(correct['layout_hex']) == arm[stage.LAYOUT:stage.LAYOUT+0x200]

    font = GameAsciiFont.from_arm9(arm)
    old_shots, new_shots = map(shots, (old, new))
    assert old_shots.keys() == new_shots.keys()
    changed, seen = [], []
    evidence = {str(p): base.digest(p) for p in (*reports, *traces, Path(__file__))}
    for frame in sorted(old_shots):
        before, after = captured(old_shots[frame]), captured(new_shots[frame])
        diff = ImageChops.difference(before, after)
        if diff.getbbox() is None:
            continue
        changed.append(frame)
        diff.paste((0, 0, 0), STATUS_REGION)
        assert diff.getbbox() is None
        for photo, revision in ((before, False), (after, True)):
            for row in staged['records']:
                _, x, y, _, _, w, h = row['staged_geometry' if revision else 'original_geometry']
                x += SCREEN_INSET_X
                text = row['english' if revision else 'previous_English']
                seen.append(dict(frame=frame, revision=revision, **mask(photo, font, text, (x, y, x+w, y+h))))
        evidence.update({ref[frame]['path']: ref[frame]['PNG_sha256'] for ref in (old_shots, new_shots)})
    assert {3720, 4750, 5150}.issubset(changed)
    frame = 4750
    sheet = Image.new('RGB', (1024, 402), '#263238')
    draw = ImageDraw.Draw(sheet)
    for column, (ref, caption) in enumerate(((old_shots, 'Previous'), (new_shots, 'Corrected'))):
        draw.text((column*512+6, 4), f'{caption} / Lisbon Square', fill='white')
        panel = captured(ref[frame]).crop((0, 0, 256, 192))
        sheet.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (column*512, 18))
    if SHEET.exists():
        with Image.open(SHEET) as prior_sheet:
            assert prior_sheet.tobytes() == sheet.tobytes()
    else:
        sheet.save(SHEET)
    evidence[str(SHEET)] = base.digest(SHEET)
    base.save(PLAYBACK, dict(candidate_sha256=new['ROM_sha256'], prior_sha256=old['ROM_sha256'],
        ordinary_input=True, hardware=False, observed_town='Lisbon', sampled_changed_frames=changed,
        pixels_outside_status_exact=True, original_draw_and_clip_exact=True, complete_heading_masks=seen,
        sheets=[dict(path=str(SHEET), sha256=evidence[str(SHEET)])], evidence=evidence))
    print(f'All four headers passed exact glyph checks in {len(changed)} Lisbon Town Summary holds.')


def verify_startup():
    """Reuse the captured startup and allow only the verified heading change at Town."""
    assert not STARTUP_PROOF.exists()
    reference = inn.boot.boot.boot_audit
    previous = base.load(stage.parent.RELEASE)
    basis = base.load(STARTUP / 'basis.json')
    assert base.digest(basis['previous_report']) == basis['previous_report_sha256']
    assert base.digest(basis['manifest']) == basis['manifest_sha256']
    assert base.digest(stage.parent.MANIFEST) == previous['manifest_sha256']
    proof = checked_text(getsource(reference.verify_startup), {
        "ROOT / 'own_startup/capture/capture_report.json'": 'REPORT',
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": 'PRIOR_REPORT',
        "    term = load(ROOT / 'own_startup/terminal.json')\n"
        "    assert term['candidate_sha256'] == digest(ROM) and term['report_sha256'] == digest(path)\n": '',
        "proof['registered_input']['candidate_sha256']": "proof['parent_sha256']",
        "BIOGRAPHIES / 'own_startup_verification.json'": 'PRIOR_BOOT',
        "    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in frames)":
            "    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in frames[:-1])\n"
            "    before, after = (captured(ref[frames[-1]]) for ref in (old, new))\n"
            "    difference = ImageChops.difference(before, after)\n"
            "    assert difference.getbbox() is not None\n"
            "    difference.paste((0, 0, 0), STATUS_REGION)\n"
            "    assert difference.getbbox() is None\n"
            "    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(ARM))\n"
            "    status = mask(after, font, 'Status', STATUS_REGION)",
        'exact_matching_frames=[new[n] for n in frames], complete_deployed_payload_exact=True,':
            'exact_matching_frames=[new[n] for n in frames[:-1]], complete_deployed_payload_exact=True,\n'
            '        town_status_only_frame=new[frames[-1]], complete_town_status_mask=status,',
        '(path, parent_path, prior_proof, Path(__file__))':
            "(path, parent_path, prior_proof, Path(__file__), old[frames[-1]]['path'], new[frames[-1]]['path'])",
        'Candidate startup matched all six holds and 24 protected name getters.':
            'Five exact startup holds, the corrected Town Summary hold and 24 protected name getters passed.',
    })
    scope = vars(reference) | dict(ROM=stage.ROM, PROOF=stage.PROOF, BOOT=STARTUP_PROOF,
        REPORT=STARTUP/'capture/capture_report.json', PRIOR_REPORT=Path(basis['previous_report']),
        PRIOR_BOOT=Path(previous['own_registered_startup']), captured=captured, ImageChops=ImageChops,
        GameAsciiFont=GameAsciiFont, STATUS_REGION=STATUS_REGION, mask=mask, __file__=__file__)
    exec(compile(proof, __file__ + '::town-summary-startup', 'exec'), scope)
    scope['verify_startup']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('verify', 'startup', 'verify_startup', 'patch'))
    action = parser.parse_args().action
    if action == 'startup':
        run = inn.boot.boot.boot_replay.previous.startup
        FunctionType(run.__code__, run.__globals__ | {'stage': stage, 'STARTUP': STARTUP})()
        verify_startup()
    else:
        tasks = {'verify': verify, 'verify_startup': verify_startup,
                 'patch': FunctionType(verification.patch.__code__, vars(verification) | globals())}
        tasks[action]()
