"""Check the exact displayed names, revised pages, and retained source symbols."""

from pathlib import Path
from types import FunctionType

from scripts import stage_hodram_B65_B70_20261122 as stage
from scripts import verify_hodram_B61_B64_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels_v2.json"
OPAQUE = ROOT / "retained_source_symbols.json"
SOURCE_DISPLAY = Path("work/analysis/Hodram_B61_B70_source_display_v8881/"
                      "224_complete_source_dispatches_alignments_pages_andmacro_binding.json")
SYMBOLS = {f"DK4_MES_B65_R{index:04d}" for index in (6, 18, 22, 38, 42, 116)}
CONTEXT_SHORT_NAMES = {
    "DK4_MES_B65_R0071": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B67_R0084": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B69_R0019": ("Lil", "Lil Argot"),
}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verification = checked_text(previous.verification, {
    'len(entries) == 96': 'len(entries) == 128',
    '"hodram_B61_B64_progressive"': '"hodram_B65_B70_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the short nameplate. Sera and Camille use the runtime given name in direct address.",
        2: "Lil Argot is the nameplate. Camille calls her Lil at the reunion, where she takes him back aboard.",
        3: "Maria Li is the header. She gives the full approved Maria Huamei Li when Hodram asks her identity.",
        9: "Camille Overijssel is the approved identity. The speakers addressing him use Camille.",
        10: "Xien Yan is the established nameplate. His polite invitation withholds whom Hodram is going to meet.",
        16: "Gerhard Adernkatz is the officer who asks whether Hodram is sure and later reports the recovered assets.",
        18: "Charles Rochefort has the final silent reaction as Hodram lets Sera go.",
        23: "Manuel Almeida has his own silent reaction in the farewell.",
        24: "Sera Shahrbaraz is the short header. The source symbols are restricted to her exchanges with Sirwood.",
        78: "Sirwood Eme is the nameplate. Sera's immediate reaction uses his given name Sirwood.",
        116: "Port Worker keeps the source occupation. His familiar address to Camille adds no kinship or title.",
    }
''',
})


def verify_retained_symbols():
    audit, stored = map(base.load, (SOURCE_DISPLAY, PROOF))
    image = base.NdsImage.open(stage.ROM)
    assert native.digest(image.read_file("/GRP/KANJI.FNT")) == audit["font_sha256"]
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    installed = {row["id"]: row for row in stored["records"]}
    qualifications = {}
    for row in audit["records"]:
        ident = row["id"]
        if ident not in SYMBOLS:
            continue
        command, = installed[ident]["stored_pages"]
        exact = bytes.fromhex(command["stored"])
        body = bytes.fromhex(row["source_hex"])
        assert command["stored"] == command["current"] and exact[:5] == b"\x00\x40\xff\xff\x00"
        assert body == exact[5:exact.index(0, 6)] and installed[ident]["body_hex"] == body.hex()
        rendered = row["complete_native_source_display"]
        page, = rendered["pages"]
        assert rendered["complete_consumed_bytes"] == len(body) - 1
        assert page["consumed_hex"] == body[1:].hex() and page["native_independent_plane_equal"]
        assert page["all_bitmap_header_input_canaries_exact"]
        plane = Path(page["native_plane"])
        assert base.digest(plane) == page["native_plane_sha256"]
        qualifications[ident] = dict(
            source_reference=row["source_reference"], exact_body_hex=body.hex(),
            current_command_offset=command["stored_offset"], plane=str(plane), plane_sha256=base.digest(plane))
    assert set(qualifications) == SYMBOLS
    base.save(OPAQUE, dict(candidate_sha256=stored["candidate_sha256"], historical_font_sha256=audit["font_sha256"],
        historical_source_proof=str(SOURCE_DISPLAY), historical_source_proof_sha256=base.digest(SOURCE_DISPLAY),
        records=qualifications, require_current_emulator_mask_comparison=True))


scope = previous.scope | globals()
for source in (verification, names):
    exec(compile(source, __file__ + "::native-pages", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
    if not OPAQUE.exists():
        verify_retained_symbols()
