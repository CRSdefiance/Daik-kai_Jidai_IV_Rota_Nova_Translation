"""Bind and stage the remaining Rafael wrap leads in their complete exchanges."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_mediterranean_followups_20261123 as parent
from scripts import stage_rafael_mediterranean_followups_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established, typed = prior.base, prior.native, prior.established, prior.typed
BATCH = Path(".codex-release-work/rafael_remaining_wraps_20261123/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Remaining_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
CHECKPOINT = Path("translations/editorial_checkpoints/rafael_remaining_wraps_20261123")
QUEUE = prior.CHECKPOINT / "current_wrap_queue.json"
MANUSCRIPTS = (Path(__file__).with_name("rafael_remaining_wraps_20261123.md"),)
PACKETS = {
    "all_routes_editorial_20261121_rafael_B181_B187_candidate": (182, 183, 184, 185, 186),
    "all_routes_editorial_20261122_rafael_B211_B220_candidate": (215, 219),
    "all_routes_editorial_20261122_rafael_B221_B240_candidate": (228, 229, 232, 234, 236, 237, 239),
    "all_routes_editorial_20261118_ruins_clues_and_guides_candidate": (303,),
    "all_routes_editorial_20261118_rafael_mosque_candidate": (318,),
    "all_routes_editorial_20261118_warrior_village_handovers_candidate": (336,),
}
ARCHIVE = prior.ARCHIVE
OVERLAYS = {
    "all_routes_editorial_20261118_story_phrase_continuity_candidate": {303},
    "all_routes_editorial_20261118_ongoing_phrase_wraps_candidate": {318, 336},
}
paired = SimpleNamespace(OUTPUT=CHECKPOINT / "paired_source.json")
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
checkpoint = SimpleNamespace(QUEUE=QUEUE)


def registered_review(package):
    folder = Path("releases") / package
    ledger = folder / "verification/registered_review.json"
    assert base.digest(ledger) == base.load(folder / "checksums.json")["verification/registered_review.json"]
    return ledger, base.load(ledger)["records"]


def package_records():
    overlays = {}
    for package, blocks in OVERLAYS.items():
        path, rows = registered_review(package)
        overlays.update({r["id"]: r | {"later_review": str(path)}
                         for r in rows if r["block"] in blocks and r["file_path"] == ARCHIVE})
    for package, blocks in PACKETS.items():
        ledger, earlier = registered_review(package)
        for block in blocks:
            records = [overlays.pop(r["id"], r) for r in earlier if r["block"] == block and r["file_path"] == ARCHIVE]
            assert records and all(all(r["review"].values()) for r in records)
            yield block, ledger, records
    assert not overlays


def check_previous(row, record, group):
    source, current = row["source_reference"], row["registered_reference"]
    if "exact_command_hex" in current:
        assert current["offset"] == record["current_offset"], record["id"]
        assert source["exact_body_hex"] == record["source_body_hex"]
        assert source["block_sha256"] == group["source_block_sha256"]
        assert current["block_sha256"] == group["current_block_sha256"]
        assert current["exact_command_hex"] == record["current_command_hex"]
    else:
        prefix = bytes([record["selector"]]).hex()
        assert source["exact_stored_hex"] == prefix + record["source_body_hex"], record["id"]
        assert current["exact_stored_hex"] == prefix + record["current_body_hex"], record["id"]


old_bind = getsource(prior.bind)
before = old_bind[old_bind.index('            before, after = old["source_reference"]'):
                  old_bind.index('            record.update(')]
jam = old_bind[old_bind.index('            if record["id"] == "DK4_MES_B176_R0040":'):
               old_bind.index("        groups.append(group)")]
bind_source = checked_text(old_bind, {
    before: '            assert old["id"] == record["id"]\n'
            '            check_previous(old, record, group)\n'
            '            historical_path = old.get("later_review", str(ledger))\n'
            '            if historical_path not in references:\n'
            '                references[historical_path] = base.digest(historical_path)\n'
            '            record["prior_registered_review"] = historical_path\n'
            '            record["prior_registered_offset"] = old["registered_reference"]["offset"]\n',
    jam: "",
    "== 401": "== 335",
    "== 14": "== 19",
    "Bound 401 texts and 14 open wrapping findings": "Bound 335 texts and all 19 remaining Rafael wrap leads",
})
bind_scope = vars(prior) | globals()
exec(compile(bind_source, __file__ + "::bind-prior-and-current", "exec"), bind_scope)

section_scope = prior.section_scope | dict(MANUSCRIPTS=MANUSCRIPTS)
read_revisions = FunctionType(prior.read_revisions.__code__, section_scope)
load_sections = FunctionType(prior.load_sections.__code__, globals())
review_source = checked_text(prior.review_source, {
    'len(records)==401 and not captions and len(leads)==14 and sum(r["kind"]=="system" for r in records)==31':
        'len(records)==335 and not captions and len(leads)==19 and sum(r["kind"]=="system" for r in records)==4',
    "Reconciled Rafael’s eight complete Mediterranean exchanges.":
        "Reconciled Rafael’s 17 complete exchanges with the remaining wrap leads.",
})
review_scope = prior.review_scope | globals()
exec(compile(review_source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_scope = prior.preflight_scope | globals() | dict(ROOT=BATCH)
exec(compile(prior.previous.prototype.prior.preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)

compiler_scope = prior.compiler_scope | globals()
compiler_scope["compilers"] = FunctionType(established.compilers.__code__, compiler_scope)
exec(compile(prior.previous.prototype.stage_source, __file__ + "::stage", "exec"), compiler_scope)
compiler_scope["native_display"] = FunctionType(prior.compiler_scope["native_display"].__code__, compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("bind", "review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "bind":
        bind_scope["bind"]()
    elif action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight_scope["preflight"]()
    elif action in ("stage", "native_display"):
        compiler_scope[action]()
    else:
        operation = getattr(established.release_tools, action)
        FunctionType(operation.__code__, operation.__globals__ | globals())()
