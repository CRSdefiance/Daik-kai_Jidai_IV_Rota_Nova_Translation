"""Register both source-checked Osaka guildmaster replies in the testing build."""

from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_kurushima_surrender_20261122 as parent
from scripts import stage_osaka_glass_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-osaka-glass-followup-v1-20261122"
ROOT = parent.ROOT.with_name("osaka_glass_registered_20261122")
ROM = ROOT / "Translation_DS_Osaka_Glass_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_osaka_glass_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_osaka_glass_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.review.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
live = SimpleNamespace(LIVE=stage.LIVE)
CHECKPOINT = "Reviewed the full Osaka glass scene on four routes and registered two corrected guildmaster replies."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup = FunctionType(parent.parent.startup.__code__, parent.parent.startup.__globals__ |
                       {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})


def native_count():
    return len(base.load(DISPLAY)["native_pages"])


def observed_count():
    return sum(len(c["sightings"]) for c in base.load(stage.LIVE)["cases"].values())


def observed_names():
    return sum(hold["nameplate"] is not None for c in base.load(stage.LIVE)["cases"].values() for hold in c["sightings"])


def pages_saved():
    return 0


def verify(registry, previous, viewed):
    stored, draft, offline, played = map(base.load, (stage.PROOF, stage.review.REVIEW, DISPLAY, stage.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == played["candidate_sha256"] == base.digest(stage.REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and base.digest(stage.review.REVIEW) == stored["reviewed_manuscript_sha256"]
    assert base.digest(DISPLAY) == stored["offline_proof_sha256"] and base.digest(stage.BINDING) == stored["scope_binding_sha256"]
    visual = base.load(VISUAL)
    assert visual["reviewed_candidate_sha256"] == candidate
    assert viewed == visual["sheets"] == (played["sheets"] | {offline["sheet"]: offline["sheet_sha256"]})
    assert all(base.digest(path) == sha for path, sha in viewed.items())
    assert played["initialized_scenes"] and played["original_scene_commands"] and not played["natural_Osaka_trigger"]
    assert not played["hardware"] and observed_count() == 22
    assert native_count() == 2 and observed_names() == 20
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, source, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    before, after = map(native.files, (source, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == set(stored["changed"])
    assert native.digest(after[native.ARM]) == previous["target_ARM9_sha256"]
    assert native.digest(after["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    for path, entry in stored["changed"].items():
        a, b = [native.IlnkContainer.parse(data) for data in (before[path], after[path])]
        assert [i for i, (x, y) in enumerate(zip(a.blocks, b.blocks, strict=True)) if x != y] == [entry["block"]]
        assert native.digest(b.blocks[entry["block"]]) == entry["target_block"]
        assert native.digest(before[path]) == entry["before"] and native.digest(after[path]) == entry["after"]
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    controls = bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup(previous, candidate, after[native.ARM])

    holds = {(int(route), row["id"]): row for route, case in played["cases"].items() for row in case["sightings"]}
    changed = {(r["route"], r["id"]) for r in offline["native_pages"]}
    assert changed == {(r["route"], r["id"]) for r in draft["records"] if r["decision"] == "revision"}
    for route, index in enumerate(stage.review.BLOCKS):
        path = f"/data/SC{route}.DK4"
        block = native.IlnkContainer.parse(after[path]).blocks[index]
        scope = stored["changed"].get(path)
        commands = {r["record_ids"][0]: r for r in scope["commands"] if r["record_ids"]} if scope else {}
        rows = [r for r in draft["records"] if r["route"] == route]
        assert len(rows) == 11
        for row in rows:
            ident = row["id"]
            hold = holds.get((route, ident))
            if scope:
                command = commands[ident]
                raw = bytes.fromhex(command["stored"])
                offset = command["stored_offset"]
                assert raw[:6] == bytes.fromhex(command["source"])[:6] and hold
            else:
                ref = row["earlier_approved_reference"]
                offset = ref["command_offset"] if "command_offset" in ref else ref["offset"] - 5
                inv, _, _ = native.scoped_inventory()
                command, = [c for c in inv(after[native.ARM], block)[0] if c["offset"] == offset]
                raw = bytes.fromhex(command["whole_command_hex"])
                assert raw[5:raw.index(0, 6)].hex() == row["current_hex"]
            assert raw == block[offset:offset+len(raw)] and raw[5] == row["source_selector"]
            row["registered_reference"] = dict(candidate_sha256=candidate, file_path=path, block=index,
                command_offset=offset, offset=offset+5, exact_stored_hex=raw[5:raw.index(0, 6)].hex(),
                complete_preamble_hex=raw[:6].hex(), complete_command_hex=raw.hex())
            if hold:
                row["gameplay_hold"] = hold
            else:
                row["reused_display_evidence"] = row["prior_editorial_review"]
            row["review"]["formatting"] = True
    draft.update(candidate_sha256=candidate, checked_story_format_guard=controls, direct_visual_review=viewed,
        focused_playback=str(stage.LIVE), offline_native_preflight=str(DISPLAY), natural_Osaka_trigger=False,
        unchanged_pending_records=276, historical_source_credit=dict(by_census_id={}, direct_keys=44),
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {path: e["after"] for path, e in stored["changed"].items()}


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1045 and len(checks) == 380": "len(batches) == 1046 and len(checks) == 381",
    "verified_rafael_deck_tutorial_predecessor=predecessor": "verified_kurushima_surrender_predecessor=predecessor",
    "changed_components=1": "changed_components=2",
    "previously_localized_records=8, contextual_records_revisited=8": "previously_localized_records=44, contextual_records_revisited=44",
    "prior_records_reviewed=8": "prior_records_reviewed=44",
    "observed_Kurushima_panels": "observed_Osaka_panels",
    "prose_revisions=1": "prose_revisions=2",
    "justified_retentions=7": "justified_retentions=42",
    "ordinary_Maria_Kurushima_encounter=True": "initialized_Osaka_scenes=True",
    "natural_activation=True": "natural_activation=False",
    "filename = source.name": 'filename = (source.parent.name + "_" + source.name) if source.name == "scenes.png" else source.name',
    old_readme: '''    (PACKAGE / "README.md").write_text(f"""# Osaka glass testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the corrected guildmaster replies for Hodram and Maria. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("maria_kurushima_surrender", "osaka_glass")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "    research = []": '    research = [Path(base.load(stage.ROOT / f"route{r}/fixture.json")["rom"]) for r in stage.CASES]',
    "Preserve the Maria Kurushima candidate, predecessor and staged ROM": "Preserve the Osaka Glass candidate, predecessor and focused ROMs",
    old_doc: '''    DOC.write_text(f"""# Osaka's glass scene

Reviewed the complete eleven-turn exchange in all four storylines. “Indeed, my lord” now gives the daimyo a direct, respectful answer in Hodram's and Maria's scenes. The other 42 turns retain their wording, including the Japanese term giyaman, its gloss, the daimyo's order, and the forecast about glass. [Exact clean Japanese, previous wording and individual decisions](../{REVIEW.as_posix()})

The two original eleven-turn sequences ran in initialized emulator scenes. Complete body text and nameplates passed, including the two revised replies and each speakerless forecast. The ordinary voyage from Nagasaki remains evidence for Kurushima's encounter. Natural Osaka activation and hardware remain unvisited. [Emulator and native display evidence](../{VERIFY.as_posix()})

Only Hodram's and Maria's Osaka entries change. The clean-input patch rebuilds the testing candidate exactly. Startup and 17 tests passed with all 114 accepted layers and the ASCII right-bound correction preserved. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_kurushima_surrender", "osaka_glass")
scope = parent.scope | globals()
for program in (build, commit):
    exec(compile(program, __file__ + "::registered", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

