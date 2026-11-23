"""Match held dialogue, both trade-choice states, and their original returns."""

from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import check_rafael_sail_controls_replay_20261119 as precedent
from scripts import check_rafael_trade_and_arms_20261119 as offline
from scripts import replay_rafael_trade_and_arms_20261119 as replay
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = offline.base, offline.native, offline.stage
deck, old = precedent.deck, precedent.previous
PROOF = replay.ROOT / 'live_display.json'
CHOICES = {'trade-advice': (0, 4165), 'trade-confident': (1, 4210)}


def choice_frame(command, entered, returned, images, font, name):
    expected, frame = CHOICES[name]
    captions = [value.decode('ascii') for value in labels(bytes.fromhex(command['stored']))]
    assert command['stored'] == command['current']
    assert captions == ['Not yet.', "I've got the hang of it."]
    assert returned['result_words'] == [2, expected] and entered['frame'] + 25 < frame < returned['frame'] - 4
    photo = images[frame]
    screen = deck.captured(photo)
    locations = []
    for index, label in enumerate(captions):
        x0 = (256 - len(label) * 6) // 2
        matches = []
        for x in range(x0 - 3, x0 + 4):
            for y in range(271 + index * 20, 276 + index * 20):
                try:
                    ink, area = old.complete_mask(font, label, screen, x, y, (8, 8, 8))
                except ValueError:
                    continue
                assert ink and screen.getpixel((x, y - 2)) == ((0, 165, 172) if index == expected else (205, 198, 180))
                matches.append(area)
        rect, = matches
        locations.append(dict(caption=label, bounds=rect))
    assert locations[1]['bounds'][1] - locations[0]['bounds'][1] == 20
    return dict(selected=expected, result_words=returned['result_words'], glyph_bounds=locations,
        frame=frame, capture=photo, both_full_caption_masks_equal=True), screen


def run_case(name, block, group, proofs, painters, font, scope, evidence):
    _, fixture_rom, fixture_file = replay.fixture_paths(block)
    root = replay.ROOT / name
    inputs = (fixture_file, root / 'capture/capture_report.json', root / 'observer/commands.json', root / 'ordinary_inputs.json')
    fixture, report, trace, schedule = map(base.load, inputs)
    assert report['ROM_sha256'] == fixture['fixture_sha256'] == base.digest(fixture_rom)
    assert fixture['stage_sha256'] == proofs['candidate_sha256'] and fixture['lesson_block_sha256'] == group['after']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    assert report['frames'] == replay.CASES[name][1] and report['scripted_input_schedule'] == schedule
    assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert not trace['errors'] and not trace['mismatches']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not fixture['natural_activation']
    evidence.update({str(p): base.digest(p) for p in inputs})
    calls = old.tavern.observed_commands(trace, 44, fixture['block_44_sha256'])
    commands = {r['stored_offset'] + fixture['offset_delta']: r for r in group['commands']}
    images = deck.shots(report)
    layout = {r['id']: r for r in proofs['revisions']}
    match = FunctionType(old.hold_with_mask.__code__, scope)
    panels, choices, executed, views = [], [], [], []
    for entered, returned in calls:
        command = commands.get(entered['source']['instruction_offset'])
        if command is None:
            continue
        word = command['word']
        assert word == entered['source']['first_word']
        executed.append(dict(offset=command['stored_offset'], word=word, results=returned['result_words'],
                             entered=entered['frame'], returned=returned['frame']))
        if word == 0x2100:
            choice, screen = choice_frame(command, entered, returned, images, font, name)
            choice['ids'] = command['record_ids']
            photo = choice['capture']
            evidence[photo['path']] = photo['PNG_sha256']
            choices.append(choice)
            views.append((f'{name} / selected option {choice["selected"] + 1}', screen))
        if word != 0x4000:
            continue
        ident, = command['record_ids']
        raw = bytes.fromhex(command['stored'])
        selector, plane, mask = scope['expected_page'](painters, raw, ident)
        hold, screen = match(entered, returned, images, font, selector, mask)
        if ident in layout:
            renders = layout[ident]['layouts']
            right = next((r for r in renders if r['scope'] == 'Rafael default'), renders[0])
            assert plane.hex() == right['pages'][0]['native_plane_hex']
        panels.append(dict(id=ident, hold=hold, full_body_and_nameplate_match=True, revision=ident in layout))
        evidence[hold['capture']] = hold['sha256']
        if ident in ('DK4_MES_B129_R0024', 'DK4_MES_B129_R0062', 'DK4_MES_B140_R0005', 'DK4_MES_B140_R0012'):
            views.append((ident, screen))
    assert executed[-1]['word'] == 0 and len(choices) == (1 if block == 129 else 0)
    unfinished = [trace['rows'][r['entry_row']] for r in trace['unreturned_at_capture_end']]
    followup = []
    staged_rom = base.NdsImage.open(stage.ROM)
    other = native.IlnkContainer.parse(staged_rom.read_file(deck.SC0)).blocks[127]
    for entry in unfinished:
        assert entry['kind'] == 'before_command' and entry['frame'] > executed[-1]['returned']
        source = entry['source']
        assert source['whole_resident_payload_exact_ROM'] and (source['route'], source['block']) == (0, 127)
        assert source['registered_sha256'] == source['actual_sha256'] == native.digest(other)
        followup.append(dict(frame=entry['frame'], block=127, offset=source['instruction_offset']))
    return dict(name=name, block=block, panels=panels, choices=choices, original_end=True, commands=executed,
                subsequent_lesson_pending_at_end=followup), views


def main():
    assert not PROOF.exists()
    stored, layouts, release = map(base.load, (stage.PROOF, offline.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == stored['candidate_sha256'] == layouts['candidate_sha256']
    assert layouts['stage_proof_sha256'] == base.digest(stage.PROOF)
    groups = {r['block']: r for r in stored['groups']}
    rom = base.NdsImage.open(stage.ROM)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release['own_registered_startup'], captain=3)
    assert ctx.arm == rom.read_file(native.ARM)
    _, painter = offline.display.early.prior.precedent.planners(ctx.arm)
    converters = (ctx.arm, rom.read_file(deck.FONT), painter, None)
    font = deck.GameAsciiFont.from_arm9(ctx.arm)
    recipe = checked_text(old.getsource(old.expected_page), {
        "    if ident == 'DK4_MES_B42_R0080':\n        assert body.startswith(b'FI,') and body.count(b'FI') == 1\n        body = body.replace(b'FI', b'Rafael')\n    else:\n        assert b'FI' not in body":
            "    body = body.replace(b'FI', b'Rafael').replace(b'FO', b'Castor Co.')",
    })
    scope = vars(old) | dict(stage=SimpleNamespace(NAMES=stage.NAMES))
    exec(compile(recipe, __file__ + '::native-progressive', 'exec'), scope)
    evidence = {str(p): base.digest(p) for p in (stage.PROOF, offline.PROOF, stage.parent.RELEASE)}
    cases, frames = [], []
    for name, (block, _) in replay.CASES.items():
        case, views = run_case(name, block, groups[block], layouts, converters, font, scope, evidence)
        cases.append(case)
        frames.extend(views)
    panels = {r['id']: r for case in cases for r in case['panels']}
    choices = [r for case in cases for r in case['choices']]
    assert len(panels) == 18 and sum(p['revision'] for p in panels.values()) == 9
    assert [r['selected'] for r in choices] == [0, 1]
    assert {r['id'] for r in cases[0]['panels']} & {r['id'] for r in cases[1]['panels']} == {'DK4_MES_B129_R0005'}
    sheet = FunctionType(precedent.sheet.__code__, vars(precedent) | {'ROOT': replay.ROOT})(frames)
    assert all(base.digest(p) == sha for p, sha in evidence.items())
    base.save(PROOF, dict(candidate_sha256=stored['candidate_sha256'], predecessor_sha256=stored['predecessor_sha256'],
        initialized_gameplay=True, natural_activation=False, hardware=False, panels=list(panels.values()), choices=choices,
        cases=cases, sheets=[sheet], evidence=evidence))
    print('Verified 18 unique dialogue bodies, both highlighted choices, and all three original returns.')


if __name__ == '__main__':
    main()
