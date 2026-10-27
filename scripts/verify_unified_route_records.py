from __future__ import annotations

import argparse
import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify every fixed route record in a registered unified ROM.")
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    base = NdsImage.open(args.base)
    candidate = NdsImage.open(args.candidate)
    paths = {f"/data/SC{number}.DK4" for number in range(4)}
    sources = {path: base.read_file(path) for path in paths}
    expected = {path: {} for path in paths}
    exclusions = {path: set() for path in paths}
    for batch_path in stack["profiles"][args.profile]["batches"]:
        batch = json.loads(Path(batch_path).read_text(encoding="utf-8"))
        path = batch.get("file_path")
        if path not in paths:
            continue
        if batch.get("encoder") != "dialogue-fixed-v1":
            raise ValueError(f"unverified route encoder: {batch_path}")
        profile = get_dialogue_profile(batch["dialogue_profile"])
        for row in materialize_translation_batch(batch, sources[path]):
            encoded = encode_fixed_dialogue(bytes.fromhex(row["source_hex"]), row["english"], profile)
            expected[path][row["id"]] = encoded.encoded
        exclusions[path].update(batch.get("excluded_records", {}))
    results = {}
    for path in sorted(paths):
        actual_blocks = IlnkContainer.parse(candidate.read_file(path)).blocks
        original_blocks = IlnkContainer.parse(sources[path]).blocks
        actual = {
            f"DK4_MES_B{block:02d}_R{record:04d}": raw
            for block, data in enumerate(actual_blocks)
            for record, raw in enumerate(data.split(b"\0"))
        }
        original = {
            f"DK4_MES_B{block:02d}_R{record:04d}": raw
            for block, data in enumerate(original_blocks)
            for record, raw in enumerate(data.split(b"\0"))
        }
        for row_id, encoded in expected[path].items():
            if actual.get(row_id) != encoded:
                raise ValueError(f"{path}: saved record differs: {row_id}")
        untouched = exclusions[path] - expected[path].keys()
        for row_id in untouched:
            if actual.get(row_id) != original.get(row_id):
                raise ValueError(f"{path}: excluded record differs: {row_id}")
        results[path] = {"exact_records": len(expected[path]), "unchanged_exclusions": len(untouched)}
        print(path, results[path])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"profile": args.profile, "routes": results}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
