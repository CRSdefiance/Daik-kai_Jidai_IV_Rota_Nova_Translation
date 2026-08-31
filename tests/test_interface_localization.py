from __future__ import annotations

import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_pxl_label_batches

BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
STACK = Path("translations/release_stack.json")

GRAPHICS_BATCHES = {
    "/_pxl/__marker.pxl": Path("translations/interface_marker_graphics_v1.json"),
    "/_pxl/haifuhin.pxl": Path(
        "translations/interface_distributed_goods_graphics_v1.json"
    ),
    "/_pxl/senrihin.pxl": Path("translations/interface_spoils_graphics_v1.json"),
    "/_pxl/tempcargo.pxl": Path(
        "translations/interface_temp_storage_graphics_v1.json"
    ),
    "/_pxl/kakutei.pxl": Path("translations/interface_confirm_graphics_v1.json"),
    "/_pxl/chihofleetinfo.pxl": Path(
        "translations/interface_regional_fleet_graphics_v1.json"
    ),
    "/_pxl/forceinfo.pxl": Path(
        "translations/interface_force_info_graphics_v1.json"
    ),
    "/_pxl/goldsearoutediscovery.pxl": Path(
        "translations/interface_golden_route_discovery_graphics_v1.json"
    ),
    "/_pxl/goldsearoutelog.pxl": Path(
        "translations/interface_golden_route_log_graphics_v1.json"
    ),
    "/_pxl/goldsearoutelog2.pxl": Path(
        "translations/interface_golden_route_total_graphics_v1.json"
    ),
}


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


@pytest.mark.parametrize(("file_path", "batch_path"), GRAPHICS_BATCHES.items())
def test_interface_graphics_change_only_declared_boxes(
    file_path: str, batch_path: Path
) -> None:
    source = NdsImage.open(BASE).read_file(file_path)
    rebuilt, changed = apply_pxl_label_batches([batch_path], source)
    batch = load(batch_path)
    records = batch["records"]
    assert changed == [record["id"] for record in records]

    before = PxlImage.from_bytes(source)
    after = PxlImage.from_bytes(rebuilt)
    assert len(rebuilt) == len(source)
    boxes = [tuple(int(value) for value in record["box"]) for record in records]
    for position, (old, new) in enumerate(zip(before.indices, after.indices, strict=True)):
        if old == new:
            continue
        x = position % before.width
        y = position // before.width
        assert any(
            left <= x < right and top <= y < bottom
            for left, top, right, bottom in boxes
        )


def test_marker_batch_covers_every_remaining_mapped_caption() -> None:
    batch = load(GRAPHICS_BATCHES["/_pxl/__marker.pxl"])
    texts = {record["text"] for record in batch["records"]}
    assert len(batch["records"]) == 18
    assert texts >= {
        "Redo",
        "Confirm",
        "Cancel",
        "Report",
        "Delegate",
        "Port",
        "Attack",
        "Classic",
        "Orders",
        "Sold",
        "Local",
        "Cargo",
        "Disc.",
        "Buy",
        "Sell",
        "Temp Store",
        "Issued",
        "Spoils",
    }


def test_interface_polish_profile_extends_the_complete_trading_profile() -> None:
    profiles = load(STACK)["profiles"]
    trading = profiles["hodram-trading-complete"]["batches"]
    interface = profiles["interface-polish-v1"]
    assert interface["status"] == "accepted-baked"
    assert interface["batches"][: len(trading)] == trading
    assert interface["batches"][len(trading) :] == [
        str(path).replace("\\", "/") for path in GRAPHICS_BATCHES.values()
    ]
