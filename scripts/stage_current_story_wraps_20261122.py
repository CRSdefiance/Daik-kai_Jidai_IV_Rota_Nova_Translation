"""Install the reviewed story wraps and verify the stored native pages."""

from argparse import ArgumentParser
from collections import Counter
from inspect import getsource
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile

from scripts import review_current_story_wraps_20261122 as review
from scripts import stage_rafael_deck_tutorial_followup_20261122 as release_tools
from scripts import stage_story_tag_wraps_20261118 as exact
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
display, layout = review.display, review.layout
ROOT = review.ROOT / "staged"
ROM = ROOT / "Early_Story_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"


def plan(row, selector, current, source):
    if row["route"] == 3 and row["id"] == "DK4_MES_B31_R0071":
        row = row | {"protected_phrases": [*row["protected_phrases"], "Damn it,"]}
    return layout.plan_progressive(row, selector, current, source)


def compilers():
    code = checked_text(getsource(exact.rebuild_function), {
        '"plan_progressive": precedent.plan_progressive': '"plan_progressive": plan',
        '        if (rows[0]["route"], rows[0]["block"]) == (0, 84):\n'
        '            return fit_training_offer(rows, source, current, inventory, arm)\n': '',
    })
    scope = exact.rebuild_function.__globals__ | {"plan": plan}
    exec(compile(code, __file__ + "::selected-command-compiler", "exec"), scope)
    fit = exact.fit_training_offer
    in_place = FunctionType(fit.__code__, fit.__globals__ | {"precedent": SimpleNamespace(plan_progressive=plan)})
    return scope["rebuild_function"](), in_place


def stage():
    assert not ROOT.exists()
    draft, preflight, release = map(base.load, (review.REVIEW, review.PREFLIGHT, parent.RELEASE))
    assert not preflight["pending"] and base.digest(review.REVIEW) == preflight["draft_sha256"]
    assert base.digest(parent.ROM) == draft["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"]
    assert base.digest(native.CLEAN) == draft["clean_sha256"] == release["clean_input_sha256"]
    original, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    before = native.files(target)
    arm, clean_arm = before[native.ARM], original.read_file(native.ARM)
    inventory, _, _ = native.scoped_inventory()
    rebuild, in_place = compilers()
    records = {(r["file_path"], r["id"]): r for r in draft["records"]}
    groups, archive_hashes = [], {}
    for path in sorted({r["file_path"] for r in draft["records"]}):
        bank = native.IlnkContainer.parse(before[path])
        source = native.IlnkContainer.parse(original.read_file(path))
        for group in (g for g in draft["groups"] if g["file_path"] == path):
            n, route = group["block"], group["route"]
            rows = [records[path, ident] for ident in group["record_ids"]]
            assert all(all(passed for gate, passed in r["review"].items() if gate != "formatting") for r in rows)
            revised_rows = [r for r in rows if r["decision"] == "revision"]
            if not revised_rows:
                continue
            old, clean = bank.blocks[n], source.blocks[n]
            assert native.digest(old) == group["current_block_sha256"]
            assert native.digest(clean) == group["source_block_sha256"]
            if (route, n) == (0, 84):
                new, commands, plans = in_place(revised_rows, clean, old, inventory, arm)
            else:
                new, commands, plans = rebuild(rows, clean, old, inventory, clean_arm, arm, None)
            assert new != old and plans.keys() == {r["id"] for r in revised_rows}
            for ident, planned in plans.items():
                planned_rows = preflight["plans"][f"{route}/{ident}"]["plan"]["lines"]
                if (route, ident) != (3, "DK4_MES_B31_R0071"):
                    assert planned["lines"] == planned_rows
            after = native.digest(new)
            groups.append(group | dict(after=after, commands=commands, plans=plans))
            bank.blocks[n] = new
        packed = bank.to_bytes()
        assert {n for n, (old, new) in enumerate(zip(native.IlnkContainer.parse(before[path]).blocks, bank.blocks,
                                                    strict=True)) if old != new} == {g["block"] for g in groups if g["file_path"] == path}
        target.replace_file(path, packed)
        archive_hashes[path] = native.digest(packed)
    final = native.files(target)
    assert final.keys() == before.keys() and {p for p in before if before[p] != final[p]} == archive_hashes.keys()
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(original), final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    result = bytes(target.rom.save())
    for path in archive_hashes:
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    base.save(PROOF, dict(candidate_sha256=native.digest(result), predecessor_sha256=release["candidate_sha256"],
        clean_sha256=release["clean_input_sha256"], draft_sha256=base.digest(review.REVIEW), groups=groups,
        archive_hashes=archive_hashes, unchanged_ARM9_sha256=native.digest(arm), source25=guard, whole_parent_inverse=True))
    print(f"Staged {len(preflight['plans'])} revisions in {len(groups)} blocks. {native.digest(result)}", flush=True)


def native_display():
    assert not NATIVE.exists()
    stored, draft, release = map(base.load, (PROOF, review.REVIEW, parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(ROM) and stored["draft_sha256"] == base.digest(review.REVIEW)
    assert stored["predecessor_sha256"] == release["candidate_sha256"] and stored["whole_parent_inverse"]
    current = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    hodram = display.contexts.hodram_context()
    routes = {1: hodram, 3: current}
    expand = display.original_expander()
    names = {}
    for route in routes:
        cases = routes[route].execute(expand, b"FI FA FO", route)["cases"]
        expanded, = {b["output_hex"] for b in cases}
        assert len(cases) == 4
        given, surname, company = bytes.fromhex(expanded).decode("ascii").split(" ", 2)
        assert given == {1: "Hodram", 3: "Maria"}[route]
        names[route] = dict(FI=given, FA=surname, FO=company)
    image = base.NdsImage.open(ROM)
    assert all(current.image.read_file(asset) == image.read_file(asset) for asset in display.ASSETS)
    arm_base = 0x02000000
    latest_sections = MainCodeFile(current.arm, arm_base).sections
    from scripts import generic_name_macro_owned_v5886b as original_macro

    macro_source = checked_text(getsource(original_macro.expand), {
        "assert identity==prefix and captain==2": "assert identity==prefix and captain in (1,3)",
        "current_executed_instruction_addresses=len(provider.executed_current)":
            "executed_addresses=sorted(provider.executed_current)",
    })
    env = vars(original_macro).copy()
    exec(compile(macro_source, __file__ + "::address-bound-substitutions", "exec"), env)
    paint = display.clipped_renderer(current)
    font = image.read_file("/GRP/KANJI.FNT")
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    banks = {path: native.IlnkContainer.parse(image.read_file(path)) for path in stored["archive_hashes"]}
    names_pattern = exact.precedent.review.TOKEN
    pictures, checked = [], []
    for group in stored["groups"]:
        path, route, block = (group[k] for k in ("file_path", "route", "block"))
        payload = banks[path].blocks[block]
        assert native.digest(payload) == group["after"]
        for command in (c for c in group["commands"] if c["record_ids"]):
            ident, = command["record_ids"]
            row = rows[path, ident]
            start, raw = command["stored_offset"], bytes.fromhex(command["stored"])
            assert payload[start:start + len(raw)] == raw
            assert raw[:6] == bytes.fromhex(row["current_reference"]["exact_command_hex"])[:6]
            stop = raw.index(0, 6)
            assert not any(raw[stop:])
            body = raw[6:stop]
            result = dict(id=ident, route=route, file_path=path, block=block, command_offset=start,
                          exact_command_hex=raw.hex(), body_hex=raw[5:stop].hex(), layouts=[])
            if ident not in group["plans"]:
                assert row["decision"] == "retention" and raw.hex() == row["current_reference"]["exact_command_hex"]
                checked.append(result)
                continue
            plan = group["plans"][ident]
            assert row["decision"] == "revision" and plan["expected_native_pages"] == 1
            assert raw[5:stop].rstrip(b" ") == bytes.fromhex(plan["encoded_hex"])
            assert " ".join(body.decode("ascii").split()) == row["english"]
            before = bytes.fromhex(row["current_hex"])[1:].decode("ascii")
            tokens = names_pattern.findall(body.decode("ascii"))
            assert tokens == names_pattern.findall(before)
            assert b"%" not in body
            layouts = [("no substitutions", {}, body)]
            if tokens:
                scope = routes[route]
                expansion = scope.execute(env["expand"], body, raw[5])
                encoded = expansion["cases"]
                if route == 1:
                    for address in expansion["executed_addresses"]:
                        old, = [s for s in scope.sections if s.ramAddress <= address < s.ramAddress + len(s.data)]
                        expected_section = [s for s in latest_sections if s.ramAddress <= address < s.ramAddress + len(s.data)]
                        if not expected_section:
                            expected_section = [s for s in current.sections if s.ramAddress <= address < s.ramAddress + len(s.data)]
                        new, = expected_section
                        a, b = address - old.ramAddress, address - new.ramAddress
                        assert old.data[a:a+4] == new.data[b:b+4], hex(address)
                expected = names_pattern.sub(lambda m: names[route][m[0]], body.decode("ascii")).encode("ascii")
                assert len(encoded) == 4 and {b["output_hex"] for b in encoded} == {expected.hex()}
                result["substitution"] = dict(execution=expansion, route_snapshot=scope.receipt())
                layouts = [("registered default", names[route], expected)]
                widest = {"FI": "W" * 16, "FA": "W" * 16, "FO": "W" * 20}
                widest_body = names_pattern.sub(lambda m: widest[m[0]], body.decode("ascii")).encode("ascii")
                layouts.append(("maximum widths", widest, widest_body))
            for label, expanded_names, data in layouts:
                lines = [display.display.expected(t, expanded_names) for t in plan["lines"]]
                page, = display.display.raster(current, font, paint, data, lines, 1)
                assert page["native_independent_plane_equal"]
                pictures.append((f"SC{route} {ident} / {label}", bytes.fromhex(page["native_plane_hex"])))
                result["layouts"].append(dict(scope=label, expanded_hex=data.hex(), lines=lines, pages=[page]))
            checked.append(result)
    assert sum(bool(r["layouts"]) for r in checked) == sum(len(g["plans"]) for g in stored["groups"])
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(NATIVE, dict(candidate_sha256=stored["candidate_sha256"], stage_sha256=base.digest(PROOF),
        records=checked, sheets=sheets, default_names=names, pages=len(pictures), offline_native_only=True,
        counts=dict(Counter(rows[r["file_path"], r["id"]]["change_class"] for r in checked))))
    print(f"Complete stored body and native glyph checks passed for {len(pictures)} pages.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action in ("patch", "startup"):
        inherited = getattr(release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
    else:
        globals()[action]()
