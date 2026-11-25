"""Verify late Hodram changes and carry forward original native choice and style tables."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_hodram_late_story_wraps_20261123 as staged
from scripts import verify_hodram_late_midroute_wraps_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(staged) | {"established": prior.compiler, "typed": prior.rendered.typed}))
base, native, gameplay = stage.base, stage.native, prior.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE, GLYPHS = ROOT / "verified_gameplay.json", stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES, STYLES = stage.ROOT / "original_choice_tables.json", stage.ROOT / "original_style_alternatives.json"
ROLES = stage.ROOT / "speaker_roles.json"
PROMPTS, RESULTS = {216: 32}, {216: ((51,), (72,), ((78, 0), (78, 1)))}
RUNS = {f"b216_{slot}": (216, slot) for slot in range(3)}
MODAL_SAMPLES = {"DK4_MES_B197_R0059", "DK4_MES_B200_R0045", "DK4_MES_B215_R0017"}
NOTES = {
    1: "Keep Hodram Bergstrom in the heading and the runtime name in the stat notices.",
    4: "Keep Janus Pasar in the letter heading and signature.",
    6: "Keep Julio Erneco for the crewmate appraising the merchant's price.",
    7: "Keep Cristina Erneco for the observer in the square and the speaker looking for the pirate's sword.",
    14: "Keep Emilio Ferog. His interest in the axe comes from his own words.",
    17: "Keep Al Shin in the heading. His separate catalogue field remains supported by earlier checks.",
    19: "Keep Carlo Sinat for the trader who negotiates prices and helps the stranger.",
    20: "Keep Fernando Dias for the crewmate advising Hodram to haggle.",
    21: "Keep Ian Dukov in the heading and Ian in the choice and stat notice.",
    23: "Keep Manuel Almeida. His belief and his advice are expressed in his reply.",
    25: "Keep Yifa Sol for the crewmate urging the buyer to press for a further discount.",
    76: "Keep Mikhail Letzel for the crewmate who spots the fungus.",
    105: "Keep Trader for the unnamed seller offering to replace the rope.",
    130: "Keep Daimyo for the Japanese lord collecting glass. The attendant addresses him as my lord.",
    149: "Keep Guildmaster for the unnamed book enthusiast in the established guild role.",
    150: "Keep Guildmaster for the unnamed attendant using the established local guild role field.",
    166: "Keep Lady for this anonymous town speaker. The scene supplies no given name.",
    167: "Keep Lady for the second anonymous town speaker, whose voice is distinguished in her replies.",
    168: "Keep Lady for the third anonymous town speaker, including the woman admiring the ruby.",
    169: "Keep Alluring Woman for the book seller. Ian wonders about her identity after she vanishes.",
    170: "Keep Mysterious Old Man for the unnamed storytellers and the expert who identifies caterpillar fungus.",
    172: "Keep Stranger for the unnamed man Carlo helps at the port.",
    173: "Keep Shady Man for the unnamed merchant. His bargaining and laughter establish the role.",
    174: "Keep Owner for the person directing the cook to put tomato dishes on the menu.",
    175: "Keep Cook for the employee asked to make tomato dishes.",
}


def samples():
    return {1: tuple((row["block"], int(row["id"].rsplit("R", 1)[1])) for row in base.load(stage.REVIEW)["records"]
        if (row["decision"] == "revision" and row["block"] != 216) or row["id"] in MODAL_SAMPLES)}


route_rom = FunctionType(prior.route_rom.__code__, globals())
choice_paths = FunctionType(prior.choice_paths.__code__, globals())


def report(run):
    directory = "b216_2_pagination" if run == "b216_2" else run
    return ROOT / directory / "capture/capture_report.json"


branch_frames = FunctionType(prior.branch_frames.__code__, globals())
play_choice = FunctionType(prior.play_choice.__code__, prior.play_choice.__globals__ | globals())
focus = prior.scope | globals()
for name in ("route_config", "replay", "verify_excerpts", "display_context", "panel_mask"):
    focus[name] = FunctionType(prior.scope[name].__code__, focus)
prepare = checked_text(prior.prior.previous.prepare_source, {
    'c["word"] == 0x2100': 'c["word"] == 0x2200',
})
exec(compile(prepare, __file__ + "::original-three-choice-suffix", "exec"), focus)

checked = SimpleNamespace(CHOICES=CHOICES)
source = checked_text(prior.source, {
    '(block, ordinal) == (167, 122)': '(block, ordinal) == (216, 78)',
    'if r["block"] == block]': 'if r["block"] == block and r["command_word"] == 0x2200]',
    'hodram_late_midroute_menus_': 'hodram_late_story_menus_',
})
branch_scope = prior.__dict__ | globals() | {"checked":checked}
exec(compile(source, __file__ + "::three-choice-gameplay", "exec"), branch_scope)


def styles():
    draft, stored, release = map(base.load, (stage.REVIEW, stage.PROOF, stage.parent.RELEASE))
    ancestor = base.NdsImage.open(stage.parent.ROM)
    image = base.NdsImage.open(stage.ROM)
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] and base.digest(stage.parent.ROM) == release["candidate_sha256"]
    assert all(ancestor.read_file(path) == image.read_file(path) for path in prior.compiler.display.ASSETS)
    group, = [g for g in stored["groups"] if g["block"] == 218]
    command, = [r for r in group["commands"] if r["word"] == 0x4100]
    archive = image.read_file(stage.ARCHIVE)
    block = native.IlnkContainer.parse(archive).blocks[218]
    assert native.digest(block) == group["after"] and command["stored"] == command["current"]
    at = command["stored_offset"]
    raw = bytes.fromhex(command["stored"])
    assert block[at:at+len(raw)] == raw
    owners = {tuple(r["slots"]):r for r in draft["retained_style_variants"]}
    records = []
    for relative, selector, body, slots in prior.typed.text_records(raw, 0x4100):
        row = owners.pop(tuple(slots))
        before = row["current_reference"]
        assert selector == 208 and raw.hex() == before["exact_command_hex"] and body.hex() == before["exact_body_hex"]
        assert " ".join(body.decode("ascii").split()) == row["english"]
        ref = before | dict(candidate_sha256=candidate, archive_sha256=native.digest(archive),
            block_sha256=group["after"], command_offset=at, offset=at+relative)
        records.append(row | dict(registered_reference=ref, review=row["review"] | {"formatting":True}))
    assert len(records) == 7 and not owners and sorted(i for row in records for i in row["slots"]) == list(range(8))
    base.save(STYLES, dict(candidate_sha256=candidate, records=records, sheets=[], stored_table_exact=True,
        reused_exact_text_and_runtime_dependencies=True, live_personality_selection=False))


def formatting():
    if not stage.FE_PROOF.exists():
        source = checked_text(getsource(prior.retained_panels), {
            'len(records) == 50': 'len(records) == 17',
            'Verified 50 retained speakerless': 'Verified 17 retained speakerless',
        })
        local = prior.__dict__ | globals()
        exec(compile(source, __file__ + "::native-modal-retentions", "exec"), local)
        local["retained_panels"]()
    if not GLYPHS.exists():
        glyphs = prior.typed.previous.verification.glyphs
        FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    if not CHOICES.exists():
        source = checked_text(prior.typed.choice_source, {
            'len(choices) == 8': 'len(choices) == 22',
            'Verified all eight original choice captions': 'Verified all 22 original choice captions',
        })
        local = vars(prior.typed) | globals()
        exec(compile(source, __file__ + "::native-choice-tables", "exec"), local)
        local["check_choices"]()
    if not STYLES.exists():
        styles()
    if not ROLES.exists():
        local = prior.nameplates.scope | dict(PROOF=ROLES, NOTES=NOTES, parent=stage.parent,
            stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
            display=SimpleNamespace(PROOF=stage.NATIVE), assets=prior.compiler.display.ASSETS)
        exec(compile(prior.nameplates.source, __file__ + "::native-nameplates", "exec"), local)
        local["main"]()


def verify():
    observations, pictures, reports, exits = focus["verify_excerpts"]()
    branches, choices, choice_reports, sheets = branch_scope["verify_branches"]()
    observations.extend(branches)
    reports.update(choice_reports)
    for offset in range(0, len(pictures), 6):
        path, digest = gameplay.make_sheet(ROOT / f"hodram_late_story_excerpts_{1+offset//6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=digest))
    changed = {row["id"] for row in base.load(stage.REVIEW)["records"] if row["decision"] == "revision"}
    assert changed <= {row["id"] for row in observations} and len(choices) == 3 and len(observations) == 31
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), observed_speech_pages=len(observations),
        observations=observations, original_menu_choices=choices, report_sha256=reports,
        return_frames=exits, sheets=sheets, initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print(f"Verified {len(observations)} focused holds and the three commander-choice outcomes.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting", "replay", "prepare_choice", "verify", *RUNS))
    action = cli.parse_args().action
    focus["SAMPLES"] = samples()
    if action == "replay":
        focus["replay"](1)
    elif action == "prepare_choice":
        focus["prepare_choice"](216)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
