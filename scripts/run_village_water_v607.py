"""Explicit village-water research runner using the unchanged opted-in harness."""

from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_water_v607 import relocate


def main():
    original = location.relocate
    location.relocate = relocate
    try:
        harness.main()
    finally:
        location.relocate = original


if __name__ == "__main__":
    main()
