"""Register the crew lessons, Sera's introduction, and Hodram's discoveries."""

from pathlib import Path
from types import SimpleNamespace

from scripts import register_hodram_B111_B130_20261122 as parent
from scripts import replay_hodram_B131_B150_20261122 as live
from scripts import verify_hodram_B131_B150_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT,ROM=writer.ROM,PROOF=writer.PROOF,OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B131-B150-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B131_B150_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B131_B150_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B131_B150_candidate")
VERIFY,PATCH = PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE = VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B131_B150_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP,QA,STARTUP_CAPTURE = EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml",live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec,startup_reference = parent.guard_spec,parent.startup_reference
CHECKPOINT = ("Revisited 350 Hodram records across the crew lessons, Camille's apology, Sera's "
              "introduction, and the discoveries. The pass revises 110 lines, aligns one wrap "
              "and corrects three punctuation glyphs, with 236 justified retentions.")
HISTORICAL = Path("translations/hodram_B131_B150_contextual_final_review_v1.json")
native_count = type(parent.native_count)(parent.native_count.__code__,parent.native_count.__globals__ | {"display":display})
observed_count = type(parent.observed_count)(parent.observed_count.__code__,parent.observed_count.__globals__ | {"live":live})
pages_saved = type(parent.pages_saved)(parent.pages_saved.__code__,parent.pages_saved.__globals__ | {"display":display})


def bind_historical_credit(draft):
    old = {r["id"]:r for r in base.load(HISTORICAL)["records"]}
    census_path = writer.paired.pairing.CENSUS
    census = {r["id"]:r for r in base.load(census_path)["records"] if r["block"]==133}
    aliases = {}
    count = 0
    for row in draft["records"]:
        ident = row["id"]
        kind = row["kind"]
        if kind not in ("actor-style","typed-choice-label"):
            continue
        if kind == "actor-style":
            census_record, = census[ident]["exact_credited_source_bindings"]
            legacy_id = census_record["id"]
            assert census_record["source_hex"] == row["source_hex"]
            assert census_record["offset"] == row["source_reference"]["offset"]
            prior = old[legacy_id]
            assert prior["source_style_indices"] == row["native_slots"]
            if ident != legacy_id:
                aliases[ident] = legacy_id
        else:
            prior = old[ident]
            assert row["native_slots"] == [prior["source_reference"]["source_index"]]
            assert prior["kind"] == kind and row["decision"] == "retention" and row["english"] == prior["english"]
            count += 1
        assert prior["source_hex"] == row["source_hex"] and all(prior["review"].values())
        for field in ("offset","command_offset"):
            assert prior["source_reference"][field] == row["source_reference"][field]
    assert len(aliases) == 7 and count == 10
    return dict(prior_review=str(HISTORICAL),prior_sha256=base.digest(HISTORICAL),
                census=str(census_path),census_sha256=base.digest(census_path),by_census_id=aliases)


old_asserts = parent.verification[parent.verification.index('    assert len(playback["holds"])'):
                                parent.verification.index('    assert playback["initialized_excerpts"]')]
glyph = parent.verification[parent.verification.index("    glyphs ="):
                           parent.verification.index('    draft["historical_choice_credit"]')]
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 35 and len(rendered["menus"]) == 5 and len(rendered["style_objects"]) == 8':
        'rendered["FE_panels"] == 23 and len(rendered["menus"]) == 5 and len(rendered["style_objects"]) == 1',
    'rendered["revised_speech_pages"] == 70 and rendered["alternate_name_width_pages"] == 3':
        'rendered["revised_speech_pages"] == 114 and rendered["alternate_name_width_pages"] == 3',
    'sum(len(g["slot_owner_sets"]) for g in rendered["style_objects"]) == 48':
        'sum(len(g["slot_owner_sets"]) for g in rendered["style_objects"]) == 8',
    'draft["contextual_records_revisited"] == 323': 'draft["contextual_records_revisited"] == 350',
    old_asserts: '''    assert len(playback["holds"]) == 66 and len(playback["menus"]) == 10
    assert [(m["block"],m["highlight"]) for m in playback["menus"]] == [
        (block,slot) for block in live.MENU_BLOCKS for slot in range(2)]
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0],live.SERA_NAME[0]}
    assert len(playback["observed_style_owners"]) == 1 and pages_saved() == 2
    assert [(m["block"],m["count"]) for m in rendered["menus"]] == [(b,2) for b in live.MENU_BLOCKS]
''',
    'len(name_check["records"]) == 24': 'len(name_check["records"]) == 17',
    'len(group["commands"]) for group in groups.values()) == 562': 'len(group["commands"]) for group in groups.values()) == 650',
    '== len(draft["records"]) == 323': '== len(draft["records"]) == 350',
    '{"wording": 65, "wrap-only": 3, "glyph": 2, "retention": 253}':
        '{"wording": 110, "wrap-only": 1, "glyph": 3, "retention": 236}',
    'blocks == list(CHANGED) == stored["changed_blocks"][path]':
        'blocks == sorted({row["block"] for row in draft["records"] if row["decision"]=="revision"}) == stored["changed_blocks"][path]',
    glyph: '''    glyphs = [row["id"] for row in draft["records"] if row["change_class"] == "glyph"
              and (row["previous_English"],row["english"]) == ("…","...")]
    assert glyphs == [f"DK4_MES_B137_R{n:04d}" for n in (21,35,74)]
    draft["punctuation_glyph_corrections"] = glyphs
    role = [row for row in draft["records"] if row["english"].startswith(writer.HEAD)]
    assert len(role) == 12 and all(r["source_selector"]==254 for r in role)
    draft["role_caption_revision"] = dict(records=[r["id"] for r in role],source="異国の少女",before="Foreign Girl",after="Girl from Abroad")
''',
    'draft["historical_choice_credit"] = bind_choice_aliases(draft)':
        'draft["historical_source_credit"] = bind_historical_credit(draft)',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1025 and len(checks) == 360': 'len(batches) == 1026 and len(checks) == 361',
    'previously_localized_records=323': 'previously_localized_records=350',
    'contextual_records_revisited=323': 'contextual_records_revisited=350',
    'prior_records_reviewed=323': 'prior_records_reviewed=350',
    'prose_revisions=65': 'prose_revisions=110',
    'justified_retentions=253': 'justified_retentions=236',
    'text_display_revisions=2': 'text_display_revisions=3',
    'punctuation_glyph_corrections=2': 'punctuation_glyph_corrections=3',
    'wrap_only_revisions=3': 'wrap_only_revisions=1',
    'contextual_nameplate_retentions=24': 'contextual_nameplate_retentions=17',
    'actual_menu_samples=9': 'actual_menu_samples=10',
    'actual_style_objects=2': 'actual_style_objects=1',
    'draft["historical_choice_credit"]': 'draft["historical_source_credit"]',
    'name_label_revisions=0': 'name_label_revisions=1',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's next crew lessons, Sera and the discoveries

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed Hodram dialogue and the earlier cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B111_B130","hodram_B131_B150").replace("initialized_Hodram_B111_B130","initialized_Hodram_B131_B150").replace(
    "verified_hodram_B91_B110_predecessor","verified_hodram_B111_B130_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B111_B130_FOCUSED_ONLY.nds': 'Hodram_B131_B150_FOCUSED_ONLY.nds',
    'Preserve the Hodram villages, riddles and sailing candidate': 'Preserve the Hodram crew lessons and Sera candidate',
    notes: '''    DOC.write_text(f"""# Hodram's next crew lessons, Sera and the discoveries

Revisited 350 records from the clean Japanese. This pass revises 110 lines, corrects three punctuation glyphs and fixes one wrap, with 236 individual retentions. The crew lessons still give the original controls and consequences for recruitment, resupply and trade. Camille's three pauses use the ordinary English font. The Guiding Staff notice now keeps the entire Spirit gain on one line for names up to 16 cells. Sera first appears as Girl from Abroad in the original embedded caption and gets her nameplate only when the game reveals her name. Preserve the distinct Rafael and Hodram identities in the tavern encounter. [Exact sources and individual decisions](../{REVIEW.as_posix()})

The native checks cover 650 commands, all eight lookout variants, 23 speakerless panels, ten choice captions, 17 nameplates and {native_count()} revised pages. The focused emulator excerpts verified {observed_count()} dialogue pages, ten menu highlights, the active lookout variant, Sera's name substitutions and nameplate, and the waiting scene's three rows of silence. Two passages now fit on one page. Natural triggers, other conditional paths and hardware remain unvisited. [Native and gameplay evidence](../{VERIFY.as_posix()})

The registered build preserves 114 accepted layers, the ASCII right-bound correction and the inherited name fields. The clean-input patch rebuilt the ROM exactly, and the own-startup comparison and 17 regression tests passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B111_B130","hodram_B131_B150").replace("B111_B130_staged","B131_B150_staged")


scope = parent.scope | globals()
for source in (verification,build,commit):
    exec(compile(source,__file__+"::registered-Hodram-crew-lessons","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

