"""Reflow the Tavern's nearby-town hint across the native town-name domain."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import unpack
from types import FunctionType

from scripts import observe_current_shared_encounters_20261123 as encounters
from scripts import probe_tavern_conversations_v764 as tavern
from scripts import register_regional_rumor_wrap_followups_20261123 as parent
from scripts import verify_current_shared_encounters_20261123 as observed
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town = parent.base, parent.native, parent.stage.town
ARM, COMMON, CLEAN = parent.ARM, parent.COMMON, native.CLEAN
ROOT = Path(".codex-release-work/tavern_nearby_town_wrap_20261123/staged")
ROM, PROOF = ROOT / "Tavern_Nearby_Town_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PLAY = ROOT / "ordinary_replays"
KEY = 823
DRAFT = "Have you heard of a nearby town called %s?"
NOTES = {
    51: ("Welcome the customer and open the choice of ordering a drink.", "Keep the welcoming question that leads to the drink menu."),
    53: ("The barkeep charges five gold coins.", "Keep the exact price and the barkeep's brisk answer before the tip."),
    820: ("A person from the named town is renowned locally in the named profession.",
          "Keep this formal report of fame distinct from the alternative about influence."),
    821: ("The person from that town has influence here in the named role.",
          "The Syracuse replay confirms that the person, town and role stay in order. Real pull fits the barkeep's voice."),
    822: ("Ask whether the listener has visited the nearby town.",
          "Keep the question about a visit as a distinct alternative to asking whether the listener knows of the town."),
    823: ("Ask whether the listener knows of the named town and explain that it is nearby.",
          "Keep the town, proximity and question in one spoken thought. The native wrap keeps the town name together with its question mark."),
    824: ("The speaker has no news of particular interest at the moment.",
          "Keep the time qualifier and the speaker's plain reply."),
    825: ("The speaker gives a short questioning sound.",
          "Keep the brief questioning interjection."),
    826: ("The speaker expresses teasing surprise that the listener cannot handle another drink.",
          "Keep this as a drinking joke. It says nothing about combat or the captain's skill."),
}


def town_names(cpu, get):
    root = get(0xCB178)
    result = []
    for index in range(90):
        obj = root + 4 + 108 * index
        table, = unpack("<I", bytes(cpu.mem_read(obj, 4)))
        address, = unpack("<I", bytes(cpu.mem_read(table + 8, 4)))
        name = bytes(cpu.mem_read(get(address - 0x02000000, obj), 34)).split(b"\0", 1)[0]
        assert name and name.isascii() and len(name) < 34
        result.append(name.decode("ascii"))
    assert len(set(result)) == 90 and "Alexandria" in result
    return result


def matrix(ctx, installed, reference):
    old, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    names = town_names(old, get)
    raster, _, _ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    chosen = {"Alexandria", min(names, key=len), max(names, key=len)}
    assert len(chosen) == 3
    rows, previews = [], []
    for name in names:
        data, lines = town.native_layout(old, installed, KEY, (name,))
        assert lines == ["Have you heard of a nearby town", f"called {name}?"]
        plane, codes = town.render_portrait(raster, ctx.arm, kanji, data)
        assert [c["code"] for c in codes] == town.glyph_codes(data)
        rows.append(dict(town=name, lines=lines, complete_native_body=True, native_plane_sha256=native.digest(bytes(plane))))
        if name in chosen:
            before, _ = town.native_layout(old, reference, KEY, (name,))
            before_plane, _ = town.render_portrait(raster, ctx.arm, kanji, before)
            previews.extend(((f"{name} before", before_plane), (f"{name} revised", plane)))
    return rows, previews


def stage():
    assert not ROOT.exists()
    release, sample = map(base.load, (parent.RELEASE, observed.OUT))
    previous = base.digest(parent.ROM)
    assert release["candidate_sha256"] == sample["candidate_sha256"] == previous
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    ctx = town.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean, rom = map(base.NdsImage.open, (CLEAN, parent.ROM))
    clean_arm = clean.read_file(ARM)
    source = town.common_message_entries(clean.read_file(COMMON), clean_arm)
    before = observed.prior.shared.paired.prior.entries(rom)
    former = before[KEY]
    sightings = [row for row in sample["cases"]["tunis"]["common_holds"] if row["message_ID"] == KEY]
    assert len(sightings) == 2 and all(row["installed_hex"] == former.text.hex() for row in sightings)
    payload = b" " + DRAFT.encode("ascii")
    assert len(payload) <= len(former.text) and payload.count(b"%s") == former.text.count(b"%s") == 1
    payload = payload.ljust(len(former.text), b" ")
    deployed, after, slots = town.owned_deployment(ctx.common, ctx.arm, before, {KEY: payload})
    assert slots[KEY]["new_null_fields"] == 0 and after[KEY].text == payload
    assert all(a == b for a, b in zip(before, after, strict=True) if a.message_id != KEY)
    rows = []
    for key, (meaning, note) in NOTES.items():
        a, b, jp = before[key], after[key], source[key]
        assert a.text.count(b"%s") == jp.text.count(b"%s") == b.text.count(b"%s")
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, message_ID=key, speaker="Barkeep",
            clean_Japanese=jp.text.decode("cp932"), source_hex=jp.text.hex(), source_reference=town.reference(jp),
            current_hex=a.text.hex(), current_reference=town.reference(a), previous_English=a.text.decode("ascii").strip(),
            english=b.text.decode("ascii").strip(), decision="revision" if key == KEY else "retention",
            source_meaning=meaning, localization_note=note, review=dict.fromkeys(town.GATES, True),
            installed_hex=b.text.hex(), registered_reference=town.reference(b),
            context="Tavern entry, drink purchase and alternate replies. Only one rumor or reply is selected at a time."))
    matrix_rows, previews = matrix(ctx, payload, former.text)
    image_files = native.files(rom)
    rom.replace_file(COMMON, deployed)
    target_files = native.files(rom)
    assert image_files.keys() == target_files.keys()
    assert {name for name in image_files if image_files[name] != target_files[name]} == {COMMON}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean), target_files)
    assert not any(guard["source_bound_new_command_counts"].values())
    result = bytes(rom.rom.save())
    rom.replace_file(COMMON, ctx.common)
    assert bytes(rom.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(result)
    candidate = base.digest(ROM)
    for row in rows:
        row["registered_reference"].update(candidate_sha256=candidate, file_path=COMMON,
            archive_sha256=native.digest(deployed), exact_stored_hex=row["installed_hex"])
    sheets = {row["path"]: row["sha256"] for row in town.portrait_sheets(ROOT, previews)}
    base.save(PROOF, dict(candidate_sha256=candidate, predecessor_sha256=previous, clean_sha256=release["clean_input_sha256"],
        target_ARM9_sha256=native.digest(ctx.arm), target_COMMON_sha256=native.digest(deployed), records=rows,
        allocations=slots, native_town_cases=matrix_rows, sheets=sheets, source25=guard,
        whole_parent_inverse=True, inherited_observations_sha256=base.digest(observed.OUT)))
    print(f"Staged {candidate}. All 90 native town-name variants preserve their complete question.")


def replay(case):
    receipt = base.load(PROOF)
    source = checked_text(getsource(encounters.voyage.playback.main), {
        "    rom = parent.ROM\n    release = base.load(parent.RELEASE)": "    rom = ROM\n    release = receipt",
    })
    scope = vars(encounters.voyage.playback) | globals() | dict(receipt=receipt, ROOT=PLAY,
        observer=encounters.voyage.scoped_observer, get_schedule=encounters.schedule, FOCUS=set(range(3668)))
    exec(compile(source, __file__ + "::ordinary-replay", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup", "tunis", "syracuse"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action in ("tunis", "syracuse"):
        replay(action)
    else:
        step = getattr(parent.staged.prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
