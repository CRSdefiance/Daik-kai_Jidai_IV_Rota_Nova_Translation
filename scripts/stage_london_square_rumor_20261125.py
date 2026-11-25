"""Stage the London Square rumor in its original slot and replay the same inputs."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import check_fleet_diversion_release_20261125 as checks
from scripts import replay_lisbon_guild_bargaining_20261125 as replay
from scripts import stage_square_country_briefings_20261115 as town
from scripts import verify_london_tavern_and_square_20261125 as review
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


play, current = review.play, review.play.current
ROOT = current.ROM.parent.with_name("editorial_20261125_london_square_rumor")
ROM, STAGED = ROOT / "London_Square_Rumor_STAGED.nds", ROOT / "unregistered_replay_manifest.json"
CAPTURE, NATIVE = ROOT / "paired", ROOT / "london_square_rumor_preflight_20261125.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / path for path in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE, QA = ROOT / "startup/capture/capture_report.json", ROOT / "qa_passed.xml"
KEY = 709
OLD = review.HOLDS[KEY][3]
LINES = ("Clifford started out as a pirate.", "Now he's a naval admiral.", "Apparently the Queen knighted him.")
PROSE = " ".join(LINES)
NOTE = "Keep the speaker's familiar account of Clifford's past, the turn to his current naval rank and the hearsay about the Queen. Each complete thought stays together in the ordinary Square panel."
FRAMES = tuple(row["frame"] for row in read(play.ROOT / "capture/capture_report.json")["frames_captured"]
               if row["path"].endswith("_navigation.png"))
CHANGED = frozenset(review.HOLDS[KEY][0])


def stage():
    release, live = map(read, (current.RELEASE, review.OUT))
    assert live["candidate_sha256"] == release["candidate_sha256"] == digest(current.ROM)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert live["ordinary_gameplay"] and live["wrap_findings"] == [KEY]
    previous, = [r for r in live["records"] if r["message_ID"] == KEY]
    assert previous["review"]["formatting"] is False and tuple(previous["lines"]) == OLD
    boot = read(release["own_registered_startup"])
    ctx = town.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=boot["actual_captain_getter"])
    clean, candidate = map(NdsImage.open, (CLEAN, current.ROM))
    source_arm, arm, archive = clean.read_file(current.ARM), ctx.arm, ctx.common
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    assert all(arm[lo:hi] == source_arm[lo:hi] for lo, hi in town.SOURCE_RANGES)
    source = town.common_message_entries(clean.read_file(current.COMMON), source_arm)[KEY]
    directory = sha256(arm[town.DIRECTORY_OFFSET:town.TABLE_OFFSET]).hexdigest()
    entries = town.owned_entries(archive, arm, directory)
    old = entries[KEY]
    expected = lambda row: review.panels.text_reference(row) | dict(exact_hex=row.text.hex())
    assert expected(source) == previous["source_reference"] and expected(old) == previous["installed_reference"]
    assert all(b"%" not in row.text for row in (source, old)) and old.text.startswith(b" ")
    raw = b" " + PROSE.encode("ascii")
    assert len(raw) <= len(old.text)
    deployed, rebound, slots = town.owned_deployment(archive, arm, entries, {KEY: raw.ljust(len(old.text), b" ")})
    assert slots[KEY]["new_null_fields"] == 0 and len(deployed) == len(archive)
    assert {a.message_id for a, b in zip(entries, rebound, strict=True) if a != b} == {KEY}
    new = rebound[KEY]
    assert new.text[:1] == old.text[:1] and b"%" not in new.text
    changed = town.with_components(ctx, arm, deployed)
    raster, _, _ = town.font_tools(candidate)
    kanji = candidate.read_file("/GRP/KANJI.FNT")
    views, layouts = [], []
    for title, runtime, row, lines in (("Installed", ctx, old, OLD), ("Proposed", changed, new, LINES)):
        cpu, get, provider = runtime.machine(arm, runtime.common, runtime.raw, runtime.plan)
        pointer = get(0x5528C, KEY)
        assert provider.reads and bytes(cpu.mem_read(pointer, len(row.text) + 1)) == row.text + b"\0"
        formatted, visible = town.native_layout(cpu, row.text, KEY, ())
        assert tuple(visible) == lines and all(0 < len(line) <= 36 for line in lines)
        assert " ".join(visible) == " ".join(row.text.decode("ascii").split())
        pixels, glyphs = town.render_portrait(raster, arm, kanji, formatted)
        assert [glyph["code"] for glyph in glyphs] == town.glyph_codes(formatted)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord("C"), ord("."))
        assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
        views.append((f"{KEY} {title}", pixels))
        layouts.append(dict(version=title, lines=visible, formatted_hex=formatted.hex(),
                            native_plane_sha256=sha256(pixels).hexdigest(), pages=1))
    ROOT.mkdir()
    previews = town.portrait_sheets(ROOT, views)
    candidate.replace_file(current.COMMON, deployed)
    candidate.save(ROM)
    candidate.replace_file(current.COMMON, archive)
    assert sha256(candidate.rom.save()).hexdigest() == release["candidate_sha256"]
    record = previous | dict(english=PROSE, localization_note=NOTE, decision="revision",
        review=dict.fromkeys(GATES, True) | {"formatting": False}, proposed_reference=expected(new),
        native_layouts=layouts, substitution_count=0)
    deployed_sha = sha256(deployed).hexdigest()
    write(NATIVE, dict(candidate_sha256=release["candidate_sha256"], original_square_formatter_parent=0x02054014,
        source_review=reference(review.OUT), records=[record], allocations=slots, native_previews=previews,
        proposed_COMMON_sha256=deployed_sha, ordinary_gameplay=False, registered=False))
    write(STAGED, dict(candidate=reference(ROM), parent=reference(current.ROM), proposal=reference(NATIVE),
        target_COMMON_sha256=deployed_sha, exact_parent_inverse=True, unregistered_staged_replay=True))
    print("Staged the rumor within its original slot and verified both native pages.")


def capture():
    source = checked_text(getsource(replay.capture), {
        "Completed the proposed Guild replay": "Completed the proposed London Square replay",
    })
    scope = vars(replay) | globals() | {"draft": SimpleNamespace(OUT=NATIVE)}
    exec(compile(source, __file__ + "::ordinary-London-replay", "exec"), scope)
    scope["capture"]()


def check_release(action):
    inputs = SimpleNamespace(draft=SimpleNamespace(current=current), PROOF=STAGED, ROM=ROM)
    scope = vars(checks) | dict(stage=inputs, PATCH=PATCH, REBUILT=REBUILT, PATCH_PROOF=PATCH_PROOF,
                                STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(checks.main.__code__, scope)(action)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "capture", "patch", "startup"))
    action = parser.parse_args().action
    if action in ("patch", "startup"):
        check_release(action)
    else:
        {"stage": stage, "capture": capture}[action]()
