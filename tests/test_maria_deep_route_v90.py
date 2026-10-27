from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments

B = Path("out/raphael_natural_v2_accepted_base.nds")
T = Path("translations/maria_deep_route_v90.json")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_v90_allocations():
    batch = load(T)
    assert batch["inventory"]["identified_records"] == 48
    source = NdsImage.open(B).read_file("/data/SC3.DK4")
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    failures = []
    for row in rows:
        errors = [
            issue
            for issue in audit_fixed_dialogue_record(
                bytes.fromhex(row["source_hex"]), row["english"], profile
            )["issues"]
            if issue["severity"] == "error"
        ]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, failures
    assert changed_segments(source, rebuild_mesfile(source, rows)) == {
        (
            int(row["id"].split("_B", 1)[1].split("_R", 1)[0]),
            int(row["id"].rsplit("R", 1)[1]),
        )
        for row in rows
    }


def test_v90_content_and_stack():
    batch = load(T)
    by_id = {row["id"]: row for row in batch["records"]}
    assert "flying crimson orca" in by_id["DK4_MES_B105_R0101"]["english"]
    assert "The Proof" in by_id["DK4_MES_B106_R0037"]["english"]
    assert "Tang Bamboo Craft" in by_id["DK4_MES_B107_R0019"]["english"]
    assert load("translations/release_stack.json")["profiles"]["maria-deep-route-v90"]["batches"][-1] == T.as_posix()
