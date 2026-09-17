from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_arm9_fixed_batch


BASE = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
BATCH = Path("translations/trading_button_labels_v2.json")
ARM9_SHA256 = "249860ab1d29ecfa8e149fd04b5cbff3c3414fb192f81459cfaf469d6c83fa52"


def test_trade_buttons_have_distinct_actions_and_fit_original_slots() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    assert hashlib.sha256(source).hexdigest() == ARM9_SHA256
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert [(record["id"], record["english"]) for record in batch["records"]] == [
        ("DK4_TRADE_CONFIRM_BUTTON_A", "Select"),
        ("DK4_TRADE_FINISH_BUTTON_X", "Finish"),
    ]

    rebuilt, changed = apply_arm9_fixed_batch(BATCH, source)
    assert changed == [record["id"] for record in batch["records"]]
    assert rebuilt[0x11B51C : 0x11B524] == b"Select\0\0"
    assert rebuilt[0x11B554 : 0x11B55C] == b"Finish\0\0"
