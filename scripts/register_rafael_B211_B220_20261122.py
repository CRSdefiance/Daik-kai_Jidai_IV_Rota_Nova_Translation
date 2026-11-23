"""Register the complete Rafael B211–220 editorial packet."""

from types import SimpleNamespace

from scripts import register_rafael_B208_B210_20261122 as parent
from scripts import replay_rafael_B211_B220_20261122 as live
from scripts import verify_rafael_B211_B220_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B211-B220-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_B211_B220_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_B211_B220_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_B211_B220_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B211_B220_registered_20261122.md")
EVIDENCE = writer.INITIAL_STAGE
REBOUND = writer.ROOT / "rebound_identical_stage.json"
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (211, 212, 213, 215, 216, 217, 218, 220)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Revisited 192 Rafael records and carried forward 32 earlier decisions. The new review made 45 wording revisions, one glyph correction, and five wrap-only fixes, with 141 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 8 and [m["count"] for m in rendered["menus"]] == [2] * 6 + [3]':
        'rendered["FE_panels"] == 19 and [m["count"] for m in rendered["menus"]] == [2, 2, 2]',
    '''    charm, = [row for row in rendered["records"] if row["id"] == display.CHARM]
    width = charm["system"][0]["width_stress"]
    assert width["rows"] == [[0, 0, "WWWWWWWWWWWWWWWW's Charm rose by 1!"]]''':
        '''    notices = {row["id"]: row["system"][0]["width_stress"]["rows"] for row in rendered["records"] if row["id"] in writer.NOTICES}
    assert set(notices) == writer.NOTICES
    assert sorted(row[0][2] for row in notices.values()) == ["WWWWWWWWWWWWWWWW's Charm rose by 1!"] * 2 + ["WWWWWWWWWWWWWWWW's Spirit rose by 1!"]
    rebound = base.load(REBOUND)
    assert rebound["candidate_sha256"] == candidate and rebound["full_ROM_identical"] and rebound["stored_commands_identical"]
    assert rebound["revised_proof_sha256"] == base.digest(stage.PROOF)
    assert rebound["initial_proof_sha256"] == base.digest(EVIDENCE / stage.PROOF.name)
    assert base.digest(EVIDENCE / stage.ROM.name) == candidate
    assert draft["contextual_records_revisited"] == 192 and draft["contextual_decisions_reused"] == 32''',
    'len(playback["holds"]) == 31 and len(playback["menus"]) == 5 and len(playback["exact_sampled_page_turn"]) == 6':
        'len(playback["holds"]) == len(live.SELECTED) - 3 and len(playback["menus"]) == 6 and len(playback["exact_sampled_page_turn"]) == 3',
    'len(name_check["records"]) == 10': 'len(name_check["records"]) == 19',
    'len(group["commands"]) for group in groups.values()) == 195': 'len(group["commands"]) for group in groups.values()) == 325',
    'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check':
        'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 77': '== len(draft["records"]) == 224',
    '{"wording": 15, "glyph": 3, "retention": 59}': '{"wording": 45, "glyph": 1, "wrap-only": 5, "retention": 173}',
    'assert len(glyphs) == 3': 'assert len(glyphs) == 1',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_B181_B187_predecessor': 'verified_rafael_B208_B210_predecessor',
    'len(batches) == 1012 and len(checks) == 347': 'len(batches) == 1013 and len(checks) == 348',
    'previously_localized_records=77': 'previously_localized_records=224, contextual_records_revisited=192, contextual_decisions_reused=32',
    'prose_revisions=15': 'prose_revisions=45',
    'wrap_only_revisions=0': 'wrap_only_revisions=5',
    'justified_retentions=59': 'justified_retentions=141',
    'text_display_revisions=3': 'text_display_revisions=1',
    'punctuation_glyph_corrections=3': 'punctuation_glyph_corrections=1',
    'prior_records_reviewed=77': 'prior_records_reviewed=192, contextual_decisions_reused=32',
    'contextual_nameplate_retentions=10': 'contextual_nameplate_retentions=19',
    'actual_menu_samples=5': 'actual_menu_samples=6',
    'initialized_Rafael_B208_B210=True': 'initialized_Rafael_B211_B220=True',
    'STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, args.visual_review,': 'STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, REBOUND, args.visual_review,',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's portrait, castle, parrot, and item encounters

The [testing ROM](../../{ROM.as_posix()}) includes the contextual review of Rafael's SC0 blocks 211–220. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B208_B210", "rafael_B211_B220").replace(
    "verified_rafael_B211_B220_predecessor", "verified_rafael_B208_B210_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B208_B210': 'glob("staged_B211_B220',
    'Rafael_B208_B210_FOCUSED_ONLY.nds': 'Rafael_B211_B220_FOCUSED_ONLY.nds',
    "Preserve the Rafael bargaining, book seller, and Namahage candidate": "Preserve the Rafael portrait, castle, parrot, and item candidate",
    notes: '''    DOC.write_text(f"""# Rafael's portrait, castle, parrot, and item encounters

The contextual pass revisits 192 records and carries forward 32 exact earlier decisions from B214 and B219. The portrait sequence preserves Rafael's attempt to hand over the book and Claudio's distraction. Carlo carries the stranger to the inn and politely accepts the gift after being pressed. The rope negotiation preserves its exact offers and the distinct stat rewards. Rafael offers to pay for the medicinal book after Hans admits wanting to read it. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Jam's claims about his figurehead remain distinct from the castle's account. The four letter panels preserve his full indented signature. Every parrot echo keeps Angelo's exact words and the original speakerless control. The earring seller's pitch remains his own sales claim, and Cristina's follow-up keeps the rumor about the lost sword qualified.

Native verification covers {native_count()} revised pages, three 16-character substitutions, 19 speakerless panels, 19 nameplates, and six menu captions. Focused cold-boot excerpts verify {observed_count()} dialogue pages, six choice highlights, the earring dialogue's page progression, four consecutive letter panels and the parrot's nameplate transitions. Natural encounter activation and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers, the ASCII right-bound correction and seven source-format controls. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B208_B210", "rafael_B211_B220")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
