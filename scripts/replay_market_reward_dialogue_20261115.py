"""Replay the established recommendation fixture against the current Market ROMs."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import native_recommendation_stock_fixture_v4983 as stock
from scripts import replay_kurushima_encounter_20261115 as startup_workflow
from scripts import run_recommendation_focus_v4984c as historical
from scripts import stage_market_reward_dialogue_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def reward(case, rom):
    staged = stage.base.load(stage.STORED)
    expected = staged['previous_sha256' if case == 'current' else 'candidate_sha256']
    assert stage.base.digest(rom) == expected
    arm = stage.base.NdsImage.open(rom).read_file(stage.ARM)
    assert stage.digest(arm) == staged['target_ARM9_sha256']
    source = checked_text(getsource(stock.assign), {
        "assert sha(arm)=='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'":
            'assert sha(arm) == QUALIFIED_ARM_SHA',
    })
    scope = vars(stock) | {'QUALIFIED_ARM_SHA': staged['target_ARM9_sha256']}
    exec(compile(source, __file__ + '::source-locked-stock', 'exec'), scope)
    original_assign, stock.assign = stock.assign, scope['assign']
    runner = checked_text(Path(historical.__file__).read_text(encoding='utf-8'), {
        "rom=Path(refs['parent' if case=='current' else 'research_ROM']);digest=sha(rom.read_bytes());assert digest==refs['parent_sha256' if case=='current' else 'research_ROM_sha256']":
            'rom=TARGET;digest=sha(rom.read_bytes());assert digest==EXPECTED',
        "observed.configure(case,rom);root=observed.ROOT;cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/recommendation775_v4984c_'+case)":
            "observed.configure(case,rom);root=observed.ROOT=OUTPUT;cap=root/'capture'",
    })
    import sys
    previous, sys.argv = sys.argv, [__file__, '--case', case]
    try:
        exec(compile(runner, __file__ + '::source-locked-reward', 'exec'), dict(__name__='__main__',
            __file__=__file__, TARGET=rom, EXPECTED=expected, OUTPUT=stage.ROOT / case))
    finally:
        sys.argv = previous
        stock.assign = original_assign


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('current', 'reviewed', 'startup'))
    mode = parser.parse_args().mode
    if mode == 'startup':
        FunctionType(startup_workflow.startup.__code__, vars(startup_workflow) | {'stage': stage})()
    else:
        reward(mode, stage.parent.ROM if mode == 'current' else stage.ROM)
