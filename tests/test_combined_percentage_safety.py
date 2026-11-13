import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


def test_lil_percentage_tutorials_do_not_introduce_printf_commands() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    targets = {22: {"DK4_MES_B164_R0140"}, 42: {f"DK4_MES_B128_R{n:04d}" for n in (268, 311, 317)}}
    for version, ids in targets.items():
        batch = json.loads(Path(f"translations/lil_deep_route_v{version}.json").read_text(encoding="utf-8"))
        profile = get_dialogue_profile(batch["dialogue_profile"])
        rows = [r for r in materialize_translation_batch(batch, source) if r["id"] in ids]
        assert {r["id"] for r in rows} == ids
        for row in rows:
            raw = bytes.fromhex(row["source_hex"])
            encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
            assert b"%" not in encoded
            assert len(encoded) == len(raw)
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
            assert raw.count(b"FI") == encoded.count(b"FI")
