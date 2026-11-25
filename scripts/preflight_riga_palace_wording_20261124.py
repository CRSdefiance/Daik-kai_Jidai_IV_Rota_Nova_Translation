"""Check the revised Palace reply through the existing native portrait path."""

from scripts import preflight_nagasaki_contract_wrap_20261124 as palace
from scripts import stage_recruit_crew_20261120 as recruit
from scripts import verify_riga_town_services_20261124 as observed
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, digest, read, reference, sha256, write
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment

KEY = 1160
OUT = observed.OUT.with_name("riga_palace_wording_preflight_20261124.json")


def main():
    active = observed.play.current
    release, live = map(read, (active.RELEASE, observed.OUT))
    assert release["candidate_sha256"] == live["candidate_sha256"] == digest(active.ROM)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    starter = read(release["own_registered_startup"])
    ctx = RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=starter["actual_captain_getter"])
    entries = recruit.catalogue(ctx.arm, ctx.common)
    old = entries[KEY]
    finding, = [row for row in live["dialogue_records"] if row["message_ID"] == KEY]
    assert old.text.hex() == finding["current_reference"]["exact_hex"]
    assert old.text.startswith(b" ") and b"%" not in old.text
    proposal = finding["proposed_English"]
    revised = (" " + proposal).encode("ascii").ljust(len(old.text), b" ")
    assert len(old.text) == len(revised) and b"\n" not in revised and b"%" not in revised
    deployed, installed, allocations = owned_deployment(ctx.common, ctx.arm, entries, {KEY: revised})
    assert {a.message_id for a, b in zip(entries, installed, strict=True) if a != b} == {KEY}
    reverted, _, _ = owned_deployment(deployed, ctx.arm, installed, {KEY: old.text})
    assert bytes(reverted) == ctx.common
    target = with_components(ctx, ctx.arm, deployed)
    cpu, get, provider = target.machine(ctx.arm, deployed, target.raw, target.plan)
    addr = get(0x5528C, KEY)
    assert bytes(cpu.mem_read(addr, len(revised) + 1)) == revised + bytes(1) and provider.reads
    bindings = {r["message_id"]: r for r in read(palace.BINDINGS)["records"]}
    native_binding = bindings[KEY]["native_binding"]
    assert native_binding["parent"] == 0x02054014 and native_binding["table_or_ID"] == 0
    assert finding["observed"]["requests"][0]["caller_LR"] == 0x02053FF8
    formatter = palace.native_format()
    painter, _, _ = recruit.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    pages, results = [], {}
    for label, content in (("current", old.text), ("proposed", revised)):
        row = dict(message_id=KEY, english=content[1:].decode("ascii"), native_binding=native_binding,
                   English_argument_source_indices=[])
        result = formatter(cpu, row, ())
        formatted = bytes.fromhex(result["formatted_hex"])
        plane, glyphs = recruit.render_portrait(painter, ctx.arm, kanji, formatted)
        codes = [glyph["code"] for glyph in glyphs]
        assert codes == recruit.glyph_codes(formatted) and (codes[0], codes[-1]) == (ord("H"), ord("."))
        assert not result["findings"] and len(result["lines"]) == 2
        pages.append((f"{KEY} / {label}", plane))
        results[label] = result | dict(ink_plane_sha256=sha256(bytes(plane)).hexdigest())
    assert results["current"]["lines"] == finding["actual_lines"]
    assert results["proposed"]["lines"] == ["Hmm. You've shown admirable spirit.", "I commend you."]
    other = entries[1151].text.decode("ascii").strip()
    alternate = formatter(cpu, dict(message_id=1151, english=other, native_binding=bindings[1151]["native_binding"],
                                     English_argument_source_indices=[0]), (b"Bergstrom",))
    assert alternate["lines"][-2:] == ["don't even have a trading", "contract here."]
    path = OUT.with_suffix("")
    path.mkdir(exist_ok=True)
    sheets = recruit.portrait_sheets(path, pages)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], original_gameplay=reference(observed.OUT),
        historical_bindings=reference(palace.BINDINGS), record=finding,
        proposed_reference=observed.panels.text_reference(installed[KEY]) | dict(exact_hex=revised.hex()),
        exact_inverse=True, fixed_allocation=allocations[KEY], native_binding=native_binding, cases=results, sheets=sheets,
        alternate_1151=dict(layout=alternate, current_English=other, argument="Bergstrom"),
        revised_gameplay_observed=False, ROM_changed=False, new_editorial_credit=0))
    print("Verified the proposed two-line reply and reproduced the separate trading-contract break in COMMON 1151.")


if __name__ == "__main__":
    main()