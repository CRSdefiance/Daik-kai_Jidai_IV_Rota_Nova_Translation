"""Register the verified Rafael story follow-up and cumulative clean-input patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_hodram_baltic_trade_20261121 as parent
from scripts import check_rafael_north_sea_africa_gameplay_20261121 as live
from scripts import verify_rafael_north_sea_africa_20261121 as rendered
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = stage.base, stage.native, parent.workflow
display = SimpleNamespace(PROOF=rendered.PROOF)
PROFILE = "all-routes-rafael-north-sea-africa-v1-20261121"
ROOT = Path("out/rafael_north_sea_africa_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_North_Sea_Africa_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_north_sea_africa_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_north_sea_africa_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed 146 records across nine complete Rafael exchanges. The candidate includes 34 wording revisions, "
              "four wrap-only revisions and 108 justified retentions.")


# The accepted prefix and commit path stay frozen. Bind the next verified
# archive transaction to the preceding manifest and registry.
verification = checked_text(getsource(parent.verify), {
    "base.load, (stage.PROOF, stage.OUTPUT, display.PROOF, live.PROOF)":
        "base.load, (stage.PROOF, stage.review.OUTPUT, display.PROOF, live.PROOF)",
    "draft['decisions'] == {'revision': 5, 'retention': 4}":
        "draft['decisions'] == {'revision': 38, 'retention': 108}",
    "playback['natural_activation'] and playback['exact_native_glyph_matches']":
        "playback['initialized_excerpts'] and not playback['natural_activation'] and playback['exact_native_glyph_matches']",
    "assert playback['original_port_transition'] and not playback['hardware_verified']":
        "assert len(playback['cases']) == 2 and not playback['hardware_verified']",
    "rendered['newly_rendered_pages'] == 5 and not rendered['actual_gameplay']":
        "rendered['newly_rendered_pages'] == 38 and rendered['offline_native_only']",
    "len(playback['holds']) == 5 and len(playback['unchanged_controls']) == 4":
        "len(playback['holds']) == 13 and len(playback['offline_only']) == 25",
    " and len(viewed) == 3": "",
    """    path, number = stage.SCENE, stage.BLOCK
    group, = stored['groups']
    assert (group['file_path'], group['block']) == (path, number)
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {path}
    old, new = [native.IlnkContainer.parse(data).blocks for data in (before[path], after[path])]
    assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [number]
    assert native.digest(old[number]) == group['before'] and native.digest(new[number]) == group['after']""":
    """    path = "/data/SC0.DK4"
    groups = {g['block']: g for g in stored['groups']}
    numbers = list(stage.review.BLOCKS[0])
    assert sorted(groups) == numbers and all(g['file_path'] == path for g in groups.values())
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {path}
    old, new = [native.IlnkContainer.parse(data).blocks for data in (before[path], after[path])]
    assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == numbers
    assert all(native.digest(old[n]) == groups[n]['before'] and native.digest(new[n]) == groups[n]['after'] for n in numbers)""",
    """    retained = {row['id'] for row in playback['unchanged_controls']}
    assert len(checked) == len(draft['records']) == 9 and revised.isdisjoint(retained)
    assert set(checked) == revised | retained""":
    """    unseen = set(playback['offline_only'])
    assert len(checked) == len(draft['records']) == 146 and revised.isdisjoint(unseen)
    assert revised | unseen == {row['id'] for row in draft['records'] if row['decision'] == 'revision'}""",
    "        result = checked[ident]": "        result = checked[ident]\n        number = row['block']\n        group = groups[number]",
    "        assert (ident in revised) == (row['decision'] == 'revision') and result['native_pages'] == 1":
        "        assert (ident in revised | unseen) == (row['decision'] == 'revision')\n"
        "        if row['decision'] == 'revision':\n            assert result['native_pages'] == 1",
    "exact_stored_hex=result['installed_selector_and_body']": "exact_stored_hex=raw[5:raw.index(0, 6)].hex()",
    "row['observed_in_ordinary_gameplay'] = True": "row['observed_in_initialized_excerpt'] = ident in revised",
    "ordinary_town_replay_evidence=str(live.PROOF)": "initialized_replay_evidence=str(live.PROOF)",
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_refit_sailing_parallel_routes_predecessor": "verified_hodram_baltic_trade_predecessor",
    "len(batches) == 995 and len(checks) == 330": "len(batches) == 996 and len(checks) == 331",
    "original_Baltic_trade_lesson_command_map_preserved=True": "nine_original_exchange_command_maps_preserved=True",
    "previously_localized_records=9, new_contextual_records=0, prose_revisions=5":
        "previously_localized_records=146, new_contextual_records=0, prose_revisions=34",
    "wrap_only_revisions=0, justified_retentions=4": "wrap_only_revisions=4, justified_retentions=108",
    "ordinary_Hodram_Hamburg_docking=True": "initialized_Rafael_excerpts=True",
    "native_revised_pages=5, observed_holds=9, natural_activation=True":
        "native_revised_pages=38, observed_holds=13, natural_activation=False",
    "prior_records_reviewed=9, observed_Hodram_panels=9, native_pages=5":
        "prior_records_reviewed=146, observed_Rafael_panels=13, native_pages=38",
    "prose_revisions=5, justified_retentions=4, wrap_only_revisions=0":
        "prose_revisions=34, justified_retentions=108, wrap_only_revisions=4",
    """        copyfile(source, VERIFY / source.name)
        assert base.digest(source) == base.digest(VERIFY / source.name)""":
    """        filename = "refreshed_" + source.name if source.parent == rendered.ROOT else source.name
        target = VERIFY / filename
        assert not target.exists()
        copyfile(source, target)
        assert base.digest(source) == base.digest(target)""",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's North Sea, Africa and Indian Ocean exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the latest reviewed Rafael dialogue. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_baltic_trade", "rafael_north_sea_africa").replace(
    "verified_rafael_north_sea_africa_predecessor", "verified_hodram_baltic_trade_predecessor")

notes = parent.commit_candidate[parent.commit_candidate.index("    DOC.write_text"):
                                parent.commit_candidate.index("    prefix =")]
commit = checked_text(parent.commit_candidate, {
    "Preserve the Baltic trade candidate, staged build and its registered predecessor":
        "Preserve the Rafael dialogue candidate, staged build, predecessor and focused emulator ROMs",
    notes: '''    DOC.write_text(f"""# Rafael's North Sea, Africa and Indian Ocean exchanges

Reviewed 146 records in nine complete exchanges, with 34 wording revisions, four wrap-only revisions and 108 justified retentions. Rafael wonders whether Sera is a princess. Fernan's appointment gift lands as a joke at Rafael's expense, and the crew members keep their distinct responses. Arcadius's visit to Emilio follows Claudio's change of heart. Uddin leaves the location clue and identification of the Rigveda appropriately tentative. [Exact source and registered decisions](../{REVIEW.as_posix()})

Native checks verified all 38 revised pages and six name-width cases. Visual review led to four final refinements. Two initialized emulator excerpts verified 13 revised panels, Fernan's full nameplate, Rafael's surname substitution, the item card, the return to the departure notice after B55 and Julio's follow-up after B58. The other 25 revised panels received offline checks. Natural triggers and hardware remain unverified. [Native and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. These 146 records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)

Block 60's 103 paired records cover the separately branching Spain sequence and its two choices. Rebind those records to this candidate before reviewing the full sequence. [Source pairing](../{stage.review.SOURCE.as_posix()})
""", encoding="utf-8")
''',
}).replace("hodram_baltic_trade", "rafael_north_sea_africa")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
