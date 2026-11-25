"""Refine private phrase preferences after wrap review; all native metrics and QA remain exact."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_layout_tools_v8245')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/plan_Hodram_B137_B45_B46_v8243.py','scripts/plan_Hodram_B137_B45_B46_v8245.py',{
      'Hodram_B137_B45_B46_layout_v8243':'Hodram_B137_B45_B46_layout_v8245',
      'translations/hodram_B137_B45_B46_editorial_manuscript_v1.json':'translations/hodram_B137_B45_B46_editorial_manuscript_v2.json',
      'Hodram_B137_B45_B46_logical_v8242/28_logical_paragraphs112_original_native_alignments_no_FE.json':'Hodram_B137_B45_B46_refinement_v8244/28_logical_paragraphs4_fresh108_exact_reused_alignments.json',
      'PHRASES={':'PHRASES={("the","Mediterranean".lower()),("the","towns"),("all","of"),("can\'t","seem"),("she\'s","right"),("what","does"),("does","she"),("she","mean"),',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
