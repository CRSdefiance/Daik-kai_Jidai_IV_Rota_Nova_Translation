"""Verify the source-bound Sofala pages, substitutions and retained reward panel."""

from inspect import getsource
from types import FunctionType

from scripts import audit_ceuta_lesson_20261119 as startup_audit
from scripts import replay_rafael_iberian_aftermath_20261119 as play
from scripts import stage_rafael_iberian_aftermath_20261119 as build
from scripts import verify_rafael_first_voyage_debrief_20261119 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
STARTUP = build.ROOT / "own_startup_verification.json"
REWARD = "DK4_MES_B55_R0054"
PRIOR_ROOT = build.ROOT.with_name("research_v1")


def native_display():
    source = checked_text(getsource(previous.main), {
        '{"/data/SC0.DK4": [44, 47]}': '{"/data/SC0.DK4": [53, 54, 55, 56, 57, 58]}',
        '    expand = names.expander()': '    expand = names.expander()\n'
            '    fe = build.stage.system.native_painter(ctx)\n'
            '    reward = None\n'
            '    before_proof = PRIOR_ROOT / "native_display/native_display.json"\n'
            '    before_stage = PRIOR_ROOT / build.PROOF.name\n'
            '    before_rom = PRIOR_ROOT / build.ROM.name\n'
            '    earlier = base.load(before_proof)\n'
            '    assert earlier["stage_proof_sha256"] == base.digest(before_stage)\n'
            '    assert earlier["candidate_sha256"] == base.digest(before_rom)\n'
            '    assert base.load(before_stage)["predecessor_sha256"] == stored["predecessor_sha256"]\n'
            '    prior_image = base.NdsImage.open(before_rom)\n'
            '    assert all(prior_image.read_file(path) == image.read_file(path) for path in assets)\n'
            '    assert earlier["maximum_name_widths"] == MAXIMUM\n'
            '    prior_revisions = {r["id"]: r for r in earlier["revisions"]}\n'
            '    prior_names = {r["id"]: r for r in earlier["native_macro_checks"]}\n'
            '    reused = set()',
        '            if all(r["decision"] == "retention" for r in chosen):':
            '            if chosen[0]["id"] == REWARD:\n'
            '                row, = chosen\n'
            '                value = raw[5:raw.index(0, 6)]\n'
            '                assert value[0] == 254 and row["current_hex"] == value.hex()\n'
            '                assert build.review.workflow.logical(value[1:].decode("ascii")) == "Received 3,000 gold coins..."\n'
            '                reward_plan = dict(encoded_hex=value.hex(), lines=["Received 3,000 gold coins..."])\n'
            '                reward = display.validate_paragraph(ctx, font, paint, expand, fe, row, value, reward_plan)\n'
            '                previews.append((REWARD + " retained reward", bytes.fromhex(reward["pages"][0]["native_plane_hex"])))\n'
            '            if all(r["decision"] == "retention" for r in chosen):',
        '            result = names.paragraph(ctx, font, paint, expand, None, model_names, row, value, plan)':
            '            before = prior_revisions[ident]\n'
            '            if (before["target_hex"], before["planned_lines"]) == (value.hex(), plan["lines"]):\n'
            '                reused.add(ident)\n'
            '                if ident in prior_names:\n'
            '                    name_cases.append(prior_names[ident])\n'
            '                    maximum, = (p for p in before["layouts"] if p["scope"] == "maximum supplied widths")\n'
            '                    previews.append((f"{ident} maximum name widths",\n'
            '                                     bytes.fromhex(maximum["pages"][0]["native_plane_hex"])))\n'
            '                checked.append(before)\n'
            '                previews.append((ident, bytes.fromhex(before["pages"][0]["native_plane_hex"])))\n'
            '                continue\n'
            '            result = names.paragraph(ctx, font, paint, expand, fe, model_names, row, value, plan)',
        '    assert len(checked) == 39 and len(retained) == 93':
            '    assert len(checked) == 25 and len(retained) == 92 and reward is not None\n'
            '    assert [r["id"] for r in checked if r["kind"] == "system-FE"] == ["DK4_MES_B55_R0036"]',
        '{f"DK4_MES_B44_R{i:04}" for i in (17, 152, 308, 316, 327)}':
            '{"DK4_MES_B55_R0168", "DK4_MES_B56_R0005", "DK4_MES_B58_R0045"}',
        'maximum_name_widths=MAXIMUM, contact_sheets=sheets, actual_gameplay=False))':
            'maximum_name_widths=MAXIMUM, contact_sheets=sheets, retained_reward_display=reward, actual_gameplay=False,\n'
            '        prior_proof_sha256=base.digest(before_proof), reused_identical_pages=sorted(reused)))',
        "Checked 39 revised pages, five macro records and 93 exact retentions.":
            "Checked 25 revised pages, three macro records, 92 exact retentions and the separate reward display.",
    })
    scope = vars(previous) | globals()
    exec(compile(source, __file__ + "::sofala-native-display", "exec"), scope)
    scope["main"]()


def startup():
    scope = vars(startup_audit) | dict(build=build, play=play, STARTUP=STARTUP)
    FunctionType(startup_audit.startup.__code__, scope)()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("native_display", "startup"))
    globals()[parser.parse_args().action]()
