"""Replay the established Search transition and cumulative startup controls."""

import argparse
from inspect import getsource
from types import FunctionType

from scripts import replay_crew_and_shore_reports_v1 as prior
from scripts import replay_refit_help_startup_20261115 as startup
from scripts import stage_expedition_report_wraps_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def main(case):
    if case == 'startup':
        FunctionType(startup.main.__code__, vars(startup) | dict(stage=stage))()
        return
    source = checked_text(getsource(prior.gameplay), {
        "proof = base.load(stage.PROOF)": "proof = base.load(stage.STORED)",
        "proof['research_ROM_sha256']": "proof['candidate_sha256']",
        "proof['research_ARM9_sha256']": "proof['target_ARM9_sha256']",
    })
    env = vars(prior) | dict(stage=stage)
    exec(compile(source, __file__ + '::existing-search-replay', 'exec'), env)
    env['gameplay']('attack')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('startup', 'attack'))
    main(parser.parse_args().case)
