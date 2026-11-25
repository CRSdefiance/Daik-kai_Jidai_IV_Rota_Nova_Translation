"""Check Hodram's installed wraps, substitutions, and original figurehead choice."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_hodram_b221_b260_wrap_fixes_20261123 as staged
from scripts import verify_hodram_late_midroute_wraps_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(staged) | {"established":prior.compiler, "typed":prior.rendered.typed}))
base, native, gameplay = stage.base, stage.native, prior.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE, GLYPHS = ROOT / "verified_gameplay.json", stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES, STYLES = stage.ROOT / "original_choice_tables.json", stage.ROOT / "original_style_alternatives.json"
ROLES = stage.ROOT / "speaker_roles.json"
PROMPTS, RESULTS = {243:64}, {243: ((), (174, 178, 182))}
RUNS = {"b243_1": (243, 1)}
MODAL_SAMPLES = {"DK4_MES_B242_R0036", "DK4_MES_B252_R0130"}
NOTES = {
    1:"Keep Hodram Bergstrom as the captain hearing the rumors and directing the search.",
    6:"Keep Julio Erneco for the reluctant sailor who helps with the figurehead.",
    11:"Keep Jam Ludwyan in the heading and Jam Jack Ludwyan in his letter signature.",
    13:"Keep Cesare Tony for the sailor who hears the figurehead's voice and brings in rumors from the crew.",
    16:"Keep Gerhard Adernkatz for the officer telling Noritsune's story and speaking about Charles Martel.",
    17:"Keep Al Shin in the heading and his separately approved catalogue field. He gives his view of Saladin in speech.",
    18:"Keep Charles Rochefort in the heading and Charles Jean Rochefort in the letter signature.",
    19:"Keep Carlo Sinat in the heading when he exchanges familiar remarks with Filippo.",
    20:"Keep Fernando Dias for the sailor who identifies the ruins inscription and tentative figurehead.",
    21:"Keep Ian Dukov in the heading and in his historical letter.",
    22:"Keep Samwell Khan in the heading and the separate approved catalogue entry. His repeated pitch is his own dialogue.",
    23:"Keep Manuel Almeida for the crewmate relaying the rumor about Attila's armor.",
    26:"Keep Julian Lopes for the sailor making the Medusa comparison.",
    64:"Keep Yuris Huygens. His own introduction and Hodram's next remarks establish who he is.",
    85:"Keep Shopkeeper for the unnamed person discussing the Crusades in the square.",
    104:"Keep Trader in the heading. Carlo identifies the trader as Filippo in dialogue.",
    139:"Keep Priest for the person tending the church and explaining the figurehead's terms.",
    151:"Keep Sailor for the participant in the Martel play scene.",
    162:"Keep Boy for the child playing Charles Martel.",
    186:"Keep Francisca for the owner of the returned Frozen Rose.",
    189:"Keep Wanda for the hostess who regrets that the town has no famous ruins.",
    190:"Keep Julia for the hostess who considers the question and gives her own answer.",
    195:"Keep Nelly for the hostess offering directions to the pyramids.",
    196:"Keep Hatra for the hostess mentioning the weather and the local ruins.",
    197:"Keep Safia for the woman who teases Julian about his comparison to Medusa.",
}


def report(run):
    return ROOT / run / "capture/capture_report.json"


def samples():
    return {1:tuple((row["block"], int(row["id"].rsplit("R",1)[1])) for row in base.load(stage.REVIEW)["records"]
        if (row["decision"]=="revision" and row["block"] != 243) or row["id"] in MODAL_SAMPLES)}


route_rom = FunctionType(prior.route_rom.__code__, globals())
choice_paths = FunctionType(prior.choice_paths.__code__, globals())
branch_frames = FunctionType(prior.branch_frames.__code__, globals())
play_choice = FunctionType(prior.play_choice.__code__, prior.play_choice.__globals__ | globals())
scope = prior.scope | globals()
for name in ("route_config", "replay", "verify_excerpts", "display_context", "panel_mask"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)
exec(compile(prior.prior.previous.prepare_source, __file__ + "::original-church-choice", "exec"), scope)
checked = SimpleNamespace(CHOICES=CHOICES)
branches = prior.__dict__ | globals()
source = checked_text(prior.prior.source, {"hodram_midroute_menus_": "hodram_b221_b260_choice_"})
exec(compile(source, __file__ + "::church-choice-verification", "exec"), branches)


def styles():
    draft, stored = map(base.load, (stage.REVIEW, stage.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] and stored["whole_parent_inverse"]
    old, image = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    assert all(old.read_file(path) == image.read_file(path) for path in prior.compiler.display.ASSETS)
    archive = image.read_file(stage.ARCHIVE)
    bank = native.IlnkContainer.parse(archive).blocks
    owners = {(r["block"],r["current_reference"]["command_offset"],tuple(r["slots"])):r for r in draft["retained_style_variants"]}
    records = []
    for group in stored["groups"]:
        block = group["block"]
        assert native.digest(bank[block]) == group["after"]
        for command in (c for c in group["commands"] if c["word"] == 0x4100):
            raw = bytes.fromhex(command["stored"])
            at = command["stored_offset"]
            assert command["stored"] == command["current"] and bank[block][at:at+len(raw)] == raw
            assigned = []
            for relative, selector, body, slots in prior.typed.text_records(raw, 0x4100):
                row = owners.pop((block,command["current_offset"],tuple(slots)))
                ref = row["current_reference"]
                assert selector == 208 and ref["exact_command_hex"] == raw.hex() and ref["exact_body_hex"] == body.hex()
                assert " ".join(body.decode("ascii").split()) == row["english"]
                assigned.extend(slots)
                installed = ref | dict(candidate_sha256=candidate, archive_sha256=native.digest(archive),
                    block_sha256=group["after"], command_offset=at, offset=at+relative)
                records.append(row | dict(registered_reference=installed, review=row["review"] | {"formatting":True}))
            assert sorted(assigned) == list(range(8))
    assert len(records) == 37 and not owners and sum(len(r["slots"]) for r in records) == 40
    base.save(STYLES, dict(candidate_sha256=candidate, records=records, sheets=[], stored_table_exact=True,
        reused_exact_text_and_runtime_dependencies=True, live_personality_selection=False))
    print("Verified 37 retained personality variants and all 40 slot assignments.")


def formatting():
    if not stage.FE_PROOF.exists():
        source = checked_text(getsource(prior.retained_panels), {
            'len(records) == 50': 'len(records) == 16',
            'Verified 50 retained speakerless': 'Verified 16 retained speakerless',
        })
        local = prior.__dict__ | globals()
        exec(compile(source, __file__ + "::native-modal-retentions", "exec"), local)
        local["retained_panels"]()
    if not GLYPHS.exists():
        glyphs = prior.typed.previous.verification.glyphs
        FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    if not CHOICES.exists():
        source = checked_text(prior.typed.choice_source, {
            'len(choices) == 8': 'len(choices) == 11',
            'Verified all eight original choice captions': 'Verified all eleven original choice captions',
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
    observations, pictures, reports, exits = scope["verify_excerpts"]()
    extra, choices, choice_reports, sheets = branches["verify_branches"]()
    observations.extend(extra)
    reports.update(choice_reports)
    for offset in range(0,len(pictures),6):
        path,digest = gameplay.make_sheet(ROOT / f"hodram_b221_b260_excerpts_{1+offset//6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=digest))
    changed={r["id"] for r in base.load(stage.REVIEW)["records"] if r["decision"] == "revision"}
    assert changed <= {r["id"] for r in observations} and len(choices) == 1 and len(observations)==34
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), observed_speech_pages=len(observations),
        observations=observations, original_menu_choices=choices, report_sha256=reports,
        return_frames=exits, sheets=sheets, initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print("Verified 34 focused holds, Hatra's given name and the original Leave it outcome.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting","replay","prepare_choice","verify",*RUNS))
    action = cli.parse_args().action
    scope["SAMPLES"] = samples()
    if action == "replay":
        scope["replay"](1)
    elif action == "prepare_choice":
        scope["prepare_choice"](243)
    elif action in RUNS:
        play_choice(action)
    else:
        globals()[action]()
