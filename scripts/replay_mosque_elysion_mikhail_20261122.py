"""Replay the two routes' revised story lines and their runtime names."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_trade_house_charles_and_earrings_20261122 as prior
from scripts import stage_mosque_elysion_mikhail_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
RAFAEL_ROOT = ROOT / "rafael"
ROM = RAFAEL_ROOT / "Rafael_Mosque_FOCUSED_ONLY.nds"
REPORT = RAFAEL_ROOT / "capture/capture_report.json"
RAFAEL_LIVE = RAFAEL_ROOT / "verified_gameplay.json"
SEQUENCE = tuple((123, i) for i in (48, 71, 115, 133, 139, 142, 157, 207))
INPUT = [(4000 + i * 340, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 260 for frame, _ in INPUT[:-1]), END - 1)
rafael_scope = prior.rafael_scope | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE, prior=prior.rafael_scope["prior"])
rafael_source = checked_text(prior.rafael_source, {
    'groups[86]["commands"][-1]': 'groups[123]["commands"][-1]',
    prior.ROM.name: ROM.name,
    '    assert not ROOT.exists()': '    assert not ROOT.exists() or set(ROOT.iterdir()) == {ROM}',
    '    ROOT.mkdir(parents=True)': '    ROOT.mkdir(parents=True, exist_ok=True)',
    '    rom.save(output)': '    if output.exists():\n        assert output.read_bytes() == bytes(rom.rom.save())\n    else:\n        rom.save(output)',
})
exec(compile(rafael_source, __file__ + "::Rafael", "exec"), rafael_scope)
rafael_verify = FunctionType(prior.rafael_verify.__code__,
    prior.rafael_verify.__globals__ | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE))

HODRAM_ROOT = ROOT / "route1"
HODRAM_ROM = HODRAM_ROOT / "Hodram_Elysion_Mikhail_FOCUSED_ONLY.nds"
HODRAM_REPORT = HODRAM_ROOT / "capture/capture_report.json"
HODRAM_LIVE = HODRAM_ROOT / "verified_gameplay.json"
SAMPLE = ((168, 31), (168, 96), (168, 153), (168, 219), (168, 225), (168, 300), (168, 317),
          (172, 106), (172, 122), (172, 137), (172, 339))
HODRAM_END = 4100 + len(SAMPLE) * 360
CASES = {1: prior.CASES[1] | dict(end=HODRAM_END, sample=SAMPLE)}
hodram_scope = prior.hodram_scope | globals() | dict(ROM=HODRAM_ROM, REPORT=HODRAM_REPORT,
    LIVE=HODRAM_LIVE, END=HODRAM_END)
exec(compile(prior.hodram.replay_source, __file__ + "::Hodram", "exec"), hodram_scope)
hodram_source = checked_text(prior.hodram_source, {
    'report, fixture, staged, native_pages, extra = map(base.load, (\n        REPORT, fixture_path, stage.PROOF, stage.NATIVE, stage.CHOICES_AND_PAGES))':
        'report, fixture, staged, native_pages = map(base.load, (REPORT, fixture_path, stage.PROOF, stage.NATIVE))',
    ' == extra["candidate_sha256"]': '',
    'earrings_gameplay_': 'elysion_and_mikhail_gameplay_',
    '        if row["layouts"]:':
        '''        if ident == "DK4_MES_B168_R0096":
            assert not row["layouts"]
            retained, = (r for r in base.load(stage.review.REVIEW)["records"] if r["route"] == 1 and r["id"] == ident)
            assert retained["decision"] == "retention" and row["exact_command_hex"] == retained["current_reference"]["exact_command_hex"]
            frame = 4360
            hold, image = shots[frame]
            assert cursor < frame
            speaker = speakers[ident]
            visual.glyphs(name_font, image, speaker, (16, 277), visual.LABEL_COLOR, 226)
            pages.append(dict(id=ident, changed=False, capture=hold, speaker=speaker,
                              body_verification="visual review of the retained mixed-glyph panel"))
            pictures.append((f"{ident} / {speaker} / original mixed glyphs", image))
            cursor = frame
            continue
        if row["layouts"]:''',
})
exec(compile(hodram_source, __file__ + "::Hodram-body-and-labels", "exec"), hodram_scope)
combine = FunctionType(prior.combine.__code__, prior.combine.__globals__ | globals())


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("rafael_replay", "rafael_verify", "hodram_replay", "hodram_verify", "combine"))
    action = cli.parse_args().action
    if action == "rafael_replay":
        rafael_scope["replay"]()
    elif action == "rafael_verify":
        rafael_verify()
    elif action == "hodram_replay":
        hodram_scope["replay"](1)
    elif action == "hodram_verify":
        hodram_scope["verify"]()
    else:
        combine()
