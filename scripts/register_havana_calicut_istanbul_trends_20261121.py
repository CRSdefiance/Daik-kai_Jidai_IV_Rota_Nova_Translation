"""Register the checked Havana, Calicut and Istanbul town scenes."""

from pathlib import Path
from types import SimpleNamespace

from scripts import havana_calicut_istanbul_trends_20261121 as batch
from scripts import register_sofala_malacca_osaka_trends_20261121 as parent
from scripts import replay_havana_calicut_istanbul_trends_20261121 as game
from scripts.source_locked_derivation_v5118 import checked_text


base, native, boot = batch.base, batch.native, parent.boot
review = SimpleNamespace(OUTPUT=batch.OUTPUT, SOURCE=batch.SOURCE, BLOCKS=batch.BLOCKS, ROOT=batch.WORK)
stage = SimpleNamespace(ROM=batch.ROM, ROOT=batch.ROOT, PROOF=batch.PROOF, review=review)
offline, live = SimpleNamespace(PROOF=batch.NATIVE_PROOF), SimpleNamespace(PROOF=game.LIVE)
NATIVE = offline.PROOF
PROFILE = "all-routes-havana-calicut-istanbul-trends-v1-20261121"
ROOT = Path("out/havana_calicut_istanbul_trends_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Havana_Calicut_Istanbul_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_havana_calicut_istanbul_trends_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_havana_calicut_istanbul_trends_registered_20261121.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", batch.WORK / "qa_passed.xml"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CHECKPOINT = "Registered the Havana medicine, Calicut dye and Istanbul tobacco exchanges across all four routes."
ROLE_REASONS = {
    86: "Shopkeeper is the source role and fits his decision about stocking the dye.",
    115: "Port Worker preserves the source role. His familiarity with the other speaker comes through the words.",
    119: "Port Worker identifies the second speaker without implying a position in the household they discuss.",
    153: "Sailor is the spoken role and Retainer is the separate catalogue identity.",
    154: "The sailor can speak familiarly to the shopkeeper. His nameplate follows the source's spoken role.",
    159: "Sailor is the spoken role. The conversation does not give him a position in the household.",
}


verify_program = checked_text(parent.parent.verify_program, {
    'assert actual["initialized_scene"] and not actual["natural_town_trigger"] and not actual["hardware"]':
        'assert actual["initialized_scene"] and not actual["natural_town_trigger"] and not actual["hardware"]\n'
        '    assert actual["dialogue_tail_only"] and actual["original_archive"] == "/data/SC3.DK4"',
    '== [14, 25]': '== [17, 13, 8]',
    '== 50 and display["exact_retentions"] == 106': '== 54 and display["exact_retentions"] == 98',
    '== 156 and rows.keys()': '== 152 and rows.keys()',
    '{"prose": 43, "wrap": 7, "retention": 106}': '{"prose": 52, "wrap": 2, "retention": 98}',
    'group["route"] == 2 and ident in observed': 'group["route"] == 3 and ident in observed',
    'for r in rows.values()) == 39': 'for r in rows.values()) == 38',
})
template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 962 and len(manifest["checks"]) == 297':
        'len(manifest["batches"]) == 963 and len(manifest["checks"]) == 298',
    'stage.PROOF, STARTUP, QA, live.PROOF, NATIVE, TEA_RETENTION_FRAME, args.visual_review,':
        'stage.PROOF, STARTUP, QA, live.PROOF, NATIVE, args.visual_review,',
    'release_stack_before_sofala_malacca_osaka_trends.json': 'release_stack_before_havana_calicut_istanbul_trends.json',
    'release_stack_with_sofala_malacca_osaka_trends.json': 'release_stack_with_havana_calicut_istanbul_trends.json',
    'verified_sao_jorge_basra_predecessor=predecessor, sofala_malacca_osaka_trends_release=str(REVIEW)':
        'verified_sofala_malacca_osaka_predecessor=predecessor, havana_calicut_istanbul_trends_release=str(REVIEW)',
    'registered_sofala_malacca_osaka_trends_and_complete_parent_inverse':
        'registered_havana_calicut_istanbul_trends_and_complete_parent_inverse',
    'manifest["sofala_malacca_osaka_trends_pipeline"]': 'manifest["havana_calicut_istanbul_trends_pipeline"]',
    'previously_localized_records=144, new_contextual_records=0, prose_revisions=44, spacing_revisions=0, wrap_only_revisions=4, justified_retentions=96':
        'previously_localized_records=152, new_contextual_records=0, prose_revisions=52, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=98',
    'initialized_Lil_town_panels=36, revised_replies_observed=7, original_scene_returns=True':
        'initialized_Maria_dialogue_panels=38, host_route="Lil", revised_replies_observed=21, dialogue_exits=True',
    'ledger["sofala_malacca_osaka_trends_20261121"]': 'ledger["havana_calicut_istanbul_trends_20261121"]',
    'prior_records_reviewed=144, initialized_emulator_records=36':
        'prior_records_reviewed=152, initialized_emulator_records=38',
    'prose_revisions=44, spacing_revisions=0, wrap_only_revisions=4, justified_retentions=96, text_display_revisions=0':
        'prose_revisions=52, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=98, text_display_revisions=0',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Havana, Calicut and Istanbul town dialogue candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised medicine, dye and tobacco exchanges on all four routes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Havana medicine, Calicut dyes and Istanbul tobacco

Reviewed all 38 turns of the exchanges on each of the four routes. Havana retains both the claim of a sudden recovery and the speaker's uncertainty about it. Calicut retains the dispute over when to buy dye and the promise of profit in the speaker's own voice. Istanbul retains the familiar peer pressure and the second speaker's stammer. There are 52 wording revisions, two wrap-only changes and 98 individually justified retentions. Twelve native getter calls confirmed six speaker labels. [Exact references and decisions](../{REVIEW.as_posix()})

All 54 revised pages passed native and visual checks. The focused emulator replay placed the original Maria dialogue commands in Lil's initialized opening. It verified all 38 panels, including 21 revisions, and all three dialogue exits. The original pre-dialogue conditions and ordinary town triggers remain outside this replay. The other route copies received offline checks. Hardware remains untested. [Display and replay evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the ROM exactly. Six startup holds, 24 protected getters and 17 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger still credits 27,700 records and tracks 276 pending shared entries. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(parent.role_program, __file__ + "::roles", "exec"), env)
exec(compile(verify_program, __file__ + "::verify", "exec"), env)
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
