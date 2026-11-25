"""Verify both revised scenes offline and through the ordinary wind-question branch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import check_rafael_tavern_lesson_20261119 as tavern
from scripts import replay_rafael_voyage_ceuta_20261119 as replay
from scripts import replay_square_label_wording_20261119 as patcher
from scripts import review_rafael_voyage_ceuta_20261119 as stage
from scripts import verify_story_short_phrase_wraps_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

base, native, deck = stage.base, stage.native, tavern.deck
ROOT = stage.STAGED / 'verified_display'
OFFLINE = stage.STAGED / 'native_display' / 'native_display.json'
PROOF = ROOT / 'native_and_ordinary_gameplay.json'
STARTUP_DIR = stage.STAGED / 'own_startup'
STARTUP = stage.STAGED / 'own_startup_verification.json'
PRIOR_VOYAGE = stage.parent.VERIFY / 'ordinary_first_voyage_replay.json'


def startup(capture):
    target = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, STAGED=stage.STAGED, parent=stage.parent)
    FunctionType(tavern.startup.__code__, vars(tavern) | dict(stage=target, STARTUP=STARTUP, STARTUP_DIR=STARTUP_DIR))(capture)


def patch():
    target = SimpleNamespace(ROM=stage.ROM, CLEAN=native.CLEAN, ROOT=stage.STAGED)
    FunctionType(patcher.patch.__code__, vars(patcher) | dict(stage=target))()


def offline_pages():
    source = checked_text(getsource(offline.main), {
        'len(stored["groups"]) == 11': 'len(stored["groups"]) == 2',
        'len(checked) == len(previews) == 19 and len(retained) == 176': 'len(checked) == len(previews) == 12 and len(retained) == 35',
        'for r in checked) == 3': 'for r in checked) == 2',
        'Verified all 19 revised pages and 176 exact retentions.': 'Verified all 12 revised pages and 35 exact retentions.',
    })
    target = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, review=stage, parent=stage.parent, stage=stage.workflow.stage)
    env = vars(offline) | dict(build=target, ROOT=OFFLINE.parent, PROOF=OFFLINE)
    exec(compile(source, __file__+'::native-pages', 'exec'), env)
    env['main']()


def load_run(folder, hashes, evidence):
    paths = [folder / name for name in ('capture/capture_report.json', 'observer/commands.json', 'inputs.json', 'source_contract.json')]
    report, trace, inputs, _ = map(base.load, paths)
    assert report['ROM_sha256'] == hashes['rom'] and report['frames'] == replay.END
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == inputs
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == base.digest(donor['source'])
    evidence.update({str(p): base.digest(p) for p in paths})
    series = {n: tavern.observed_commands(trace, n, hashes[n]) for n in (42, 127)}
    assert len(series[42]) == 31 and len(series[127]) == 27
    return report, series, deck.shots(report)


def expected_page(painters, raw, ident):
    arm, cjk, paint, system_paint = painters
    selector, body = raw[5], raw[6:raw.index(0, 6)]
    assert body.isascii()
    if ident == 'DK4_MES_B42_R0080':
        assert body.startswith(b'FI,') and body.count(b'FI') == 1
        body = body.replace(b'FI', b'Rafael')
    else:
        assert b'FI' not in body
    if selector == 254:
        rendered = system_paint(body)
        stage.workflow.stage.system.check_FE_rows(body, rendered)
        pixels = rendered['physical']
        assert len(pixels) == 228 * 64
        assert all(not any(pixels[y * 228 + 216:(y + 1) * 228]) for y in range(64))
        plane = b''.join(pixels[y * 228:y * 228 + 216] for y in range(64))
    else:
        rendered = paint(arm, cjk, body)
        page, = rendered['pages']
        assert page['native_independent_plane_equal']
        plane = bytes.fromhex(page['native_plane_hex'])
    assert rendered['complete_consumed_bytes'] == len(body)
    mask = deck.TOOL.prior.masks(bytes(bool(p) for p in plane) if selector == 254 else plane)
    return selector, plane, mask


def hold_with_mask(entered, returned, pictures, font, selector, expected):
    for frame, photo in sorted(pictures.items()):
        if not entered['frame'] + 25 < frame < returned['frame'] - 4:
            continue
        screen = deck.captured(photo)
        if deck.TOOL.body_masks(screen) != expected:
            continue
        if selector == 254:
            assert not any(screen.getpixel((x,y)) == (98,97,98) for y in range(276,289) for x in range(14,244))
            assert not any(screen.getpixel((x,y)) == (0,8,0) for y in range(296,360) for x in range(232,244))
            name = None
        else:
            name = stage.NAMES[selector]
            complete_mask(font, name, screen, 16, 277, (98,97,98))
        return dict(frame=frame, nameplate=name, capture=photo['path'], sha256=photo['PNG_sha256']), screen
    raise AssertionError((selector, entered['frame'], returned['frame'], 'complete mask missing'))


def render_sheets(images, label, evidence):
    sheets = []
    for start in range(0, len(images), 3):
        batch = images[start:start+3]
        sheet = Image.new('RGB', (1024, len(batch)*284), '#263238')
        draw = ImageDraw.Draw(sheet)
        for row, (ident, before, after) in enumerate(batch):
            for col, (image, title) in enumerate(((before, 'Previous'), (after, 'Revised'))):
                x, y = col*512, row*284
                draw.text((x+5,y+4), f'{ident} / {title}', fill='white')
                crop = image.crop((0,252,256,384)).resize((512,264), Image.Resampling.NEAREST)
                sheet.paste(crop, (x,y+18))
        path = ROOT / f'{label}_{start//3+1}.png'
        sheet.save(path)
        evidence[str(path)] = base.digest(path)
        sheets.append(dict(path=str(path), sha256=evidence[str(path)]))
    return sheets


def gameplay():
    assert not ROOT.exists()
    stored, draft, release, previous_voyage, checks = map(base.load,
        (stage.PROOF, stage.OUTPUT, stage.parent.RELEASE, PRIOR_VOYAGE, OFFLINE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == checks['candidate_sha256'] and stored['whole_parent_inverse']
    assert stored['predecessor_sha256'] == release['candidate_sha256'] == previous_voyage['candidate_sha256']
    assert stored['manuscript_sha256'] == base.digest(stage.OUTPUT)
    evidence = {str(p): base.digest(p) for p in (stage.PROOF, stage.OUTPUT, PRIOR_VOYAGE, OFFLINE, Path(__file__))}
    before, after = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    for p in (native.ARM, deck.FONT, '/data/EV0.DK4', '/COMMON/MESFILE.DK4'):
        assert before.read_file(p) == after.read_file(p)
    bank = [native.IlnkContainer.parse(im.read_file(deck.SC0)).blocks for im in (before, after)]
    assert [i for i, (a,b) in enumerate(zip(*bank, strict=True)) if a != b] == [42,127]
    baseline_release = stage.parent.parent
    baseline = base.load(baseline_release.RELEASE)
    assert base.digest(baseline_release.ROM) == baseline['candidate_sha256']
    assert release['predecessor']['candidate_sha256'] == baseline['candidate_sha256']
    comparison = base.NdsImage.open(baseline_release.ROM)
    original, latest = map(native.files, (comparison, before))
    assert original.keys() == latest.keys()
    assert {p for p in original if original[p] != latest[p]} == {deck.SC0}
    older = native.IlnkContainer.parse(original[deck.SC0]).blocks
    assert [i for i, (a,b) in enumerate(zip(older, bank[0], strict=True)) if a != b] == [138]
    evidence[str(baseline_release.RELEASE)] = base.digest(baseline_release.RELEASE)
    runs = [load_run(stage.ROOT / case, {'rom': rom} | {g['block']:g[own] for g in stored['groups']}, evidence)
        for case, rom, own in (('current_v2',baseline['candidate_sha256'],'before'), ('revised_v3',candidate,'after'))]
    assert runs[0][0]['scripted_input_schedule'] == runs[1][0]['scripted_input_schedule']
    assert runs[0][0]['core_options'] == runs[1][0]['core_options']
    assert runs[0][0]['core_DLL_sha256'] == runs[1][0]['core_DLL_sha256']
    assert runs[0][0]['battery_save_preloaded']['source_sha256'] == runs[1][0]['battery_save_preloaded']['source_sha256']
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release['own_registered_startup'], captain=3)
    system_paint = stage.workflow.stage.system.native_painter(ctx)
    _, paint = offline.workflow.early.prior.precedent.planners(ctx.arm)
    font = deck.GameAsciiFont.from_arm9(ctx.arm)
    painters = (ctx.arm, after.read_file(deck.FONT), paint, system_paint)
    rows = {r['id']:r for r in draft['records']}
    proofs = {r['id']:r for r in checks['revisions']}
    voyage_old = {r['id']:r for r in previous_voyage['native_speech_pages']}
    pairs, shots, menus, unvisited = [], [], [], []
    for group in stored['groups']:
        block = group['block']
        commands = {c['stored_offset']:c for c in group['commands']}
        observed_before = {r['source']['instruction_offset']:(e,r) for e,r in runs[0][1][block]}
        expected = {c['current_offset'] for e,r in runs[1][1][block] for c in [commands[r['source']['instruction_offset']]]}
        assert observed_before.keys() == expected
        assert runs[1][1][block][-1][1]['result_words'] == [0, 1 if block == 127 else 0]
        for entered, returned in runs[1][1][block]:
            at, word = returned['source']['instruction_offset'], returned['source']['first_word']
            command = commands.pop(at)
            assert command['word'] == word
            prior = observed_before[command['current_offset']]
            assert prior[1]['result_words'] == returned['result_words']
            old, new = map(bytes.fromhex, (command['current'], command['stored']))
            assert old == bank[0][block][command['current_offset']:command['current_offset']+len(old)]
            assert new == bank[1][block][at:at+len(new)]
            if word == 0x2100:
                assert old == new and returned['result_words'] == [2, 1]
                assert tuple(labels(new)) == (b"I've got it!", b'The wind might be against us...')
                for frame in (31708,31800):
                    a,b = (deck.captured(run[2][frame]) for run in runs)
                    assert ImageChops.difference(a,b).getbbox() is None
                    row = runs[1][2][frame]
                    evidence[row['path']] = row['PNG_sha256']
                    menus.append(row)
                continue
            if word != 0x4000:
                continue
            ident, = command['record_ids']
            row = rows[ident]
            selector, plane, mask = expected_page(painters, new, ident)
            assert selector == row['source_selector']
            held, photo = hold_with_mask(entered, returned, runs[1][2], font, selector, mask)
            evidence[held['capture']] = held['sha256']
            item = dict(id=ident, current=held, revised=row['decision']=='revision', plane_sha256=native.digest(plane))
            if item['revised']:
                assert bytes.fromhex(proofs[ident]['pages'][0]['native_plane_hex']) == plane
                if block == 42:
                    old_shot = voyage_old[ident]
                    prior_photo = next(r for r in base.load(Path(old_shot['capture']).parent/'capture_report.json')['frames_captured']
                                       if r['path'] == old_shot['capture'])
                    old_image = deck.captured(prior_photo)
                    evidence[prior_photo['path']] = prior_photo['PNG_sha256']
                else:
                    _, _, old_mask = expected_page(painters, old, ident)
                    _, old_image = hold_with_mask(*prior, runs[0][2], font, selector, old_mask)
                shots.append((ident, old_image, photo))
            pairs.append(item)
        unvisited.extend(r for c in commands.values() for r in c['record_ids'])
    assert len(pairs) == 44 and len(shots) == 12 and len(menus) == 2
    assert unvisited == ['DK4_MES_B127_R0044']
    for frame in (29295, 33860):
        a,b = (deck.captured(run[2][frame]) for run in runs)
        assert ImageChops.difference(a,b).getbbox() is None
        row = runs[1][2][frame]
        evidence[row['path']] = row['PNG_sha256']
    ROOT.mkdir()
    sheets = render_sheets(shots, 'voyage_ceuta_comparisons', evidence)
    base.save(PROOF, dict(candidate_sha256=candidate, predecessor_sha256=stored['predecessor_sha256'], hardware=False,
        ordinary_gameplay_existing_save=True, panels=pairs, seen_native_choice_labels=menus, wind_choice_native_result=[2,1],
        unvisited_confident_branch_records=unvisited, Port_menu_frame=29295, after_Ceuta_return_frame=33860,
        comparison_candidate_sha256=baseline['candidate_sha256'], comparison_differs_from_predecessor_only_in_SC0_B138=True,
        exact_offline_retention_count=len(checks['exact_retentions']), sheets=sheets, evidence=evidence))
    print('Verified 28 first-voyage panels and 16 Ceuta panels, both choice captions, and the ordinary wind-branch return.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('offline', 'startup', 'capture-startup', 'patch', 'gameplay'))
    action = parser.parse_args().action
    if action in ('startup', 'capture-startup'):
        startup(action == 'capture-startup')
    else:
        {'offline': offline_pages, 'patch': patch, 'gameplay': gameplay}[action]()
