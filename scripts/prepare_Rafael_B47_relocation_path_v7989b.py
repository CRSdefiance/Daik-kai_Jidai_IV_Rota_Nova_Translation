"""Correct only the duplicated analysis prefix;preserve the failed relocation producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_relocation_path_tools_v7989b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/relocate_Rafael_B47_v7989.py','scripts/relocate_Rafael_B47_v7989b.py',{
        'work/analysis/work/analysis/Rafael_B47_archive_tools_v7989':'work/analysis/Rafael_B47_archive_tools_v7989',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        prior_failure='V7989 stopped beforeROOT creation because the branch-proof path had a duplicated work/analysis prefix.',
        correction='Remove only the duplicated prefix;all reconstruction,warning,span,preamble,native-case andinverse guards remain identical.',
        no_prior_ROM_proof_orproducer_overwritten=True,new_credit=0,full_goal_complete=False))
    print('Prepared path-only source-locked relocation successor;failed producer preserved.')
