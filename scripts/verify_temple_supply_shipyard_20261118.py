"""Verify native pages and both revised two-way decision menus."""

from inspect import getsource
from types import FunctionType

from scripts import stage_temple_supply_shipyard_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR_ROOT = build.ROOT.with_name("remaining_three_routes_research_v1")
PRIOR = PRIOR_ROOT / ROOT.name / PROOF.name
MENU_ROOT = PRIOR_ROOT / "native_menus_v1"
inherited = previous.inherited
menu = FunctionType(inherited.menu_checker.__code__, vars(inherited) | {"parent": parent})


def check_menu(ctx, release, cmd, rows, route, block):
    MENU_ROOT.mkdir(exist_ok=True)
    folder = MENU_ROOT / f"SC{route}_B{block}_{cmd['source_offset']}"
    path = folder / "menu_provider_and_planes.json"
    if not path.exists():
        menu(ctx, release, cmd, rows, folder)
    data = base.load(path)
    sheet = data["review_sheet"]
    assert data["native_choice_object_hex"] == cmd["stored"]
    assert data["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    assert base.digest(sheet["path"]) == sheet["sha256"]
    return dict(menu_path=str(path), proof_sha256=base.digest(path), option_ids=cmd["record_ids"],
                candidate_menu_offset=cmd["stored_offset"], current_archive=rows[0]["file_path"],
                block=block, source_command_offset=cmd["source_offset"], review_sheet=sheet)


source = getsource(previous.main)
old_setup = source[source.index("    previous = base.load(PRIOR)"):source.index("    image =")]
old_reuse = source[source.index("                qualified ="):source.index("                try:")]
source = checked_text(source, {
    old_setup: """    previous = base.load(PRIOR)
    prior_stage_path = PRIOR_ROOT / build.PROOF.name
    prior_stage = base.load(prior_stage_path)
    assert previous["stage_proof_sha256"] == base.digest(prior_stage_path)
    assert prior_stage["predecessor_sha256"] == proof["predecessor_sha256"]
    assert previous["candidate_sha256"] == base.digest(PRIOR_ROOT / build.ROM.name)
    prior_image = base.NdsImage.open(PRIOR_ROOT / build.ROM.name)
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
        "assert len(rendered) == 115 and len(styles) == 12 and len(menus) == 2",
    'k for k, row in rows.items() if row["decision"] == "revision"':
        'k for k, row in rows.items() if row["decision"] == "revision" and row["native_command_word"] not in stage.MENU',
    '        reused_records=reused, prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)),\n'
    '        previous_sheets=previous["previous_sheets"] + previous["contact_sheets"],\n':
        '        menu_proofs=menus, reused_records=reused, previous_sheets=previous["contact_sheets"],\n'
        '        prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)),\n',
})
scope = vars(previous) | globals()
exec(compile(source, __file__ + "::source-bound-native-checks", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

