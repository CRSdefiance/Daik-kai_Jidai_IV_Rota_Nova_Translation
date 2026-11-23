"""Verify and stage Rafael's Mediterranean dialogue follow-ups."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_ship_lessons_20261123 as parent
from scripts import stage_rafael_ship_lessons_20261123 as previous
from scripts.pair_rafael_midroute_exchanges_20261122 import ARCHIVE, bind_block
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established, typed = previous.base, previous.native, previous.established, previous.typed
BATCH = Path(".codex-release-work/rafael_mediterranean_followups_20261123/final")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Mediterranean_Followups_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
CHECKPOINT = Path("translations/editorial_checkpoints/rafael_mediterranean_followups_20261123")
MANUSCRIPTS = (Path(__file__).with_name("rafael_mediterranean_followups_20261123.md"),)
QUEUE = CHECKPOINT.with_name("rafael_ship_lessons_20261123") / "current_wrap_queue.json"
PACKETS = {
    "all_routes_editorial_20261121_rafael_B161_B169_candidate": (162, 166, 167, 168),
    "all_routes_editorial_20261121_rafael_B170_B176_candidate": (170, 172, 173),
    parent.PACKAGE.name: (176,),
}
paired = SimpleNamespace(OUTPUT=CHECKPOINT / "paired_source.json")
checkpoint = SimpleNamespace(QUEUE=QUEUE)
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)


def package_records():
    for package, blocks in PACKETS.items():
        path = Path("releases") / package
        ledger = path / "verification/registered_review.json"
        checksums = base.load(path / "checksums.json")
        assert base.digest(ledger) == checksums["verification/registered_review.json"]
        prior = base.load(ledger)
        for block in blocks:
            records = [row for row in prior["records"] if row["block"] == block]
            assert records and all(all(r["review"].values()) for r in records)
            yield block, ledger, records


def bind():
    active, queue = (base.load(path) for path in (parent.RELEASE, QUEUE))
    candidate = base.digest(parent.ROM)
    assert candidate == active["candidate_sha256"] == queue["candidate_sha256"]
    assert base.digest(base.REGISTRY) == active["registry_sha256"]
    assert base.digest(parent.MANIFEST) == active["manifest_sha256"]
    assert base.digest(native.CLEAN) == active["clean_input_sha256"]
    images = [base.NdsImage.open(path) for path in (native.CLEAN, parent.ROM)]
    arms = [image.read_file(native.ARM) for image in images]
    reused_assets = {p: native.digest(images[1].read_file(p)) for p in established.display.ASSETS}
    archives = [image.read_file(ARCHIVE) for image in images]
    archive_hashes = [native.digest(data) for data in archives]
    assert archive_hashes[1] == active["target_SC0_sha256"]
    assert reused_assets[native.ARM] == active["target_ARM9_sha256"]
    banks = [native.IlnkContainer.parse(data).blocks for data in archives]
    inventory, _, _ = native.scoped_inventory()
    groups, references = [], {}
    for number, ledger, earlier in package_records():
        references[str(ledger)] = base.digest(ledger)
        owners = {}
        for row in earlier:
            reference = row["source_reference"]
            ordinal = int(row["id"].rsplit("R", 1)[1])
            assert row.get("source_record_index", ordinal) == ordinal
            owners[reference["offset"]] = row | {"source_reference": reference | {"record_index": ordinal}}
        assert len(owners) == len(earlier)
        leads = {r["offset"]: r for r in queue["records"]
                 if r["file_path"] == ARCHIVE and r["block"] == number and "reviewed" not in r}
        group = bind_block(number, [bank[number] for bank in banks], arms, archive_hashes,
                           owners.copy(), leads, inventory)
        group["prior_registered_review"] = str(ledger)
        for record in group["records"]:
            old = owners[record["source_offset"]]
            before, after = old["source_reference"], old["registered_reference"]
            assert old["id"] == record["id"]
            assert before["block_sha256"] == group["source_block_sha256"]
            assert after["block_sha256"] == group["current_block_sha256"]
            assert before["exact_body_hex"] == record["source_body_hex"]
            assert after["exact_command_hex"] == record["current_command_hex"]
            assert after["offset"] == record["current_offset"]
            record.update(prior_source_meaning=old["source_meaning"], prior_localization_note=old["localization_note"],
                          prior_context=old["context"])
            if record["id"] == "DK4_MES_B176_R0040":
                rows = [" ".join(row.split()) for row in record["current_English"].splitlines()]
                assert rows[-2].endswith("abandoned! True") and rows[-1].startswith("story.")
                assert not any(lead["id"] == record["id"] for lead in group["open_wrap_leads"])
                group["open_wrap_leads"].append(dict(
                    id=record["id"], offset=record["current_offset"], finding="The final two rows split True story.",
                    rows=rows,
                ))
        groups.append(group)
    assert sum(len(g["records"]) for g in groups) == 401
    assert sum(len(g["open_wrap_leads"]) for g in groups) == 14
    paired.OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    assert not paired.OUTPUT.exists()
    base.save(paired.OUTPUT, dict(candidate_sha256=candidate, clean_sha256=active["clean_input_sha256"],
        profile=active["profile"], groups=groups, wrap_queue_sha256=base.digest(QUEUE),
        exact_prior_registered_reviews=references, current_runtime_assets=reused_assets, new_review_credit=0))
    print("Bound 401 texts and 14 open wrapping findings to the clean and registered bytes.")


section_scope = previous.section_scope | dict(MANUSCRIPTS=MANUSCRIPTS)
read_revisions = FunctionType(previous.original_sections.__code__, section_scope)


def load_sections():
    revised = read_revisions()
    sections = {}
    for group in base.load(paired.OUTPUT)["groups"]:
        route, block = group["route"], group["block"]
        context, edits = revised.pop((route, block))
        decisions = {}
        for row in group["records"]:
            key = row["source_record_index"]
            assert row["native_command_word"] == 0x4000 and key not in decisions
            decisions[key] = edits.pop(key, [
                row["prior_source_meaning"], "", "", row["prior_localization_note"],
            ])
        assert not edits
        sections[route, block] = context, decisions
    assert not revised
    return sections


review_source = checked_text(previous.review_source, {
    'len(records)==209 and len(captions)==8 and len(leads)==11 and sum(r["kind"]=="system" for r in records)==1':
        'len(records)==401 and not captions and len(leads)==14 and sum(r["kind"]=="system" for r in records)==31',
    '        lateen_refinement_preflight={str(LATEEN):base.digest(LATEEN)},':
        '        exact_prior_registered_reviews=packet["exact_prior_registered_reviews"],',
    'Reviewed 217 texts across the five Rafael recruitment and lesson exchanges.':
        'Reconciled Rafael’s eight complete Mediterranean exchanges.',
})
review_scope = previous.review_scope | globals()
exec(compile(review_source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_scope = previous.preflight_scope | globals() | dict(ROOT=BATCH)
exec(compile(previous.prototype.prior.preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)

compiler_scope = previous.compiler_scope | globals()
compiler_scope["compilers"] = FunctionType(established.compilers.__code__, compiler_scope)
exec(compile(previous.prototype.stage_source, __file__ + "::stage", "exec"), compiler_scope)
compiler_scope["native_display"] = FunctionType(previous.compiler_scope["native_display"].__code__, compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("bind", "review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "bind":
        bind()
    elif action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight_scope["preflight"]()
    elif action in ("stage", "native_display"):
        compiler_scope[action]()
    else:
        operation = getattr(established.release_tools, action)
        FunctionType(operation.__code__, operation.__globals__ | globals())()
