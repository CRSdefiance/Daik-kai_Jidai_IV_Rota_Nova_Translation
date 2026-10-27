"""Explicit research runner for a village coordinate fixture; unchanged ROM/harness.

The original harness already owns the opted-in coordinate-write API. This runner
binds its single location helper to the version-locked village helper and restores
the imported module afterward; all other harness code and tools remain untouched.
The legacy command key location_town now denotes a village ID in this runner only.
"""

from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_location_v606 import relocate


def main():
    original = location.relocate
    location.relocate = relocate
    try:
        harness.main()
    finally:
        location.relocate = original


if __name__ == "__main__":
    main()
