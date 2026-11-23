"""Verify the staged pagination and replay the original menu and dialogue paths."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import stage_observed_wrap_followups_20261123 as staged
from scripts import verify_hodram_late_midroute_wraps_20261123 as hodram
from scripts import verify_palace_london_glyphs_20261122 as glyphs
from scripts import verify_rafael_remaining_wraps_20261123 as rafael
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(staged) | {"established":staged.compiler}))
base, native, gameplay = stage.base, stage.native, hodram.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE, GLYPHS = ROOT / "verified_gameplay.json", stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES, ROLES = stage.ROOT / "original_choice_tables.json", stage.ROOT / "speaker_roles.json"
RAFAEL_PACKAGE = Path("releases/all_routes_editorial_20261123_rafael_remaining_wraps_candidate")
PROMPTS = {167:86, 216:32}
RESULTS = {167:((118, (122, 0), (122, 1), 125), (104, 108)),
           216:((51,), (72,), (78,))}
RUNS = {"b167_0":(167,0), "b216_2":(216,2)}
NOTES = {
    0: "Keep Rafael Castor as the captain asking about Avalon and listening to Noritsune's story.",
    1: "Keep Hodram Bergstrom as the captain who recruits Cesare.",
    5: "Keep Claudio Manaus in the heading and his familiar speech about where to ask.",
    8: "Keep Arcadius Eudoxios as the crewmate suggesting the tavern.",
    13: "Keep Cesare Tony as the former captain of the Elysion and the source of the ship advice.",
    16: "Keep Gerhard Adernkatz as the officer telling the Noritsune story.",
    18: "Keep Charles Rochefort in the heading and Jean in the separate native catalogue field.",
    82: "Keep Shopkeeper for the unnamed person who accuses Vivian of driving away customers.",
    149: "Keep Guildmaster for the unnamed enthusiast who asks about the novel.",
    169: "Keep Alluring Woman in the heading until Vivian gives her name in speech.",
}


def formatting():
    stored = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"]
    assert all(bytes.fromhex(c["stored"])[5] != 254 for g in stored["groups"] for c in g["commands"] if c["word"] == 0x4000)
    if not stage.FE_PROOF.exists():
        base.save(stage.FE_PROOF, dict(candidate_sha256=candidate, records=[], sheets=[],
            original_modal_consumer=True, complete_stored_page_count=0))
    if not GLYPHS.exists():
        FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    if not CHOICES.exists():
        source = checked_text(hodram.typed.choice_source, {
            'len(choices) == 8': 'len(choices) == 7',
            'Verified all eight original choice captions': 'Verified all seven original choice captions',
        })
        local = vars(hodram.typed) | globals()
        exec(compile(source, __file__ + "::native-choice-tables", "exec"), local)
        local["check_choices"]()
    names_without_player = ROLES.with_name("speaker_roles_static.json")
    local = hodram.nameplates.scope | dict(PROOF=names_without_player,
        NOTES={key:value for key,value in NOTES.items() if key != 0}, parent=stage.parent,
        stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
        display=SimpleNamespace(PROOF=stage.NATIVE), assets=staged.compiler.display.ASSETS)
    if not names_without_player.exists():
        source = checked_text(hodram.nameplates.source, {'if r["source_selector"] < 207': 'if 0 < r["source_selector"] < 207'})
        exec(compile(source, __file__ + "::native-nameplates", "exec"), local)
        local["main"]()
    proof = base.load(names_without_player)
    assert proof["candidate_sha256"] == candidate
    earlier_proof = RAFAEL_PACKAGE / "verification/speaker_roles.json"
    earlier_hash = base.digest(earlier_proof)
    assert earlier_hash == base.load(RAFAEL_PACKAGE / "checksums.json")["verification/speaker_roles.json"]
    previous = base.load(RAFAEL_PACKAGE / "release_manifest.json")
    witness = base.load(earlier_proof)
    assert previous["candidate_sha256"] == witness["candidate_sha256"] == base.digest(Path(previous["candidate"]))
    old, new = map(base.NdsImage.open, (Path(previous["candidate"]), stage.ROM))
    assert all(old.read_file(asset) == new.read_file(asset) for asset in local["assets"])
    former, = [row for row in witness["records"] if row["actor_ID"] == 0]
    assert all(former["review"].values()) and all(g["text"] == "Rafael Castor" for g in former["native_getters"])
    context = [r for r in base.load(stage.REVIEW)["records"] if r["source_selector"] == 0]
    assert context and {r["speaker"] for r in context} == {"Rafael Castor"}
    proof["records"].append(former | dict(context_records=[r["id"] for r in context], localization_note=NOTES[0],
        exact_reused_route_specific_getters=dict(path=earlier_proof.as_posix(), sha256=earlier_hash)))
    assert len(proof["records"]) == 10
    base.save(ROLES, proof)
    print("Verified nine static nameplates and preserved the exact Rafael-specific getter evidence.")


def report(run):
    if run == "0":
        return rafael_scope["report_path"](0)
    return ROOT / run / "capture/capture_report.json"


rafael_replay = ROOT / "rafael_replay.json"
rafael_scope = rafael.scope | globals() | dict(LIVE=rafael_replay, SAMPLE={0:((228,31), (234,35))})
rafael_scope["scope"] = rafael_scope
for name in ("receipt", "report_path", "run_file", "play"):
    rafael_scope[name] = FunctionType(rafael.scope[name].__code__, rafael_scope)
source = checked_text(rafael.fixture, {
    'Rafael_Remaining_Wraps_FOCUSED_ONLY.nds': 'Observed_Wraps_Rafael_FOCUSED_ONLY.nds',
})
exec(compile(source, __file__ + "::Rafael-excerpt", "exec"), rafael_scope)
source = checked_text(rafael.verify, {
    'rafael_remaining_wraps_excerpt_': 'observed_wraps_rafael_excerpt_',
    'including the speakerless voice in the book and curse exchange, default names and the host exit':
        'including Vivian’s Avalon clue, Noritsune’s crossing and the host exit',
})
exec(compile(source, __file__ + "::Rafael-excerpt-verification", "exec"), rafael_scope)

choice_paths = FunctionType(hodram.choice_paths.__code__, globals())
branch_frames = FunctionType(hodram.branch_frames.__code__, globals())
play_choice = FunctionType(hodram.play_choice.__code__, hodram.play_choice.__globals__ | globals())
focus = hodram.scope | globals()
focus["route_config"] = FunctionType(hodram.scope["route_config"].__code__, focus)
focus["SAMPLES"] = {1: ()}
prepare = checked_text(hodram.prior.previous.prepare_source, {
    'c["word"] == 0x2100': 'c["word"] == (0x2200 if block == 216 else 0x2100)',
})
exec(compile(prepare, __file__ + "::original-menu-suffixes", "exec"), focus)

checked = SimpleNamespace(CHOICES=CHOICES)
source = checked_text(hodram.source, {
    'if r["block"] == block]': 'if r["block"] == block and r["command_word"] == (0x2200 if block == 216 else 0x2100)]',
    'hodram_late_midroute_menus_': 'observed_wraps_hodram_menus_',
    '                plane = bytes.fromhex(result["pages"][page_index]["native_plane_hex"])':
        '                page = result["pages"][page_index]\n'
        '                assert page["native_plane_hex"] == bodies[1, row["id"]]["layouts"][0]["pages"][page_index]["native_plane_hex"]\n'
        '                plane = bytes.fromhex(page["native_plane_hex"])',
})
branches = vars(hodram) | globals()
exec(compile(source, __file__ + "::installed-pagination-and-menu-replay", "exec"), branches)


def verify():
    if not rafael_replay.exists():
        rafael_scope["verify"]()
    excerpts = base.load(rafael_replay)
    observations, choices, reports, sheets = branches["verify_branches"]()
    observations.extend(excerpts["observations"])
    reports.update(excerpts["report_sha256"])
    sheets.extend(excerpts["sheets"])
    candidate = base.digest(stage.ROM)
    assert candidate == excerpts["candidate_sha256"]
    assert len(observations) == 9 and len(choices) == 2
    assert {r["id"] for r in base.load(stage.REVIEW)["records"] if r["decision"] == "revision"} <= {r["id"] for r in observations}
    changed = [r for r in observations if r["id"] == "DK4_MES_B167_R0122"]
    assert [r["page_number"] for r in changed] == [1,2]
    base.save(LIVE, dict(candidate_sha256=candidate, observed_speech_pages=len(observations), observations=observations,
        original_menu_choices=choices, report_sha256=reports, sheets=sheets, initialized_excerpts=True,
        natural_story_triggers_claimed=False, hardware=False))
    print("Verified nine holds, both Cesare lesson pages and the revised Zhuge Liang response.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("formatting", "rafael", "prepare_choices", "verify", *RUNS))
    action = parser.parse_args().action
    if action == "rafael":
        rafael_scope["fixture"](0)
        rafael_scope["play"](0)
    elif action == "prepare_choices":
        for block in PROMPTS:
            focus["prepare_choice"](block)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
