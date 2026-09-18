from __future__ import annotations

import json
from pathlib import Path


BATCH = Path("translations/common_mesfile_spacing_v4.json")
STACK = Path("translations/release_stack.json")


def test_spacing_batch_is_global_and_has_no_stored_prose_breaks() -> None:
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    assert payload["source_file_sha256"] == (
        "75d48f50da7b3a4185276048a3779dee3e1dfb503dee5f228f88c9023dbc629c"
    )
    assert len(payload["records"]) >= 400
    assert len({record["id"] for record in payload["records"]}) == len(
        payload["records"]
    )
    for record in payload["records"]:
        raw = bytes.fromhex(record["replacement_hex"])
        for start, end in record["translated_ranges"]:
            assert b"\n" not in raw[start:end].rstrip(b" "), record["id"]


def test_unified_profile_contains_latest_routes_and_replaces_legacy_layouts() -> None:
    profiles = json.loads(STACK.read_text(encoding="utf-8"))["profiles"]
    unified = profiles["all-routes-unified-v1"]["batches"]
    assert "translations/common_mesfile_spacing_v4.json" in unified
    assert "translations/common_mesfile_spacing_v3.json" not in unified
    assert "translations/common_mesfile_spacing_v2.json" not in unified
    for old in (
        "translations/common_shipyard_layout_v2.json",
        "translations/guild_item_descriptions_layout_v3.json",
        "translations/common_mystery_items_v1.json",
        "translations/common_runtime_layout_v4.json",
        "translations/common_global_layout_v1.json",
    ):
        assert old not in unified
    for profile in (
        "raphael-deep-route-v93",
        "lil-deep-route-v21",
        "hodram-deep-route-v32",
    ):
        route_batches = [
            batch
            for batch in profiles[profile]["batches"]
            if "_deep_route_" in batch
        ]
        assert set(route_batches) <= set(unified)
