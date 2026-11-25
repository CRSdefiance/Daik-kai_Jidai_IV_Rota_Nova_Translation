"""Register the complete Hangzhou and Veracruz town dialogue review."""

from pathlib import Path
from types import SimpleNamespace

from scripts import hangzhou_veracruz_trends_20261121 as batch
from scripts import register_havana_calicut_istanbul_trends_20261121 as parent
from scripts import replay_hangzhou_veracruz_trends_20261121 as game
from scripts.source_locked_derivation_v5118 import checked_text


base, native, boot = batch.base, batch.native, parent.boot
review = SimpleNamespace(OUTPUT=batch.OUTPUT, SOURCE=batch.SOURCE, BLOCKS=batch.BLOCKS, ROOT=batch.WORK)
stage = SimpleNamespace(ROM=batch.ROM, ROOT=batch.ROOT, PROOF=batch.PROOF, review=review)
offline, live = SimpleNamespace(PROOF=batch.NATIVE_PROOF), SimpleNamespace(PROOF=game.LIVE)
NATIVE = offline.PROOF
PROFILE = "all-routes-hangzhou-veracruz-trends-v1-20261121"
ROOT = Path("out/hangzhou_veracruz_trends_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Hangzhou_Veracruz_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_hangzhou_veracruz_trends_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_hangzhou_veracruz_trends_registered_20261121.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", batch.WORK / "qa_passed.xml"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CHECKPOINT = "Registered the Hangzhou sake and Veracruz cheese exchanges across all four routes."
ROLE_REASONS = {
    0: "Keep Rafael Castor, the approved name for the speaker who calls after Julio in Rafael's variant.",
    6: "Keep Julio Erneco. His voice and source name belong to both versions of the excited interruption.",
    92: "Barkeep identifies the source role and the speaker who serves the cheese dish.",
    103: "Patron is the source occupation label for the customer who responds to his companion.",
    117: "Port Worker preserves the established source role of Julio's second overheard speaker.",
    119: "Port Worker preserves the source role of the customer who leads the Veracruz exchange.",
    156: "Sailor is the spoken header. Retainer is the separately checked catalogue label.",
}


role_program = checked_text(parent.parent.role_program, {
    'fresh_native_getter_cases=12': 'fresh_native_getter_cases=14',
    '''        names = []
        for old, source in zip(record["current_consumers"], record["clean_ordinary_role_consumers"], strict=True):
            assert old["consumer"] == source["consumer"]''': '''        names = []
        clean_roles = record["clean_ordinary_role_consumers"]
        if clean_roles is None:
            assert ident in {0, 6}
            fields = [f for f in record["clean_actor_table_fields"] if f["field"] in {"primary", "secondary"}]
            for entry in fields:
                field = entry["clean"]
                source_at, source_bytes = field["offset"], bytes.fromhex(field["hex"])
                assert clean[source_at:source_at + len(source_bytes) + 1] == source_bytes + b"\\0"
            source = {"clean_name_fields": fields}
        for i, old in enumerate(record["current_consumers"]):
            if clean_roles is not None:
                source = clean_roles[i]
                assert old["consumer"] == source["consumer"]
                source_at, source_bytes = source["offset"], bytes.fromhex(source["hex"])
                assert clean[source_at:source_at + len(source_bytes) + 1] == source_bytes + b"\\0"''',
    '''            source_bytes = bytes.fromhex(source["hex"])
            source_at = source["offset"]
            assert clean[source_at:source_at + len(source_bytes) + 1] == source_bytes + b"\\0"
''': '',
})
verify_program = checked_text(parent.verify_program, {
    'assert len(viewed) == 8': 'assert len(viewed) == 10',
    'actual["dialogue_tail_only"]': 'actual["speech_fixture"]',
    '== [17, 13, 8]': '== [11, 20]',
    '== 54 and display["exact_retentions"] == 98': '== 49 and display["exact_retentions"] == 76',
    '== 152 and rows.keys()': '== 125 and rows.keys()',
    '{"prose": 52, "wrap": 2, "retention": 98}': '{"prose": 48, "wrap": 1, "retention": 76}',
    'for r in rows.values()) == 38': 'for r in rows.values()) == 31',
    '    validate_natural_dialogue_batch(draft)': '''    macro_rows = {r["file_path"]: r for r in display["receipts"] if "layouts" in r}
    assert len(macro_rows) == 4 and set(macro_rows) == archives.keys()
    assert all(len(r["layouts"]) == 4 and len(r["layouts"][3]["pages"]) == 1 for r in macro_rows.values())
    rafael = macro_rows["/data/SC0.DK4"]
    assert rafael["previous_max_width_midword_break"] == ["What?! ABCDEFGHIJKLMNOP, did you hea", "r that?!"]
    assert rafael["layouts"][3]["lines"] == ["What?! ABCDEFGHIJKLMNOP,", "did you hear that?!"]
    assert rows["/data/SC0.DK4", rafael["id"]]["finding"] == "wrap"
    draft["maximum_given_name_wrap_fix"] = dict(id=rafael["id"], previous=rafael["previous_max_width_midword_break"],
                                                registered=rafael["layouts"][3]["lines"])
    validate_natural_dialogue_batch(draft)''',
})

template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 963 and len(manifest["checks"]) == 298':
        'len(manifest["batches"]) == 964 and len(manifest["checks"]) == 299',
    'release_stack_before_havana_calicut_istanbul_trends.json': 'release_stack_before_hangzhou_veracruz_trends.json',
    'release_stack_with_havana_calicut_istanbul_trends.json': 'release_stack_with_hangzhou_veracruz_trends.json',
    'verified_sofala_malacca_osaka_predecessor=predecessor, havana_calicut_istanbul_trends_release=str(REVIEW)':
        'verified_havana_calicut_istanbul_predecessor=predecessor, hangzhou_veracruz_trends_release=str(REVIEW)',
    'registered_havana_calicut_istanbul_trends_and_complete_parent_inverse':
        'registered_hangzhou_veracruz_trends_and_complete_parent_inverse',
    'manifest["havana_calicut_istanbul_trends_pipeline"]': 'manifest["hangzhou_veracruz_trends_pipeline"]',
    'previously_localized_records=152, new_contextual_records=0, prose_revisions=52, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=98':
        'previously_localized_records=125, new_contextual_records=0, prose_revisions=48, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=76',
    'initialized_Maria_dialogue_panels=38, host_route="Lil", revised_replies_observed=21, dialogue_exits=True':
        'initialized_Maria_dialogue_panels=31, host_route="Lil", revised_replies_observed=16, dialogue_exits=True',
    'ledger["havana_calicut_istanbul_trends_20261121"]': 'ledger["hangzhou_veracruz_trends_20261121"]',
    'prior_records_reviewed=152, initialized_emulator_records=38':
        'prior_records_reviewed=125, initialized_emulator_records=31',
    'prose_revisions=52, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=98, text_display_revisions=0':
        'prose_revisions=48, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=76, text_display_revisions=0',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Hangzhou and Veracruz town dialogue candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised sake and cheese exchanges on all four routes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Hangzhou sake and Veracruz cheese

Reviewed 125 records from both exchanges across all four routes. Hangzhou keeps Julio's two distinct reactions and Rafael's reply. Veracruz restores the matching chewing sounds and the diners' turn from doubt to enthusiasm. The ledger records 48 wording revisions, one wrap-only fix, 76 individually justified retentions and seven verified speaker labels. [Exact references and decisions](../{REVIEW.as_posix()})

All 49 revised pages passed native and visual checks, including the original given-name substitution on four pages. Rafael's original words now keep “did you hear that?!” together with a 16-character given name. Three other versions keep “Admiral” and the substituted name together. The focused emulator test ran all 31 Maria speech commands after Lil's initialized prelude and verified 16 revised panels and both fixture exits. Original town triggers and branch conditions remain outside this replay. Hardware remains untested. [Display and replay evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the ROM exactly. Six startup holds, 24 protected getters and 17 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger still credits 27,700 records and tracks 276 pending shared entries. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(role_program, __file__ + "::roles", "exec"), env)
exec(compile(verify_program, __file__ + "::verify", "exec"), env)
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
