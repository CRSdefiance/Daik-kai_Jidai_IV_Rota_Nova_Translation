"""Exercise original Shipyard detail drawing with one stock ship-model link."""

from argparse import ArgumentParser
from json import dumps
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import stage_specialized_ship_labels_20261115 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_special_target_labels_20261115 import c_string
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
FRAME, END = 4500, 6500
SHOTS = (4200, 4500, 5000, 5209, 5500, 5800, 6200, 6499)
MODELS = {65: 15, 82: 32, 107: 22}


def select_model(arm, raw, model, expected, arm_sha):
    assert stage.sha256(arm).hexdigest() == arm_sha and len(raw) == 0x400000
    cpu, get = get_machine(arm, raw)
    assert get(0x2E58C) == 1
    company = get(0xCB1A8) + 4 + 132
    model_root = get(0xCB148)
    old = get(0x36C94, company + 12)
    assert old == model_root + 4 and c_string(cpu, old + 8, 'ascii')['text'] == 'Vestaros'
    target = model_root + 4 + model * 140
    assert get(0x11DB0, target) == MODELS[model]
    assert c_string(cpu, target + 8, 'cp932')['text'] == expected
    field = company + 16
    at = field - stage.BASE
    assert raw[at] == 0
    cpu.mem_write(field, bytes([model]))
    assert get(0x36C94, company + 12) == target
    after = raw[:at] + bytes([model]) + raw[at + 1:]
    return after, dict(changes=[dict(address=field, before=0, after=model)],
        scope='One existing fleet model link in the copied save session',
        original_catalogue_model=model, unchanged_stock_model_label=expected, original_model_class=MODELS[model],
        natural_acquisition=False, no_custom_label_or_render_state_written=True)


def replay(model, version, attempt):
    release, manuscript = map(base.load, (stage.parent.RELEASE, stage.OUTPUT))
    before = version == 'parent'
    rom = stage.parent.ROM if before else stage.ROM
    identity = release['candidate_sha256'] if before else manuscript['candidate_sha256']
    arm_sha = (release if before else manuscript)['target_ARM9_sha256']
    assert base.digest(rom) == identity
    row, = [r for r in manuscript['records'] if r['decision'] == 'revision'
            and any(x['pointer_field'] == stage.design_field(model) for x in r['source_references'])]
    ref, = [r for r in row['source_references'] if r['pointer_field'] == stage.design_field(model)]
    expected = ref['current']['text'] if before else row['english']
    root = stage.ROOT / f'focused_{model}_{version}_{attempt}'
    root.mkdir()
    history = base.load(stage.ROOT / 'istanbul_special_parent/capture_report.json')
    donor = history['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256'] and donor['copied_byte_exact_before_cold_boot']
    inputs = [r for r in base.load(stage.ROOT / 'istanbul_special_continue_inputs.json') if r['start'] <= 5101]
    inputs.extend(dict(start=t, duration=8, buttons=['B']) for t in (5901, 6301))
    plan = root / 'inputs.json'
    base.save(plan, inputs)
    commands = [{'until': END, 'condition_fixture': model}, {'stop': True}]
    journal = root / 'commands.jsonl'
    journal.write_text(''.join(dumps(command) + '\n' for command in commands), encoding='utf-8')
    settings = [harness.__file__, '--rom', str(rom), '--out', str(root / 'capture'), '--frames', str(END + 1),
        '--inputs-json', str(plan), '--touchscreen', '--battery-save', donor['source'], '--capture-every', '99999',
        '--capture-at', *map(str, SHOTS), '--pause-at', str(FRAME), '--allow-condition-fixtures']
    stdin, argv, setter = sys.stdin, sys.argv, adapter.set_condition
    stream = GrowingCommands(journal)
    try:
        sys.stdin, sys.argv = stream, settings
        adapter.set_condition = lambda arm, raw, request: select_model(arm, raw, request, expected, arm_sha)
        harness.main()
    finally:
        sys.stdin, sys.argv, adapter.set_condition = stdin, argv, setter
        stream.close()
    report = root / 'capture/capture_report.json'
    result = base.load(report)
    assert result['ROM_sha256'] == identity and result['frames'] == END and not result['callback_errors']
    assert result['cold_boot'] and not result['savestate_loaded']
    fixture, = result['synthetic_condition_fixtures']
    assert fixture['frame'] == FRAME and fixture['original_catalogue_model'] == model
    assert len(fixture['changes']) == 1


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('model', type=int, choices=MODELS)
    parser.add_argument('version', choices=('parent', 'staged'))
    parser.add_argument('--attempt', type=int, default=1)
    options = parser.parse_args()
    replay(options.model, options.version, options.attempt)
