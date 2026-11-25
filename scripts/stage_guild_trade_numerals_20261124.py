"""Stage the four remaining Guild item-price exchanges with regular digits."""

from inspect import getsource
from pathlib import Path
from struct import pack, unpack_from

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.yard_numerals_20261124 import BASE, HELPER, ITCM, NUMBER, compact_helper
from scripts import observe_seoul_guild_trade_20261124 as play
from scripts import stage_london_guild_display_20261124 as london
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write


native, active, panels = london.native, play.active, london.panels
ARM, COMMON = london.ARM, london.COMMON
ROOT = Path(".codex-release-work/guild_trade_numerals_20261124")
ROM = ROOT / "Guild_Trade_Numerals_STAGED.nds"
OUT = panels.OUT.with_name("guild_trade_numerals_preflight_20261124.json")
PRICE_CALLS = {1072: 0x0205C3F4, 1083: 0x0205C340, 1086: 0x0205BEF4, 1095: 0x0205BFA0}
QUOTE_WRAPPER, REPLY_WRAPPER = 0x02053F9C, 0x02053FE4
RANGES = {1072: "buy", 1083: "buy", 1086: "sale", 1095: "sale"}
PROSE = {
    1072: ("Can you even afford %s coins?", "The Guildmaster gives the price and doubts that the player can pay it.",
           "The amount stays explicit and even keeps the Guildmaster's skeptical tone within one complete question."),
    1083: ("Fine. %s coins it is.", "The Guildmaster reluctantly accepts the lower purchase price.",
           "Fine preserves the concession. The complete amount remains together with the agreement after bargaining."),
    1086: ("Hmm... How about %s coins?", "The Guildmaster considers the selected item and proposes a sale price for the player to accept.",
           "The appraisal pause comes before a complete offer. The item is already selected and the player still decides."),
    1095: ("All right... I'll pay %s coins.", "The Guildmaster yields and offers the revised amount for the player's item.",
           "The pause keeps the reluctant agreement. I'll pay makes the direction of the sale explicit."),
}
CONTEXT = "The Guildmaster quotes a price, may react to affordability or bargaining, and waits for the transaction decision."


def patch_arm(clean, arm):
    # These three calls take the ID from a literal. The insufficient-funds
    # branch takes the original 1072 initialized earlier in the same function.
    for offset, key in ((0x5C09C, 1086), (0x5C0B0, 1095), (0x5C47C, 1083)):
        assert unpack_from("<I", arm, offset)[0] == key and arm[offset:offset + 4] == clean[offset:offset + 4]
    assert arm[0x5C204:0x5C20C] == clean[0x5C204:0x5C20C] == assemble("mov r0,#1072; str r0,[sp,#0x1c]", 0x0205C204)
    for key, caller, wrapper in ((1072, 0x0205C404, REPLY_WRAPPER), (1083, 0x0205C350, REPLY_WRAPPER),
                                  (1086, 0x0205BF04, QUOTE_WRAPPER), (1095, 0x0205BFB0, REPLY_WRAPPER)):
        lo, hi = PRICE_CALLS[key] - BASE, caller - BASE + 4
        assert arm[lo:hi] == clean[lo:hi] and arm[hi - 4:hi] == assemble(f"bl {wrapper}", caller)
    assert arm[london.BUY_CALL - BASE:london.BUY_CALL - BASE + 4] == assemble(f"bl {HELPER}", london.BUY_CALL)
    itcm = native.patch.MainCodeFile(arm, BASE).sections[4]
    helper = compact_helper()
    assert itcm.ramAddress == ITCM and bytes(itcm.data[HELPER - ITCM:HELPER - ITCM + len(helper)]) == helper
    assert arm[NUMBER - BASE:NUMBER - BASE + 0x7C] == clean[NUMBER - BASE:NUMBER - BASE + 0x7C]
    target = bytearray(arm)
    edits = []
    for key, address in PRICE_CALLS.items():
        offset = address - BASE
        before, after = assemble(f"bl {NUMBER}", address), assemble(f"bl {HELPER}", address)
        assert arm[offset:offset + 4] == before and len(before) == len(after) == 4
        target[offset:offset + 4] = after
        edits.append(dict(message_ID=key, address=address, previous_hex=before.hex(), installed_hex=after.hex()))
    assert native.patch.cache_plan(bytes(target)) == native.patch.cache_plan(arm)
    return bytes(target), edits


def native_cases(runtime, arm, edits, previous, revised):
    src = checked_text(getsource(native.formatters.layout), {
        "else 0x02053FCC if n in YESNO else": "else 0x02053FCC if n in GUILD_CHOICES else",
    })
    scope = vars(native.formatters) | dict(GUILD_CHOICES=(1073, 1086))
    exec(compile(src, __file__ + "::Guild-price-layout", "exec"), scope)
    fmt = scope["layout"]
    raw = bytearray(runtime.raw)
    for row in edits:
        at = row["address"] - BASE
        assert raw[at:at + 4].hex() == row["previous_hex"]
        raw[at:at + 4] = arm[at:at + 4]
    cpus = native.get_machine(runtime.arm, runtime.raw)[0], native.get_machine(arm, bytes(raw))[0]
    ring, size = london.RING, london.RING_SIZE
    initial = bytes(cpus[0].mem_read(ring, size))
    assert initial == bytes(cpus[1].mem_read(ring, size))

    price = read(london.PRICE)
    assert all(sha256(runtime.arm[a:b]).hexdigest() == p["sha256"] for p in price["source_clean_exact_spans"] for a, b in (p["span"],))
    domains = price["source_native_price_ranges"]
    raster, _, _ = native.portraits.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    totals, history, pages = {}, {}, []
    for key, site in PRICE_CALLS.items():
        category = RANGES[key]
        limits = [min(p[f"{category}_min"] for p in domains), max(p[f"{category}_max"] for p in domains)]
        assert limits == ([90, 420000] if category == "buy" else [80, 378000])
        samples = sorted({p[f"{category}_{side}"] for p in domains for side in ("min", "max")}
                         | {99, 100, 999, 1000, 6160, 7700, 9999, 10000, 99999, 100000})
        cases = {}
        for i, amount in enumerate(samples):
            slot = i % 32
            for cpu in cpus:
                cpu.mem_write(ring, initial[:8] + pack("<I", slot) + initial[12:])
            (p, old), (q, new) = (native.call_number(cpu, site, amount) for cpu in cpus)
            assert p == q and london.normalize(old) == new == str(amount).encode("ascii")
            a, b = p - ring, p - ring + len(old) + 1
            lo = 12 + 128 * slot
            assert lo <= a < b <= lo + 128
            before_ring, after_ring = (bytes(cpu.mem_read(ring, size)) for cpu in cpus)
            assert before_ring[:a] == after_ring[:a] and before_ring[b:] == after_ring[b:]
            result = fmt(cpus[1], revised[key].text, key, (new,))
            assert result["lines"] == [PROSE[key][0] % amount] and not result["findings"]
            cases[amount] = result
            if amount in (*limits, 6160):
                historical = fmt(cpus[0], previous[key].text, key, (old,))
                history[key, amount] = historical
                body = bytes.fromhex(result["formatted_hex"])
                plane, points = native.portraits.render_portrait(raster, arm, kanji, body)
                assert points and all(0 <= point["x"] < 228 and 0 <= point["y"] < 48 for point in points)
                pages.append((f"{key} at {amount}", plane))
        totals[key] = cases
    return totals, history, pages


def main():
    release = read(active.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    ctx = RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=3)
    clean = NdsImage.open(CLEAN)
    original = clean.read_file(ARM)
    source = london.common_message_entries(clean.read_file(COMMON), original)
    previous = native.yard.common_rows(ctx.common, ctx.arm)
    target, edits = patch_arm(original, ctx.arm)
    assert active.template.right_bound(target, release["right_bound_configuration"])["matched_repair_spans"] == 8
    compiled = {key: (b" " + row[0].encode("ascii")).ljust(len(previous[key].text), b" ") for key, row in PROSE.items()}
    for key, body in compiled.items():
        assert len(body) == len(previous[key].text) and b"\n" not in body and b"\0" not in body
        assert source[key].text.count(b"%s") == previous[key].text.count(b"%s") == body.count(b"%s") == 1
    common, after, allocations = london.owned_deployment(ctx.common, target, previous, compiled)
    assert [b.message_id for a, b in zip(previous, after, strict=True) if a != b] == sorted(PROSE)
    assert after[1073] == previous[1073]
    cases, history, pages = native_cases(ctx, target, edits, previous, after)
    records = [dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker="Guildmaster", context=CONTEXT,
                   clean_Japanese=source[key].text.decode("cp932"), source_meaning=meaning, previous_English=previous[key].text.decode("ascii").strip(),
                   english=english, localization_note=reason, source_reference=london.exact_row(source[key]),
                   current_reference=london.exact_row(previous[key]), staged_reference=london.exact_row(after[key]),
                   decision="revision", review=dict.fromkeys(GATES, True)) for key, (english, meaning, reason) in PROSE.items()]
    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
                      review_gates=list(GATES), records=records)
    validate_natural_dialogue_batch(manuscript)
    ctx.image.replace_file(ARM, target)
    ctx.image.replace_file(COMMON, common)
    image = bytes(ctx.image.rom.save())
    ctx.image.replace_file(ARM, ctx.arm)
    ctx.image.replace_file(COMMON, ctx.common)
    assert sha256(ctx.image.rom.save()).hexdigest() == release["candidate_sha256"]
    ROOT.mkdir()
    ROM.write_bytes(image)
    final = NdsImage.open(ROM)
    assert final.read_file(ARM) == target and final.read_file(COMMON) == common
    visuals = OUT.with_suffix("")
    visuals.mkdir(exist_ok=True)
    sheets = native.portraits.portrait_sheets(visuals, pages)
    write(OUT, manuscript | dict(candidate=reference(ROM), predecessor=reference(active.ROM), clean_input=reference(CLEAN),
        target_ARM9_sha256=sha256(target).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        exact_ARM9_edits=edits, allocations=allocations, prior_price_proof=reference(london.PRICE),
        quote_cases=cases, prior_cases=[dict(message_ID=key, amount=amount, display=row) for (key, amount), row in history.items()],
        sheets=sheets, whole_parent_inverse=True, ordinary_replay_pending=True, registered=False, new_editorial_credit=0))
    print(f"Staged four Guild price corrections after {sum(map(len, cases.values()))} native substitution and layout cases. {digest(ROM)}")


if __name__ == "__main__":
    main()
