"""Move only the Online viewer's title canvas and border to the bottom screen."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

RECORDS = (
    ("ONLINE_TITLE_CANVAS_BOTTOM_LAYER", 0x105904, "102095e5", "0020a0e3"),
    ("ONLINE_TITLE_BORDER_BOTTOM_LAYER", 0x1058D4, "0130a0e3", "0030a0e3"),
)


def apply_release(source, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-online-title-banner-release-v1":
        raise ValueError("Unknown Online banner release format")
    if sha(source) != config["source_ARM9_sha256"] or sha(canonical) != config["canonical_ARM9_sha256"]:
        raise ValueError("Exact complete input stack and canonical source required")
    result = bytearray(source)
    changed = []
    for record_id, offset, before, after in RECORDS:
        expected, replacement = bytes.fromhex(before), bytes.fromhex(after)
        if canonical[offset:offset + 4] != expected or source[offset:offset + 4] != expected:
            raise ValueError("Original Online-specific screen-selection instruction differs")
        result[offset:offset + 4] = replacement
        changed.append(record_id)
    result = bytes(result)
    if sha(result) != config["target_ARM9_sha256"]:
        raise ValueError("Online banner output identity differs")
    expected_offsets = {
        offset + index for _, offset, before, after in RECORDS
        for index, (left, right) in enumerate(zip(bytes.fromhex(before), bytes.fromhex(after)))
        if left != right
    }
    if {index for index, (before, after) in enumerate(zip(source, result)) if before != after} != expected_offsets:
        raise ValueError("Unexpected code, wording or artwork changed")
    return result, {"status": "pass-two-scoped-screen-selection-instructions", "source_ARM9_sha256": sha(source), "target_ARM9_sha256": sha(result), "changed_records": changed, "title_local_origin_preserved": [24, 4], "title_canvas_dimensions_preserved": [256, 192], "text_and_border_destination_layer": 0, "screenshots_and_description_artwork_unchanged": True}
