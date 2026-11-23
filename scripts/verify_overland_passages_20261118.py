"""Check the new progressive, FE and both typed menu layouts."""

from inspect import getsource
from types import FunctionType

from scripts import stage_overland_passages_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
MENU_ROOT = build.ROOT.with_name("research_v1") / "native_menus_v1"
PRIOR = build.ROOT.with_name("research_v1") / ROOT.name / PROOF.name
inherited = previous.inherited
menu = FunctionType(inherited.menu_checker.__code__, vars(inherited) | {"parent": parent})


def check_menu(ctx, release, cmd, rows, route, block):
    MENU_ROOT.mkdir(exist_ok=True)
    folder = MENU_ROOT / f"SC{route}_B{block}_{cmd['source_offset']}"
    path = folder / "menu_provider_and_planes.json"
    if not path.exists():
        menu(ctx, release, cmd, rows, folder)
    data = base.load(path)
    if cmd["word"] == 0x2200:
        raw = data["menus"][0]["target_object_hex"]
        sheets = data["review_sheets"]
    else:
        raw = data["native_choice_object_hex"]
        sheets = [data["review_sheet"]]
    assert raw == cmd["stored"]
    assert data["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    assert all(base.digest(item["path"]) == item["sha256"] for item in sheets)
    return dict(menu_path=str(path), proof_sha256=base.digest(path),
        option_ids=cmd["record_ids"], candidate_menu_offset=cmd["stored_offset"],
        current_archive=rows[0]["file_path"], block=block,
        source_command_offset=cmd["source_offset"], review_sheets=sheets)


source = getsource(previous.main)
old_setup = source[source.index("    previous = base.load(PRIOR)"):source.index("    image =")]
old_reuse = source[source.index("                qualified ="):source.index("                try:")]
source = checked_text(source, {
    old_setup: """    previous = base.load(PRIOR)
    prior_stage_path = PRIOR.parent.parent / build.PROOF.name
    prior_stage = base.load(prior_stage_path)
    assert previous["stage_proof_sha256"] == base.digest(prior_stage_path)
    assert prior_stage["predecessor_sha256"] == proof["predecessor_sha256"]
    prior_image = base.NdsImage.open(prior_stage_path.parent / build.ROM.name)
    assert previous["candidate_sha256"] == base.digest(prior_stage_path.parent / build.ROM.name)
    reusable = {(r["file_path"], r["id"]): r for r in previous["checked_records"]}
""",
    old_reuse: """                qualified = reusable.get((path, ident))
                if qualified and qualified.get("stored_hex", qualified.get("target_hex")) == value.hex():
                    rendered.append(qualified)
                    reused.append([path, ident])
                    continue
""",
    '    _, paint = inherited.early.prior.precedent.planners(ctx.arm)':
        """    assert all(image.read_file(resource) == prior_image.read_file(resource)
               for resource in (native.ARM, "/GRP/KANJI.FNT", "/COMMON/MESFILE.DK4"))
    _, paint = inherited.early.prior.precedent.planners(ctx.arm)""",
    "rendered, styles, pictures, reused = [], [], [], []":
        "rendered, styles, pictures, menus, reused = [], [], [], [], []",
    "            if word == stage.STYLE:":
        """            if word in stage.MENU:
                captions = [rows[path, ident] for ident in cmd["record_ids"]]
                menus.append(check_menu(ctx, release, cmd, captions, group["route"], n))
                continue
            if word == stage.STYLE:""",
    "assert len(rendered) == 40 and len(styles) == 1":
        "assert len(rendered) == 159 and len(menus) == 3",
    'k for k, row in rows.items() if row["decision"] == "revision"':
        'k for k, row in rows.items() if row["decision"] == "revision" and row["native_command_word"] not in stage.MENU',
    '        reused_records=reused, prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)),\n'
    '        previous_sheets=previous["previous_sheets"] + previous["contact_sheets"],\n':
        '        menu_proofs=menus, reused_records=reused,\n'
        '        prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)), previous_sheets=previous["contact_sheets"],\n',
})
scope = vars(previous) | globals()
exec(compile(source, __file__ + "::source-bound-native-checks", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()


