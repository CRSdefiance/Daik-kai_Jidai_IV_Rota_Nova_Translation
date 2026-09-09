from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    apply_fls_label_batch,
    apply_pxl_label_batches,
)

BASE = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
FLS_BATCHES = [
    Path("translations/opening_movie_m20_subtitle_v1.json"),
    Path("translations/opening_movie_m22_subtitles_v2.json"),
    Path("translations/opening_movie_m24_subtitles_v2.json"),
]
PXL_BATCHES = [
    Path("translations/opening_title02_graphics_v1.json"),
    Path("translations/opening_title06_graphics_v1.json"),
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_opening_movie_subtitles_are_source_locked_outlined_and_fixed_size() -> None:
    image = NdsImage.open(BASE)
    for batch_path in FLS_BATCHES:
        batch = _load(batch_path)
        source = image.read_file(str(batch["file_path"]))
        assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

        rebuilt, changed = apply_fls_label_batch(batch_path, source)

        assert len(rebuilt) == len(source)
        assert rebuilt != source
        assert changed == [str(row["id"]) for row in batch["records"]]
        archive = FlsArchive(rebuilt)
        for row in batch["records"]:
            assert row["background_index"] == 0
            assert row["color_index"] == 1
            assert row["outline_index"] == 2
            counts = Counter(archive.texture(int(row["asset_index"])).indices)
            assert counts[0] > counts[2] > 0
            assert counts[1] > 0

    m20 = _load(FLS_BATCHES[0])
    assert m20["records"][0]["layout_width"] == 168
    rebuilt, _ = apply_fls_label_batch(
        FLS_BATCHES[0], image.read_file(str(m20["file_path"]))
    )
    texture = FlsArchive(rebuilt).texture(27)
    visible = [index % texture.width for index, value in enumerate(texture.indices) if value]
    assert max(visible) < 168


def test_opening_prompts_are_source_locked_and_fixed_size() -> None:
    image = NdsImage.open(BASE)
    for batch_path in PXL_BATCHES:
        batch = _load(batch_path)
        source = image.read_file(str(batch["file_path"]))
        assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

        rebuilt, changed = apply_pxl_label_batches([batch_path], source)

        assert len(rebuilt) == len(source)
        assert rebuilt != source
        assert changed == [str(row["id"]) for row in batch["records"]]
        rendered = PxlImage.from_bytes(rebuilt).render()
        assert rendered.size == (256, 29)
