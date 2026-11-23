"""Reflow Faticia's teasing drink refusal and preserve the complete Tavern exchange."""

from argparse import ArgumentParser
from functools import partial
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import observe_village_tavern_routes_20261123 as ordinary
from scripts import probe_tavern_conversations_v764 as tavern
from scripts import register_cabin_square_wrap_20261123 as parent
from scripts import stage_cabin_square_wrap_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town, market = prior.base, prior.native, prior.town, prior.market
ARM, COMMON, CLEAN = prior.ARM, prior.COMMON, prior.CLEAN
ROOT = Path(".codex-release-work/tavern_drink_reply_20261123/staged")
ROM, PROOF = ROOT / "Tavern_Drink_Reply_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PLAY = ROOT / "ordinary_replay"
BASELINE = ordinary.ROOT / "tavern/terminal.json"
EDITS = {826: "Oh, can't handle another drink?"}
native_layout = FunctionType(town.native_layout.__code__, town.native_layout.__globals__ |
    {"call": partial(town.native_layout.__globals__["call"], instruction_limit=2_000_000)},
    argdefs=town.native_layout.__defaults__)

# Complete held samples across the two visits, excluding repeated identical panels.
HOLDS = {
    3800: (51, "Barkeep", (), "The friendly greeting leads into the choice of drinks."),
    4600: (53, "Barkeep", (), "The barkeep states the five-coin charge before sharing a tip."),
    5000: (821, "Barkeep", ("Hayreddin", "Alexandria", "pirate"),
        "Real pull makes this an informal report about influence and preserves all three arguments."),
    5400: (55, "Barkeep", ("Faticia",), "The barkeep calls Faticia over after noticing the customer."),
    5800: (56, "Faticia", (), "On it is a quick, willing answer to the barkeep's call."),
    6200: (59, "Faticia", (), "The friendly question fits the choice to accept or decline another drink."),
    6600: (61, "Barkeep", (), "The ten-coin charge follows acceptance and reflects the source amount."),
    7000: (827, "Faticia", ("Hodram",), "The toast warmly marks meeting the named customer."),
    8200: (823, "Barkeep", ("Ragusa",), "The question keeps the nearby town and question mark together."),
    9000: (57, "Faticia", (), "The shorter greeting fits the second visit and the speaker's surprise is mild."),
    9800: (826, "Faticia", (), "The surprised Oh and the teasing question follow the refusal naturally. "
        "Another drink stays together and preserves the object of the joke."),
}
MEANINGS = {
    51: "The barkeep welcomes the customer and asks what they would like.",
    53: "The first drink costs five gold coins.",
    821: "The named person from the named town has influence here in the given role.",
    55: "The barkeep calls the named hostess because a customer has arrived.",
    56: "The hostess answers promptly and cheerfully.",
    59: "The hostess urges the customer to have one more drink.",
    61: "The barkeep says the second drink costs ten gold coins.",
    827: "The hostess confirms the customer's name and proposes a toast to their acquaintance.",
    823: "The barkeep asks if the customer knows the named town and says it is nearby.",
    57: "The hostess greets the customer in a lightly surprised voice.",
    826: "The hostess teases the customer for unexpectedly low drinking tolerance.",
}


def run_records(terminal, expected_sha):
    result = base.load(terminal)
    report_path = terminal.parent / "capture/capture_report.json"
    report = base.load(report_path)
    assert result["ROM_sha256"] == report["ROM_sha256"] == expected_sha
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert all(base.digest(path) == sha for path, sha in result["evidence"].items())
    schedule, _, end, _, donor = ordinary.schedule("tavern")
    assert report["frames"] == end and report["scripted_input_schedule"] == schedule
    assert donor["source_sha256"] == report["battery_save_preloaded"]["source_sha256"]
    return result, report


def display(ctx, key, raw, cpu, args, lr):
    if key == 59:
        assert lr == 0x02053FB0 and raw == b"How about one more drink?" and not args
        return raw, [raw.decode("ascii")]
    if key == 821:
        result = tavern.format_case(cpu, dict(message_id=key, english=raw.decode("ascii").strip()),
                                    tuple(arg.encode("ascii") for arg in args))
        return bytes.fromhex(result["formatted_hex"]), result["lines"]
    return native_layout(cpu, raw, key, args, parent=lr + 0x1C)


def stage():
    assert not ROM.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    candidate = base.digest(parent.ROM)
    assert candidate == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    trace, _ = run_records(BASELINE, candidate)
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    ja = clean.read_file(ARM)
    ctx = town.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert native.digest(ctx.arm) == release["target_ARM9_sha256"]
    assert native.digest(ctx.common) == release["target_COMMON_sha256"]
    source = town.common_message_entries(clean.read_file(COMMON), ja)
    before = prior.prior.parent.stage.observed.prior.shared.paired.prior.entries(image)
    key, = EDITS
    payload = b" " + EDITS[key].encode("ascii")
    assert len(payload) <= len(before[key].text)
    payload = payload.ljust(len(before[key].text), b" ")
    common, after, slots = town.owned_deployment(ctx.common, ctx.arm, before, {key: payload})
    assert slots[key]["new_null_fields"] == 0 and after[key].text == payload
    assert all(a == b for a, b in zip(before, after, strict=True) if a.message_id != key)
    target = market.with_components(ctx, ctx.arm, common)
    cpu, get, provider = target.machine(ctx.arm, common, target.raw, target.plan)
    raster, _, _ = town.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows, previews = [], []
    for frame, (n, speaker, args, reason) in HOLDS.items():
        src, old, new = source[n], before[n], after[n]
        matches = [r for r in trace["target_COMMON_calls"] if r["message_ID"] == n and 0 < frame - r["frame"] <= 220]
        getter, copier = matches
        assert (getter["PC"], copier["PC"]) == (0x0205528C, 0x020534F4)
        assert dict(getter, PC=copier["PC"]) == copier
        lr = getter["caller_LR"]
        off = lr - 0x02000000
        assert ja[off - 4:off] == ctx.arm[off - 4:off]
        assert all(body.count(b"%s") == len(args) for body in (src.text, old.text, new.text))
        address = get(0x5528C, n)
        assert bytes(cpu.mem_read(address, len(new.text) + 1)) == new.text + b"\0"
        try:
            earlier, old_lines = display(ctx, n, old.text, cpu, args, lr)
            body, lines = display(ctx, n, new.text, cpu, args, lr)
        except (AssertionError, ValueError) as error:
            raise ValueError(f"Formatting check for COMMON {n}") from error
        english = " ".join(new.text.decode("ascii").split())
        expected = (english % args) if args else english
        assert " ".join(lines) == expected and 0 < len(lines) <= 4 and all(0 < len(line) <= 36 for line in lines)
        plane, glyphs = town.render_portrait(raster, ctx.arm, kanji, body)
        assert [g["code"] for g in glyphs] == town.glyph_codes(body)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(expected[0]), ord(expected[-1]))
        if n == key:
            assert len(old_lines) == 2 and old_lines[1] == "another drink."
            assert lines == [EDITS[key]]
            old_plane, _ = town.render_portrait(raster, ctx.arm, kanji, earlier)
            previews.extend((("826 previous", old_plane), ("826 revised", plane)))
        rows.append(dict(message_ID=n, id=f"COMMON_MESSAGE_{n}", file_path=COMMON, speaker=speaker,
            context="The two Istanbul Tavern visits cover ordering, rumors, greeting Faticia, accepting her offer, "
                    "the toast, and declining her next offer.",
            clean_Japanese=src.text.decode("cp932"), source_meaning=MEANINGS[n], localization_note=reason,
            decision="revision" if n == key else "retention", english=english,
            source_reference=town.reference(src), current_reference=town.reference(old), registered_reference=town.reference(new),
            source_hex=src.text.hex(), current_hex=old.text.hex(), installed_hex=new.text.hex(),
            previous_English=" ".join(old.text.decode("ascii").split()), previous_lines=old_lines, installed_lines=lines,
            substitutions=args, native_request=getter, display_hex=body.hex(), native_plane_sha256=native.digest(plane),
            review=dict.fromkeys(town.GATES, True)))
    assert len(rows) == 11 and provider.reads
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    first = native.files(image)
    image.replace_file(COMMON, common)
    final = native.files(image)
    assert first.keys() == final.keys() and {name for name in first if first[name] != final[name]} == {COMMON}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean), final)
    assert not any(guard["source_bound_new_command_counts"].values())
    data = bytes(image.rom.save())
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(data)
    digest = base.digest(ROM)
    for row in rows:
        row["registered_reference"].update(candidate_sha256=digest, file_path=COMMON,
            archive_sha256=native.digest(common), exact_stored_hex=row["installed_hex"])
    base.save(PROOF, dict(candidate_sha256=digest, predecessor_sha256=candidate,
        clean_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(ctx.arm),
        target_COMMON_sha256=native.digest(common), records=rows, whole_parent_inverse=True,
        source25=guard, allocations=slots, baseline_trace=dict(path=str(BASELINE), sha256=base.digest(BASELINE)),
        sheets={row["path"]: row["sha256"] for row in town.portrait_sheets(ROOT, previews)},
        translation_policy="natural-dialogue-v2", target_locale="en-US", gates=town.GATES))
    print(f"Staged {digest}; verified the entire drink exchange and its revised one-line reply.")


def replay():
    receipt = base.load(PROOF)
    source = checked_text(getsource(ordinary.playback.main), {
        "    rom = parent.ROM\n    release = base.load(parent.RELEASE)": "    rom = ROM\n    release = receipt",
    })
    scope = vars(ordinary.playback) | globals() | dict(receipt=receipt, ROOT=PLAY,
        observer=ordinary.trace.scoped_observer, get_schedule=ordinary.schedule, FOCUS=set(range(3668)))
    exec(compile(source, __file__ + "::ordinary_tavern_replay", "exec"), scope)
    scope["main"]("tavern")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "replay", "patch", "startup"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    elif action == "replay":
        replay()
    else:
        step = getattr(prior.prior.parent.parent.staged.prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
