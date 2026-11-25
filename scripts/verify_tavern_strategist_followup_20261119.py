"""Verify complete Schemes substitutions through the installed queued formatter."""

from inspect import getsource
from itertools import product
from struct import unpack

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_market_reward_dialogue_20261115 as display
from scripts import stage_tavern_strategist_followup_20261119 as stage
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_scheme_scoped_layout_v776 import formatter
from scripts.verify_scheme_gameplay_v776 import raster

base, native, workflow = stage.base, stage.native, stage.workflow
ROOT = stage.ROOT / "native_display_v2"
PROOF = ROOT / "native_display.json"


def native_portrait(arm, font, text, lines):
    # The original verifier loads its font from an older research ROM. The
    # renderer and all its memory/consumption guards stay identical.
    source = getsource(raster)
    legacy = 'NdsImage.open("out/all_routes_combined_v255_candidate.nds").read_file("/GRP/KANJI.FNT")'
    assert source.count(legacy) == 1
    env = raster.__globals__ | {"REGISTERED_FONT": font}
    exec(compile(source.replace(legacy, "REGISTERED_FONT"), __file__ + "::scheme-font", "exec"), env)
    events = []
    plane = env["raster"](arm, text, 0x01FFCE40 - 0x02000000, size=(228, 64),
                          instruction_limit=1000000, glyph_events=events)
    expected = bytearray(228 * 64)
    glyphs = GameAsciiFont.from_arm9(arm)
    assert all(e["style"] == 1 and 0 <= e["code"] < 128 and e["y"] in range(0, 16 * len(lines), 16) for e in events)
    for index, line in enumerate(lines):
        row = [e for e in events if e["y"] == 16 * index]
        assert bytes(e["code"] for e in row).strip(b" ") == line.encode("ascii")
        visible = [(offset, e) for offset, e in enumerate(row) if e["code"] != 32]
        start = visible[0][0]
        assert all(e["x"] == 6 + 6 * (offset - start) for offset, e in visible)
        for e in row:
            if e["code"] == 32:
                continue
            assert 6 <= e["x"] and e["x"] + 6 <= 228
            glyph = glyphs.decode(chr(e["code"]))
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        # This portrait renderer draws style 1 one pixel below its row origin.
                        expected[(e["y"] + 1 + y) * 228 + e["x"] + x] = 1
    assert plane == expected
    return plane


def names(cpu, get):
    def text(pointer):
        return bytes(cpu.mem_read(pointer, 80)).split(b"\0", 1)[0]

    def value(obj):
        vptr, = unpack("<I", cpu.mem_read(obj, 4))
        getter, = unpack("<I", cpu.mem_read(vptr + 8, 4))
        return text(get(getter - 0x02000000, obj))

    faction_root, town_root = get(0xCB160), get(0xCB178)
    factions = tuple(value(faction_root + 4 + 76 * i) for i in range(20))
    towns = tuple(value(town_root + 4 + 108 * i) for i in range(114))
    labels = tuple(text(get(0x93D5C, i)) for i in range(6, 10))
    assert len(set(factions)) == 20 and len(set(towns)) == 114
    assert labels == (b"Lure Fleet", b"Forge Papers", b"Bad Rumors", b"Bribe")
    assert all(s.isascii() and s for s in (*factions, *towns, *labels))
    return factions, towns, labels


def values(ident, factions, towns, labels):
    if 915 <= ident <= 920:
        return [(label,) for label in labels]
    if 940 <= ident <= 947:
        return list(product(factions, towns))
    if 956 <= ident <= 963:
        return list(product(towns, factions))
    return [()]


def main():
    assert not ROOT.exists()
    proof, previous = map(base.load, (stage.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == proof["candidate_sha256"]
    assert proof["entire_parent_inverse"]
    ctx = workflow.RegisteredRuntime(stage.parent.RELEASE, previous["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    arm, common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    runtime = display.with_components(ctx, arm, common)
    cpu, get, provider = runtime.machine(arm, common, runtime.raw, runtime.plan)
    factions, towns, labels = names(cpu, get)
    original_cpu, prev_get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    assert names(original_cpu, prev_get) == (factions, towns, labels)
    assert b"Clifford" in factions and b"London" in towns
    formatter_fn, program = formatter()
    bound = machine(arm)
    bound.mem_write(0x02000000, runtime.raw)
    kanji = image.read_file("/GRP/KANJI.FNT")
    assert kanji == ctx.image.read_file("/GRP/KANJI.FNT")
    revised = []
    sheets = []
    cases_total = 0
    for row in proof["records"]:
        ident = row["message_ID"]
        if row["decision"] == "retention":
            assert row["current_hex"] == row["staged_hex"]
            continue
        assert isinstance(row["original_voice_table"], int)
        table = row["original_voice_table"]
        data = cpu.mem_read(table, 32)
        assert ident in unpack("<8i", data)
        template = bytes.fromhex(row["staged_hex"])
        assert template == b" " + row["english"].encode("ascii")
        ptr = get(0x5528C, ident)
        assert bytes(cpu.mem_read(ptr, len(template) + 1)) == template + b"\0"
        case_row = row | {"source_voice_table": table}
        cases, advisory = [], []
        for args in values(ident, factions, towns, labels):
            case = formatter_fn(bound, case_row, args)
            expanded = row["english"] % tuple(s.decode() for s in args) if args else row["english"]
            lines = case["lines"]
            assert " ".join(lines) == expanded and all(lines)
            assert len(lines) <= 4 and all(len(line) <= 35 for line in lines), (ident, args, lines)
            assert "four_row_width_bound" not in case["findings"], (ident, args, lines)
            case["full_phrase_split"] = [arg.decode() for arg in args if not any(arg.decode() in line for line in lines)]
            if case["findings"] or case["full_phrase_split"]:
                advisory.append(dict(args=case["source_values_hex"], lines=lines, soft_findings=case["findings"],
                                     wrapped_argument=case["full_phrase_split"]))
            cases.append(case)
        cases_total += len(cases)
        max_case = max(cases, key=lambda case: (len(case["lines"]), max(map(len, case["lines"])), sum(map(len, case["lines"]))))
        default = [b"Clifford", b"London"] if 940 <= ident <= 947 else [b"London", b"Clifford"] if ident == 957 else \
            [b"Lure Fleet"] if ident in (915, 918) else []
        example = next(case for case in cases if case["source_values_hex"] == [arg.hex() for arg in default])
        native_example = formatter_fn(cpu, case_row, tuple(default))
        assert native_example == {key: value for key, value in example.items() if key != "full_phrase_split"}
        previews = []
        for index, case in enumerate((example,) if example == max_case else (example, max_case)):
            body = bytes.fromhex(case["formatted_hex"])
            plane = native_portrait(arm, kanji, body, case["lines"])
            assert len(plane) == 228 * 64
            sheets.append((f"{ident} {'London' if index == 0 else 'bound sample'}", plane))
            previews.append(case | dict(ink_sha256=native.digest(plane), complete_glyph_count=len(workflow.glyph_codes(body)),
                                         independent_full_plane_exact=True))
        revised.append(dict(message_ID=ident, template_hex=template.hex(), tested_cases=len(cases),
            voice_table=table, representative_previews=previews, wrap_advisories=advisory))
        print(f"COMMON {ident}: {len(cases)} native layout cases; {len(advisory)} wrap advisories.", flush=True)
    assert provider.reads and len(revised) == 15
    ROOT.mkdir()
    images = display.portrait_sheets(ROOT, sheets)
    base.save(PROOF, dict(candidate_sha256=proof["candidate_sha256"], stage_proof_sha256=base.digest(stage.PROOF),
        native_formatter_sha256=native.digest(program.encode()), unchanged_source_arguments=True,
        original_catalogue_sizes=[len(factions), len(towns), len(labels)], native_layout_cases=cases_total,
        scope="Every faction-by-town combination and every registered scheme label was tested for the relevant changed templates.",
        revisions=revised, retained_template_count=91, contact_sheets=images, actual_gameplay=False,
        integration_pending=True, new_editorial_credit=0))


if __name__ == "__main__":
    main()
