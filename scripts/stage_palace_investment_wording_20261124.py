"""Stage two source-reviewed military investment lines through the Palace consumer."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import preflight_riga_palace_wording_20261124 as earlier
from scripts import register_riga_recruitment_20261124 as parent
from scripts import stage_tunis_shop_advice_20261124 as release_checks
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, GATES, NdsImage, digest, read, reference, sha256, write

ARM, COMMON = parent.ARM, parent.COMMON
ROOT = parent.ROM.parent.with_name("editorial_20261124_palace_investment_wording")
ROM = ROOT / "Palace_Investment_Wording_STAGED.nds"
OUT = ROOT / "palace_investment_wording_native.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
played = SimpleNamespace(RELEASE=parent.RELEASE)
KEYS = 1151, 1160
GREETING = "Even without a trading contract, you offer to help defend our city. Most generous, %s."
ADDRESSES = ("Li", "Argot", "Pereira", "Bergstrom", "A" * 16, "W" * 19)


def main():
    release = read(parent.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"]
    previous = read(earlier.OUT)
    assert previous["candidate_sha256"] == release["candidate_sha256"]
    assert digest(previous["original_gameplay"]["path"]) == previous["original_gameplay"]["sha256"]
    starter = read(release["own_registered_startup"])
    ctx = earlier.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=starter["actual_captain_getter"])
    old = earlier.recruit.catalogue(ctx.arm, ctx.common)
    assert sha256(ctx.common).hexdigest() == release["target_COMMON_sha256"]
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = earlier.recruit.batch.common_message_entries(clean.read_file(COMMON), clean_arm)
    historical = {r["message_id"]: r for r in read(earlier.palace.BINDINGS)["records"]}
    drafts = {1151: GREETING, 1160: previous["record"]["proposed_English"]}
    assets = {key: (" " + text).encode("ascii").ljust(len(old[key].text), b" ") for key, text in drafts.items()}
    count = {1151: 1, 1160: 0}
    for key, data in assets.items():
        assert data.isascii() and len(data) == len(old[key].text) and b"\n" not in data
        for text in (source[key].text, old[key].text, data):
            assert text.count(b"%") == text.count(b"%s") == count[key]
        assert source[key].text.hex() == historical[key]["source_hex"]
    assert assets[1160].hex() == previous["proposed_reference"]["exact_hex"]
    assert old[1160].text.hex() == previous["record"]["current_reference"]["exact_hex"]
    changed, new, allocations = earlier.owned_deployment(ctx.common, ctx.arm, old, assets)
    assert {a.message_id for a, b in zip(old, new, strict=True) if a != b} == set(KEYS)
    assert all(slot["new_null_fields"] == 0 for slot in allocations.values())
    reverted, _, _ = earlier.owned_deployment(changed, ctx.arm, new, {key: old[key].text for key in KEYS})
    assert bytes(reverted) == ctx.common
    target = earlier.with_components(ctx, ctx.arm, changed)
    cpu, get, provider = target.machine(ctx.arm, changed, target.raw, target.plan)
    painter, _, _ = earlier.recruit.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    format_case = earlier.palace.native_format()
    text_reference = earlier.observed.panels.text_reference
    prose, pages = [], []
    for key, text in drafts.items():
        binding = historical[key]["native_binding"]
        assert binding["parent"] == 0x02054014 and binding["table_or_ID"] == 0
        data = assets[key]
        assert bytes(cpu.mem_read(get(0x5528C, key), len(data) + 1)) == data + bytes(1)
        row = dict(message_id=key, english=text, native_binding=binding, English_argument_source_indices=list(range(count[key])))
        cases = []
        for name in (ADDRESSES if count[key] else ("",)):
            args = (name.encode("ascii"),) if count[key] else ()
            result = format_case(cpu, row, args)
            expected = (text.encode("ascii") % args).decode("ascii")
            lines = result["lines"]
            assert " ".join(lines) == expected and not result["findings"]
            if key == 1151:
                assert lines == ["Even without a trading contract,", "you offer to help defend our city.", f"Most generous, {name}."]
            else:
                assert lines == previous["cases"]["proposed"]["lines"]
            rendered = bytes.fromhex(result["formatted_hex"])
            plane, glyphs = earlier.recruit.render_portrait(painter, ctx.arm, kanji, rendered)
            codes = [glyph["code"] for glyph in glyphs]
            assert codes == earlier.recruit.glyph_codes(rendered) and (codes[0], codes[-1]) == (ord(expected[0]), ord("."))
            cases.append(dict(address=name or None, layout=result, ink_plane_sha256=sha256(bytes(plane)).hexdigest()))
            pages.append((f"{key} / {name}" if name else str(key), plane))
        prose.append(row | dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, decision="revision",
            speaker="Palace ruler", context="The ruler greets the investor before the selected defense contribution and praises the completed investment.",
            source_meaning=historical[key]["source_meaning"],
            localization_note=("Keep the city's trading contract and the offer of help explicit. The ruler addresses the captain in his last approving clause."
                               if count[key] else "Retain the opening hesitation and the two beats of formal praise, with a direct commendation for the second beat."),
            clean_Japanese=source[key].text.decode("cp932"),
            source_reference=text_reference(source[key]) | dict(exact_hex=source[key].text.hex()),
            current_reference=text_reference(old[key]) | dict(exact_hex=old[key].text.hex()),
            installed_reference=text_reference(new[key]) | dict(exact_hex=new[key].text.hex()),
            review=dict.fromkeys(GATES, True) | dict(formatting=False), cases=cases))
    assert provider.reads
    ctx.image.replace_file(COMMON, changed)
    candidate = bytes(ctx.image.rom.save())
    ctx.image.replace_file(COMMON, reverted)
    assert sha256(ctx.image.rom.save()).hexdigest() == release["candidate_sha256"]
    ROOT.mkdir(exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == candidate
    else:
        with ROM.open("xb") as stream:
            stream.write(candidate)
    sheets = earlier.recruit.portrait_sheets(ROOT, pages)
    write(OUT, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=release["target_ARM9_sha256"],
        target_COMMON_sha256=sha256(changed).hexdigest(), exact_parent_reserialize=True,
        allocations=allocations, records=prose, sheets=sheets, native_pages=len(pages),
        reused_reply_proof=reference(earlier.OUT), retained_play_evidence=previous["original_gameplay"],
        translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US", review_gates=list(GATES),
        visual_review_complete=False, paired_gameplay_complete=False, registered=False))
    print(f"Staged {len(prose)} Palace text edits with {len(pages)} checked native pages and an exact complete-parent inverse.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", choices=("stage", "patch", "startup"), default="stage")
    action = parser.parse_args().action
    if action == "stage":
        main()
    else:
        FunctionType(release_checks.release_check.__code__, vars(release_checks) | globals())(read(OUT), action)