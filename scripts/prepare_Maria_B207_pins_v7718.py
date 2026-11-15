"""Preserve the new candidate andexact reconstruction without pruning."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_pin_tools_v7718')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/pin_papal_trade_release_v7662.py','scripts/pin_Maria_B207_release_v7718.py',{
        'papal_trade_release_pins_v7662':'maria_B207_release_pins_v7718',
        'papal_trade_release_v7661':'maria_B207_release_v7718',
        'V7660 registered cumulative628-batch papal-trade integration':'V7717 registered cumulative629-batch Maria B207 integration',
        'reviews26 revisions10 retentions':'reviews13 revisions5 retentions',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_candidate_andreconstruction_pins.json',dict(tool=tool,preserve_every_prior_ROM_andpin=True,new_credit=0,full_goal_complete=False))
