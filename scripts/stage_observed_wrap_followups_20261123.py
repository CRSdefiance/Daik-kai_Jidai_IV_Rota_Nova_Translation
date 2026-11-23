"""Install the four observed wrap fixes with the registered dialogue compiler."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import preflight_observed_wrap_followups_20261123 as drafted
from scripts import stage_current_story_wraps_20261122 as compiler
from scripts.source_locked_derivation_v5118 import checked_text


base, native = drafted.base, drafted.native
BATCH = drafted.ROOT.parent / "release"
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight_summary.json"
ROM = ROOT / "Observed_Wrap_Followups_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
CHECKPOINT = drafted.CHECKPOINT
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
registered = drafted.active
parent = SimpleNamespace(ROM=registered.ROM, MANIFEST=registered.MANIFEST, RELEASE=registered.RELEASE,
    STARTUP_CAPTURE=registered.STARTUP_CAPTURE, guard_spec=registered.guard_spec,
    bind_registered_story_percent_guard=registered.bind_registered_story_percent_guard)
PLAN_PROOF = drafted.ROOT / "native_preflight.json"


def author():
    release, preflight = map(base.load, (parent.RELEASE, PLAN_PROOF))
    candidate = base.digest(parent.ROM)
    assert candidate == release["candidate_sha256"] == preflight["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    assert base.digest(drafted.MANUSCRIPT) == preflight["manuscript_sha256"]
    assert all(base.digest(Path(item["path"])) == item["sha256"] for item in preflight["sheets"])
    images = [base.NdsImage.open(path) for path in (native.CLEAN, parent.ROM)]
    records, groups, captions, plans, references = [], [], [], {}, {}
    for item in preflight["records"]:
        archive, ident = item["file_path"], item["id"]
        route, block = int(archive[-5]), item["current_reference"]["block"]
        ordinal = int(ident.rsplit("R", 1)[1])
        _, protection, pages = drafted.CASES[route, block, ordinal]
        assert item["plan"]["expected_native_pages"] == pages
        ledger = Path(item["prior_ledger"])
        assert base.digest(ledger) == item["prior_ledger_sha256"]
        references[ledger.as_posix()] = item["prior_ledger_sha256"]
        history = base.load(ledger)
        group = [r for r in history["records"] if (r["file_path"], r["block"]) == (archive, block)]
        archives = [img.read_file(archive) for img in images]
        archive_hashes = [native.digest(blob) for blob in archives]
        payloads = [native.IlnkContainer.parse(blob).blocks[block] for blob in archives]

        def current_ref(earlier):
            raw_refs = (earlier["source_reference"], earlier["registered_reference"])
            for ref, payload in zip(raw_refs, payloads, strict=True):
                at = ref["command_offset"]
                command = bytes.fromhex(ref["exact_command_hex"])
                assert payload[at:at+len(command)] == command
                assert native.digest(payload) == ref["block_sha256"]
            return raw_refs[1] | dict(archive_sha256=archive_hashes[1], candidate_sha256=candidate)

        revision = None
        for earlier in group:
            r = {key:earlier[key] for key in ("id", "route", "block", "file_path", "Japanese", "speaker", "context",
                                             "source_meaning", "localization_note", "source_reference", "kind", "source_selector")}
            installed = current_ref(earlier)
            selector = bytes([r["source_selector"]]).hex()
            r.update(current_reference=installed, previous_English=earlier["english"], english=earlier["english"],
                source_hex=selector + earlier["source_reference"]["exact_body_hex"],
                current_hex=selector + installed["exact_body_hex"], protected_phrases=[], decision="retention",
                change_class="retention", review=earlier["review"].copy(), prior_registered_review=ledger.as_posix())
            assert all(r["review"].values()) and r["kind"] == "progressive"
            if r["id"] == ident:
                assert r["english"] != item["english"]
                r.update(english=item["english"], change_class="prose", decision="revision", protected_phrases=protection,
                    localization_note={
                        (1,167): "Keep the fleet advice and the exact market-share limit. Give the rule its own page.",
                        (1,216): "Keep the memorial, emotional response and ranking together on one page.",
                        (0,228): "Keep Vivian's address and the island phrase intact before Rafael echoes it.",
                        (0,234): "Keep the battle phrase and hearsay while preserving the crossing and its purpose.",
                    }[route, block])
                r["review"]["formatting"] = False
                revision = r
            records.append(r)
        assert revision is not None and len(group) == item["exchange_source_and_current_commands_verified"]
        labels = history["retained_native_controls"].get("retained_choice_labels", [])
        for label in labels:
            if (label["file_path"], label["block"]) == (archive, block):
                installed = current_ref(label)
                captions.append({k:v for k,v in label.items() if k not in ("registered_reference", "observed_focused")}
                    | dict(current_reference=installed, prior_registered_review=ledger.as_posix()))
        plans[f"{route}/{ident}"] = {"plan":item["plan"]}
        groups.append(dict(route=route, block=block, file_path=archive, context=revision["context"],
            record_ids=[r["id"] for r in group], source_block_sha256=native.digest(payloads[0]),
            current_block_sha256=native.digest(payloads[1])))
    assert len(records) == 77 and len(captions) == 7 and len(groups) == 4
    assert len(plans) == sum(r["decision"] == "revision" for r in records) == 4
    BATCH.mkdir(parents=True, exist_ok=True)
    base.save(REVIEW, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"], groups=groups,
        records=records, retained_choice_labels=captions, counts=dict(prose=4, retention=73), wrap_leads_covered=[],
        exact_prior_registered_reviews=references, manuscripts_sha256={str(drafted.MANUSCRIPT):base.digest(drafted.MANUSCRIPT)},
        original_preflight_sha256=base.digest(PLAN_PROOF), translation_policy="natural-dialogue-v2", target_locale="en-US"))
    base.save(PREFLIGHT, dict(candidate_sha256=candidate, draft_sha256=base.digest(REVIEW), plans=plans, pending=[],
        sheets=preflight["sheets"], source_preflight_sha256=base.digest(PLAN_PROOF)))
    print("Bound 84 previously reviewed texts and four observed wrap revisions to the current candidate.")


def plan(row, selector, current, source):
    packed = base.load(PREFLIGHT)["plans"][f'{row["route"]}/{row["id"]}']["plan"]
    assert packed["logical_English"] == row["english"] and packed["source_selector"] == selector
    assert packed["planning_record"]["source_hex"] == (bytes([selector]) + source).hex()
    assert current.hex() == row["current_reference"]["exact_body_hex"]
    encoded = bytes.fromhex(packed["encoded_hex"])
    assert encoded[:1] == bytes([selector])
    return encoded[1:], packed


compiler_scope = vars(compiler) | globals()
compiler_scope["compilers"] = FunctionType(compiler.compilers.__code__, compiler_scope)
source = checked_text(getsource(compiler.native_display), {
    'plan["expected_native_pages"] == 1': 'plan["expected_native_pages"] in (1,2)',
    '                page, = display.display.raster(current, font, paint, data, lines, 1)\n'
    '                assert page["native_independent_plane_equal"]\n'
    '                pictures.append((f"SC{route} {ident} / {label}", bytes.fromhex(page["native_plane_hex"])))\n'
    '                result["layouts"].append(dict(scope=label, expanded_hex=data.hex(), lines=lines, pages=[page]))':
        '''                pages = display.display.raster(current, font, paint, data, lines, plan["expected_native_pages"])
                for index, page in enumerate(pages, 1):
                    assert page["native_independent_plane_equal"]
                    pictures.append((f"SC{route} {ident} / page {index}", bytes.fromhex(page["native_plane_hex"])))
                result["layouts"].append(dict(scope=label, expanded_hex=data.hex(), lines=lines, pages=pages))''',
})
exec(compile(source, __file__ + "::full-stored-pagination", "exec"), compiler_scope)


def run(action):
    if action == "review":
        author()
    elif action == "stage":
        FunctionType(compiler.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    else:
        inherited = getattr(compiler.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review", "stage", "native_display", "patch", "startup"))
    run(parser.parse_args().action)
