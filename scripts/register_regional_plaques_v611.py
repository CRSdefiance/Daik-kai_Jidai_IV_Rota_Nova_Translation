"""Register source-framed regional plaques after the complete compact V610 stack."""

import copy
import json
from pathlib import Path


def main():
    path = Path("translations/release_stack.json")
    stack = json.loads(path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v610"])
    profile.update({"regional_fleet_plaques": "translations/regional_fleet_plaques_v1.json",
                    "description": "Complete V610 plus five source-framed regional-fleet plaques and reviewed financial labels.",
                    "note": "Original wallpaper and own source rims; reconstructed fine wood. Native display verification required.",
                    "status": "experimental"})
    if "all-routes-unified-v611" in stack["profiles"]:
        assert stack["profiles"]["all-routes-unified-v611"] == profile
    stack["profiles"]["all-routes-unified-v611"] = profile
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Registered V611 regional plaques; all V610 dependencies retained, no canonical promotion.")


if __name__ == "__main__":
    main()
