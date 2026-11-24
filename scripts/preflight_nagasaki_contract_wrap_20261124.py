"""Preflight one logical Palace paragraph through its registered consumer."""

from inspect import getsource
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import probe_tavern_continuation_layout_v768 as formatter
from scripts import verify_nagasaki_market_20261124 as market
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import GATES, digest, read, reference, sha256, write
from scripts.stage_tavern_nearby_town_wrap_20261123 import town


OUT = market.OUT.with_name("nagasaki_contract_wrap_preflight_20261124.json")
ROOT = market.played.ROOT / "contract_preflight"
BINDINGS = Path("translations/palace_inn_contextual_editorial_manuscript_v1.json")
KEY = 1157
PROPOSAL = "Your fee sets your market share. How much will you offer?"


def native_format():
    source = checked_text(getsource(formatter.format_case), {
        "    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)": """    binding = row['native_binding']
    for at, value in ((0x264, binding['parent']), (0x270, 0), (0x274, row['message_id']), (0x27C, binding['table_or_ID'])):
        u.mem_write(STACK + at, struct.pack('<I', value))
    call(u, WRAP_ENTRY - BASE, (wrapped, output, 0), instruction_limit=2000000)""",
    })
    scope = vars(formatter) | dict(WRAP_ENTRY=0x01FFCF3C)
    exec(compile(source, __file__ + "::palace-native-formatter", "exec"), scope)
    return scope["format_case"]


def main():
    active = market.played.current
    release, gameplay = map(read, (active.RELEASE, market.OUT))
    assert digest(active.ROM) == release["candidate_sha256"] == gameplay["candidate_sha256"]
    finding, = [row for row in gameplay["observed_dialogue"] if row["message_ID"] == KEY]
    assert finding["decision"] == "wrap finding" and finding["substitution_values"] == []
    historical, = [row for row in read(BINDINGS)["records"] if row["message_id"] == KEY]
    assert historical["native_binding"]["parent"] == 0x02054014 and historical["native_binding"]["table_or_ID"] == 0
    ctx = RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=3)
    baseline = market.common_rows(ctx.common, ctx.arm)
    original = baseline[KEY].text
    assert original.decode("ascii") == finding["current_English"] and original.startswith(b" ") and b"%" not in original
    revised = (" " + PROPOSAL).encode("ascii").ljust(len(original), b" ")
    assert len(revised) == len(original) and b"\n" not in revised and b"%" not in revised
    _, installed, slots = town.owned_deployment(ctx.common, ctx.arm, baseline, {KEY: revised})
    assert [new.message_id for old, new in zip(baseline, installed, strict=True) if old != new] == [KEY]
    assert installed[KEY].text == revised and slots[KEY]["new_null_fields"] == 0
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    layout = native_format()
    painter, _, _ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    record = dict(id=f"COMMON_MESSAGE_{KEY}", message_id=KEY, file_path=active.COMMON, speaker=finding["speaker"],
        context="The Daimyo has quoted the minimum fee. This panel explains how the offer affects market share before amount entry.",
        source_meaning=historical["source_meaning"], localization_note="The preceding panel already names the contract fee. A direct first sentence leaves the ruler's complete question together.",
        native_binding=historical["native_binding"], English_argument_source_indices=[], english=PROPOSAL,
        review=dict.fromkeys(GATES, True))
    cases, figures = [], []
    for label, payload in (("Current", original), ("Proposed", revised)):
        result = layout(cpu, record | dict(english=payload[1:].decode("ascii")), ())
        data = bytes.fromhex(result["formatted_hex"])
        plane, glyphs = town.render_portrait(painter, ctx.arm, kanji, data)
        codes = [g["code"] for g in glyphs]
        assert codes == town.glyph_codes(data) and (codes[0], codes[-1]) == (ord("Y"), ord("?"))
        assert not result["findings"] and 1 <= len(result["lines"]) <= 4
        cases.append(dict(label=label, native_plane_sha256=sha256(bytes(plane)).hexdigest(), layout=result))
        figures.append((label, plane))
    assert cases[0]["layout"]["lines"] == finding["observed_lines"]
    assert cases[1]["layout"]["lines"] == ["Your fee sets your market share.", "How much will you offer?"]
    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", records=[record],
                      encoder="dialogue-relocatable-v1", review_gates=list(GATES))
    validate_natural_dialogue_batch(manuscript)
    ROOT.mkdir(exist_ok=True)
    sheets = town.portrait_sheets(ROOT, figures)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], key=KEY, manuscript=manuscript,
        original_dialogue=finding, proposed_storage_hex=revised.hex(), fixed_slot=slots[KEY],
        native_cases=cases, sheets=sheets, existing_binding=reference(BINDINGS), original_gameplay=reference(market.OUT),
        revised_gameplay_verified=False, ROM_changed=False, new_editorial_credit=0))
    print("COMMON 1157 uses two complete native lines, with the original fixed allocation and zero runtime arguments.")


if __name__ == "__main__":
    main()
