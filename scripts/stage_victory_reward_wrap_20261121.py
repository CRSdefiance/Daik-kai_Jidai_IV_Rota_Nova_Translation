"""Review all decimal widths of the captured-gold and national reward notices."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import victory_reward_wrap_v1 as selector
from scripts import register_victory_reward_digits_20261121 as parent
from scripts.stage_victory_reward_digits_20261121 import RegisteredRuntime, discovery, prior, shared


base, native = parent.base, parent.native
ROOT = Path("work/victory_reward_wrap_20261121")
ROM, PROOF = ROOT / "Victory_Reward_Wrap_STAGED.nds", ROOT / "staged.json"
GOLD, AWARD = 301, 305
TEXT = {
    GOLD: ("You recovered %s gold", "from captured ships."),
    AWARD: ("The nation awarded you", "%s gold."),
}
CONTROLS = {
    288: ("105",), 292: ("Santo Domingo",), 297: ("Inuvik",), 303: ("109", "103"),
    311: ("400",), 348: ("25",), 349: ("Coutinho Co.",),
}


def verify_visible_layout(ctx, revised, old):
    clean = base.NdsImage.open(shared.CLEAN)
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), clean.read_file(shared.ARM))
    current = shared.entries(ctx.image)
    rows = {r["message_ID"]: dict(r) for r in old["records"] if r["message_ID"] in TEXT}
    assert set(rows) == set(TEXT)
    number_cases = tuple(dict.fromkeys(
        tuple(amount for width in range(1, 10) for amount in (10**(width - 1), 10**width - 1))
        + (6055, 214748364, 1000000000, 2147483647)))
    assert {len(str(n)) for n in number_cases} == set(range(1, 11))
    raster, _, font = discovery.mixed.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    run = discovery.native_reader()
    reviewed, planes, controls = [], [], []
    for n in TEXT.keys() | CONTROLS.keys():
        jp, installed = source[n], current[n]
        alternates = [(str(amount),) for amount in number_cases] if n in TEXT else [CONTROLS[n]]
        record = dict(id=f"COMMON_MESSAGE_{n}", message_ID=n, current_hex=installed.text.hex(),
                      english=installed.text.decode("ascii").replace("\n", "{LB}"),
                      current_copies=[dict(wrapper=prior.WRAPPER)])
        assert all(len(args) == installed.text.count(b"%s") for args in alternates), n
        if n in TEXT:
            row = rows[n]
            assert row["current_hex"] == installed.text.hex() and row["source_hex"] == jp.text.hex()
            assert row["current_reference"] == shared.workflow.reference(installed)
            assert row["source_reference"] == shared.workflow.reference(jp)
            assert " ".join(TEXT[n]) == row["english"] == installed.text.decode("ascii")
            row.update(decision="wrap_only", localization_note=row["localization_note"] + (
                " Keep “from captured ships” together on the second line."
                if n == GOLD else " Keep the amount with “gold” whenever the notice needs two lines."),
                layout_protected_phrase="from captured ships." if n == GOLD else "decimal amount + gold.")
        for args in alternates:
            before, after = [run(version, record, args) for version in (ctx, revised)]
            for version in (ctx, revised):
                version.calls.clear()
            old_bytes, new_bytes = [bytes.fromhex(r["native_wrapper_output_hex"]) for r in (before, after)]
            if n not in TEXT:
                assert old_bytes == new_bytes, n
                controls.append(dict(message_ID=n, arguments=args, display_hex=new_bytes.hex()))
                continue
            words = installed.text % tuple(a.encode("ascii") for a in args)
            pieces = tuple(part.encode("ascii") for part in TEXT[n])
            target = tuple((part % args[0].encode("ascii")) if b"%s" in part else part for part in pieces)
            target = (words,) if len(words) <= 36 else target
            lines = tuple(line.strip() for line in new_bytes.split(b"\n"))
            assert lines == target and len(lines) <= 2, (n, args, lines, target)
            assert b" ".join(lines) == words and new_bytes.isascii() and b"\x1f" not in new_bytes
            assert after["expanded_hex"] == before["expanded_hex"] == words.hex()
            pixels, glyphs = discovery.mixed.render(raster, revised.arm, kanji, new_bytes)
            assert (glyphs[0]["code"], glyphs[-1]["code"]) == (words[0], words[-1])
            assert all(0 < len(line) <= 36 for line in lines)
            reviewed.append(after | dict(before_hex=old_bytes.hex(), lines=[line.decode() for line in lines],
                pages=1, complete_first_and_last_glyphs=True, ink_sha256=sha256(pixels).hexdigest()))
            planes.append(pixels)
    assert len(controls) == len(CONTROLS) and len(reviewed) == 2 * len(number_cases)
    return list(rows.values()), reviewed, planes, controls, font


def main():
    assert not ROOT.exists()
    release, old = map(base.load, (parent.RELEASE, parent.REVIEW))
    assert base.digest(parent.ROM) == release["candidate_sha256"] == old["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(shared.CLEAN) == release["clean_input_sha256"]
    ctx = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    arm, runtime = selector.transform(ctx.arm, release["target_ARM9_sha256"])
    revised = discovery.with_components(ctx, arm, ctx.common)
    rows, cases, planes, controls, font = verify_visible_layout(ctx, revised, old)
    review = {key: old[key] for key in ("translation_policy", "target_locale", "encoder", "review_gates")}
    review["records"] = rows
    validate_natural_dialogue_batch(review)
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(shared.ARM, arm)
    binary = bytes(image.rom.save())
    image.replace_file(shared.ARM, ctx.arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    sheets = FunctionType(discovery.save_sheets.__code__, discovery.save_sheets.__globals__ | {"ROOT": ROOT})
    base.save(PROOF, review | dict(candidate_sha256=native.digest(binary), parent_sha256=release["candidate_sha256"],
        target_ARM9_sha256=native.digest(arm), target_COMMON_sha256=release["target_COMMON_sha256"],
        exact_parent_inverse=True, runtime=runtime, native_display_cases=cases, unchanged_native_controls=controls,
        font=font, sheets=sheets(cases, planes), emulator_and_visual_gate_pending=True, new_editorial_credit=0,
        source_evidence={str(p): base.digest(p) for p in (parent.RELEASE, parent.REVIEW)}))
    print(f"Verified {len(cases)} complete gold notices, including every decimal width, and {len(controls)} unchanged controls.")


if __name__ == "__main__":
    main()
