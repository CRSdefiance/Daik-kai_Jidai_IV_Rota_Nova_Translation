"""Resolve the concrete weak determiner ending without changing prose or QA rules."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    prior=ROOT/'visual_preferences_v5.json';output=ROOT/'visual_preferences_v6.json';assert not output.exists()
    doc=deepcopy(load(prior))
    doc['records']['DK4_MES_B64_R0144']['line_phrases'].append('the wrong way')
    doc['records']['DK4_MES_B64_R0144']['reason']+=' Keep the wrong way together as well, resolving the measured weak the ending without waiving QA.'
    doc['records']['DK4_MES_B64_R0126']['line_phrases'].append('Thinking back,')
    doc['records']['DK4_MES_B64_R0126']['reason']+=' Keep the short Thinking back expression together as the paragraph is rebalanced.'
    doc.update(previous_preferences=str(prior),previous_preferences_sha256=sha(prior.read_bytes()),
        prior_QA_warning_preserved=str(ROOT/'automatic_v6/automatic_plans.json'),
        no_QA_warning_waiver_orprose_change=True,producer_sha256=sha(Path(__file__).read_bytes()))
    save(output,doc)
