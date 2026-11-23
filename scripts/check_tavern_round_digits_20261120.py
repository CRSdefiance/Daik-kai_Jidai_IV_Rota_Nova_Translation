"""Verify native Tavern price formatting and the normal Amsterdam round."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R8, UC_ARM_REG_SP

from scripts import check_departure_numerals_native_20261119 as number_checks
from scripts import replay_tavern_round_digits_20261120 as replay
from scripts import stage_tavern_round_digits_20261120 as stage
from scripts.check_swimmer_leak_square_dialogue_20261120 import one_frame
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import STACK, call
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.verify_inn_numerals_native_20261119 import normalize, read_cstring
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold
from scripts.verify_personal_gameplay_v841 import get_machine


base, batch, BASE = stage.base, stage.batch, stage.runtime.BASE
ROOT, PROOF, SHEET = stage.ROOT, stage.ROOT / "verification.json", stage.ROOT / "gameplay_comparison.png"
NATIVE = ROOT / "native_prices.json"
GETTER = ROOT / "original_getter.json"
PRICES = (100, 101, 199, 200, 268, 999, 1000, 2721)
RECORDS = tuple(range(852, 859))
HOLDS = {25630: (855, ("268",)), 26500: (855, ("268",)), 26900: (866, ()),
         27230: (872, ("Argot",)), 27560: (874, ()), 27890: (880, ("Clifford", "Bristol"))}
CONFIRMATIONS = (25630, 26500)
DECISIONS = {
    852: ("Sailor", "The careful estimate and polite question suit the default voice."),
    853: ("Sailor", "The casual estimate leads to a quick 'Okay?' that carries the original familiar register."),
    854: ("Sailor", "The direct estimate and short 'All right?' keep the speaker's courteous request together."),
    855: ("Sailor", "The clipped question keeps the sailor's familiar tone in the observed exchange."),
    856: ("Sailor", "The measured estimate and full question suit the deliberate voice. The amount stays with 'gold'."),
    857: ("Sailor", "'Sound okay?' keeps this voice's tentative request for agreement and gives the question its own beat."),
    858: ("Sailor", "The polite question keeps the estimate and leaves the spending decision to the captain."),
}
QUESTION = {852: "Is that all right?", 853: "Okay?", 854: "All right?", 855: "Okay with you?",
            856: "Is that all right?", 857: "Sound okay?"}


def capture_ram(report, frame):
    snap, = [row for row in report["read_only_capture_RAM_snapshots"] if row["frame"] == frame]
    ram = Path(snap["path"]).read_bytes()
    assert len(ram) == 0x400000 and snap["read_only_export"] and batch.digest(ram) == snap["sha256"]
    return snap, ram


def fill_model(image_before, image_after):
    release = base.load(stage.parent.RELEASE)
    source_path = Path(release["own_registered_startup"])
    receipt = base.load(source_path)
    assert release["own_registered_startup_sha256"] == base.digest(source_path)
    snapshot = receipt["read_only_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and len(raw) == 0x400000 and batch.digest(raw) == snapshot["sha256"]
    old, new = [image.read_file(stage.ARM) for image in (image_before, image_after)]
    offset = stage.CALL - BASE
    assert raw[offset:offset + 4] == old[offset:offset + 4]
    cpus = get_machine(old, raw), get_machine(new, raw[:offset] + new[offset:offset + 4] + raw[offset + 4:])
    return cpus, snapshot


def ready_quote(cpu, growth):
    cpu.reg_write(UC_ARM_REG_R0, growth)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.emu_start(0x0205836C, 0x02058398, count=20000)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x02058398 and cpu.reg_read(UC_ARM_REG_SP) == STACK
    assert cpu.reg_read(UC_ARM_REG_R0) == 3 and cpu.reg_read(UC_ARM_REG_R1) == BASE + stage.VOICE_TABLE
    return cpu.reg_read(UC_ARM_REG_R8), read_cstring(cpu, cpu.reg_read(UC_ARM_REG_R2))


def getter():
    assert not GETTER.exists()
    _, _, new, arm, _, _, _, table, _ = assets()
    release = base.load(stage.parent.RELEASE)
    baseline = RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    ctx = with_components(baseline, arm, new.read_file(stage.COMMON))
    offset = stage.CALL - BASE
    assert ctx.raw[offset:offset+4] == baseline.arm[offset:offset+4]
    ctx.raw = ctx.raw[:offset] + arm[offset:offset+4] + ctx.raw[offset+4:]
    cpu, get, _ = ctx.machine(arm, ctx.common, ctx.raw, ctx.plan)
    rows = []
    for message in RECORDS:
        pointer = get(0x5528C, message)
        body = table[message].text
        assert bytes(cpu.mem_read(pointer, len(body) + 1)) == body + b"\0"
        rows.append(dict(message_ID=message, returned_pointer=pointer, exact_installed_hex=body.hex()))
    base.save(GETTER, dict(candidate_sha256=base.digest(stage.ROM), original_getter_cases=rows,
                           read_only_source_context=release["own_registered_startup"]))
    print(f"Original loader returned all {len(rows)} complete installed templates.")


def assets():
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, stage.parent.ROM, stage.ROM))
    source_arm, before, arm = [image.read_file(stage.ARM) for image in (clean, old, new)]
    common, kanji = [new.read_file(path) for path in (stage.COMMON, "/GRP/KANJI.FNT")]
    assert stage.patch(before, source_arm)[0] == arm
    assert old.read_file("/GRP/KANJI.FNT") == kanji
    owned, table, _ = stage.deploy_text(old.read_file(stage.COMMON), arm)
    assert owned == common
    previous_table = batch.owned_entries(old.read_file(stage.COMMON), arm,
                                         batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    source = batch.common_message_entries(clean.read_file(stage.COMMON), source_arm)
    painter, _, _ = font_tools(new)
    return clean, old, new, arm, kanji, source, previous_table, table, painter


def native():
    assert not NATIVE.exists()
    _, old, new, arm, kanji, source, previous_table, table, painter = assets()
    machines, snapshot = fill_model(old, new)
    (old_cpu, _), (cpu, get) = machines
    assert unpack_from("<I", arm, 0x585F8)[0] == 0x51EB851F
    towns = get(0xCB178) + 4
    census = [get(0xB3FD4, towns + town * 108, 0) for town in range(90)]
    assert all(0 <= growth <= 65535 for growth in census)
    check_ring = FunctionType(number_checks.verify_numbers.__code__, number_checks.verify_numbers.__globals__ |
                              {"CASES": {stage.CALL: PRICES}})
    ring = check_ring(old_cpu, cpu)
    assert len(ring) == len(PRICES) * 32
    values = sorted({0, 1, 24, 25, 26, 65535, *census, *[(p - 100) * 25 for p in PRICES]})
    arithmetic = []
    for growth in values:
        cost = 100 + growth // 25
        previous, current = [ready_quote(machine, growth) for machine, _ in machines]
        assert previous[0] == current[0] == cost
        assert normalize(previous[1]) == current[1] == str(cost).encode("ascii")
        arithmetic.append(dict(supplied_original_unsigned_growth=growth, fee=cost,
                               old_number_hex=previous[1].hex(), revised_number_hex=current[1].hex()))
    root = get(0xCB184)
    voices = {}
    for actor in range(40):
        ptr = root + 4 + actor * 32
        voice = get(0x7E988, ptr)
        assert 0 <= voice < len(stage.TABLE)
        expected = stage.TABLE[voice] if stage.TABLE[voice] >= 0 else stage.TABLE[0]
        assert get(0x53F4C, ptr, BASE + stage.VOICE_TABLE) == expected
        voices.setdefault(voice, dict(actor_ID=actor, actual_actor_pointer=ptr, selected_message_ID=expected))
    assert set(voices) == set(range(len(stage.TABLE)))
    assert get(0x53F4C, 0, BASE + stage.VOICE_TABLE) == 852

    def call_layout(cpu, offset, arguments):
        return call(cpu, offset, arguments, instruction_limit=2_000_000)

    layout = FunctionType(native_layout.__code__, native_layout.__globals__ | {"call": call_layout}, argdefs=native_layout.__defaults__)
    pages, output, records = [], [], []
    for n in RECORDS:
        template, original = table[n].text, source[n].text
        assert template.count(b"%s") == original.count(b"%s") == 1 and template.startswith(b" ")
        speaker, reason = DECISIONS[n]
        records.append(dict(id=f"COMMON_MESSAGE_{n}", message_ID=n, file_path=stage.COMMON, speaker=speaker,
            english=template.decode("ascii").strip(), source_Japanese=original.decode("cp932"),
            source_reference=batch.reference(source[n]), current_reference=batch.reference(previous_table[n]),
            final_reference=batch.reference(table[n]), source_hex=original.hex(), current_hex=previous_table[n].text.hex(),
            final_hex=template.hex(), decision="revision" if n in stage.REVISIONS else "retention",
            context="Treat Everyone offers the captain a round for the original town-dependent price before asking for approval.",
            source_meaning="A sailor states the likely price in gold and asks the captain to approve the purchase.",
            localization_note=reason, review=dict.fromkeys(batch.GATES, True)))
        for price in PRICES:
            amount = str(price)
            formatted, lines = layout(cpu, template, n, (amount,), parent=0x02053D24)
            assert b" ".join(formatted.split()) == (template % amount.encode("ascii")).strip()
            assert 1 <= len(lines) <= 3 and all(lines)
            assert any(f"{amount} gold" in line for line in lines), (n, amount, lines)
            assert n not in QUESTION or lines[-1].endswith(QUESTION[n]), (n, amount, lines)
            plane, glyphs = render_portrait(painter, arm, kanji, formatted.replace(b"\r", b""))
            codes = [glyph["code"] for glyph in glyphs]
            assert codes == glyph_codes(formatted) and (codes[0], codes[-1]) == (template[1], ord("?"))
            assert all(code < 128 for code in codes)
            pages.append((f"{n} / {amount} gold", plane))
            output.append(dict(message_ID=n, price=price, page_count=1, lines=lines, formatted_hex=formatted.hex(),
                               full_glyph_mask_sha256=batch.digest(plane)))
    base.save(NATIVE, dict(candidate_sha256=base.digest(stage.ROM), native_model_snapshot=snapshot,
        representative_prices=list(PRICES), initialized_stock_town_growth=census, native_price_cases=arithmetic,
        native_ring_cases=ring, original_voice_selector=list(voices.values()), default_no_actor=852,
        records=records, offline_rendered_pages=output, sheets=portrait_sheets(ROOT, pages)))
    print(f"Checked {len(ring)} numeric-ring cases and {len(output)} complete Tavern price pages.")


def wallet(arm, ram):
    _, get = get_machine(arm, ram)
    root, faction = get(0xCB160), get(0x397D8)
    return get(0x3CCC8, root + 4 + faction * 76)


def gameplay():
    assert not PROOF.exists() and not SHEET.exists()
    staged, offline = map(base.load, (stage.PROOF, NATIVE))
    _, old, new, arm, kanji, source, previous_table, table, painter = assets()
    paths = [ROOT.with_name("tavern_round_digits_20261120") / "before/capture/capture_report.json",
             ROOT / "after/capture/capture_report.json"]
    reports = [base.load(path) for path in paths]
    original = base.load(stage.tavern.ROOT / "capture/capture_report.json")
    schedule = [row for row in original["scripted_input_schedule"] if row["start"] < replay.FRAMES[-1]]
    before_arm = old.read_file(stage.ARM)
    assert offline["candidate_sha256"] == staged["candidate_sha256"] == base.digest(stage.ROM)
    assert reports[0]["core_DLL_sha256"] == reports[1]["core_DLL_sha256"]
    assert reports[0]["core_options"] == reports[1]["core_options"]
    for report, digest in zip(reports, (staged["parent_sha256"], staged["candidate_sha256"]), strict=True):
        assert report["ROM_sha256"] == digest and report["frames"] == replay.FRAMES[-1]
        assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
        assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
        assert report["scripted_input_schedule"] == schedule and report["exact_requested_capture_frames"] == list(replay.FRAMES)
    addresses = [unpack_from("<I", arm, at)[0] - BASE for at in (0x5444C, 0x54450)]
    evidence = {str(p): base.digest(p) for p in (*paths, stage.tavern.OUTPUT, NATIVE)}
    comparison, rows = Image.new("RGB", (1032, 208 * 2), "#263238"), []
    labels = ImageDraw.Draw(comparison)
    read_snapshots = []
    for frame in replay.FRAMES:
        pair = [one_frame(r, frame) for r in reports]
        images = [p[1] for p in pair]
        diff = ImageChops.difference(*images).getbbox()
        if frame in CONFIRMATIONS:
            assert diff and 16 <= diff[0] < diff[2] <= 244 and 296 <= diff[1] < diff[3] <= 360
        else:
            assert diff is None, (frame, diff)
        evidence.update({p[0]["path"]: p[0]["PNG_sha256"] for p in pair})
        heard = []
        if frame in HOLDS:
            n, amounts = HOLDS[frame]
            for side, (report, image, code) in enumerate(zip(reports, images, (before_arm, arm), strict=True)):
                snap, ram = capture_ram(report, frame)
                read_snapshots.append(snap)
                paragraph, wrapped = [ram[at:at+256].split(b"\0", 1)[0] for at in addresses]
                if frame in CONFIRMATIONS and side == 0:
                    rendered_args = ("２６８",)
                else:
                    rendered_args = amounts
                assert paragraph == table[n].text % tuple(a.encode("cp932") for a in rendered_args), (frame, paragraph)
                assert b" ".join(wrapped.split()) == paragraph.strip(), (frame, wrapped)
                plane, glyphs = render_portrait(painter, code, kanji, wrapped.replace(b"\r", b""))
                native_hold(image, plane)
                assert [g["code"] for g in glyphs] == glyph_codes(wrapped)
                heard.append(dict(paragraph_hex=paragraph.hex(), wrapped_hex=wrapped.hex(), complete_glyphs=True))
                if frame in CONFIRMATIONS:
                    x, y = side * 516, CONFIRMATIONS.index(frame) * 208
                    labels.text((x + 6, y + 3), f"{('Before', 'Regular digits')[side]} / {'Cancel' if frame == 25630 else 'Accept'}", fill="white")
                    panel = image.crop((0, 284, 256, 380)).resize((512, 192), Image.Resampling.NEAREST)
                    comparison.paste(panel, (x + 2, y + 14))
        rows.append(dict(frame=frame, changed_body_bounds=diff, after_and_before_matching_text=heard))
    for report, code in zip(reports, (before_arm, arm), strict=True):
        for frame, amount in ((24550, 34980), (25960, 34980), (28220, 34712)):
            snap, raw = capture_ram(report, frame)
            assert wallet(code, raw) == amount
            read_snapshots.append(snap)
    evidence.update({row["path"]: row["sha256"] for row in read_snapshots})
    assert len(rows) == len(replay.FRAMES)
    following = []
    for n in (866, 872, 874, 880):
        prior = next(r for r in base.load(stage.tavern.OUTPUT)["records"] if r["message_ID"] == n)
        assert prior["current_hex"] == previous_table[n].text.hex() == table[n].text.hex()
        assert prior["source_hex"] == source[n].text.hex()
        following.append(prior | {"id": f"COMMON_MESSAGE_{n}", "file_path": stage.COMMON,
            "speaker": {866: "Lil", 872: "Barkeep", 874: "Patron", 880: "Patron"}[n], "decision": "retention",
            "context": "The approved Tavern round leads to the request, announcement, thanks and a tip.",
            "current_reference": batch.reference(previous_table[n]),
            "final_reference": batch.reference(table[n]), "final_hex": table[n].text.hex(),
            "review": dict.fromkeys(batch.GATES, True)})
    comparison.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], parent_sha256=staged["parent_sha256"],
        records=offline["records"] + following, observed_holds=rows, physically_identical_other_samples=True,
        declined_wallet=34980, accepted_wallet=34712, price=268, ordinary_Amsterdam_gameplay=True,
        sheets={str(SHEET): base.digest(SHEET), **{p["path"]: p["sha256"] for p in offline["sheets"]}},
        evidence=evidence, hardware=False))
    print("Verified the complete confirmation, wallet, ordinary menu returns and Clifford's Bristol rumor.")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("native", "getter", "gameplay"))
    globals()[parser.parse_args().mode]()
