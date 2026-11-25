"""Bind ordinary Tunis shop talk to its source and check the wording revision."""

from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import observe_tunis_delicacy_shops_20261124 as played
from scripts import stage_square_trend_dialogue_20261115 as trend
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import read, reference, write


OUT = panels.OUT.with_name("tunis_shop_advice_preflight_20261124.json")
KEY = 654
DRAFT = "If you brought %s, please sell your stock at the Market soon."
HOLDS = {5800: KEY, 7000: 732, 7800: KEY, 8600: KEY, 9400: KEY}
REVIEW = {
    653: ("The named product is selling briskly.", "The exuberant sales idiom suits this separate trend response."),
    KEY: ("If the sailor has brought in the named good, the shopkeeper politely asks them to sell it soon at the Market.",
          "A complete conditional and please restore the courteous tone. Your stock works with both mass nouns and plural goods."),
    655: ("The shopkeeper rallies to sell the named good and earn a lot of money.",
          "Make a bundle expresses the original eagerness and the self-directed pep talk."),
    732: ("The shopkeeper thinks this trend will probably continue for a fair while.",
          "May and quite a while preserve the tentative forecast, which reads smoothly on a single line."),
}


def main():
    release = read(played.RELEASE)
    assert trend.base.digest(trend.CLEAN) == release["clean_input_sha256"]
    assert trend.base.digest(trend.base.REGISTRY) == release["registry_sha256"]
    # Reuse the established controller journal, donor, and observer checks.
    observed = SimpleNamespace(ROOT=played.ROOT.parent)
    capture_adapter = FunctionType(panels.capture.__code__, vars(panels) | {"observed": observed})
    frames, requests, gameplay = capture_adapter(played.ROOT.name, release)
    assert max(frames) == 10200
    ctx = trend.RegisteredRuntime(played.RELEASE, release["own_registered_startup"], captain=3)
    clean = trend.base.NdsImage.open(trend.CLEAN)
    ja_arm = clean.read_file(trend.ARM)
    source = trend.common_message_entries(clean.read_file(trend.COMMON), ja_arm)
    arm, common = ctx.arm, ctx.common
    assert arm[0x5FB54:0x5FC84] == ja_arm[0x5FB54:0x5FC84]
    old = trend.owned_entries(common, arm, trend.digest(arm[trend.DIRECTORY_OFFSET:trend.TABLE_OFFSET]))
    target, installed, slots = trend.owned_deployment(common, arm, old, {KEY: trend.compile_template(DRAFT, KEY)})
    assert all(a.text == b.text for a, b in zip(old, installed, strict=True) if a.message_id != KEY)
    assert old[KEY].text != installed[KEY].text
    runtime = trend.with_components(ctx, arm, target)
    cpu, get, provider = runtime.machine(arm, target, ctx.raw, ctx.plan)
    address = get(0x5528C, KEY)
    assert bytes(cpu.mem_read(address, len(installed[KEY].text) + 1)) == installed[KEY].text + b"\0"
    names = trend.products(cpu, get)
    raster, _, fonts = trend.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    font = GameAsciiFont.from_arm9(arm)
    cases, pages, live = [], [], []
    for index, name in names.items():
        case = trend.run_layout(cpu, KEY, installed[KEY].text, name)
        raw = bytes.fromhex(case["formatted_hex"])
        plane, glyphs = trend.render_portrait(raster, arm, kanji, raw)
        assert len(plane) == 228 * 64 and glyphs
        cases.append(dict(goods_index=index, goods=name, lines=case["lines"], formatted_hex=raw.hex(),
                          native_plane_sha256=trend.digest(plane)))
        pages.append((f"{KEY} / {index} / {name}", plane))
    assert len(cases) == len(pages) == 124 and provider.reads
    for frame, key in HOLDS.items():
        first, second = [call for call in requests if call["message_ID"] == key
                         and 0 < frame - call["frame"] < 400]
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
        args = "Whale Meat" if key == KEY else ""
        lines = trend.run_layout(cpu, key, old[key].text, args)["lines"]
        screen = panels.picture(frames[frame])
        live.append(dict(frame=frame, message_ID=key, lines=lines, complete_body_ink=panels.exact_body(font, lines, screen),
                         nameplate=panels.nameplate(font, "Shopkeeper", screen), native_requests=[first, second],
                         capture=frames[frame]))
    for frame in (4200, 10200):
        panels.find_mask(font, "Tunis", panels.picture(frames[frame]), (14, 14, 147, 31))
    root = OUT.with_suffix("")
    root.mkdir(parents=True, exist_ok=True)
    sheets = trend.portrait_sheets(root, pages)
    rows = []
    for key, (meaning, rationale) in REVIEW.items():
        ja, en, proposed = source[key], old[key], installed[key]
        assert ja.text.count(b"%s") == en.text.count(b"%s") == proposed.text.count(b"%s")
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker="Shopkeeper",
                         context="The shopkeeper reads the local market trend and offers a sales comment or forecast.",
                         source_meaning=meaning, Japanese=ja.text.decode("cp932"), localization_note=rationale,
                         decision="revision" if key == KEY else "retention",
                         english=" ".join(proposed.text.decode("ascii").split()),
                         file_path=trend.COMMON, source_reference=panels.text_reference(ja),
                         current_reference=panels.text_reference(en), proposed_reference=panels.text_reference(proposed),
                         source_hex=ja.text.hex(), current_hex=en.text.hex(), proposed_hex=proposed.text.hex(),
                         review=dict.fromkeys(trend.GATES, True) | {"formatting": key != KEY}))
    paired_captures = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT},
                                   argdefs=panels.sheets_for.__defaults__)
    observed_sheets = paired_captures("tunis_delicacy_shop_dialogue",
        [(f'{row["frame"]} / COMMON {row["message_ID"]}', panels.picture(row["capture"])) for row in live])
    write(OUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US", records=rows,
        candidate_sha256=release["candidate_sha256"], source_sha256=release["clean_input_sha256"],
        unchanged_ARM9_sha256=trend.digest(arm), proposed_COMMON_sha256=trend.digest(target),
        allocation=slots[KEY], ordinary_installed_holds=live, current_gameplay_sheets=observed_sheets,
        native_proposed_cases=cases, proposed_sheets=sheets, fonts=fonts, exact_gameplay=gameplay,
        source_refs=list(map(reference, (played.RELEASE, trend.MANUSCRIPT))),
        scope="The installed replay covers all three Delicacy Shops. Cases for the draft are offline only. "
              "Other trend branches and live testing of the proposed revision remain unvisited.",
        new_editorial_credit=0, ROM_changed=False))
    print(f"Verified {len(live)} ordinary Tunis holds and rendered {len(cases)} revised goods variants.")


if __name__ == "__main__":
    main()
