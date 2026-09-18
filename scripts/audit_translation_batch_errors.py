from __future__ import annotations

import argparse
import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


def main() -> None:
    parser = argparse.ArgumentParser(description="Print fixed-dialogue errors for one translation batch.")
    parser.add_argument("batch", type=Path)
    parser.add_argument("rom", type=Path)
    args = parser.parse_args()
    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    source = NdsImage.open(args.rom).read_file(batch["file_path"])
    profile = get_dialogue_profile(batch["dialogue_profile"])
    errors = 0
    for row in materialize_translation_batch(batch, source):
        issues = [
            issue
            for issue in audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)["issues"]
            if issue["severity"] == "error"
        ]
        if issues:
            errors += len(issues)
            print(row["id"], row["english"])
            for issue in issues:
                print(f"  {issue['code']}: {issue['message']}")
    print(f"{errors} error(s)")
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
