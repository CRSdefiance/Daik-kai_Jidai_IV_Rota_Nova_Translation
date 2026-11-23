"""Register the reviewed item-title corrections over the cumulative Crown build."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_current_item_story_terms_20261119 as game
from scripts import check_current_item_story_term_dispositions_20261119 as terms
from scripts import register_hodram_mihwa_crown_20261119 as parent
from scripts import register_story_short_phrase_wraps_20261119 as template
from scripts import stage_current_item_story_terms_20261119 as stage
from scripts import verify_current_item_story_terms_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base,native=stage.base,stage.native
PROFILE="all-routes-story-item-titles-v1-20261119"
ROOT=Path("out/story_item_titles_registered_20261119_v1")
ROM=ROOT/"Translation_DS_Story_Item_Titles_20261119_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=Path("releases/all_routes_editorial_20261119_story_item_titles_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=Path("docs/editorial_story_item_titles_20261119.md")
STARTUP,QA=game.play.STARTUP_PROOF,stage.ROOT/"supported_qa.xml"
VISUAL_REVIEW=stage.ROOT/"direct_visual_review.json"
CHECKPOINT="Rafael’s two item exchanges and Lil’s stolen-item notices now use the inventory names."
verified=SimpleNamespace(PROOF=offline.PROOF,LIVE=game.PROOF)

verification=checked_text(getsource(template.verify),{
    '    path, = playback["paths"]\n'
    '    assert path["result"] == [0, 1] and len(path["speeches"]) == 16\n'
    '    assert len(path["checked_revisions"]) == playback["revised_pages_verified"] == 6':
        '    assert playback["initialized_fixture"] and playback["normal_return_result"][0] == 0\n'
        '    assert len(playback["speeches"]) == 19 and playback["revised_pages_verified"] == 1',
    'sheets = painter["contact_sheets"] + path["sheets"]':'sheets = painter["contact_sheets"] + playback["sheets"]',
    '    assert len(sheets) == 5 and viewed == {s["path"]: s["sha256"] for s in sheets}':
        '    assert viewed == {s["path"]: s["sha256"] for s in sheets}',
    '[34, 0, 0, 0]':'[22, 0, 0, 0]',
    '    archives = {f"/data/SC{i}.DK4": native.digest(after[f"/data/SC{i}.DK4"]) for i in range(4)}':
        '    archives = {file: native.digest(after[file]) for file in stored["changed_blocks"]}',
    'len(stored["groups"]) == 11 and len(commands) == len(draft["records"]) == 195':
        'len(stored["groups"]) == 3 and len(commands) == len(draft["records"]) == 83',
    'len(revisions) == 19 and len(retentions) == 176':
        'len(revisions) == 12 and len(retentions) == 71\n'
        '    assert sum(r["kind"] == "system-FE" for r in revisions.values()) == 8\n'
        '    item = base.load(terms.OUTPUT)\n'
        '    assert item["candidate_sha256"] == candidate and len(item["revision_bindings"]) == 10\n'
        '    assert len(item["contextual_retentions"]) == 9',
    'seen = set(path["speeches"])':'seen = set(playback["speeches"])',
    'block == 127':'block == 214',
    'shared_storage_scope=prior["shared_storage_scope"])':
        'shared_storage_scope=prior["shared_storage_scope"], item_title_review=item)',
})

publish=parent.main
doc=publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme=publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
evidence=next(line for line in publish.splitlines() if line.startswith("    for source in ("))
main=checked_text(publish,{
    'len(manifest["batches"]) == 911 and len(manifest["checks"]) == 246':
        'len(manifest["batches"]) == 912 and len(manifest["checks"]) == 247',
    "verified_story_market_terms_predecessor":"verified_hodram_mihwa_crown_predecessor",
    "hodram_mihwa_crown":"story_item_titles",
    evidence:'    for source in (stage.PROOF, stage.review.SOURCE, stage.review.OUTPUT, terms.OUTPUT,\n'
             '                   stage.review.ROOT / "block_term_inventory.json", stage.review.ROOT / "short_item_term_followup.json", STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review,',
    "changed_components=1":"changed_components=2",
    "prose_revisions=7, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=11":
        "prose_revisions=12, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=71",
    "text_display_revisions=7":"text_display_revisions=12",
    "name_consistency_revisions=4":"name_consistency_revisions=10",
    "initialized_complete_Hodram_crown_exchange=True":"initialized_complete_Rafael_glassmaking_exchange=True",
    "previously_localized_records=18":"previously_localized_records=83",
    "Preserve Crown dialogue ROM or reconstruction":"Preserve story item title ROM or reconstruction",
    readme:"""    (PACKAGE / "README.md").write_text(f\"\"\"# Story item titles candidate

The [local ROM](../../{ROM.as_posix()}) includes the Glassmaking Guide and Minotaur Axe exchanges and Lil’s revised item-loss notices.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc:"""    DOC.write_text(f\"\"\"# Story item title consistency

Reread 83 records in the complete Rafael Glassmaking Guide and Minotaur Axe exchanges and Lil’s confrontation with Clifford. The batch includes 12 revisions and 71 justified retentions. The names in Rafael’s dialogue and eight notices of stolen items now match the inventory. Lil’s response to the betrayal, the alternate alliance wording and the conditions selecting the notices still follow the original exchanges. [Review ledger](../{REVIEW.as_posix()})

The source-term scan also resolved nine contextual exceptions without changing their text. In the peppercorn joke, the thing the speaker misidentifies turns out to be rabbit droppings. The figurehead rumor keeps “demon statue” until the crew can see what it is. Clear shorthand for the arrow and the two tablet halves also stays. The earlier Crown evidence accounts for eight more short references. [Exact item names and retentions](../{VERIFY.as_posix()}/item_term_dispositions.json)

All four revised dialogue pages and eight revised system notices passed native glyph, wrap, bounds and visual checks. The initialized Rafael replay observed the complete 19-speech Glassmaking Guide exchange, matched the revised name and returned to town. The Minotaur Axe scene and Lil’s conditional notices received offline checks. Natural activation and hardware remain unverified. [Emulator replay](../{VERIFY.as_posix()}/glassmaking_playback_1.png)

The clean-input patch reconstructs the ROM byte for byte. Only three blocks in SC0 and SC2 change. The item table, Help, shared text, the ASCII right-bound correction and all 114 accepted layers carry forward. Six startup holds, 24 protected name getters and 22 focused tests passed. The ledger still credits 27,700 reviews, with 276 shared entries open for classification. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env=template.env|globals()
exec(compile(verification+"\n\n"+main,__file__+"::register","exec"),env)

if __name__=="__main__":
    env["main"]()
