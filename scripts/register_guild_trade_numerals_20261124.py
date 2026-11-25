"""Register the four source-bound Guild price replies after ordinary Seoul play."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_guild_trade_numeral_release_20261124 as checks
from scripts import register_london_guild_display_20261124 as parent
from scripts import replay_guild_trade_numerals_20261124 as replay
from scripts import stage_guild_trade_numerals_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


files, template = parent.files, parent.template
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-guild-trade-numerals-v1-20261124"
CHECK = "registered_guild_trade_numerals_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_guild_trade_numerals_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = (build.ROOT / name for name in ("release_stack_guild_trade_numerals.json.gz", "ledger_after.json.gz"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = checks.PATCH, checks.REBUILT, checks.PATCH_PROOF, checks.STARTUP_CAPTURE
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_guild_trade_numerals_registered_20261124.md")
CHECKPOINT = "Registered consistent Guild sale, bargaining, and insufficient-funds quotes."
SHEET, PREVIEW = replay.SHEET, build.OUT.with_suffix("") / "portrait_sheet_01.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.OUT)))


verify_source = checked_text(getsource(parent.verify), {
    'len(live["revised"]) == 4 and len(live["unchanged_frames"]) == 18':
        'len(live["revised"]) == 2 and len(live["unchanged_frames"]) == 28',
    'assert len(stored["quote_cases"]) == 201 and stored["price_domain"] == [90, 420000]':
        'assert sum(map(len, stored["quote_cases"].values())) == 812 and set(stored["quote_cases"]) == set(map(str, build.PROSE))\n'
        '    assert {90, 420000} <= set(map(int, stored["quote_cases"]["1072"]))',
    'offset = row["offset"]': 'offset = row["address"] - build.BASE',
    'sorted(build.EDIT)': 'sorted(build.PROSE)',
    'build.exact_row(new_rows': 'build.london.exact_row(new_rows',
    'build.text_reference(new_rows': 'build.london.text_reference(new_rows',
    'Guild_literal_and_price_call_preserve_startup_extent': 'four_Guild_price_calls_preserve_startup_extent',
    'native_price_cases=len(stored["quote_cases"])': 'native_price_cases=sum(map(len, stored["quote_cases"].values()))',
})

old_record_update = parent.prepare[parent.prepare.index('        revised = [row["id"]'):parent.prepare.index('        update = dict(profile=')]
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_yard_numerals_predecessor=predecessor, london_guild_display_release=str(REVIEW)":
        "verified_london_guild_display_predecessor=predecessor, guild_trade_numerals_release=str(REVIEW)",
    "len(batches) == 1125 and len(checks) == 460": "len(batches) == 1126 and len(checks) == 461",
    old_record_update: '''        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert len(revised) == 4 and len(outcome["records"]) == 9
        records[COMMON].extend(ident for ident in revised if ident not in records[COMMON])
        for key in build.PRICE_CALLS:
            branch = f"ARM9_GUILD_PRICE_NUMERALS_{key}"
            assert branch not in records[ARM]
            records[ARM].append(branch)
''',
    'london_guild_display_release_proof=stage.reference(stage.PROOF)': 'guild_trade_numerals_release_proof=stage.reference(stage.PROOF)',
    '"london_guild_display_pipeline"': '"guild_trade_numerals_pipeline"',
    "registered_manifest_entries=1126, passing_release_checks=461, changed_components=2":
        "registered_manifest_entries=1127, passing_release_checks=462, changed_components=2",
    "contextual_records_revisited=7, contextual_decisions_reused=4, previously_localized_records=7":
        "contextual_records_revisited=9, contextual_decisions_reused=5, previously_localized_records=9",
    "prose_revisions=3, justified_retentions=4, text_display_revisions=3": "prose_revisions=4, justified_retentions=5, text_display_revisions=4",
    "ordinary_London_Guild=True, revised_gameplay_holds=4, native_pages=6, unchanged_gameplay_holds=18":
        "ordinary_Seoul_Guild=True, revised_gameplay_holds=2, native_pages=12, unchanged_gameplay_holds=28",
    "prose_revisions=3, wrap_only_revisions=0, texts_retained=4": "prose_revisions=4, wrap_only_revisions=0, texts_retained=5",
    '"london_guild_display_20261124"': '"guild_trade_numerals_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Guild trade numerals testing candidate

The Guildmaster uses regular digits and complete lines in sale and bargaining quotes and the insufficient-funds reply. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered London Guild candidate": "Preserve the registered Guild trade numeral candidate",
    "1,126 entries and 461 passing checks": "1,127 entries and 462 passing checks",
    doc: '''    DOC.write_text(f"""# Guild sale and bargaining quotes

The Guildmaster uses regular digits in the sale offer, both bargaining replies and the insufficient-funds question. Each revision keeps the exact price and the original stage of the transaction. The four new bodies passed 812 native substitution and layout cases across the original price ranges. Five companion turns keep their wording, including the earlier corrected buy offer. [Exact records and five review gates](../{REVIEW.as_posix()}) · [Native previews](../{VERIFY.as_posix()}/{PREVIEW.name})

Ordinary Seoul play verified both answers to the 6,160-coin sale offer. The 7,700-coin purchase, the sale proceeds and the return to town match the registered predecessor. The two revised holds have complete body and nameplate glyphs, and 28 other frames match pixel for pixel. The other three conditional replies have offline coverage. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name})

The candidate passed six startup holds, 462 release checks and 17 focused repository tests. The clean-input patch reconstructs it byte for byte. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    assert args.finish_only or args.visual_sha256
    lineage = [parent]
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 6:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(verify_source + "\n" + prepare + "\n" + finish, __file__ + "::Guild-trade-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
