"""Register the reviewed naturalist, Camille and shield-rumor exchanges."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_naturalist_aliases_and_shield_20261119 as game
from scripts import checkpoint_remaining_dialogue_glyphs_20261119 as glyphs
from scripts import prove_lil_B167_names_v4124b as original_names
from scripts import register_story_short_phrase_wraps_20261119 as parent
from scripts import stage_naturalist_aliases_and_shield_20261119 as stage
from scripts import verify_naturalist_aliases_and_shield_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-naturalist-aliases-shield-v1-20261119"
ROOT = Path("out/naturalist_aliases_shield_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Naturalist_and_Shield_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_naturalist_aliases_shield_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_naturalist_aliases_and_shield_20261119.md")
STARTUP, QA = game.STARTUP, stage.ROOT.with_name("research_v2") / "supported_qa_v2.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "The Athens and Camille exchanges and all four Armadillo Hide rumors have a registered candidate and a focused Athens replay."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=game.PROOF)


def current_getters(previous, identity):
    source = checked_text(getsource(original_names.names), {
        "for ident in [2,4,13,23,109]:": "for ident in (9,22,75,76):",
    })
    scope = vars(original_names).copy()
    exec(compile(source, __file__ + "::four-actor-consumers", "exec"), scope)
    ctx = native.RegisteredRuntime(parent.RELEASE, previous["own_registered_startup"], captain=3)
    check = ctx.execute(scope["names"])
    actual = {(r["actor_ID"], r["consumer"]): r["text"] for r in check["rows"]}
    expected = base.load(stage.review.DEFAULT_NAMES)["current_default_names"]
    for row in expected:
        if row["actor_ID"] in (9, 22, 75, 76):
            for form in row["current_consumers"]:
                assert actual[row["actor_ID"], form["consumer"]] == form["text"]
    assert len(actual) == 8
    assert all(actual[int(actor), "progressive-nameplate"] == text for actor, text in identity["default_forms"].items())
    return dict(verified_runtime=ctx.receipt(), rows=check["rows"], candidate_ARM9_and_COMMON_exact_to_runtime=True)


verification = checked_text(getsource(parent.verify), {
    '    assert path["result"] == [0, 1] and len(path["speeches"]) == 16\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        '    assert path["source_commands_visited"] > 100 and path["exit_frame"] > 0\n'
        '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] >= 10\n'
        '    assert not path["rendered_mismatches"]',
    '    assert len(sheets) == 5 and viewed == {s["path"]: s["sha256"] for s in sheets}':
        '    assert viewed == {s["path"]: s["sha256"] for s in sheets}',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 7 and len(commands) == len(draft["records"]) == 230',
    'len(revisions) == 19 and len(retentions) == 176': 'len(revisions) == 57 and len(retentions) == 173',
    'block == 127 and': 'block == 48 and',
    '        row["review"]["formatting"] = True':
        '        if file_path == "/data/SC2.DK4" and block == 65:\n'
        '            row["context"] = "Lil learns why Camille answers to Marinus when Kuhn appears after their campaign in Southeast Asia."\n'
        '        row["review"]["formatting"] = True',
    '    validate_natural_dialogue_batch(draft)':
        '    draft["identity_and_item"]["confirmed_getters"] = current_getters(previous, draft["identity_and_item"])\n'
        '    scan = base.load(glyphs.OUTPUT)\n'
        '    assert scan["ARM9_sha256"] == previous["target_ARM9_sha256"] and scan["COMMON_sha256"] == previous["target_COMMON_sha256"]\n'
        '    draft["remaining_glyphs"] = dict(path=glyphs.OUTPUT.as_posix(), sha256=base.digest(glyphs.OUTPUT))\n'
        '    validate_natural_dialogue_batch(draft)',
})

publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 898 and len(manifest["checks"]) == 233':
        'len(manifest["batches"]) == 899 and len(manifest["checks"]) == 234',
    "release_stack_before_story_phrase_wraps.json": "release_stack_before_naturalist_aliases_shield.json",
    "release_stack_with_story_phrase_wraps.json": "release_stack_with_naturalist_aliases_shield.json",
    "verified_market_followup_predecessor": "verified_story_short_phrase_wraps_predecessor",
    "story_short_phrase_wraps_release": "naturalist_aliases_and_shield_release",
    "registered_story_short_phrase_wraps_and_complete_parent_inverse": "registered_naturalist_aliases_and_shield_and_complete_parent_inverse",
    "story_short_phrase_wraps_pipeline": "naturalist_aliases_and_shield_pipeline",
    "prose_revisions=17, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=176":
        "prose_revisions=56, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=173",
    "text_display_revisions=19": "text_display_revisions=57",
    "initialized_Ceuta_wind_choice_and_return=True": "initialized_Rafael_Athens_scene_and_return=True",
    "previously_localized_records=195": "previously_localized_records=230",
    'ledger["story_short_phrase_wraps_20261119"]': 'ledger["naturalist_aliases_and_shield_20261119"]',
    "*(stage.ROOT.parent / \"research_v1\").glob(\"*.nds\")]":
        "*(stage.ROOT.parent / \"research_v1\").rglob(\"*.nds\"),\n"
        "                  *(stage.ROOT.parent / \"research_v2\").rglob(\"*.nds\")]",
    "Preserve story phrase-wrap ROM, fixture or reconstruction": "Preserve naturalist and shield rumor ROM, fixture or reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Naturalist and Shield Rumor test candidate

The [local ROM](../../{ROM.as_posix()}) carries Rafael’s revised Athens scene, Lil’s Camille and Mikhail conversations, and the Armadillo Hide rumor in all four routes.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 {candidate} byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Naturalist, Camille and shield-rumor candidate

The review covers 230 records in seven complete exchanges. It records 56 wording revisions, one wrap-only correction and 173 justified retentions. Rafael’s Athens scene now reads more naturally from Hans’s plea for passage through the introduction to the Proof of Conquest and the two system notices. The review preserves Hans and Mikhail as distinct naturalists, Camille as the crew knows him, and Marinus Kuhn as the name he reveals. All four captains’ shield rumors retain Samwell’s informal voice, the uncertain lead in Africa and the item name shown by the registered game. [Exact review ledger](../{REVIEW.as_posix()})

The 57 revised pages passed native layout and direct visual review, including the two speakerless panels and the expansion cases for the player’s entered name. The focused emulator run entered the complete Athens block through the original Rafael New Game prelude. It verified {base.load(verified.LIVE)['revised_pages_verified']} revised pages and the original return. The other revised exchanges received offline checks. Natural scene activation and hardware remain unverified. [Athens replay](../{(VERIFY / 'athens_playback_1.png').as_posix()})

The patch rebuilt the cumulative candidate byte for byte. Six startup checkpoints, 24 protected getters and 34 focused tests passed. This release preserves all 114 accepted layers, the ASCII right-bound correction and the existing credit for all 230 records. The 276 pending shared text entries still have open display coverage. Main awaits acceptance. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)

A separate offline scan checked the 3,668 stored COMMON entries and found Japanese script or full-width Latin only among the already tracked keys. The aligned standard dialogue scan isolated the original masked shouts in Hodram’s confrontation with Pasha. Their American English presentation and the surrounding challenge remain in review. [Exact glyph checkpoint](../{glyphs.OUTPUT.as_posix()})
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification + "\n\n" + main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
