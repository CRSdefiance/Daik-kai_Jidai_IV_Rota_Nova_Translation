"""Preserve failed empty-map preparation; use an explicit source identity mapping."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    derive('scripts/prepare_Hodram_B50_runs_v8505.py','scripts/prepare_Hodram_B50_runs_v8505b.py',{
        "checked_text('if True:\\n'+contract,{}) .split":"checked_text('if True:\\n'+contract,{'contract=read':'contract=read'}).split",
    })
