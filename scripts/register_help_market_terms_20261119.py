"""Register the current cumulative Market and Source Item Help corrections."""
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.help_source_links import readable_source, source_links
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_square_shop_followup_20261119 as parent
from scripts import stage_help_market_terms_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = parent.base, parent.native
HELP = stage.HELP
PROFILE = "all-routes-help-market-terms-v1-20261119"
ROOT = Path("out/help_market_terms_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Market_Help_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_help_market_terms_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_help_market_terms_20261119.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
QA = stage.ROOT / "supported_qa.xml"
LIVE = stage.ROOT / "gameplay_verification" / "ordinary_gameplay_verification.json"
verified = SimpleNamespace(LIVE=LIVE)
CHECKPOINT = "Five Help topics now use Market and Source Item consistently, with all five pages and linked navigation verified in the emulator."
GATES = ("source", "context", "localization", "naturalness", "formatting")
GLOSSES = {
    21: ("Town Commands link to the Market and its Trade, Commercial Investment and Market Info commands.",
         "At the market, buy and sell trade goods and gather information. If you bring a Source Item, the city may ask to take it. Giving it to them adds a specialty."),
    23: ("The Market's Commercial Investment command. Also linked from Growth.",
         "Invest in groups of 1 to 20 units. Each costs half the city's Growth in gold. Investment raises Growth and raises your share when the total is below 100 percent or a faction at war with you owns a share. Growth can add a specialty."),
    110: ("Shared Commands to Deck View to Workrooms. The article links to the Purser's Office.",
          "Officers do their assigned work in these rooms or stations. The source links to all sixteen rooms and stations."),
    119: ("Purser's Office in the Deck View workrooms. The role affects trading at the Market.",
          "The fleet does its accounting here. An officer assigned here becomes Purser and needs Finance of at least 100. A Purser may get a lower price and may be able to buy out stock at double price. The double price does not apply to sales."),
    148: ("City Info links here. This article links to the Market's Commercial Investment command.",
          "Growth measures a city's development. It rises with commercial investment at the Market. Greater Growth may add specialties and changes recruitment numbers and available cannon types."),
    152: ("City specialty supply and its relationship to Commercial Investment and Source Items.",
          "The trade goods a city sells are its specialties. Development or introduction of a Source Item can add to them. Specialties are restocked in their arrival months."),
    191: ("The Data section links here, with separate pages on types and quality grades.",
          "Trade goods are bought and sold at the Market. The goods sold in a particular city are its specialties. Prices vary by city and market conditions, and base prices vary by cultural region."),
    194: ("Market and Specialties both link here. Market Share is the original outgoing link.",
          "A Source Item is the basis of a specialty. Bringing one to the Market can add a specialty if the city suits the item and has fewer than five already. Several cities can qualify. Give the item in a city that works for you, such as one where your faction has a high share."),
}


def verify(registry, previous, viewed):
    stored, playback, boot, plan = map(base.load, (stage.PROOF, LIVE, STARTUP, stage.PLAN))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == playback["research_ROM_sha256"] == boot["candidate_sha256"]
    assert stored["previous_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["clean_input_sha256"] == previous["clean_input_sha256"] == base.digest(stage.CLEAN)
    assert stored["complete_parent_inverse"]
    for proof in (stored, playback, boot):
        assert all(base.digest(path) == digest for path, digest in proof["evidence"].items())
    assert playback["actual_ordinary_controls_no_state_injection"] and not playback["hardware"]
    assert playback["all_selected_complete_actual_pages_andnative_child_targets_pass"]
    observed = {row["topic_id"] for row in playback["actual_HELP_cases"]}
    assert observed == set(stage.ARTICLES) and playback["offline_only_pages"] == 0
    back, = playback["original_forward_back_andL_R_history_returns"]
    assert back["topic"] == 194 and back["complete_title_andbody_RGB_equal"]
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    sheets = stored["sheets"] + playback["readable_actual_sheets"]
    assert viewed == {sheet["path"]: sheet["sha256"] for sheet in sheets}
    assert all(base.digest(path) == digest for path, digest in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert int(suite.get("tests", 0)) > 0
    assert not any(int(suite.get(key, 0)) for key in ("failures", "errors", "skipped"))
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    original, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (old, new))
    assert before.keys() == after.keys()
    assert {path for path in before if before[path] != after[path]} == {HELP}
    assert sha(after[HELP]) == stored["target_HELP_sha256"] == plan["target_HELP_sha256"]
    controls = bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(original), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    new.replace_file(HELP, before[HELP])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    clean_raw = original.read_file(HELP)
    clean, prior, final = (IlnkContainer.parse(value).blocks for value in (clean_raw, before[HELP], after[HELP]))
    assert len(clean) == 202 and len(prior) == len(final) == 217 and prior[203] == final[203] == b"\0"
    assert [i for i, (was, now) in enumerate(zip(prior, final, strict=True)) if was != now] == list(stage.ARTICLES)
    for row in stored["records"]:
        topic = row["topic_id"]
        assert clean[topic].hex() == row["clean_source_hex"] and prior[topic].hex() == row["current_source_hex"]
        assert [link["topic_id"] for link in source_links(final[topic])] == row["original_link_IDs"]
        if row["decision"] == "revision":
            assert row["registered_hex"] == final[topic].hex()
            assert row["native_display"]["all_executed_current_instruction_bytes_exact"]
        else:
            assert prior[topic] == final[topic]
            row["english"] = " ".join(readable_source(final[topic]).split())
        context, gloss = GLOSSES[topic]
        row.update(speaker="Help system", context=context, source_meaning=gloss, ordinary_emulator_page_observed=topic in observed,
                   registered_reference=dict(file_path=HELP, topic_id=topic, block_sha256=sha(final[topic]),
                                             archive_sha256=sha(after[HELP]), candidate_sha256=candidate))
        row["review"]["formatting"] = True
    review = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
                  review_gates=list(GATES), formatter="registered Help article formatter", records=stored["records"],
                  candidate_sha256=candidate, checked_story_format_guard=controls, observed_gameplay=playback,
                  new_contextual_credit=0, direct_visual_review=viewed, preserved_217_topics_and_original_link_targets=True,
                  preserved_story_archives=True, preserved_ARM9_and_COMMON=True,
                  repository_tests=int(suite.get("tests")))
    validate_natural_dialogue_batch(review)
    return stored, review, {HELP: sha(after[HELP])}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    "len(manifest[\"batches\"]) == 908 and len(manifest[\"checks\"]) == 243":
        "len(manifest[\"batches\"]) == 909 and len(manifest[\"checks\"]) == 244",
    "verified_rafael_iberian_aftermath_predecessor": "verified_square_shop_followup_predecessor",
    "square_shop_followup": "help_market_terms",
    "owned_shared_records=[row[\"registered_reference\"] for row in draft[\"records\"]], target_COMMON_sha256=archives[stage.COMMON]":
        "owned_help_topics=[row[\"registered_reference\"] for row in draft[\"records\"] if row[\"decision\"] == \"revision\"], target_HELP_sha256=archives[HELP]",
    "stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review":
        "stage.PROOF, stage.PLAN, STARTUP, QA, verified.LIVE, args.visual_review",
    "target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON], changed_components=2":
        "target_HELP_sha256=archives[HELP], changed_components=1",
    'ARM9_sha256=archives[stage.ARM], COMMON_sha256=archives[stage.COMMON],':
        "HELP_sha256=archives[HELP],",
    "repository_tests=34": 'repository_tests=draft["repository_tests"]',
    "prose_revisions=4, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=25":
        "prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3",
    "ordinary_Amsterdam_Square_shop_choices_and_menu_returns=True": "ordinary_Help_pages_child_targets_and_history_return=True",
    "previously_localized_records=30": "previously_localized_records=8",
    "Preserve Square shop ROM or reconstruction": "Preserve Market Help ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Market and Source Item Help test candidate

The [local ROM](../../{ROM.as_posix()}) includes five revised Help articles and carries forward the Square Shops build.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Market and Source Item Help

Reviewed eight complete articles against the clean Japanese. The Purser's Office, Growth, Trade Goods and Source Item articles use Market, matching the building and its Help heading. The Specialties article describes and links to Source Item. Market, Commercial Investment and Workrooms retain their exact bytes for the reasons recorded in the ledger. [Exact source and review records](../{REVIEW.as_posix()})

All five revised pages passed the original parser, complete glyph and bounds checks and direct visual review. An ordinary cold-boot emulator replay opened all five, checked the original child link targets, followed Source Item to Market Share and verified return to Source Item through history. Each article stays on one page and all 217 slots and existing continuation owners carry forward. Hardware remains unverified. [Display and replay evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the candidate byte for byte. Only the Help archive changes. All four story archives, native ARM9, the ASCII right-bound correction, all 276 pending shared records and 114 accepted layers carry forward. Six startup frames and 24 protected name getters pass. Review credit stays at 27,700. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
