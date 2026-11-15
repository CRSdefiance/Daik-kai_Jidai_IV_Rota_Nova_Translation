"""Replay Rafael's early tutorial dialogue and two pagination cases."""

import argparse
from inspect import getsource
from pathlib import Path
from struct import pack_into, unpack_from
import sys
from types import FunctionType, SimpleNamespace

from scripts import stage_rafael_early_wraps_20261111 as stage
from scripts import replay_story_question_wraps_20261111 as parent_replay
from scripts import verify_historical_story_wraps_storage_20261111 as storage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
prior = parent_replay.prior
ROOT = Path('out/rafael_early_wraps_20261111_v2')
ROM = ROOT / 'rafael_early_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_early_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
INPUTS = ROOT / 'inputs.json'
LIL = '/data/SC2.DK4'
END_FRAME = 8100
EXCERPTS = (
    (42, 504, 768, (0x4000,) * 5),
    (52, 74, 290, (0x4000, 0x4000, 0x0502, 0x4000)),
    (60, 4872, 5088, (0x4000,) * 3),
)
REVISED_IDS = ('DK4_MES_B42_R0026', 'DK4_MES_B42_R0036',
               'DK4_MES_B52_R0018', 'DK4_MES_B60_R0399')
FOLLOWING_IDS = ('DK4_MES_B52_R0021', 'DK4_MES_B60_R0402')
PLAY_ORDER = (*REVISED_IDS[:3], FOLLOWING_IDS[0], REVISED_IDS[3], FOLLOWING_IDS[1])


def read_excerpts(image, inventory, arm):
    source = stage.IlnkContainer.parse(image.read_file(stage.FILE)).blocks
    chosen, blocks = [], []
    for block, start, stop, words in EXCERPTS:
        raw = source[block]
        commands, _ = inventory(arm, raw)
        selected = [row for row in commands if start <= row['offset'] < stop]
        assert tuple(row['word'] for row in selected) == words
        assert selected[0]['offset'] == start
        assert selected[-1]['offset'] + selected[-1]['native_extent'] == stop
        if block == 60:
            assert {tuple(row['ancestor_0100_offsets']) for row in selected} == {(4392,)}
        else:
            assert not any(row['ancestor_0100_offsets'] for row in selected)
        chosen.extend(selected)
        blocks.append(raw[start:stop])
    last = source[EXCERPTS[-1][0]]
    end = 8 + unpack_from('<H', last, 4)[0]
    terminal = last[end - 4:end]
    assert terminal == bytes(4)
    return chosen, b''.join(blocks) + terminal


def prepare():
    draft, proof, release = map(base.load, (stage.REVIEW, stage.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.REVIEW) == proof['review_sha256']
    assert base.digest(stage.parent.ROM) == proof['candidate_sha256'] == release['candidate_sha256']
    original, target = [base.NdsImage.open(stage.parent.ROM) for _ in range(2)]
    before = prior.files(original)
    for path, raw in stage.prior.transform(original, draft['records']):
        archive = proof['archives'][path]
        assert raw == Path(archive['path']).read_bytes() and stage.sha(raw) == archive['sha256']
        target.replace_file(path, raw)
    after = prior.files(target)
    assert before.keys() == after.keys()
    assert {path for path in before if before[path] != after[path]} == {stage.FILE}
    if ROOT.exists():
        assert set(ROOT.iterdir()) == {ROM, INPUTS}
        assert bytes(target.rom.save()) == ROM.read_bytes()
    else:
        ROOT.mkdir()
        target.save(ROM)
    for path in proof['archives']:
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == stage.parent.ROM.read_bytes()
    inputs = base.load(prior.prior.INPUTS)
    inputs.extend(dict(start=frame, duration=5, buttons=['A']) for frame in range(2600, 6801, 260))
    if INPUTS.exists():
        assert base.load(INPUTS) == inputs
    else:
        base.save(INPUTS, inputs)

    inventory, _, _ = stage.prior.scoped_inventory()
    arm = before[stage.ARM]
    _, paint = stage.prior.precedent.planners(arm)
    unchanged = {}
    for group in draft['complete_exchange_references']:
        block = group['block']
        pairs = zip(group['source_progressive_exchange'], group['current_progressive_exchange'], strict=True)
        for source, row in pairs:
            ident = f"DK4_MES_B{block}_R{source['record_index']:04d}"
            if ident not in FOLLOWING_IDS:
                continue
            body = bytes.fromhex(row['raw_hex'])[1:]
            native, = paint(arm, before['/GRP/KANJI.FNT'], body)['pages']
            unchanged[ident] = native['native_plane_hex']
    assert set(unchanged) == set(FOLLOWING_IDS)

    variants = {}
    for side, source_path in (('before', stage.parent.ROM), ('after', ROM)):
        image = base.NdsImage.open(source_path)
        selected, excerpts = read_excerpts(image, inventory, arm)
        bank = stage.IlnkContainer.parse(before[LIL])
        logical = bytearray(bank.blocks[22][:56] + excerpts)
        pack_into('<H', logical, 4, len(logical) - 8)
        fixture = bytes(logical) + bytes(-len(logical) % 4)
        commands, _ = inventory(arm, fixture)
        assert len(commands) == 9 + len(selected) + 1 and commands[-1]['word'] == 0
        assert [row['whole_command_hex'] for row in selected] == [
            row['whole_command_hex'] for row in commands[9:-1]
        ]
        bank.blocks[22] = fixture
        fixture_image = base.NdsImage.open(stage.parent.ROM)
        fixture_image.replace_file(LIL, bank.to_bytes())
        path = ROOT / f'{side}_RESEARCH_ONLY.nds'
        fixture_image.save(path)
        variants[side] = dict(path=path.as_posix(), sha256=base.digest(path),
                              excerpt_commands=selected, fixture_SHA256=stage.sha(fixture))
    base.save(SETUP, dict(parent_sha256=release['candidate_sha256'], candidate_sha256=base.digest(ROM),
        proof_sha256=base.digest(stage.PROOF), fixture_ROMs=variants, whole_parent_inverse_exact=True,
        unchanged_transition_planes=unchanged, excerpts=EXCERPTS,
        fixture_scope='Original command excerpts placed at initialized Lil entry. B60 branch body is replayed without its outer condition.'))


def capture(side):
    fixture = base.load(SETUP)['fixture_ROMs'][side]
    assert base.digest(fixture['path']) == fixture['sha256'] and not (ROOT / side).exists()
    old = sys.argv
    try:
        sys.argv = [old[0], '--rom', fixture['path'], '--out', str(ROOT / side), '--frames', str(END_FRAME),
            '--inputs-json', str(INPUTS), '--capture-every', '999999', '--capture-at',
            *map(str, (2100, *range(2450, 7551, 20), 7800, 8000))]
        prior.harness.main()
    finally:
        sys.argv = old


def startup():
    setup = base.load(SETUP)
    assert setup['candidate_sha256'] == base.digest(ROM)
    proof = ROOT / 'startup_input.json'
    base.save(proof, dict(research_ROM_sha256=setup['candidate_sha256'],
                          registered_input=dict(candidate_sha256=setup['parent_sha256'])))
    boot = prior.prior.boot
    FunctionType(boot.startup_replay.main.__code__, vars(boot.startup_replay) | dict(
        EVIDENCE=proof, ROM=ROM, STARTUP=ROOT / 'own_startup',
        PRIOR=parent_replay.ROOT / 'own_startup'))()
    FunctionType(boot.startup_check.verify_startup.__code__, vars(boot.startup_check) | dict(
        ROOT=ROOT, ROM=ROM, PROOF=proof, BIOGRAPHIES=parent_replay.ROOT, BOOT=STARTUP))()


def verify():
    setup, draft = map(base.load, (SETUP, stage.REVIEW))
    records = {row['id']: row for row in draft['records']}
    observed, outside, evidence = {}, {}, {str(SETUP): base.digest(SETUP)}
    for side in ('before', 'after'):
        report_path = ROOT / side / 'capture_report.json'
        report = base.load(report_path)
        assert report['ROM_sha256'] == setup['fixture_ROMs'][side]['sha256'] and report['frames'] == END_FRAME
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded')
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
        assert report['scripted_input_schedule'] == base.load(INPUTS)
        photos = prior.photos(report)
        available = [(frame, photo, prior.body_masks(image)) for frame, (photo, image) in sorted(photos.items())]
        shown, last_frame = {}, 2100
        for ident in PLAY_ORDER:
            if ident in FOLLOWING_IDS:
                planes = [setup['unchanged_transition_planes'][ident]]
            else:
                planes = [page['native_plane_hex'] for page in records[ident][side + '_native']['pages']]
            holds = []
            for plane in planes:
                expected = prior.prior.masks(bytes.fromhex(plane))
                matches = [(frame, photo) for frame, photo, mask in available
                           if frame > last_frame and mask == expected]
                assert matches, (side, ident, last_frame)
                last_frame, photo = matches[0]
                holds.append(photo)
                evidence[photo['path']] = base.digest(photo['path'])
            shown[ident] = holds
        observed[side] = shown
        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in (2100, 7800, 8000)]
        evidence[str(report_path)] = base.digest(report_path)
    assert outside['before'] == outside['after']
    assert [len(observed[side]['DK4_MES_B52_R0018']) for side in ('before','after')] == [2, 1]
    assert [len(observed[side]['DK4_MES_B60_R0399']) for side in ('before','after')] == [2, 2]
    base.save(LIVE, dict(candidate_sha256=setup['candidate_sha256'], parent_sha256=setup['parent_sha256'],
        observed=observed, outside_exact_frames=[2100,7800,8000], source_commands_preserved=True,
        initialized_excerpts_at_Lil_entry=True, hardware=False, natural_event_eligibility_observed=False,
        verified_albuquerque_pages=[2,1], verified_pereira_pages=[2,2], evidence=evidence))
    print('Matched B42’s revised questions, the B52 two-to-one page change, B60’s two pages, and both following replies.')


def verify_storage():
    adapter = SimpleNamespace(**(vars(stage.prior) | vars(stage)))
    source = checked_text(getsource(storage.main), {
        'assert len(matches)==12': 'assert len(matches)==22',
        '12 unchanged native boundaries and before/after catalog misses on all four routes verified.':
            '22 unchanged native boundaries and before/after catalog misses on Rafael’s route verified.',
    })
    env = vars(storage) | dict(stage=adapter, replay=SimpleNamespace(SETUP=SETUP, ROM=ROM),
                               PROOF=PROOF, __file__=__file__)
    exec(compile(source, __file__ + '::existing-boundary-and-catalogue-proof', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare','before','after','startup','verify','verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
