"""Review Port Fleet refusals and resupply dialogue on the registered Market build."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

from scripts import register_market_introduction_wrap_20261123 as parent
from scripts import replay_port_fleet_refusals_20261123 as live
from scripts import stage_market_introduction_wrap_20261123 as prior
from scripts.review_port_services_v761 import BINDINGS


base, native, town, market = prior.base, prior.native, prior.town, prior.market
ARM, COMMON, CLEAN = prior.ARM, prior.COMMON, prior.CLEAN
ROOT = live.ROOT / "staged"
ROM, PROOF = ROOT / "Port_Fleet_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
SERVICE = Path("releases/all_routes_editorial_20261115_port_supply_dialogue_candidate/verification/registered_review.json")
COMPANION = Path("translations/town_trade_port_contextual_editorial_manuscript_v1.json")
IDS = tuple(range(805, 818))
EDITS = {
    805: "You're the admiral! You need to captain a ship!",
    809: "No. I will remain your aide.",
}
PHRASES = {
    805: ("You're the admiral!", "You need to captain a ship!"),
    809: ("No. I will remain your aide.",),
}
NOTES = {
    805: "The port worker objects after checking whether any ship has the admiral as captain. "
         "Give the warning two complete beats and keep the direct, familiar tone.",
    809: "Gerhard answers the admiral directly in the appointee picker. Your aide keeps the existing relationship "
         "clear and I will preserves his formal resolve. The full refusal fits on one row.",
}


def parent_address(key):
    return {0x53FE4: 0x02054014, 0x53F9C: 0x02053FCC}[BINDINGS[key][2]]


def display(ctx, data, key, cpu, values=()):
    return market.native_layout(cpu, data, key, values, parent=parent_address(key))


def history():
    supply = {row["message_ID"]: row for row in base.load(SERVICE)["records"]}
    crew = {row["message_ID"]: row for row in base.load(COMPANION)["records"]}
    return {key: (supply[key], SERVICE) if key in supply else (crew[key], COMPANION) for key in IDS}


def original_callers(clean, current):
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    dis.detail = True
    offset = 0x02000000
    rows = {}
    for key in IDS:
        start, last, consumer = BINDINGS[key]
        end = last + 4
        span = clean[start:end]
        assert span == current[start:end]
        ins = tuple(dis.disasm(span, offset + start))
        first, final = ins[0], ins[-1]
        if first.mnemonic == "ldr":
            literal = start + 8 + first.operands[1].mem.disp
            assert clean[literal:literal + 4] == current[literal:literal + 4]
            assert unpack_from("<I", current, literal)[0] == key
        else:
            assert first.mnemonic == "mov" and first.operands[1].imm == key
        assert final.mnemonic == "bl" and final.operands[0].imm == offset + consumer
        rows[key] = dict(load=offset + start, call=offset + last, caller_hex=span.hex(),
            native_display=offset + consumer, formatting_parent=parent_address(key))
    qualification = [(0x5A9DC, 0x5AA24), (0x5AE6C, 0x5B0A4)]
    assert all(clean[start:end] == current[start:end] for start, end in qualification)
    return rows, [dict(start=offset + start, end=offset + end, sha256=native.digest(clean[start:end]))
                  for start, end in qualification]


def stage():
    assert not PROOF.exists() and not ROM.exists()
    release = base.load(parent.RELEASE)
    previous = base.digest(parent.ROM)
    assert release["candidate_sha256"] == previous and release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == base.digest(CLEAN)
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    clean_arm = clean.read_file(ARM)
    ctx = town.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert native.digest(ctx.arm) == release["target_ARM9_sha256"]
    assert native.digest(ctx.common) == release["target_COMMON_sha256"]
    source = town.common_message_entries(clean.read_file(COMMON), clean_arm)
    before = prior.prior.parent.stage.observed.prior.shared.paired.prior.entries(image)
    callers, qualification = original_callers(clean_arm, ctx.arm)
    phrases = {key: rows for key, rows in PHRASES.items() if len(rows) > 1}
    compiler = FunctionType(market.compile_layouts.__code__, market.compile_layouts.__globals__ | {"PHRASES": phrases})
    encoded = compiler({key: {"english": prose} for key, prose in EDITS.items()})
    assert set(encoded) == EDITS.keys()
    assert all(len(raw) <= len(before[key].text) for key, raw in encoded.items())
    encoded = {key: raw.ljust(len(before[key].text), b" ") for key, raw in encoded.items()}
    deployed, after, slots = town.owned_deployment(ctx.common, ctx.arm, before, encoded)
    assert {old.message_id for old, new in zip(before, after, strict=True) if old != new} == EDITS.keys()
    assert all(slot["new_null_fields"] == 0 for slot in slots.values())
    target = market.with_components(ctx, ctx.arm, deployed)
    cpu, get, provider = target.machine(ctx.arm, deployed, target.raw, target.plan)
    raster, _, _ = town.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows, previews = [], []
    for key, (earlier, path) in history().items():
        jp, old, new = source[key], before[key], after[key]
        assert (earlier["source_reference"], earlier["source_hex"]) == (town.reference(jp), jp.text.hex())
        word_before = earlier.get("staged_hex", earlier["current_hex"])
        assert word_before == old.text.hex()
        assert all(earlier["review"][gate] for gate in town.GATES if gate != "formatting")
        placeholders = int(key == 808)
        assert all(body.count(b"%s") == body.count(b"%") == placeholders for body in (jp.text, old.text, new.text))
        address = get(0x5528C, key)
        assert bytes(cpu.mem_read(address, len(new.text) + 1)) == new.text + b"\0"
        english = EDITS.get(key, earlier["english"].removesuffix("{PAD}"))
        values = ("Hodram",) if placeholders else ()
        former_bytes, former = display(ctx, old.text, key, cpu, values)
        complete, lines = display(ctx, new.text, key, cpu, values)
        shown = english % values[0] if values else english
        assert " ".join(lines) == shown and 0 < len(lines) <= 4 and all(0 < len(item) <= 36 for item in lines)
        plane, glyphs = town.render_portrait(raster, ctx.arm, kanji, complete)
        assert [row["code"] for row in glyphs] == town.glyph_codes(complete)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(shown[0]), ord(shown[-1]))
        arg_checks = []
        if placeholders:
            for argument in ("Rafael", "Lil", "Maria", "FALCON", "ABCDEFGHIJKLMNOPQRSTUVW"):
                native_body, native_lines = display(ctx, new.text, key, cpu, (argument,))
                expected = english % argument
                assert " ".join(native_lines) == expected and 0 < len(native_lines) <= 4
                native_plane, ink = town.render_portrait(raster, ctx.arm, kanji, native_body)
                assert [glyph["code"] for glyph in ink] == town.glyph_codes(native_body)
                assert (ink[0]["code"], ink[-1]["code"]) == (ord(expected[0]), ord(expected[-1]))
                arg_checks.append(dict(value=argument, display_hex=native_body.hex(), lines=native_lines,
                    native_plane_sha256=native.digest(native_plane)))
        if key in EDITS:
            assert tuple(lines) == PHRASES[key] and former != lines, (key, former, lines)
            old_plane, _ = town.render_portrait(raster, ctx.arm, kanji, former_bytes)
            previews.extend(((f"{key} previous", old_plane), (f"{key} revised", plane)))
        context = {805: "The port worker checks the ships and warns the admiral if none has the admiral as captain.",
                   809: "Selecting Gerhard as fleet admiral prompts his refusal. The fleet-admiral prompt returns after dismissal."}
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker=earlier["speaker"],
            context=context.get(key, earlier["context"]), source_meaning=earlier["source_meaning"], clean_Japanese=jp.text.decode("cp932"),
            localization_note=NOTES.get(key, earlier["localization_note"]), decision="revision" if key in EDITS else "retention",
            source_reference=town.reference(jp), current_reference=town.reference(old), registered_reference=town.reference(new),
            source_hex=jp.text.hex(), current_hex=old.text.hex(), installed_hex=new.text.hex(),
            previous_English=" ".join(old.text.decode("ascii").split()), english=english,
            previous_lines=former, installed_lines=lines, display_hex=complete.hex(),
            native_plane_sha256=native.digest(plane), source_caller=callers[key], substitutions=arg_checks,
            prior_review=dict(path=str(path), sha256=base.digest(path)), review=dict.fromkeys(town.GATES, True)))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    first = native.files(image)
    image.replace_file(COMMON, deployed)
    final = native.files(image)
    assert first.keys() == final.keys() and {name for name in first if first[name] != final[name]} == {COMMON}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean), final)
    assert not any(guard["source_bound_new_command_counts"].values())
    data = bytes(image.rom.save())
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(data)
    candidate = base.digest(ROM)
    for row in rows:
        row["registered_reference"].update(candidate_sha256=candidate, file_path=COMMON,
            archive_sha256=native.digest(deployed), exact_stored_hex=row["installed_hex"])
    base.save(PROOF, dict(candidate_sha256=candidate, predecessor_sha256=previous,
        clean_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(ctx.arm),
        target_COMMON_sha256=native.digest(deployed), records=rows, whole_parent_inverse=True,
        source25=guard, allocations=slots, original_command_and_companion_qualifications=qualification,
        sheets={row["path"]: row["sha256"] for row in town.portrait_sheets(ROOT, previews)},
        translation_policy="natural-dialogue-v2", target_locale="en-US", gates=town.GATES))
    print(f"Staged {candidate}. Reconciled {len(rows)} Port records and verified the two revised native pages.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    else:
        step = getattr(prior.prior.parent.parent.staged.prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
