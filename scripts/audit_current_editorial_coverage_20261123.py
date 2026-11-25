"""Reconcile the current source inventory and carry forward specific regression proofs."""

from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import prepare_all_routes_promotion_20261111 as runtime_contract
from scripts import reconcile_current_route_coverage_20261123 as routes
from scripts import reconcile_current_shared_evidence_20261123 as shared
from scripts import register_rafael_deck_tutorial_followup_20261122 as julio
from scripts import register_regional_rumor_wrap_followups_20261123 as current
from scripts import register_sailing_help_20261120 as help_release
from scripts import register_sailor_stat_labels_20261114 as deck
from scripts import verify_early_setup_current_20261122 as names
from scripts.source_locked_derivation_v5118 import checked_text


base, native = current.base, current.native
OUT = shared.OUT.with_name("current_editorial_coverage_audit_20261123.json")
WRAPS = Path("translations/editorial_checkpoints/hodram_b261_b310_wrap_fixes_20261123/current_wrap_queue.json")
HELP = "/COMMON/HELP.DK4"

runtime_source = checked_text(getsource(runtime_contract.verify_runtime), {
    "assert len(sections) == 6 and sections[NEW_FORMAT][:len(PAYLOAD)] == PAYLOAD":
        "assert sections[NEW_FORMAT][:len(PAYLOAD)] == PAYLOAD",
})
runtime_scope = vars(runtime_contract).copy()
exec(compile(runtime_source, __file__ + "::current-runtime-contract", "exec"), runtime_scope)


def approved_help(original, installed):
    release = base.load(help_release.RELEASE)
    assert base.digest(help_release.ROM) == release["candidate_sha256"]
    older = base.NdsImage.open(help_release.ROM)
    source, active = (image.read_file(HELP) for image in (original, installed))
    assert active == older.read_file(HELP)
    source_blocks, active_blocks = (native.IlnkContainer.parse(data).blocks for data in (source, active))
    assert len(source_blocks) == 202 and len(active_blocks) >= len(source_blocks)
    return dict(clean_topics=len(source_blocks), installed_blocks=len(active_blocks),
        continuations=len(active_blocks) - len(source_blocks), installed_sha256=native.digest(active),
        exact_prior_help_archive=True, most_recent_tested_release=str(help_release.RELEASE))


def deck_dependencies(active, arm):
    release = base.load(deck.RELEASE)
    assert base.digest(deck.ROM) == release["candidate_sha256"]
    reference = base.NdsImage.open(deck.ROM)
    asset = deck.stage.ART
    assert active.read_file(asset) == reference.read_file(asset)
    proof = base.load(deck.STAGED)
    assert len(proof["words"]) == 29
    for word in proof["words"]:
        at = word["offset"]
        assert arm[at:at + 4].hex() == word["after"]
    previous_arm = reference.read_file(deck.stage.ARM)
    spans = ((0x7FA6C, 0x7FB74), (0x80898, 0x808D0), (0x81528, 0x8158C), (0x11964C, 0x1196AC),
             (0x148398, 0x1483B0), (0x148CA8, 0x148CB0))
    assert all(arm[lo:hi] == previous_arm[lo:hi] for lo, hi in spans)
    return dict(verified_repair_words=len(proof["words"]), exact_display_spans=spans,
        asset=asset, asset_sha256=native.digest(active.read_file(asset)),
        prior_release=str(deck.RELEASE), previous_gameplay_only=True, handheld_title_check_open=True)


def julio_dependency(active, arm):
    prior = base.load(julio.RELEASE)
    assert base.digest(julio.ROM) == prior["candidate_sha256"]
    archive, block_number = "/data/SC0.DK4", 43
    reference = base.NdsImage.open(julio.ROM)
    archived, current_block = (native.IlnkContainer.parse(image.read_file(archive)).blocks[block_number]
                              for image in (reference, active))
    assert current_block == archived
    review_path = julio.REVIEW
    review = base.load(review_path)
    row, = [r for r in review["records"] if r["id"] == "DK4_MES_B43_R0017"]
    ref = row["registered_reference"]
    assert all(row["review"].values())
    raw = bytes.fromhex(ref["exact_stored_hex"])
    assert raw.startswith(b"\x06F") and raw[1:].isascii() and raw.count(b"FI") == 1
    at = ref["offset"]
    assert current_block[at:at + len(raw)] == raw
    assert active.read_file("/GRP/KANJI.FNT") == reference.read_file("/GRP/KANJI.FNT")
    return dict(block=block_number, id=row["id"], source_reference=row["source_reference"], installed_reference=ref,
        verified_first_ascii_character="F", given_name_control="FI", block_sha256=native.digest(current_block),
        earlier_review=dict(path=str(review_path),sha256=base.digest(review_path)), previous_gameplay_only=True)


def main():
    assert not OUT.exists()
    release, route, scope, wrap = map(base.load, (current.RELEASE, routes.OUT, shared.OUT, WRAPS))
    candidate = base.digest(current.ROM)
    assert release["candidate_sha256"] == scope["candidate_sha256"] == candidate
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert route["candidate_sha256"] == release["predecessor"]["candidate_sha256"] == wrap["candidate_sha256"]
    assert all("reviewed" in row for row in wrap["records"])
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, installed = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    arm, clean_arm = (image.read_file(current.ARM) for image in (installed, clean))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    for i, path in enumerate(routes.ROUTES):
        assert native.digest(installed.read_file(path)) == route["routes"][path]["installed_archive_sha256"] == release[f"target_SC{i}_sha256"]
    mapped, field, value = (current.scope[name] for name in ("mapped", "field", "value"))
    with mapped(base.LEDGER) as data:
        assert value(data, "current_integrated_candidate", 1)["sha256"] == candidate
        assert not value(data, "full_goal_complete", 1)
        _, lo, hi, _ = field(data, base.CONTEXT, 1)
        keys = [(row["file_path"], row["id"]) for row in value(data, "integrated_record_keys", 2, lo, hi)]
    assert len(keys) == len(set(keys)) == 27700
    counts = Counter(path for path, _ in keys)
    assert {i for p, i in keys if p == HELP} == {f"HELP_TOPIC_{n}" for n in range(202)}
    source = shared.prior.current.stage.workflow.common_message_entries(clean.read_file(current.COMMON), clean_arm)
    active = shared.paired.paired.prior.entries(installed)
    stored_ids = {row.message_id for row in active}
    assert stored_ids == {row.message_id for row in source} == set(range(3668))
    credited = {int(ident.split("_")[-1]) for path, ident in keys if path == current.COMMON}
    assert len(credited) == 3392 and len(stored_ids - credited) == 276
    assert stored_ids - credited == {row["message_ID"] for row in scope["records"]}
    runtime_scope["verify_runtime"](arm, release)
    help_proof = approved_help(clean, installed)
    names_current = FunctionType(names.name_bindings.__code__, names.name_bindings.__globals__ | {"current": current})
    name_proof = names_current(release, clean_arm)
    assert name_proof["original_default_getter_cases"] == 414
    result = dict(candidate_sha256=candidate, ledger_sha256=base.digest(base.LEDGER), unique_historical_credits=len(keys),
        credits_by_asset=dict(counts), inventory=dict(registered_story_source_positions=route["exact_credited_clean_positions"],
            mapped_COMMON=len(stored_ids), credited_COMMON=len(credited), pending_COMMON=len(stored_ids - credited),
            original_Help=help_proof, open_scoped_story_wrap_leads=0),
        default_actor_names=name_proof, regression_checks=dict(Julio=julio_dependency(installed, arm),
            Deck=deck_dependencies(installed, arm), Market_Goods_Info_and_ASCII_right_bound="Current native data and the registered repair words match."),
        evidence={str(p):base.digest(p) for p in (routes.OUT, shared.OUT, WRAPS, current.RELEASE)},
        sampled_gameplay_added=False, other_player_facing_resources_and_conditional_paths_remain_under_review=True,
        new_editorial_credit=0, full_goal_complete=False)
    base.save(OUT, result)
    print(f"Bound {len(keys)} credited records, verified the complete Help archive and 414 default-name getters, "
          "and checked the three reported regressions on the current build.")


if __name__ == "__main__":
    main()
