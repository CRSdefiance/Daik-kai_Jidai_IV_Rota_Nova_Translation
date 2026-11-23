"""Register the four story exchanges and verified Tripoli Tavern observation."""

from types import FunctionType

from scripts import observe_tripoli_tavern_20261122 as town
from scripts import register_aziza_shamshir_20261122 as parent
from scripts import replay_palace_eirene_pereira_london_20261122 as live
from scripts import stage_palace_eirene_pereira_london_20261122 as stage
from scripts import verify_palace_london_glyphs_20261122 as glyphs
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-palace-eirene-pereira-london-v1-20261122"
ROOT = parent.ROOT.with_name("palace_eirene_pereira_london_registered_20261122")
ROM = ROOT / "Translation_DS_Palace_And_London_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_palace_eirene_pereira_london_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_palace_eirene_pereira_london_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
ORDINARY = town.ROOT / "verified_tavern.json"
CHECKPOINT = "Registered Rafael's palace lesson, Eirene's disclosure, Pereira's challenge and Hodram's London rescue scene."
FIRST_STAGE = stage.BATCH.parent / "staged"
FIRST_REPLAY = FIRST_STAGE / "focused_gameplay/r47_initial_replay/Eirene_R47_INITIAL_FOCUSED_ONLY.nds"
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
prior_startup = parent.startup_scope["startup_proof"]
startup_scope["startup_proof"] = FunctionType(prior_startup.__code__, startup_scope)


def native_count():
    display, proof = map(base.load, (DISPLAY, glyphs.OUTPUT))
    assert proof["candidate_sha256"] == display["candidate_sha256"]
    assert proof["native_report_sha256"] == base.digest(DISPLAY)
    assert proof["complete_font_pixels"] and proof["exact_contact_sheet_pixels"]
    assert len(proof["pages"]) == display["pages"]
    return display["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def preserved_scene_controls(records, image, candidate):
    proof = base.load(stage.CHOICE_PROOF)
    assert proof["candidate_sha256"] == candidate and proof["offline_exact"]
    row = proof["choice"]
    assert len(row["english"]) == 2 and all(row["review"].values())
    bank = native.IlnkContainer.parse(image["/data/SC0.DK4"]).blocks[143]
    at, raw = row["installed_offset"], bytes.fromhex(row["installed_command_hex"])
    assert native.digest(bank) == row["installed_block_sha256"] and bank[at:at+len(raw)] == raw
    held = [r for r in records if r["source_selector"] == 254]
    assert len(held) == 7 and all(r["decision"] == "retention" for r in held)
    for item in held:
        assert item["current_reference"]["exact_command_hex"] == item["registered_reference"]["exact_command_hex"]
    return dict(choice=row, retained_speakerless=[r["registered_reference"] for r in held])


def verify_town(candidate):
    result = base.load(ORDINARY)
    assert result["candidate_sha256"] == candidate and result["ordinary_saved_gameplay"]
    assert result["port"] == "Tripoli" and result["message_ID"] == 51
    assert [row["message_ID"] for row in result["decisions"]] == [51, 53, 823]
    assert all(base.digest(p) == sha for p, sha in result["evidence"].items())
    return result


verify_source = checked_text(parent.parent.verify_source, {
    'observed_count() == 19': 'observed_count() == 23',
    'native_count() == 29': 'native_count() == 27',
    'checked["sheets"] + played["sheets"]':
        'checked["sheets"] + played["sheets"] + verify_town(candidate)["sheets"]',
    'len(records) == 180': 'len(records) == 275',
    'len(changed) == 27': 'len(changed) == 25',
    'assert sum(r["change_class"] == "wrap_only" for r in changed) == 3':
        'assert all(r["change_class"] == "prose" for r in changed)',
    'exact_display_retentions=exact_display_retentions(records),':
        'native_controls=preserved_scene_controls(records, b, candidate), ordinary_town_visits=verify_town(candidate),',
    'wording_revisions=24, wrap_only_revisions=3': 'wording_revisions=25, wrap_only_revisions=0',
    'justified_retentions=153': 'justified_retentions=250',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1063 and len(checks) == 398": "len(batches) == 1064 and len(checks) == 399",
    "previously_localized_records=78, contextual_records_revisited=78": "previously_localized_records=277, contextual_records_revisited=277",
    "prior_records_reviewed=78": "prior_records_reviewed=277",
    "changed_components=1": "changed_components=2",
    "justified_retentions=64": "justified_retentions=250, retained_choice_labels=2",
    "prose_revisions=14": "prose_revisions=25",
    "punctuation_glyph_corrections=1": "punctuation_glyph_corrections=0",
    "focused_initialized_Rafael=True": "focused_initialized_Rafael_and_Hodram=True",
    "(live.LIVE, DISPLAY, stage.PROOF, ORDINARY)": "(live.LIVE, DISPLAY, stage.PROOF, ORDINARY, stage.CHOICE_PROOF, glyphs.OUTPUT)",
    "DISPLAY, ORDINARY, args.visual_review,": "DISPLAY, ORDINARY, stage.CHOICE_PROOF, glyphs.OUTPUT, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Palace lesson and London rescue testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries 25 dialogue revisions in four complete exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("aziza_shamshir", "palace_eirene_pereira_london").replace(
    "verified_mosque_elysion_mikhail_predecessor", "verified_aziza_shamshir_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Aziza candidate, predecessor and unique focused ROM":
        "Preserve the palace and London candidate, predecessor and unique focused ROMs",
    "earlier = [live.ROM]":
        "earlier = [live.ROM, live.HODRAM_ROM, FIRST_STAGE / stage.ROM.name, FIRST_REPLAY,\n"
        "               FIRST_STAGE / 'focused_gameplay/rafael' / live.ROM.name,\n"
        "               FIRST_STAGE / 'focused_gameplay/route1' / live.HODRAM_ROM.name]",
    old_doc:'''    DOC.write_text(f"""# Palace lesson, Eirene, Pereira and the London rescue

The clean-Japanese review covers 275 dialogue records and both labels of Silveira's lesson choice. It uses 25 wording revisions and 250 dialogue retentions. Silveira's two ways of opening hostilities, the scope of the instruction, the king's amount of gold and the investment restrictions keep their original details. Eirene keeps her established names and speaks for herself about the disguise. Cristina's gratitude and her response to Mivor remain distinct. [Coverage ledger](../{REVIEW.as_posix()})

Focused Rafael and Hodram replays checked 23 panels and nameplates. They include the two name substitutions, the Eirene disclosure and Mivor's original comparison signs. Offline checks covered 27 native layout variants. Both lesson options and seven speakerless commands are byte-exact. Natural story activation, the lesson choice's live branches and hardware remain unvisited. [Testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)

An ordinary saved-game visit to Tripoli verified the Barkeep's greeting, the five-coin drink price and the random lead about Algiers. The evidence links all three panels to their original COMMON requests. [Town observation](../{ORDINARY.as_posix()})
""",encoding="utf-8")
''',
}).replace("aziza_shamshir", "palace_eirene_pereira_london")
scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
