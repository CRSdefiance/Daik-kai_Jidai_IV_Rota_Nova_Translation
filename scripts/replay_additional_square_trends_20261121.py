"""Open verified port saves for two ordinary Square trend routes."""
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import register_stockholm_dialogue_followup_20261121 as active
from scripts import replay_stockholm_december_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("out/additional_square_trend_gameplay_20261121")
DEPARTURES = {
    "hamburg": (prior.HISTORY/"lubeck_voyage_v421/capture_report.json",3760,2801),
    "seville": (prior.HISTORY/"lisbon_reload_v470/capture_report.json",3760,2801),
}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("town",choices=DEPARTURES)
    town = parser.parse_args().town
    code = checked_text(getsource(prior.main),{'\"145000\"':'\"49000\"'})
    scope = vars(prior) | globals()
    exec(compile(code,__file__+"::opening", "exec"),scope)
    scope["main"](ROOT/town,town)
