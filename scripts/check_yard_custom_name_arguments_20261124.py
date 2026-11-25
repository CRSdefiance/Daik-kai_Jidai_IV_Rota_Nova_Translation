"""Check mixed-width ship-name arguments on the registered Yard numeral build."""

from scripts import register_yard_numerals_20261124 as current
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, reference, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_yard_numerals_native_20261124 import layout_function, yard


OUT = yard.OUT.with_name("yard_custom_name_arguments_20261124.json")
NAMES = ("かもめ", "Sea あお", "あいうえおかきくけこ", "あいうえおかきくけこさ")


def main():
    receipt = read(current.RELEASE)
    assert digest(REGISTRY) == receipt["registry_sha256"]
    ctx = RegisteredRuntime(current.RELEASE, receipt["own_registered_startup"], captain=3)
    rows = yard.common_rows(ctx.common, ctx.arm)
    cpu, _ = get_machine(ctx.arm, ctx.raw)
    fmt = layout_function()
    cases = []
    for key in (803, 804):
        for name in NAMES:
            encoded = name.encode("cp932")
            price = b"2147483647 gold coins"
            values = (encoded, price, b"16 days") if key == 803 else (encoded, price)
            result = fmt(cpu, rows[key].text, key, values)
            assert name in " ".join(result["lines"]) and not result["findings"]
            assert sum(line.encode("cp932").count(encoded) for line in result["lines"]) == 1
            cases.append(dict(message_ID=key, stored=yard.panels.text_reference(rows[key]), input_name=name, nominal_name_bytes=len(encoded),
                native_layout=result, entire_name_on_one_line=True))
    write(OUT, dict(candidate_sha256=receipt["candidate_sha256"], reviewed_cases=cases,
        source=reference(current.RELEASE), native_input=ctx.receipt() | {"captain": 3},
        scope="Offline native printf and layout for synthetic stored names and an upper-bound price. No gameplay, artwork, or new glyph-plane claim."))
    print(f"Verified {len(cases)} exact custom-name layouts in the registered Yard build.")


if __name__ == "__main__":
    main()
