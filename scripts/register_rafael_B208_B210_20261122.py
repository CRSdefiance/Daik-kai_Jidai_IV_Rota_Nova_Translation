"""Register Rafael's reviewed bargaining, book seller, and Namahage encounters."""

from types import SimpleNamespace

from scripts import register_rafael_B181_B187_20261121 as parent
from scripts import replay_rafael_B208_B210_20261122 as live
from scripts import verify_rafael_B208_B210_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B208-B210-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_B208_B210_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_B208_B210_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_B208_B210_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B208_B210_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (208, 210)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Reviewed 77 Rafael records with 15 wording revisions, three glyph corrections, and 59 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 13 and not rendered["menus"] and rendered["full_name_retention_cases"] == [display.FULL_NAME_ID]':
        'rendered["FE_panels"] == 8 and [m["count"] for m in rendered["menus"]] == [2] * 6 + [3]',
    'len(playback["holds"]) == 40 and not playback["menus"] and len(playback["exact_sampled_page_turn"]) == 5':
        'len(playback["holds"]) == 31 and len(playback["menus"]) == 5 and len(playback["exact_sampled_page_turn"]) == 6',
    'len(group["commands"]) for group in groups.values()) == 308': 'len(group["commands"]) for group in groups.values()) == 195',
    'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check':
        'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 227': '== len(draft["records"]) == 77',
    '{"wording": 39, "glyph": 3, "wrap-only": 2, "retention": 183}':
        '{"wording": 15, "glyph": 3, "retention": 59}',
    'and r["previous_English"] in ("…", "……") and r["english"] == "..."':
        'and (r["previous_English"], r["english"]) in (("…", "..."), ("……", "......"))',
    '    assert not rendered["style_objects"]':
        '''    assert not rendered["style_objects"]
    charm, = [row for row in rendered["records"] if row["id"] == display.CHARM]
    width = charm["system"][0]["width_stress"]
    assert width["rows"] == [[0, 0, "WWWWWWWWWWWWWWWW's Charm rose by 1!"]]''',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_B177_B180_predecessor': 'verified_rafael_B181_B187_predecessor',
    'len(batches) == 1011 and len(checks) == 346': 'len(batches) == 1012 and len(checks) == 347',
    'previously_localized_records=227': 'previously_localized_records=77',
    'prose_revisions=39': 'prose_revisions=15',
    'wrap_only_revisions=2': 'wrap_only_revisions=0',
    'justified_retentions=183': 'justified_retentions=59',
    'prior_records_reviewed=227': 'prior_records_reviewed=77',
    'actual_menu_samples=0': 'actual_menu_samples=5',
    'initialized_Rafael_B181_B187=True': 'initialized_Rafael_B208_B210=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's bargaining, book seller, and Namahage scenes

The [testing ROM](../../{ROM.as_posix()}) includes the contextual review of Rafael's SC0 blocks 208–210. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B181_B187", "rafael_B208_B210").replace(
    "verified_rafael_B208_B210_predecessor", "verified_rafael_B181_B187_predecessor").replace(
    '"rafael_B208_B210_20261121"', '"rafael_B208_B210_20261122"')

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B181_B187': 'glob("staged_B208_B210',
    'Rafael_B181_B187_FOCUSED_ONLY.nds': 'Rafael_B208_B210_FOCUSED_ONLY.nds',
    "Preserve the Rafael Yifa, crown, and Aziza candidate": "Preserve the Rafael bargaining, book seller, and Namahage candidate",
    '# Current editorial checkpoint - 2026-11-21': '# Current editorial checkpoint - 2026-11-22',
    notes: '''    DOC.write_text(f"""# Rafael's bargaining, book seller, and Namahage scenes

The contextual pass covers 77 records in SC0 blocks 208–210. The six offers retain their exact amounts and use gold consistently. Carlo's initial advice links the first refusal to the price dropping by half and leaves room for at least two further cuts. Ian's scene preserves the purchase, refusal, delegation, and gift paths. The Namahage retains its repeated questions and original Japanese term. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

The Charm notice retains the original given-name substitution and fits on a single row with a 16-character name. Eight speakerless panels retain the original control. Offline checks cover {native_count()} revised pages, ten nameplates, and all 15 labels across seven choice menus. The focused emulator excerpts verified {observed_count()} speech pages, five choice highlight states, named-to-speakerless transitions, and the return to port. Natural branch activation and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The registered candidate preserves 114 accepted layers, the right-bound correction, and seven source-format controls. Six startup comparisons, 17 regression tests, and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B181_B187", "rafael_B208_B210")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
