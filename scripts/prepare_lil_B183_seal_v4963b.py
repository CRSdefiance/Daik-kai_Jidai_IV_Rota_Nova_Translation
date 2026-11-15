"""Correct three whole-expression replacement keys before executing the sealer."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/lil_B183_seal_tools_v4963b');assert not root.exists()
    tool=derive('scripts/seal_lil_B183_references_v4963.py','scripts/seal_lil_B183_references_v4963b.py',{
        "f['all22_stored_fixture_commands']":"f['all37_stored_fixture_commands']",
        "len(visual['all2_actual_sheets_viewed'])":"len(visual['all5_actual_sheets_viewed'])",
        "visual['postscene9001_PRNG_seeds']":"visual['postscene11001_PRNG_seeds']",
        "assert visual['postscene11001_whole1A04_actor_models_and_captain2_equal']":"assert not visual['PRNG_equality'] and visual['postscene11001_whole1A04_actor_models_and_captain2_equal']",
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,unexecuted_prior_sealer_preserved=True))
