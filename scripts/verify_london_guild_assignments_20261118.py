"""Check each revised guild page, its original text consumer, and name expansion."""

from inspect import getsource
from types import FunctionType

from scripts import generic_name_macro_owned_v5886b as original
from scripts import stage_london_guild_assignments_20261118 as build
from scripts import verify_forest_expeditions_20261118 as inherited
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR = build.ROOT.with_name("research_v3") / ROOT.name / PROOF.name


def expander():
    source = checked_text(getsource(original.expand), {
        "assert identity==prefix and captain==2":
            "assert captain == 3 and (0 <= identity < 207 if 207 <= prefix < 224 else identity == prefix)",
    })
    env = vars(original).copy()
    exec(compile(source, __file__ + "::registered-original-macro-ABI", "exec"), env)
    return env["expand"]


def current_names(ctx):
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    player = get(0xCB184) + 0x19E4
    memory = bytes(cpu.mem_read(0x02000000, 0x400000))
    vtable = int.from_bytes(cpu.mem_read(player, 4), "little")
    names = {}
    for macro, slot in (("FI", 0x20), ("FA", 0x24)):
        address = int.from_bytes(cpu.mem_read(vtable + slot, 4), "little")
        pointer = get(address - 0x02000000, player)
        name = bytes(cpu.mem_read(pointer, 17)).split(b"\0", 1)[0]
        assert 1 <= len(name) <= 16 and name.isascii()
        names[macro] = name.decode("ascii")
    assert bytes(cpu.mem_read(0x02000000, 0x400000)) == memory
    assert names == {"FI": "Maria", "FA": "Li"}
    ctx.calls.clear()
    return names


def expected(template, macro_names):
    for symbol, name in macro_names.items():
        template = template.replace("{MACRO:" + symbol + "}", name)
    return template


def raster(ctx, font, paint, text, lines, num_pages):
    rendered = paint(ctx.arm, font, text)
    assert rendered["complete_consumed_bytes"] == len(text)
    pages = rendered["pages"]
    assert len(pages) == num_pages and pages[0]["first_visible_origin"] == [0, 0]
    assert [line for page in pages for line in inherited.visible_lines(page)] == lines
    return pages


def paragraph(ctx, font, paint, expand, fe_paint, names, row, raw, plan):
    selector, body = raw[0], raw[1:]
    compiled = bytes.fromhex(plan["encoded_hex"])
    assert compiled[:1] == raw[:1] and raw in (compiled, compiled + b" ")
    assert build.review.logical(body.decode("ascii")) == row["english"]
    if selector == 254:
        result = inherited.validate_paragraph(ctx, font, paint, expand, fe_paint, row, raw, plan)
        return result | {"layouts": [{"scope": "original FE", "pages": result["pages"]}]}
    tokens = set(build.review.TOKEN.findall(row["english"]))
    regular = {macro: names[macro] for macro in tokens}

    def substitute(raw_body, values):
        return build.review.TOKEN.sub(lambda match: values[match[0]], raw_body.decode("ascii")).encode("ascii")

    expansion = ctx.execute(expand, body, selector)
    actual = substitute(body, regular)
    assert len(expansion["cases"]) == 4 and all(c["output_hex"] == actual.hex() for c in expansion["cases"])
    assert all(c["original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact"] for c in expansion["cases"])
    stress = tuple((f"offline {n}-cell name", {macro: example for macro in tokens})
                   for n, example in ((1, "I"), (15, "ABCDEFGHIJKLMNO"), (16, "ABCDEFGHIJKLMNOP"))) if tokens else ()
    layouts = []
    for scope, used in (("registered default", regular), *stress):
        text = substitute(body, used)
        lines = [expected(line, used) for line in plan["lines"]]
        pages = raster(ctx, font, paint, text, lines, plan["expected_native_pages"])
        if compiled != raw:
            reference = raster(ctx, font, paint, substitute(compiled[1:], used), lines, len(pages))
            assert [p["native_plane_hex"] for p in pages] == [p["native_plane_hex"] for p in reference]
        layouts.append(dict(scope=scope, names=used, expanded_hex=text.hex(), lines=lines, pages=pages))
    return dict(id=row["id"], file_path=row["file_path"], kind=row["kind"], stored_hex=raw.hex(),
                macro_alignment_checks=expansion, layouts=layouts)


def main():
    assert not ROOT.exists()
    proof, manuscript, release = map(base.load, (build.PROOF, build.review.OUTPUT, parent.RELEASE))
    assert proof["whole_parent_inverse"] and proof["candidate_sha256"] == base.digest(build.ROM)
    assert proof["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    previous = base.load(PRIOR)
    prior_stage_path = PRIOR.parent.parent / build.PROOF.name
    prior_stage = base.load(prior_stage_path)
    assert previous["stage_proof_sha256"] == base.digest(prior_stage_path)
    assert prior_stage["predecessor_sha256"] == proof["predecessor_sha256"]
    reusable = {(r["file_path"], r["id"]): r for r in previous["checked_records"]}
    image = base.NdsImage.open(build.ROM)
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    font = image.read_file("/GRP/KANJI.FNT")
    assert font == ctx.image.read_file("/GRP/KANJI.FNT") and image.read_file(native.ARM) == ctx.arm
    _, paint = inherited.early.prior.precedent.planners(ctx.arm)
    fe_paint = stage.system.native_painter(ctx)
    names, expand = current_names(ctx), expander()
    roles = inherited.validate_roles(ctx, proof)
    rows = {(row["file_path"], row["id"]): row for row in manuscript["records"]}
    rendered, styles, pictures, reused = [], [], [], []
    for group in proof["groups"]:
        path, n = group["file_path"], group["block"]
        block = native.IlnkContainer.parse(image.read_file(path)).blocks[n]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"] or cmd["current"] == cmd["stored"]:
                continue
            raw = bytes.fromhex(cmd["stored"])
            start, word = cmd["stored_offset"], cmd["word"]
            assert block[start:start + len(raw)] == raw
            if word == stage.STYLE:
                slots, bodies = inherited.check_styles(ctx, raw)
                slices = [raw[19:20] + bodies[offset] for offset in sorted(bodies)]
                styles.append(dict(file_path=path, block=n, offset=start, slots=slots))
            else:
                assert word == stage.SPEECH
                slices = [raw[5:raw.index(0, 6)]]
            for ident, value in zip(cmd["record_ids"], slices, strict=True):
                row = rows[path, ident]
                if row["decision"] == "retention":
                    assert value[1:].hex() == row["current_hex"]
                    continue
                qualified = reusable.get((path, ident))
                if qualified:
                    stored = qualified.get("stored_hex", qualified.get("target_hex"))
                    if stored == value.hex():
                        rendered.append(qualified)
                        reused.append([path, ident])
                        continue
                try:
                    result = paragraph(ctx, font, paint, expand, fe_paint, names, row, value, group["plans"][ident])
                except (AssertionError, ValueError) as error:
                    raise AssertionError((path, ident, value, group["plans"][ident]["lines"])) from error
                rendered.append(result)
                for layout in result["layouts"]:
                    for page in layout["pages"]:
                        label = f"SC{group['route']} {ident} {layout['scope']} {page['page']}"
                        pictures.append((label, bytes.fromhex(page["native_plane_hex"])))
        print(f"SC{group['route']} B{n} verified", flush=True)
    assert len(rendered) == 40 and len(styles) == 1
    assert {(r["file_path"], r["id"]) for r in rendered} == {
        k for k, row in rows.items() if row["decision"] == "revision"
    }
    ROOT.mkdir()
    make_sheets = FunctionType(inherited.early.contact_sheets.__code__, vars(inherited.early) | {"ROOT": ROOT})
    sheets = make_sheets(pictures)
    base.save(PROOF, dict(candidate_sha256=proof["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        revision_count=len(rendered), fresh_page_count=len(pictures), checked_records=rendered, style_slots=styles,
        original_style_resolution=roles, native_default_given_and_surname=names, actual_gameplay=False,
        reused_records=reused, prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)),
        previous_sheets=previous["previous_sheets"] + previous["contact_sheets"],
        contact_sheets=sheets, visual_review_pending=True))
    print(f"Native checks passed for {len(rendered)} revised records with {len(pictures)} fresh rendered pages.", flush=True)


if __name__ == "__main__":
    main()
