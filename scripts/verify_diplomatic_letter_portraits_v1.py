"""Verify the letter demand, original rejection, and return to the inn."""

import argparse
import inspect
from pathlib import Path

from scripts import replay_diplomatic_letter_portraits_v2 as replay
from scripts import verify_rumor_and_cooperation_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT, ROM, PROOF = replay.ROOT, replay.ROM, replay.EVIDENCE
PREDECESSOR = prior.stage.ROOT
LIVE = ROOT / 'diplomatic_letter_portraits_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/diplomatic_letter_portraits_repo_qa_20261111.xml')


def verify_live():
    proof = prior.load(PROOF)
    assert prior.digest(ROM) == proof['research_ROM_sha256']
    image = prior.NdsImage.open(ROM)
    arm = image.read_file('/__arm9__.bin')
    raster, _, _ = prior.font_tools(image)
    font = prior.GameAsciiFont.from_arm9(arm)
    kanji = image.read_file('/GRP/KANJI.FNT')

    data = checked_text(inspect.getsource(prior.run_data), {"'cooperation_decline'": "'submission_decline'"})
    match = checked_text(inspect.getsource(prior.portrait_match), {
        "'Trader', captured(frames[frame])": "'Martin Speyer', captured(frames[frame])",
        "text='Trader'": "text='Martin Speyer'",
    })
    env = vars(prior) | {'FINAL': 9700}
    exec(compile(data + '\n\n' + match, __file__ + '::exact-submission-portrait-comparison', 'exec'), env)
    frames, raw, snaps, fixture, evidence = env['run_data'](ROOT, proof, arm, replay.set_condition, replay.ACTION)
    assert fixture['expected_native_demand_ID'] == 2757 and fixture['recipient_actor_ID'] == 29
    observed = [env['portrait_match'](frame, n, frames, raw, snaps, arm, kanji, raster, font, proof)
                for frame, n in ((8500, 2757), (8900, 2766))]
    assert observed[0]['original_arguments'] == ('Bergstrom Fleet',) and not observed[1]['original_arguments']
    transitions = (
        (8100, 'Speyer Co. received the letter.', (14, 292, 244, 318)),
        (9300, 'Speyer Co. rejected the merger', (14, 292, 244, 318)),
        (9300, 'offer.', (14, 308, 244, 340)),
        (9700, 'Stay 1 Day', (80, 258, 172, 290)),
    )
    screens = [dict(capture=frames[frame], text=prior.dark_text(font, text, prior.captured(frames[frame]), box))
               for frame, text, box in transitions]
    after = raw(9700)
    cpu, get = prior.get_machine(arm, after)
    assert get(0xB65E4) == 22
    companies = get(0xCB160)
    assert get(0x3CBF4, companies + 4 + 76 * fixture['recipient_faction']) != fixture['sender_faction']
    slot = get(0xCB130) + 4 + 16 * fixture['slot']
    assert get(0x91464, slot) == 0
    assert bytes(cpu.mem_read(replay.previous.BASE, len(after))) == after
    prior.save(LIVE, dict(candidate_sha256=prior.digest(ROM), observed_ids=[2757, 2766],
        portraits=observed, native_receipt_rejection_and_inn_return=screens,
        original_letter_consumed_and_recipient_independent=True, fixture=fixture,
        actual_natural_letter_generation=False, hardware=False,
        evidence={str(path): prior.digest(path) for path in (PROOF, *evidence, Path(__file__))}))
    print('Verified the original submission demand, voiced rejection, result, and return to the inn.')


def verify_startup():
    source = checked_text(inspect.getsource(prior.verify_startup), {'SHARK': 'PREDECESSOR'})
    env = vars(prior) | globals()
    exec(compile(source, __file__ + '::same-boot-and-protected-getter-checks', 'exec'), env)
    env['verify_startup']()


def approve(viewed):
    from types import FunctionType
    FunctionType(prior.approve.__code__, vars(prior) | globals())(viewed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    elif args.action == 'live':
        verify_live()
    else:
        verify_startup()

