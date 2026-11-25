"""Check the stored and ordinary-gameplay display of the Baltic trade lesson."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_hodram_baltic_trade_20261121 as replay
from scripts import stage_hodram_baltic_trade_20261121 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as inherited


base, native = stage.base, stage.native
square = stage.preview.dialogue.square
town = square.town
ROOT = stage.ROOT / 'native_display'
PROOF = ROOT / 'native_display.json'
LIVE = replay.ROOT / 'ordinary_hamburg_port_replay.json'


def stored_display():
    assert not ROOT.exists()
    draft, proof, release = map(base.load, (stage.OUTPUT, stage.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == proof['candidate_sha256']
    assert proof['predecessor_sha256'] == release['candidate_sha256'] and proof['whole_parent_inverse']
    assert proof['manuscript_sha256'] == base.digest(stage.OUTPUT)
    image, parent = map(base.NdsImage.open, (stage.ROM, stage.parent.ROM))
    assert all(image.read_file(path) == parent.read_file(path) for path in inherited.ASSETS)
    arm, font = (image.read_file(path) for path in (native.ARM, '/GRP/KANJI.FNT'))
    draw = town.clipped_renderer(SimpleNamespace(arm=arm, image=image))
    block = native.IlnkContainer.parse(image.read_file(stage.SCENE)).blocks[stage.BLOCK]
    group, = proof['groups']
    assert native.digest(block) == group['after']
    rows = {row['id']: row for row in draft['records']}
    pictures, readings = [], []
    for command in group['commands']:
        at, data = command['stored_offset'], bytes.fromhex(command['stored'])
        assert block[at:at + len(data)] == data
        if not command['record_ids']:
            continue
        ident, = command['record_ids']
        row = rows.pop(ident)
        selector = row['source_selector']
        old = bytes.fromhex(command['current'])
        assert data[:6] == old[:6] == bytes.fromhex('0040ffff00') + bytes([selector])
        end = data.index(0, 6)
        assert not any(data[end:]) and len(data) % 2 == 0
        body = data[6:end]
        assert not any(token in body for token in (b'FI', b'FA', b'FO'))
        entry = dict(id=ident, file_path=stage.SCENE, block=stage.BLOCK, decision=row['decision'],
            stored_offset=at, stored_command_hex=data.hex(), installed_selector_and_body=data[5:end].hex(),
            native_pages=1)
        if row['decision'] == 'revision':
            plan = group['plans'][ident]
            encoded = bytes.fromhex(plan['encoded_hex'])
            assert data != old and plan['expected_native_pages'] == 1
            assert encoded[0] == selector and body[len(encoded) - 1:] in (b'', b' ')
            assert body[:len(encoded) - 1] == encoded[1:]
            assert ' '.join(body.decode('ascii').split()) == row['english']
            picture = draw(arm, font, body)
            page, = picture['pages']
            assert picture['complete_consumed_bytes'] == len(body) and page['native_independent_plane_equal']
            assert page['all_bitmap_header_input_canaries_exact']
            pixels = bytes.fromhex(page['native_plane_hex'])
            entry.update(automatic_lines=plan['lines'], complete_visible_characters=True,
                         native_mask_sha256=native.digest(pixels), canaries_and_bounds_exact=True)
            pictures.append((f"{ident} {row['speaker']}", pixels))
        else:
            assert data == old
        readings.append(entry)
    assert not rows and len(readings) == 9 and len(pictures) == 5
    ROOT.mkdir()
    contact = inherited.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {'ROOT': ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=proof['candidate_sha256'], stage_proof_sha256=base.digest(stage.PROOF),
        records=readings, newly_rendered_pages=len(pictures), sheets=sheets, actual_gameplay=False))
    print('Verified five one-page stored revisions and four byte-exact retentions.')


def observed_play():
    assert not LIVE.exists()
    evidence = (PROOF, replay.REPORT, replay.BASELINE, replay.PLAN, replay.ROOT / 'replay_scope.json',
                replay.ROOT / 'inputs.json')
    rendered, current, before, plan, scope, schedule = map(base.load, evidence)
    manuscript = base.load(stage.OUTPUT)
    candidate = base.digest(stage.ROM)
    assert candidate == current['ROM_sha256'] == rendered['candidate_sha256'] == scope['candidate_sha256']
    assert candidate == base.digest(stage.ROOT / 'clean_rebuilt.nds')
    assert current['frames'] == plan['port_return']
    assert scope['original_report_sha256'] == base.digest(replay.BASELINE)
    assert scope['original_plan_sha256'] == base.digest(replay.PLAN) and scope['schedule_sha256'] == base.digest(evidence[-1])
    assert schedule == current['scripted_input_schedule']
    assert schedule == [row for row in before['scripted_input_schedule'] if row['start'] <= current['frames']]
    for report in (current, before):
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == scope['donor_sha256']
        assert base.digest(donor['source']) == donor['source_sha256']
    new_shots = {r['frame']: r for r in current['frames_captured'] if r['path'].endswith('_cold_boot.png')}
    old_shots = {r['frame']: r for r in before['frames_captured'] if r['path'].endswith('_navigation.png')}
    image = base.NdsImage.open(stage.ROM)
    arm, font = (image.read_file(p) for p in (native.ARM, '/GRP/KANJI.FNT'))
    draw = town.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    name_font = square.GameAsciiFont.from_arm9(arm)
    holds, controls, previews = [], [], []
    rows = {row['id']: row for row in manuscript['records']}
    for checked, frame in zip(rendered['records'], plan['panels'], strict=True):
        ident = checked['id']
        row = rows[ident]
        observed, picture = town.read_frame(new_shots, frame)
        if row['decision'] == 'retention':
            earlier, _ = town.read_frame(old_shots, frame)
            assert earlier['framebuffer_sha256'] == observed['framebuffer_sha256'], ident
            controls.append(dict(id=ident, frame=frame, before=earlier, after=observed))
        else:
            body = bytes.fromhex(checked['installed_selector_and_body'])[1:]
            page, = draw(arm, font, body)['pages']
            mask = bytes.fromhex(page['native_plane_hex'])
            assert native.digest(mask) == checked['native_mask_sha256']
            assert square.previous.mask_check(mask, 216, picture), (ident, frame)
            square.previous.complete_mask(name_font, row['speaker'], picture, 16, 277, town.INKS[1])
            holds.append(dict(id=ident, file_path=stage.SCENE, block=stage.BLOCK, frame=frame, observed=observed))
        previews.append((ident, picture))
    transitions = {}
    for frame, label in ((19965, 'Speyer fleet warning'), (24965, 'Hamburg discovery'),
                         (plan['dock_prompt'], 'Docking prompt'), (plan['port_return'], 'Return to Hamburg')):
        after, picture = town.read_frame(new_shots, frame)
        earlier, _ = town.read_frame(old_shots, frame)
        assert after['framebuffer_sha256'] == earlier['framebuffer_sha256'], (label, frame)
        transitions[label] = after
        if frame == plan['port_return']:
            previews.append((label, picture))
    snapshot = current['read_only_RAM_snapshot']
    assert snapshot['read_only_export'] and base.digest(snapshot['path']) == snapshot['sha256']
    state = square.navigation_state(arm, Path(snapshot['path']).read_bytes(), square.EXCHANGES['hamburg'])
    assert state['town'] == 5 and state['calendar'][1:] == [6, 29]
    assert len(holds) == 5 and len(controls) == 4
    sheets = []
    for index in range(0, len(previews), 6):
        file = replay.ROOT / f'baltic_trade_gameplay_{index // 6 + 1}.png'
        town.sheet(previews[index:index + 6], file)
        sheets.append(dict(path=str(file), sha256=base.digest(file)))
    base.save(LIVE, dict(candidate_sha256=candidate, exact_native_glyph_matches=True, natural_activation=True,
        original_port_transition=True, hardware_verified=False, holds=holds, unchanged_controls=controls,
        transitions=transitions, sheets=sheets, read_only_snapshot=snapshot,
        evidence={str(path): base.digest(path) for path in evidence}))
    print('Verified five revised and four retained panels during the ordinary Hamburg approach and port return.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('check', choices=('native', 'voyage'))
    args = parser.parse_args()
    (stored_display if args.check == 'native' else observed_play)()
