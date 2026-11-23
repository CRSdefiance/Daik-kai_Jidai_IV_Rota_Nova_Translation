"""Verify the revised flagship warning on the earlier working voyage."""

import argparse
import json
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import replay_swimmer_leak_square_dialogue_20261120 as replay
from scripts import stage_madeira_resupply_numerals_20261120 as price
from scripts import stage_swimmer_leak_square_dialogue_20261120 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands


ROOT = Path('work/swimmer_leak_compatible_playback_20261120_v1')
ROM = ROOT / 'revised_leak_qualified_fixture.nds'
PROOF = ROOT / 'fixture.json'
LEAK_RELEASE = stage.RELEASES / stage.PRIOR[1] / 'verification/registered_release_verification.json'
LEAK_HISTORY = LEAK_RELEASE.with_name('ship_emergency_gameplay_verification.json')
MERMAID_RELEASE = stage.RELEASES / stage.PRIOR[0] / 'verification/registered_release_verification.json'
MERMAID_HISTORY = MERMAID_RELEASE.with_name('registered_review.json')
SPAN_RANGES = ((0x30EA0, 0x30F90), (0x314B4, 0x3160C), (0x31EC0, 0x325CC),
               (0x53BD8, 0x54164), (0x118600, 0x118640), (0xD7720, 0xD77E0))
FONT = '/GRP/KANJI.FNT'


def digest(path):
    return stage.digest(Path(path).read_bytes())


def compatible_arm(old, updated):
    before, after = old.read_file(stage.ARM), updated.read_file(stage.ARM)
    assert all(before[a:b] == after[a:b] for a, b in SPAN_RANGES)
    assert old.read_file(FONT) == updated.read_file(FONT)
    return [{'start': a, 'end': b, 'sha256': stage.digest(before[a:b])} for a, b in SPAN_RANGES]


def entries(image):
    arm = image.read_file(stage.ARM)
    return stage.owned_entries(image.read_file(stage.COMMON), arm, stage.digest(arm[stage.DIRECTORY_OFFSET:stage.TABLE_OFFSET]))


def prepare():
    assert not ROOT.exists()
    historical = stage.load(LEAK_RELEASE)
    source_rom = Path(historical['candidate'])
    assert digest(source_rom) == historical['candidate_sha256']
    parent = stage.load(price.PROOF)
    assert digest(price.ROM) == parent['candidate_sha256']
    own, target = map(stage.NdsImage.open, (source_rom, price.ROM))
    same = compatible_arm(own, target)
    old, staged = entries(own), entries(target)
    provenance = stage.load(LEAK_HISTORY)
    assert provenance['candidate_sha256'] == historical['candidate_sha256']
    sample, = provenance['flagship_leak']['observed']
    assert sample['message_ID'] == 573 and sample['frame'] == 9627
    arm, common = own.read_file(stage.ARM), own.read_file(stage.COMMON)
    assert old[573].text != staged[573].text
    out, rows, allocation = stage.owned_deployment(common, arm, old, {573: staged[573].text})
    assert rows[573].text == staged[573].text
    own.replace_file(stage.COMMON, out)
    candidate = bytes(own.rom.save())
    own.replace_file(stage.COMMON, common)
    assert bytes(own.rom.save()) == source_rom.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    stage.write(PROOF, dict(fixture_sha256=stage.digest(candidate), historical_ROM_sha256=historical['candidate_sha256'],
          target_ROM_sha256=parent['candidate_sha256'], historical_ROM=str(source_rom), owned_message=573,
          exact_inverse=True, matched_original_arm_spans=same, target_display_record=staged[573].text.hex(),
          original_display_record=old[573].text.hex(), allocation=allocation,
          historical_replay_sha256=digest(LEAK_HISTORY), kanji_sha256=stage.digest(target.read_file(FONT))))
    print('Made a one-record fixture from the earlier working leak voyage.')


def play(output):
    spec = stage.load(PROOF)
    assert digest(ROM) == spec['fixture_sha256']
    previous_path, donor, pause, end, initial, commands, _, set_condition = replay.plan('leak', rom=ROM)
    assert stage.load(previous_path)['battery_save_preloaded']['source_sha256'] == digest(donor)
    inputs, journal = ROOT / 'inputs.json', ROOT / 'commands.jsonl'
    assert not inputs.exists() and not journal.exists()
    stage.write(inputs, initial)
    journal.write_text(''.join(json.dumps(command) + '\n' for command in commands), encoding='utf-8')
    cursor = GrowingCommands(journal)
    old = adapter.set_condition, sys.stdin, sys.argv
    try:
        adapter.set_condition, sys.stdin = set_condition, cursor
        sys.argv = [harness.__file__, '--rom', str(ROM), '--out', str(output), '--frames', str(end+1),
                    '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
                    '--pause-at', str(pause), '--allow-condition-fixtures',
                    '--capture-every', '999999', '--dump-pause-ram', '--dump-ram']
        harness.main()
    finally:
        adapter.set_condition, sys.stdin, sys.argv = old
        cursor.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        play(args.output)
    else:
        prepare()
