"""Keep B226 explicit in the all-prior-audits checkpoint label before completion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_completion_labels_v7330b')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/complete_lil_B227_v7330.py','scripts/complete_lil_B227_v7330b.py',{'all_B218_B222_B223_B224_B225_andB227_technical_leads_preserved':'all_B218_B222_B223_B224_B225_B226_andB227_technical_leads_preserved'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_prior_audit_label.json',r)
