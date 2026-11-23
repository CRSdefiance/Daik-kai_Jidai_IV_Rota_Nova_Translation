"""Register the verified complete Sao Jorge and Basra town exchanges."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_seville_stockholm_trends_20261121 as parent
from scripts import replay_sao_jorge_basra_trends_20261121 as game
from scripts import sao_jorge_basra_trends_20261121 as batch
from scripts.source_locked_derivation_v5118 import checked_text


base, native, boot = batch.base, batch.native, parent.boot
review = SimpleNamespace(OUTPUT=batch.OUTPUT, SOURCE=batch.SOURCE, BLOCKS=batch.BLOCKS, ROOT=batch.WORK)
stage = SimpleNamespace(ROM=batch.ROM, ROOT=batch.ROOT, PROOF=batch.PROOF, review=review)
offline, live = SimpleNamespace(PROOF=batch.NATIVE_PROOF), SimpleNamespace(PROOF=game.LIVE)
NATIVE = offline.PROOF
PROFILE = "all-routes-sao-jorge-basra-trends-v1-20261121"
ROOT = Path("out/sao_jorge_basra_trends_registered_20261121_v1")
ROM = ROOT / "Translation_DS_Sao_Jorge_Basra_Trends_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_sao_jorge_basra_trends_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_sao_jorge_basra_trends_registered_20261121.md")
STARTUP, QA = (stage.ROOT / name for name in ("own_startup_verification.json", "qa_passed.xml"))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
CHECKPOINT = "Registered the Sao Jorge wine and Basra artwork exchanges across all four routes."
ACTORS = batch.OUTPUT.with_name("actor_name_inventory_current_v1.json")
CURRENT_NAMES = batch.OUTPUT.with_name("default_actor_names_current_20261120_v1.json")
ROLE_REASONS = {
    85: "The Square shopkeeper handles the art sales and complains after his customers leave.",
    92: "The tavernkeeper answers the drink order, so Barkeep suits the exchange.",
    96: "The Japanese identifies a tavern customer, which Patron conveys in the nameplate.",
    110: "The Japanese identifies the man from the shipyard. Buying art does not give him a new occupation.",
    132: "Officiant preserves the approved title for the person who presides over rites.",
    148: "The Japanese title identifies the head of a guild. Guildmaster is the established role label.",
    152: "Sailor is the original spoken nameplate identity. The separate catalog identity remains Retainer.",
    153: "Sailor is the original spoken nameplate identity. The separate catalog identity remains Retainer.",
}


def confirm_roles(draft):
    evidence = base.load(ACTORS)
    names_by_actor = {r["actor_ID"]: r for r in base.load(CURRENT_NAMES)["source_and_current_default_name_fields"]}
    clean, target = [base.NdsImage.open(p).read_file(native.ARM) for p in (native.CLEAN, stage.ROM)]
    assert native.digest(clean) == evidence["clean_ARM9_sha256"]
    startup = base.load(STARTUP)
    assert startup["candidate_sha256"] == draft["candidate_sha256"]
    _, ram = boot.checked_report(STARTUP_CAPTURE, startup["candidate_sha256"], boot.START_FRAMES[-1])
    cpu, get = boot.tavern.get_machine(target, ram)
    root = get(0xCB184)
    selectors = {r["source_selector"] for r in draft["records"]} - {254}
    assert selectors == ROLE_REASONS.keys()
    checked = []
    for record in evidence["records"]:
        ident = record["actor_ID"]
        if ident not in selectors:
            continue
        current = names_by_actor[ident]
        actor = root + 4 + 32 * ident
        names = []
        for old, source in zip(record["current_consumers"], record["clean_ordinary_role_consumers"], strict=True):
            assert old["consumer"] == source["consumer"]
            field = "progressive_nameplate" if old["consumer"] == "progressive-nameplate" else "full_catalogue"
            approved = current[field]
            pointer = get(old["getter"] - boot.BASE, actor)
            expected = approved.encode("ascii")
            assert bytes(cpu.mem_read(pointer, len(expected) + 1)) == expected + b"\0"
            source_bytes = bytes.fromhex(source["hex"])
            source_at = source["offset"]
            assert clean[source_at:source_at + len(source_bytes) + 1] == source_bytes + b"\0"
            if old["consumer"] == "progressive-nameplate":
                rows = [d for d in draft["records"] if d["source_selector"] == ident]
                assert {d["speaker"] for d in rows} == {old["text"]}
                for row in rows:
                    row["speaker"] = approved
            names.append(dict(consumer=old["consumer"], clean=source,
                              registered=dict(pointer=pointer, getter=old["getter"], text=approved,
                                              text_hex=expected.hex())))
        assert len(names) == 2
        checked.append(dict(actor_ID=ident, actor_object=actor, names=names, decision="retention",
                            reason=ROLE_REASONS[ident]))
    assert len(checked) == len(selectors)
    return dict(records=checked, source_inventory=str(ACTORS), source_inventory_sha256=base.digest(ACTORS),
                current_inventory=str(CURRENT_NAMES), current_inventory_sha256=base.digest(CURRENT_NAMES),
                startup_evidence_sha256=base.digest(STARTUP), fresh_native_getter_cases=16)


verify_program = checked_text(getsource(parent.verify), {
    'assert len(viewed) == 5': 'assert len(viewed) == 8',
    '== [10, 8]': '== [14, 25]',
    '== 26 and display["exact_retentions"] == 46': '== 50 and display["exact_retentions"] == 106',
    '== 72 and rows.keys()': '== 156 and rows.keys()',
    '{"prose": 23, "wrap": 3, "retention": 46}': '{"prose": 43, "wrap": 7, "retention": 106}',
    'for r in rows.values()) == 18': 'for r in rows.values()) == 39',
    '    validate_natural_dialogue_batch(draft)\n': '',
    '    return stored, draft, archives': '    draft["speaker_nameplate_review"] = confirm_roles(draft)\n'
                                        '    validate_natural_dialogue_batch(draft)\n    return stored, draft, archives',
})
template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index("    DOC.write_text"):template.index("    prefix =")]
program = checked_text(template, {
    'len(manifest["batches"]) == 960 and len(manifest["checks"]) == 295':
        'len(manifest["batches"]) == 961 and len(manifest["checks"]) == 296',
    'release_stack_before_seville_stockholm_trends.json': 'release_stack_before_sao_jorge_basra_trends.json',
    'release_stack_with_seville_stockholm_trends.json': 'release_stack_with_sao_jorge_basra_trends.json',
    'verified_early_wrap_predecessor=predecessor, seville_stockholm_trends_release=str(REVIEW)':
        'verified_seville_stockholm_predecessor=predecessor, sao_jorge_basra_trends_release=str(REVIEW)',
    'registered_seville_stockholm_trends_and_complete_parent_inverse':
        'registered_sao_jorge_basra_trends_and_complete_parent_inverse',
    'manifest["seville_stockholm_trends_pipeline"]': 'manifest["sao_jorge_basra_trends_pipeline"]',
    'previously_localized_records=72, new_contextual_records=0, prose_revisions=23, spacing_revisions=0, wrap_only_revisions=3, justified_retentions=46':
        'previously_localized_records=156, new_contextual_records=0, prose_revisions=43, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=106',
    'initialized_Lil_town_panels=18, revised_replies_observed=4':
        'initialized_Lil_town_panels=39, revised_replies_observed=11',
    'ledger["seville_stockholm_trends_20261121"]': 'ledger["sao_jorge_basra_trends_20261121"]',
    'prior_records_reviewed=72, initialized_emulator_records=18':
        'prior_records_reviewed=156, initialized_emulator_records=39',
    'prose_revisions=23, spacing_revisions=0, wrap_only_revisions=3, justified_retentions=46, text_display_revisions=0':
        'prose_revisions=43, spacing_revisions=0, wrap_only_revisions=7, justified_retentions=106, text_display_revisions=0',
    readme: r'''    (PACKAGE / "README.md").write_text(f"""# Sao Jorge and Basra town dialogue candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised Sao Jorge and Basra town scenes on all four routes. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\n")
''',
    doc: r'''    DOC.write_text(f"""# Sao Jorge wine and Basra artwork

Reviewed all 39 turns of the two scenes in each storyline. The wine exchange preserves the drinkers' banter and the skeptic's second order. The Basra exchange preserves the art buyers' competing opinions and the shopkeeper's change from courtesy to frankness after they leave. There are 43 wording revisions, seven wrap-only changes and 106 justified retentions. Sixteen original getter checks reconfirmed the eight source-bound role labels. [Exact references and decisions](../{REVIEW.as_posix()})

All 50 revised pages passed native and visual review. Paired emulator replays of the original commands on Lil's route verified all 39 panels, including 11 revisions, and both scene exits. Ordinary town activation and hardware remain unvisited in this batch. The three other route copies received offline checks. [Display and replay evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the ROM byte for byte. Six startup holds, 24 protected getters and 17 focused tests passed. The 114 accepted layers and the ASCII right-bound correction carry forward. The ledger remains at 27,700 credited records and 276 shared entries pending. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
''',
})
env = parent.env | globals()
exec(compile(verify_program, __file__ + "::verify", "exec"), env)
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
