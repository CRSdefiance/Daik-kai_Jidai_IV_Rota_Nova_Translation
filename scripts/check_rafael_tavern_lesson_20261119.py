"""Check full native glyph masks and bind the observed recruitment sequence to the ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_rafael_deck_after_trade_20261119 as deck
from scripts import replay_deck_comments_20261119 as boot
from scripts import replay_rafael_tavern_lesson_20261119 as replay
from scripts import review_rafael_tavern_lesson_20261119 as stage
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.STAGED / 'verified_display'
PROOF = ROOT / 'native_and_ordinary_gameplay.json'
STARTUP = stage.STAGED / 'own_startup_verification.json'
STARTUP_DIR = stage.STAGED / 'own_startup'


def startup(capture=False):
    if capture:
        run = boot.boot_replay.previous.startup
        target = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, ROOT=stage.STAGED, parent=stage.parent)
        FunctionType(run.__code__, run.__globals__ | dict(stage=target, STARTUP=STARTUP_DIR))()
    basis = base.load(STARTUP_DIR/'basis.json')
    for key in ('previous_report', 'manifest'):
        assert base.digest(basis[key]) == basis[f'{key}_sha256']
    source = checked_text(getsource(boot.boot_audit.verify_startup), {
        "ROOT / 'own_startup/capture/capture_report.json'": "REPORT",
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": "PRIOR_REPORT",
        "    term = load(ROOT / 'own_startup/terminal.json')\n"
        "    assert term['candidate_sha256'] == digest(ROM) and term['report_sha256'] == digest(path)\n": "",
        "proof['registered_input']['candidate_sha256']": "proof['predecessor_sha256']",
        "BIOGRAPHIES / 'own_startup_verification.json'": "PRIOR_BOOT",
    })
    previous = base.load(stage.parent.RELEASE)
    scope = vars(boot.boot_audit) | dict(ROM=stage.ROM, PROOF=stage.PROOF, BOOT=STARTUP,
        REPORT=STARTUP_DIR/'capture/capture_report.json', PRIOR_REPORT=Path(basis['previous_report']),
        PRIOR_BOOT=Path(previous['own_registered_startup']), __file__=__file__)
    exec(compile(source, __file__ + '::startup', 'exec'), scope)
    scope['verify_startup']()


def observed_commands(trace, block, expected):
    matches = []
    for returned in trace['rows']:
        if returned['kind'] != 'after_command' or returned['source'].get('block') != block:
            continue
        entered = trace['rows'][returned['entry_row']]
        assert entered['kind'] == 'before_command'
        for row in (entered, returned):
            source = row['source']
            assert (source['classification'], source['route'], source['block']) == ('original_SC_cache', 0, block)
            assert source['whole_resident_payload_exact_ROM']
            assert source['actual_sha256'] == source['registered_sha256'] == expected
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        assert entered['source']['instruction_offset'] == returned['source']['instruction_offset']
        matches.append((entered, returned))
    return matches


def checked_run(case, rom_hash, block_hash, evidence):
    folder = replay.ROOT / case
    paths = [folder / p for p in ('capture/capture_report.json', 'observer/commands.json', 'inputs.json', 'source_contract.json')]
    report, trace, inputs, _ = map(base.load, paths)
    assert report['ROM_sha256'] == rom_hash and report['cold_boot'] and not report['savestate_loaded']
    assert report['scripted_input_schedule'] == inputs and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['mismatches'] and not trace['errors']
    evidence.update({str(p): base.digest(p) for p in paths})
    return report, trace, observed_commands(trace, 138, block_hash), deck.shots(report)


def main():
    assert not ROOT.exists()
    stored, draft, packet = map(base.load, (stage.PROOF, stage.OUTPUT, stage.SOURCE))
    assert base.digest(stage.ROM) == stored['candidate_sha256'] and stored['whole_parent_inverse']
    assert base.digest(stage.parent.ROM) == stored['predecessor_sha256']
    assert base.digest(stage.OUTPUT) == stored['manuscript_sha256']
    assert base.digest(stage.SOURCE) == draft['source_packet_sha256']
    group, = stored['groups']
    evidence = {str(p): base.digest(p) for p in (stage.PROOF, stage.OUTPUT, stage.SOURCE, Path(__file__), Path(replay.__file__))}
    before, after = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    for path in (native.ARM, deck.FONT, '/data/EV0.DK4', '/COMMON/MESFILE.DK4'):
        assert before.read_file(path) == after.read_file(path)
    bank = [native.IlnkContainer.parse(im.read_file(deck.SC0)).blocks for im in (before, after)]
    assert [i for i, (a, b) in enumerate(zip(*bank, strict=True)) if a != b] == [138]
    assert group['before'] == native.digest(bank[0][138]) and group['after'] == native.digest(bank[1][138])
    arm, cjk = after.read_file(native.ARM), after.read_file(deck.FONT)
    _, paint = stage.template.stage.progressive.layout.prior.precedent.planners(arm)
    font = GameAsciiFont.from_arm9(arm)
    runs = [checked_run(case, stored[rom_key], group[block_key], evidence) for case, rom_key, block_key in (
        ('recruit_probe_v1', 'predecessor_sha256', 'before'), ('tavern_final_v3', 'candidate_sha256', 'after'))]
    assert runs[0][0]['core_DLL_sha256'] == runs[1][0]['core_DLL_sha256']
    assert runs[0][0]['core_options'] == runs[1][0]['core_options']
    assert runs[0][0]['battery_save_preloaded']['source_sha256'] == runs[1][0]['battery_save_preloaded']['source_sha256']
    pre_assignment = [[r for r in run[0]['scripted_input_schedule'] if r['start'] < 21440] for run in runs]
    assert pre_assignment[0] == pre_assignment[1]
    assert all(len(run[2]) == len(group['commands']) == packet['groups'][0]['native_commands'] == 10 for run in runs)
    assert all(run[2][-1][1]['result_words'][0] == 0 for run in runs)
    drafts = {r['id']: r for r in draft['records']}
    pairs, images = [], []
    for i, cmd in enumerate(group['commands']):
        word = cmd['word']
        holds = []
        for n, (run, side) in enumerate(zip(runs, ('current', 'stored'), strict=True)):
            entered, returned = run[2][i]
            at = cmd[f'{side}_offset']
            raw = bytes.fromhex(cmd[side])
            assert raw == bank[n][138][at:at+len(raw)]
            assert entered['source']['instruction_offset'] == at and entered['source']['first_word'] == word
            if word != 0x4000:
                assert cmd['current'] == cmd['stored'] and not cmd['record_ids']
                continue
            selector, body, page, mask = deck.pixel_page(arm, cjk, paint, raw)
            assert selector == 6 and body.isascii() and page['native_independent_plane_equal']
            hold, photo = deck.match_page(entered, returned, run[3], font, selector, mask)
            evidence[hold['capture']] = hold['sha256']
            holds.append((dict(**hold, body_hex=body.hex(), native_plane_sha256=native.digest(bytes.fromhex(page['native_plane_hex']))), photo))
        if word != 0x4000:
            continue
        ident, = cmd['record_ids']
        revision = drafts[ident]['decision'] == 'revision'
        assert (cmd['current'] != cmd['stored']) == revision
        assert (holds[0][0]['native_plane_sha256'] != holds[1][0]['native_plane_sha256']) == revision
        pairs.append(dict(id=ident, revision=revision, previous=holds[0][0], current=holds[1][0], command=cmd))
        if revision:
            images.append((ident, holds[0][1], holds[1][1]))
    assert len(pairs) == 7 and len(images) == 5

    # The original event dispatches the resupply block after completing the Tavern lesson.
    event_file = after.read_file('/data/EV0.DK4')
    assert event_file == base.NdsImage.open(native.CLEAN).read_file('/data/EV0.DK4')
    events = [e for e in parse_events(event_file) if e['event_ID'] in (42, 138)]
    assert [(e['event_ID'], e['script_block'], e['must_be_completed']) for e in events] == [(42, 42, [138]), (138, 138, [])]
    reserve = observed_commands(runs[1][1], 42, native.digest(bank[1][42]))
    root_frames = runs[1][3]
    menu = {n: root_frames[n] for n in (20305, 21625, 21845, 22325, 22565)}
    for row in menu.values():
        assert base.digest(row['path']) == row['PNG_sha256']
        evidence[row['path']] = row['PNG_sha256']
    ROOT.mkdir()
    sheets = []
    for index in range(0, len(images), 3):
        batch = images[index:index+3]
        sheet = Image.new('RGB', (1024, len(batch)*404), '#263238')
        draw = ImageDraw.Draw(sheet)
        for row, (ident, old, new) in enumerate(batch):
            for col, (photo, caption) in enumerate(((old, 'Previous'), (new, 'Revised'))):
                x, y = col*512, row*404
                draw.text((x+5, y+3), f'{ident} / {caption}', fill='white')
                sheet.paste(photo.crop((0,192,256,384)).resize((512,384), Image.Resampling.NEAREST), (x,y+18))
        path = ROOT / f'recruitment_comparison_{index//3+1}.png'
        sheet.save(path)
        evidence[str(path)] = base.digest(path)
        sheets.append(dict(path=str(path), sha256=evidence[str(path)]))
    base.save(PROOF, dict(candidate_sha256=stored['candidate_sha256'], predecessor_sha256=stored['predecessor_sha256'],
        ordinary_gameplay_existing_save=True, hardware=False, pairs=pairs, command_count=10,
        tutorial_exit_frames=[run[2][-1][1]['frame'] for run in runs],
        prior_and_current_exact_joined_speaker='Julio Erneco', menus_and_transitions=menu,
        event_file_sha256=native.digest(event_file), related_event_rows=events,
        first_voyage_observed_commands=[dict(frame=r['frame'], source=r['source']) for _,r in reserve],
        sheets=sheets, evidence=evidence))
    print(f'Verified all seven recruitment panels in both runs and {len(reserve)} naturally returned first-voyage commands.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('scene', 'startup', 'capture-startup'))
    action = parser.parse_args().action
    if action == 'scene':
        main()
    else:
        startup(capture=action == 'capture-startup')
