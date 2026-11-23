"""Register the cumulative Athens and London trend candidate."""
from inspect import getsource
from pathlib import Path

from scripts import register_lisbon_fragrance_wraps_20261121 as parent
from scripts import stage_athens_london_trends_20261121 as stage
from scripts import verify_athens_london_trends_display_20261121 as display
from scripts import verify_athens_london_trends_replay_20261121 as live
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
base, native, workflow = stage.base, stage.native, parent.scope["workflow"]
PROFILE = "all-routes-athens-london-trends-v1-20261121"
ROOT = Path("out/athens_london_trend_repairs_registered_20261121")
ROM = ROOT / "Translation_DS_Athens_London_Trends_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_athens_london_trends_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_athens_london_trends_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
CHECKPOINT = ("Athens and London Square scenes have ten edits and 62 justified retentions across all four routes. "
              "Hodram's two full scenes passed ordinary gameplay. Stockholm's December 19 gate passed focused checks.")


verify_source = getsource(template.verify)
single_archive = verify_source[verify_source.index('    groups ='):verify_source.index('    assert bytes(target.rom.save())')]
verification = checked_text(verify_source, {
    'draft["decisions"] == {"revision": 5, "retention": 32}': 'draft["decisions"] == {"revision": 10, "retention": 62}',
    'playback["initialized_excerpts"]': 'playback["natural_activation"]',
    'assert not playback["natural_activation"] and not playback["hardware_verified"]':
        'assert playback["original_notice_dismissal_and_Square_return"] and not playback["hardware_verified"]',
    'rendered["newly_rendered_pages"] == 5': 'rendered["newly_rendered_pages"] == 10',
    'len(playback["holds"]) == 21 and {h["route"] for h in playback["holds"]} == {0, 1}':
        'len(playback["holds"]) == 18 and {h["route"] for h in playback["holds"]} == {1}',
    'and len(viewed) == 3': 'and len(viewed) == 5',
    single_archive: '''    groups = {(g["file_path"], g["block"]): g for g in stored["groups"]}
    assert len(groups) == 8 and before.keys() == after.keys()
    changed_paths = {p for p in before if before[p] != after[p]}
    assert changed_paths == {"/data/SC1.DK4", "/data/SC3.DK4"}
    archives, blocks = {}, {}
    for path in sorted({p for p, _ in groups}):
        japan, old, new = [native.IlnkContainer.parse(data).blocks for data in (source[path], before[path], after[path])]
        changes = {number for (p, number), g in groups.items() if p == path and g["before"] != g["after"]}
        assert {i for i, (a,b) in enumerate(zip(old, new, strict=True)) if a != b} == changes
        for (p, number), group in groups.items():
            if p == path:
                assert native.digest(japan[number]) == group["source"]
                assert native.digest(old[number]) == group["before"] and native.digest(new[number]) == group["after"]
                blocks[path, number] = new[number]
        if changes:
            archives[path] = native.digest(after[path])
            target.replace_file(path, before[path])
''',
    'for path in groups:\n        target.replace_file': 'for path in changed_paths:\n        target.replace_file',
    'after[stage.review.shared.COMMON]': 'after["/COMMON/MESFILE.DK4"]',
    '    assert stage.review.bind_movie(clean, target, (source[native.ARM], arm))["sha256"] == draft["artwork"]["sha256"]':
        '    assert all(after[f"/data/EV{i}.DK4"] == source[f"/data/EV{i}.DK4"] for i in range(4))',
    'seen = {r["id"] for r in playback["holds"]}': 'seen = {(r["file_path"], r["id"]) for r in playback["holds"]}',
    'len(checked) == len(draft["records"]) == 37': 'len(checked) == len(draft["records"]) == 72',
    'blocks[path][at:at+len(raw)]': 'blocks[path, row["block"]][at:at+len(raw)]',
    'assert ident in seen and result["native_pages"] == 1':
        'assert ((path, ident) in seen) == (row["route"] == 1) and result["native_pages"] == 1',
    'archive_sha256=archives[path]': 'archive_sha256=native.digest(after[path])',
    'groups[path]["after"]': 'groups[path, row["block"]]["after"]',
    'row["observed_in_initialized_excerpt"] = ident in seen':
        'row["observed_in_ordinary_gameplay"] = (path, ident) in seen',
    'status="registered", direct_visual_review=viewed,': 'status="registered", direct_visual_review=viewed,\n'
        '        encoder="dialogue-relocatable-v1",',
    'excerpt_evidence=str(live.PROOF)': 'ordinary_town_replay_evidence=str(live.PROOF)',
})

main_source = getsource(template.main)
readme = main_source[main_source.index('    (PACKAGE / "README.md").write_text'):main_source.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(main_source, {
    "verified_search_forage_wrap_predecessor": "verified_lisbon_fragrance_predecessor",
    "len(batches) == 979 and len(checks) == 314": "len(batches) == 982 and len(checks) == 317",
    "source_movie_preserved=True": "original_town_events_preserved=True",
    "previously_localized_records=37, new_contextual_records=0, prose_revisions=4":
        "previously_localized_records=72, new_contextual_records=0, prose_revisions=9",
    "wrap_only_revisions=0, justified_retentions=32, name_label_revisions=0, text_display_revisions=1":
        "wrap_only_revisions=1, justified_retentions=62, name_label_revisions=0, text_display_revisions=0",
    "initialized_Rafael_and_Hodram_excerpts=True": "ordinary_Hodram_Athens_and_London=True",
    "native_revised_pages=5, observed_panels=21, natural_activation=False":
        "native_revised_pages=10, observed_panels=18, natural_activation=True",
    "prior_records_reviewed=37, actual_Rafael_and_Hodram_panels=21, offline_pages=5":
        "prior_records_reviewed=72, actual_Hodram_panels=18, offline_pages=10",
    "prose_revisions=4, justified_retentions=32, text_display_revisions=1":
        "prose_revisions=9, justified_retentions=62, wrap_only_revisions=1",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Athens and London Square testing candidate

The [testing ROM](../../{ROM.as_posix()}) updates dialogue and wrapping in two town scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("moonlit_violin", "athens_london_trends")

commit_source = getsource(template.commit)
checkpoint_prose = commit_source[commit_source.index("    DOC.write_text"):commit_source.index("    prefix =")]
commit_candidate = checked_text(commit_source, {
    "Preserve the violin candidate or replay ROM": "Preserve the Athens and London candidate or staging ROM",
    checkpoint_prose: '''    DOC.write_text(f"""# Athens and London Square dialogue

Reviewed 72 source-bound records across all four routes. In Hodram's and Maria's Athens scenes, the women's sighs now read as actions. The Athens wish and London ring comparison keep their phrases together, and one London reflow preserves the existing wording. Each of the 62 retentions has a reason. [Clean Japanese and exact registered references](../{REVIEW.as_posix()})

Ordinary gameplay verified 18 panels across both Hodram scenes, including six revised lines, the original forecasts and both returns to the Square. The ten changed pages passed native bounds and visual review. Maria's four revised panels received offline checks. Six startup holds, 24 protected name getters and 17 focused tests passed. [Cumulative candidate and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)

An ordinary February visit reached Stockholm's Square. Opening the fur exchange in December remains unvisited. Focused testing of the original date check confirmed that December 18 is too early and December 19 is eligible. [Town gameplay and date evidence](../translations/editorial_checkpoints/SharedText_20261110_v1/european_trend_gameplay_20261121_v1.json)
""", encoding="utf-8")
''',
}).replace("moonlit_violin", "athens_london_trends")

scope = vars(template) | globals()
for source in (verification, build, commit_candidate):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
