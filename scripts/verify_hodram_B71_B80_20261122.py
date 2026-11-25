"""Verify progressive pages, modal notices, and exact symbol and name data."""

from pathlib import Path
from types import FunctionType

from scripts import stage_hodram_B71_B80_20261122 as stage
from scripts import verify_hodram_B54_B60_20261122 as panel_template
from scripts import verify_hodram_B65_B70_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
OPAQUE = ROOT / "retained_source_symbols.json"
SYMBOLS = {f"DK4_MES_B80_R{n:04d}" for n in (26, 37, 41)}
HISTORICAL = Path("work/analysis/Hodram_B71_B80_stored_20261101/stored_native_verification.json")
CONTEXT_SHORT_NAMES = {
    "DK4_MES_B72_R0121": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B77_R0012": ("Gerhard", "Gerhard Adernkatz"),
    "DK4_MES_B79_R0049": ("Barbarossa", "Barbarossa Hayreddin"),
    "DK4_MES_B80_R0080": ("Hodram", "Hodram Bergstrom"),
}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verification = checked_text(previous.verification, {
    'len(entries) == 128 and fe_count == 0': 'len(entries) == 144 and fe_count == 4',
    '"hodram_B65_B70_progressive"': '"hodram_B71_B80_progressive"',
})
panels = checked_text(panel_template.panels, {"len(panels) == 1": "len(panels) == 4"})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom remains the short header. Maria uses the running surname; Sera and Sirwood use the given name.",
        3: "Maria Li is the nameplate for the woman summoning Hodram and later warning him. The messenger uses Admiral Maria Li when identifying her.",
        10: "Xien Yan remains the approved nameplate for the intermediary who ushers Hodram to Admiral Li.",
        16: "Gerhard Adernkatz can bring and read the same letter as Charles. He speaks in his own formal register outside the quotation.",
        18: "Charles Rochefort is the alternative reader. His spoken introduction and closing need not match Gerhard's.",
        24: "Sera Shahrbaraz keeps the same short header when she returns to help and when she speaks with her compatriots.",
        34: "Barbarossa Hayreddin is the current header. The port worker and Hodram use Hayreddin in their own dialogue.",
        43: "Diogo Escante is the established name. The notices and Hodram refer to him by his surname.",
        78: "Sirwood Eme remains the nameplate. He calls Hodram by the runtime given name and continues in the original symbols.",
        115: "Port Worker identifies the source role of the man reporting the navy's defeat of Hayreddin.",
        156: "Sailor identifies the original messenger role without adding a rank to the emissary.",
    }
''',
})


def verify_retained_symbols():
    old, rendered = map(base.load, (HISTORICAL, PROOF))
    historical_native = Path(old["native"])
    assert base.digest(historical_native) == old["native_sha256"]
    image = base.NdsImage.open(stage.ROM)
    assert base.digest(stage.ROM) == rendered["candidate_sha256"]
    assert native.digest(image.read_file("/GRP/KANJI.FNT")) == base.load(historical_native)["font_sha256"]
    ctx = scope["current_runtime"](image)
    expand = scope["display"].original_expander()
    verified = {r["id"]: r for r in rendered["records"]}
    result = {}
    for row in old["records"]:
        ident = row["id"]
        if ident not in SYMBOLS:
            continue
        command, = verified[ident]["stored_pages"]
        assert command["current"] == command["stored"]
        exact = bytes.fromhex(verified[ident]["body_hex"])
        assert exact.hex() == row["stored_hex"]
        clean = bytes.fromhex(command["source"])
        source = clean[5:clean.index(0, 6)]
        assert source.replace(b"\n", b" ") == exact
        cases = ctx.execute(expand, exact[1:], exact[0])["cases"]
        assert len(cases) == 4 and {r["output_hex"] for r in cases} == {row["expanded_hex"]}
        page, = row["directly_viewed_planes"]
        assert base.digest(page["path"]) == page["sha256"]
        result[ident] = dict(exact_body_hex=exact.hex(), default_expanded_hex=row["expanded_hex"],
                             plane=page["path"], plane_sha256=page["sha256"], source_hex=source.hex(), alignment_cases=cases)
    assert set(result) == SYMBOLS
    base.save(OPAQUE, dict(candidate_sha256=rendered["candidate_sha256"], records=result,
        reference=str(HISTORICAL), reference_sha256=base.digest(HISTORICAL),
        exact_font_match=True, require_current_emulator_mask_comparison=True))


scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::native-pages", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
    if not OPAQUE.exists():
        verify_retained_symbols()
