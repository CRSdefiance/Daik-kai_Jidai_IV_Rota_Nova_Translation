import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_unified_v2_contains_every_completed_route_stack():
    profiles = load("translations/release_stack.json")["profiles"]
    batches = profiles["all-routes-unified-v2"]["batches"]
    assert len(batches) == len(set(batches))
    expected_v1 = set(profiles["all-routes-unified-v1"]["batches"])
    expected_v1.remove("translations/common_mesfile_spacing_v4.json")
    expected_v1.add("translations/common_mesfile_spacing_v4_unified_base.json")
    assert expected_v1 <= set(batches)
    assert set(profiles["maria-deep-route-v111"]["batches"]) <= set(batches)
    assert sum("raphael_deep_route" in batch for batch in batches) == 95
    assert sum("hodram_deep_route" in batch for batch in batches) == 46
    assert sum("lil_deep_route" in batch for batch in batches) == 23
    assert sum("maria_deep_route" in batch for batch in batches) == 111
    assert "translations/common_encounter_directions_arm9_v1.json" in batches
    assert batches[-1] == "translations/maria_deep_route_v111.json"


def test_encounter_direction_batch_covers_all_eight_compass_values():
    batch = load("translations/common_encounter_directions_arm9_v1.json")
    records = batch["records"]
    assert [record["english"] for record in records] == [
        "N",
        "NE",
        "E",
        "SE",
        "S",
        "SW",
        "W",
        "NW",
    ]
    assert len({record["offset"] for record in records}) == 8


def test_unified_common_base_has_no_superseded_duplicates():
    batch = load("translations/common_mesfile_spacing_v4_unified_base.json")
    assert len(batch["records"]) == 5
    assert batch["inventory"]["superseded_records"] == 421
