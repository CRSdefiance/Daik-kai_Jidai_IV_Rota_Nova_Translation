"""Play additional town trends on the registered cumulative testing ROM."""
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import register_lisbon_fragrance_wraps_20261121 as active
from scripts import replay_town_trends_saved_game_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("out/european_trends_gameplay_20261121")
ARCHIVE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
HISTORY = {city: ARCHIVE / source / "capture_report.json" for city, source in (
    ("stockholm", "auto_move_riga_v399"), ("london", "condition_rumor_v774_london_pilot_v773"),
    ("athens", "environment_voyage_v510_leg"),
)}
FIRST = {"stockholm": 8000, "london": 3760, "athens": 3760}


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("city", choices=HISTORY)
    args = parser.parse_args()
    city = args.city
    source = checked_text(getsource(previous.main), {
        '    parser = argparse.ArgumentParser(description=__doc__)\n'
        '    parser.add_argument("city", choices=HISTORY)\n'
        '    args = parser.parse_args()\n': "",
        "folder = ROOT / args.city": "folder = ROOT / city",
        "HISTORY[args.city]": "HISTORY[city]",
        'if row["start"] <= 2801': 'if row["start"] < FIRST[city] and (city == "stockholm" or row["start"] <= 2801)',
        'for row in boot] ==': 'for row in boot[:4]] ==',
        '"--pause-at", "3760"': '"--pause-at", str(FIRST[city])',
    })
    scope = vars(previous) | globals() | {"city": city}
    exec(compile(source, __file__ + "::town-input", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()

