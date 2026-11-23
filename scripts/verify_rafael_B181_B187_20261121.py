"""Verify the stored story pages and the retained full-name reply to Aziza."""

from inspect import getsource

from scripts import stage_rafael_B181_B187_20261121 as stage
from scripts import verify_rafael_B161_B169_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
display = previous.display
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
FULL_NAME_ID = "DK4_MES_B187_R0091"


def name_reply(ctx, font, paint, expand, selector, body):
    template = body.decode("ascii")
    assert template.strip() == "FI FA" and "\n" not in template
    cases = ctx.execute(expand, body, selector)["cases"]
    evidence, images = [], []
    for label, given, surname in (
        ("registered default", "Rafael", "Castor"),
        ("offline 32-cell full name", "ABCDEFGHIJKLMNOP", "ABCDEFGHIJKLMNO"),
        ("offline 33-cell full name", "ABCDEFGHIJKLMNOP", "ABCDEFGHIJKLMNOP"),
    ):
        text = template.replace("FI", given).replace("FA", surname)
        encoded, rendered = text.encode("ascii"), [text.strip()]
        if label == "registered default":
            assert len(cases) == 4 and {case["output_hex"] for case in cases} == {encoded.hex()}
        page, = display.display.raster(ctx, font, paint, encoded, rendered, 1)
        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
        plane = bytes.fromhex(page["native_plane_hex"])
        images.append((f"{FULL_NAME_ID} {label}", plane))
        evidence.append(dict(scope=label, expanded_hex=encoded.hex(), lines=rendered,
                             page_sha256=[native.digest(plane)]))
    return evidence, images, cases


verification = checked_text(getsource(previous.verify), {
    'len(entries) == 368 and fe_count == 30': 'len(entries) == 227 and fe_count == 13',
    '"rafael_B161_B169_progressive"': '"rafael_B181_B187_progressive"',
    '    entries, pictures, pagination = [], [], []': '    entries, pictures, pagination, full_name = [], [], [], []',
    '        print(f"B{n}: exact stored controls and changed pages verified", flush=True)':
        '''            elif ident == FULL_NAME_ID:
                paths, samples, checks = name_reply(ctx, font, paint, expand, selector, body[1:])
                entry.update(layouts=paths, original_expansion=checks)
                pictures.extend(samples)
                full_name.append(ident)
        print(f"B{n}: exact stored controls and changed pages verified", flush=True)''',
    '        initialized_dependencies=ctx.receipt(),': '        full_name_retention_cases=full_name, initialized_dependencies=ctx.receipt(),',
})
names = checked_text(getsource(previous.verify_names), {
    '("B161_B165", "B166_B167", "B168_B169")': '("B181_B200",)',
    '    notes[132] = "Officiant matches the registered generic ceremonial role. This speaker formally confers the item, and the exchange gives no specific rank."':
        '    notes = {ident: note for ident, note in notes.items() if ident in selectors}',
})
scope = vars(previous) | globals()
for script in (verification, names):
    exec(compile(script, __file__ + "::stored-native-display", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
