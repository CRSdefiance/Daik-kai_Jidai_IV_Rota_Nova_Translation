"""Observe an ordinary Azores voyage from the rested Lisbon cartridge save."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_ordinary_azores_voyage_20261123 as earlier
from scripts.reconcile_editorial_acceptance_20261123 import digest, read
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/lisbon_azores")
HISTORY = Path("work/emulation_v193/lisbon_reload_v470/capture_report.json")
RELEASE = Path("releases/all_routes_editorial_20261123_supply_ratio_hint_candidate/verification/registered_release_verification.json")
DONOR = Path("E:/Rota Nova translations/Saves/hodram-lisbon-rested-blue-oak-v468.dsv")
FIRST_PAUSE = 3200


def main():
    assert not ROOT.exists()
    source = checked_text(getsource(earlier.main), {
        'donor = history["battery_save_preloaded"]':
            'donor = history["battery_save_preloaded"] | {"source": str(DONOR)}',
    })
    release = read(RELEASE)
    assert digest(DONOR) == read(HISTORY)["battery_save_preloaded"]["source_sha256"]
    current = SimpleNamespace(RELEASE=RELEASE, ROM=Path(release["candidate"]))
    scope = vars(earlier) | dict(ROOT=ROOT, HISTORY=HISTORY, FIRST_PAUSE=FIRST_PAUSE,
                                DONOR=DONOR, current=current, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-controller", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
