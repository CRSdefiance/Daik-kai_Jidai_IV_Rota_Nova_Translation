"""Source-lock all325 native SC1 load/cache paths and650 original entry modes to the research archive."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_loader_tools_v8277')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/verify_Gerhard_loaders_v8222.py','scripts/verify_Hodram_loaders_v8277.py',{
      'scripts.create_Gerhard_reference_v8215':'scripts.create_Hodram_reference_v8276',
      'Gerhard_loaders_v8222':'Hodram_loaders_v8277',
      'work/analysis/Gerhard_reference_v8215/research_image_receipt.json':'work/analysis/Hodram_reference_v8276/research_image_receipt.json',
      'for r in [2]':'for r in [1]','counts=={2:336}':'counts=={1:325}',
      'for route in [2]:':'for route in [1]:','for route in (2,):':'for route in (1,):',
      '336':'325','672':'650','whole_SC2':'whole_SC1','exact_B27_B74_headers':'exact_B137_B45_B46_headers',
      'all_original_EV2_actions':'all_original_EV1_actions','Resized SC2':'Resized SC1',
      'native SC2':'native SC1','five-surname research image':'28-speech Hodram research image',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_loader_derivation.json',receipt)
