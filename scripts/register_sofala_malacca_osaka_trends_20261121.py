"""Register the reviewed Sofala, Malacca and Osaka scenes over the current ROM."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_sao_jorge_basra_trends_20261121 as parent
from scripts import replay_sofala_malacca_osaka_trends_20261121 as game
from scripts import sofala_malacca_osaka_trends_20261121 as batch
from scripts.source_locked_derivation_v5118 import checked_text


base, native, boot = batch.base, batch.native, parent.boot
review = SimpleNamespace(OUTPUT=batch.OUTPUT, SOURCE=batch.SOURCE, BLOCKS=batch.BLOCKS, ROOT=batch.WORK)
stage = SimpleNamespace(ROM=batch.ROM, ROOT=game.VALIDATION, PROOF=batch.PROOF, review=review)
offline, live = SimpleNamespace(PROOF=batch.NATIVE_PROOF), SimpleNamespace(PROOF=game.LIVE)
NATIVE = offline.PROOF
PROFILE = "all-routes-sofala-malacca-osaka-trends-v1-20261121"
ROOT = Path("out/sofala_malacca_osaka_trends_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Sofala_Malacca_Osaka_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_sofala_malacca_osaka_trends_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_sofala_malacca_osaka_trends_registered_20261121.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", batch.ROOT / "qa_passed.xml"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CHECKPOINT = "Registered the Sofala tea, Malacca almond and Osaka glass exchanges across all four routes."
TEA_RETENTION_FRAME = game.ROOT / "sofala/after/frame_004030_cold_boot.png"
ROLE_REASONS = {
    87: "The source identifies a Square shopkeeper. The role carries through his casual advice in Malacca.",
    130: "Daimyo preserves the Japanese title and fits the collector's authority in the Osaka exchange.",
    150: "Guildmaster preserves the source's recurring occupational label. His deferential replies fit the scene.",
    155: "Sailor matches the spoken nameplate. Retainer preserves the separate full catalogue identity.",
    164: "Man reads naturally as the counterpart to Woman in their shared tea conversation.",
    165: "Woman identifies the speaker without turning her request about their shared tea into a different relationship.",
}


role_program = checked_text(getsource(parent.confirm_roles), {'fresh_native_getter_cases=16': 'fresh_native_getter_cases=12'})
verify_program = checked_text(parent.verify_program, {
    'assert len(viewed) == 8': 'assert len(viewed) == 7',
    '== [14, 25]': '== [9, 16, 11]',
    '== 50 and display["exact_retentions"] == 106': '== 48 and display["exact_retentions"] == 96',
    '== 156 and rows.keys()': '== 144 and rows.keys()',
    '{"prose": 43, "wrap": 7, "retention": 106}': '{"prose": 44, "wrap": 4, "retention": 96}',
    'for r in rows.values()) == 39': 'for r in rows.values()) == 36',
    '    validate_natural_dialogue_batch(draft)': '''    example = actual["cases"]["sofala"]["records"][4]
    assert example["frame"] == 4030 and example["body_change"] is None
    assert Path(example["after"]["path"]) == TEA_RETENTION_FRAME
    assert base.digest(TEA_RETENTION_FRAME) == example["after"]["PNG_sha256"]
    row = rows["/data/SC2.DK4", example["id"]]
    assert row["speaker"] == "Woman" and row["decision"] == "retention"
    assert row["english"] == "Oh, we're almost out of tea. Would you pick some up tomorrow?"
    draft["tea_example_observed"] = example
    validate_natural_dialogue_batch(draft)''',
})
template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 961 and len(manifest["checks"]) == 296':
        'len(manifest["batches"]) == 962 and len(manifest["checks"]) == 297',
    'stage.PROOF, STARTUP, QA, live.PROOF, NATIVE, args.visual_review,':
        'stage.PROOF, STARTUP, QA, live.PROOF, NATIVE, TEA_RETENTION_FRAME, args.visual_review,',
    'release_stack_before_sao_jorge_basra_trends.json': 'release_stack_before_sofala_malacca_osaka_trends.json',
    'release_stack_with_sao_jorge_basra_trends.json': 'release_stack_with_sofala_malacca_osaka_trends.json',
    'verified_seville_stockholm_predecessor=predecessor, sao_jorge_basra_trends_release=str(REVIEW)':
        'verified_sao_jorge_basra_predecessor=predecessor, sofala_malacca_osaka_trends_release=str(REVIEW)',
    'registered_sao_jorge_basra_trends_and_complete_parent_inverse':
        'registered_sofala_malacca_osaka_trends_and_complete_parent_inverse',
    'manifest["sao_jorge_basra_trends_pipeline"]': 'manifest["sofala_malacca_osaka_trends_pipeline"]',
    'previously_localized_records=156, new_contextual_records=0, prose_revisions=43, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=106':
        'previously_localized_records=144, new_contextual_records=0, prose_revisions=44, spacing_revisions=0, wrap_only_revisions=4, justified_retentions=96',
    'initialized_Lil_town_panels=39, revised_replies_observed=11':
        'initialized_Lil_town_panels=36, revised_replies_observed=7',
    'ledger["sao_jorge_basra_trends_20261121"]': 'ledger["sofala_malacca_osaka_trends_20261121"]',
    'prior_records_reviewed=156, initialized_emulator_records=39':
        'prior_records_reviewed=144, initialized_emulator_records=36',
    'prose_revisions=43, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=106, text_display_revisions=0':
        'prose_revisions=44, spacing_revisions=0, wrap_only_revisions=4, justified_retentions=96, text_display_revisions=0',
    '*stage.review.ROOT.rglob("*.nds")]':
        '*stage.ROOT.rglob("*.nds"), *(p for p in stage.review.ROOT.rglob("*.nds") if p.stat().st_size > 512)]',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Sofala, Malacca and Osaka town dialogue candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised tea, almonds and glass exchanges on all four routes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Sofala tea, Malacca almonds and Osaka glass

Reviewed the 36 turns of all three exchanges on each route, with 44 wording revisions, four wrap-only changes and 96 individual retentions. The Sofala scene keeps the shared tea supply and the request for tomorrow. Malacca keeps the claimed effect of the almond remedy in the character's hearsay. Osaka keeps `giyaman` and its Japanese gloss, glass. Twelve native getter calls reconfirmed the six approved speaker labels. [Exact references and decisions](../{REVIEW.as_posix()})

All 48 changed pages passed native and visual checks. Initialized replays of the original Lil commands verified all 36 panels, seven revisions and three scene exits. The Sofala tea request in the user's screenshot displayed the approved **Woman** label. The other routes received offline checks. Ordinary town activation and hardware remain unvisited for this batch. [Tea request frame](../{(VERIFY / TEA_RETENTION_FRAME.name).as_posix()}) · [Display and replay evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the ROM exactly. Six startup holds, 24 protected getters and 17 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger still credits 27,700 records, with 276 shared entries pending. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(role_program, __file__ + "::roles", "exec"), env)
exec(compile(verify_program, __file__ + "::verify", "exec"), env)
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
