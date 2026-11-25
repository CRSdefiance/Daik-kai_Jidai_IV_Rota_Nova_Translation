"""Check the first-voyage text in the native renderer and initialized Rafael route."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import stage_rafael_first_voyage_20261119 as build
from scripts import verify_rafael_deck_lesson_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
R_ROOT = build.ROOT / "initialized_replay"
ROM = R_ROOT / "Rafael_First_Voyage_Excerpt_RESEARCH_ONLY.nds"
SETUP, LIVE = R_ROOT / "rafael_fixture.json", R_ROOT / "verified.json"
RAFAEL = ((42, (5, 15, 19, 26, 33, 74, 80, 84, 99, 103)),)
STARTUP_DIR = build.ROOT / "startup_fixture"
STARTUP = build.ROOT / "own_startup_verification.json"


def render_layout(paint, arm, font, data, plan, tokens):
    assert tokens in ([], ["FI"]) and data.isascii()
    layouts = []
    for name in ("Rafael", "I", "ABCDEFGHIJKLMNO", "ABCDEFGHIJKLMNOP") if tokens else (None,):
        resolved = data if name is None else data.replace(b"FI", name.encode("ascii"))
        lines = [s if name is None else s.replace("{MACRO:FI}", name) for s in plan["lines"]]
        rendered = paint(arm, font, resolved)
        assert rendered["complete_consumed_bytes"] == len(resolved)
        page, = rendered["pages"]
        assert page["native_independent_plane_equal"] and page["first_visible_origin"] == [0, 0]
        assert workflow.display.inherited.visible_lines(page) == lines
        layouts.append(dict(name=name, page=page, lines=lines, renderer_supplied_name=name is not None))
    return layouts


source = getsource(workflow.offline)
before_render = source.index('            assert not build.review.TOKEN')
after_render = source.index("        records.append(entry)", before_render)
source = checked_text(source, {
    "archive.blocks[43]": "archive.blocks[42]",
    source[before_render:after_render]: '''            tokens = build.review.workflow.TOKEN.findall(row["english"])
            issues = plan["diagnostics"]
            assert all(i["severity"] == "warning" and i["code"] == "line-break-count" for i in issues)
            layouts = render_layout(paint, arm, font, data[1:], plan, tokens)
            old_body = current[6:current.index(0, 6)].replace(b"FI", b"Rafael") if tokens else current[6:current.index(0, 6)]
            old = paint(arm, font, old_body)
            entry.update(page=layouts[0]["page"], layouts=layouts, lines=plan["lines"],
                         source_row_count_notes=issues, pagination=[len(old["pages"]), 1],
                         stored_command_allocation=len(raw))
            for layout in layouts:
                label = ident if layout["name"] in (None, "Rafael") else f"{ident} ({len(layout['name'])} cells)"
                pictures.append((label, bytes.fromhex(layout["page"]["native_plane_hex"])))
''',
    "len(records) == len(commands) == 12 and len(pictures) == 7":
        "len(records) == len(commands) == 28 and len(pictures) == 24",
    "Seven revised pages match the native font and bounds; five exact retentions carry forward.":
        "Checked 21 revised pages, three additional name-width samples, and seven exact retentions.",
})
replay = checked_text(getsource(workflow.run_rehearsal), {
    '"Rafael", "Castor", 9': '"Rafael", "Castor", 10',
    '[1] * 9': '[1] * 10',
    'assert b"Rafael" in bytes.fromhex(result["holds"][2]["body_hex"])':
        'assert result["holds"][6]["id"] == "DK4_MES_B42_R0080"\n'
        '        assert b"FI" not in bytes.fromhex(result["holds"][6]["body_hex"])\n'
        '        assert bytes.fromhex(result["holds"][6]["body_hex"]).startswith(b"Rafael,")',
})
env = vars(workflow) | globals()
for code in (source, replay):
    exec(compile(code, __file__ + "::first-voyage-verification", "exec"), env)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("offline", "prepare", "capture", "verify", "startup"))
    action = parser.parse_args().action
    if action == "offline":
        env["offline"]()
    elif action == "startup":
        FunctionType(workflow.startup.__code__, env)()
    else:
        env["run_rehearsal"](action)
